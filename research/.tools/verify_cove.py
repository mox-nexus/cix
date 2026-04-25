#!/usr/bin/env python3
"""Round-2 CoVE verifier — cross-model (Gemini) verification of extracted claims.

Reads a stream's `verification/unverified-cited.txt`, for each `source:cN`:
  - locates the extraction file, pulls the claim text + quote
  - locates the source context (full-text md if present, else the extraction file itself)
  - constructs a CoVE prompt
  - calls `gemini -p`, parses JSON verdict
  - appends to `verification/cove-gemini-round-2.jsonl`

Resumable: already-verified claim IDs in the JSONL are skipped.

Usage:
    python3 research/.tools/verify_cove.py <stream> [--limit N] [--only SRC:cN]

    stream: a | b | c
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STREAM_DIRS = {
    "a": ROOT / "stream-a-human-memory",
    "b": ROOT / "stream-b-llm-memory",
    "c": ROOT / "stream-c-landscape",
}

# ---------------------------------------------------------------------------
# Citation-to-extraction-slug mapping
# ---------------------------------------------------------------------------
# synthesis citation (bartlett1995) -> extraction slug (bartlett-kintsch-1995)
# Built by scanning extraction filenames; override below when heuristic fails.

MANUAL_MAP = {
    "bartlett1995": "bartlett-kintsch-1995-remembering",
    "metcalfewiebe1987": "metcalfe-wiebe-1987-intuition-insight",
    "lutzthompson2003": "lutz-thompson-2003-neurophenomenology",
    "stafford1984": "stafford-daly-1984-conversation",
    "vonoswald2022": "von-oswald-2022-icl-gradient-descent",
}


def build_source_index(stream_dir: Path) -> dict[str, Path]:
    """Map citation-key -> extraction file path."""
    idx = {}
    for f in (stream_dir / "extractions").glob("*.md"):
        stem = f.stem  # e.g. bartlett-kintsch-1995-remembering
        parts = stem.split("-")
        # Locate year
        year_idx = next((i for i, p in enumerate(parts) if p.isdigit() and len(p) == 4), None)
        if year_idx is None:
            continue
        # first author token + year
        author = parts[0]
        year = parts[year_idx]
        key = f"{author}{year}"
        idx[key] = f
        # Also underscore variant (used in Stream C citations)
        idx[f"{author}_{year}"] = f
    # Apply manual overrides
    for citekey, slug in MANUAL_MAP.items():
        path = stream_dir / "extractions" / f"{slug}.md"
        if path.exists():
            idx[citekey] = path
    return idx


# ---------------------------------------------------------------------------
# Extraction parsing
# ---------------------------------------------------------------------------

CLAIM_HEADER_RE = re.compile(r"^###\s+([a-zA-Z0-9_-]+):(c\d+)\s*$", re.MULTILINE)


def load_claim(extraction_path: Path, cn: str) -> dict | None:
    """Find the claim block with id `cN` in the extraction file."""
    text = extraction_path.read_text()

    # Parse frontmatter
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            fm_text = text[3:end]
            for line in fm_text.splitlines():
                m = re.match(r"^([\w]+):\s*(.*)$", line.strip())
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")

    # Split on claim headers
    matches = list(CLAIM_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        slug, this_cn = m.group(1), m.group(2)
        if this_cn == cn:
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[start:end].strip()
            return {
                "claim_id": f"{slug}:{cn}",
                "block": block,
                "claim_text": _extract_field(block, "Claim"),
                "quote": _extract_field(block, "Quote"),
                "title": fm.get("title", "?"),
                "year": fm.get("year", "?"),
                "source_type": fm.get("source_type", "abstract-only"),
                "slug": slug,
            }
    return None


def _extract_field(block: str, name: str) -> str:
    """Pull value of field `name` in either format:
    (a) - **Name:** value (markdown-list style)
    (b) NAME: value (plain uppercase style, newline-terminated)
    """
    # Format (a)
    pat_a = re.compile(rf"^-\s*\*\*{name}:\*\*\s*(.*?)(?=\n-\s*\*\*|\Z)", re.MULTILINE | re.DOTALL)
    m = pat_a.search(block)
    if m:
        return m.group(1).strip().strip('"').strip("'").strip()
    # Format (b): NAME: ... up to next all-caps field or blank line
    upname = name.upper()
    pat_b = re.compile(
        rf"^{upname}:\s*(.*?)(?=\n[A-Z]{{2,}}:|\n\n|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pat_b.search(block)
    if m:
        return m.group(1).strip().strip('"').strip("'").strip()
    return ""


# ---------------------------------------------------------------------------
# Source context loader
# ---------------------------------------------------------------------------


def load_source_context(
    stream_dir: Path, slug: str, source_type: str, extraction_path: Path
) -> tuple[str, str]:
    """Return (context_label, context_text) for CoVE prompt.

    Tries full-text file first; falls back to extraction-file context.
    """
    # Try full-text (Stream A has this dir)
    ft_dir = stream_dir / "sources" / "full-text"
    if ft_dir.exists():
        # Tokenize splitting on separators AND alpha/digit boundaries
        split_re = re.compile(r"[-_.]|(?<=\D)(?=\d)|(?<=\d)(?=\D)")
        slug_tokens = {t.lower() for t in split_re.split(slug) if len(t) > 2}
        slug_years = {t for t in slug_tokens if t.isdigit() and len(t) == 4}
        slug_authors = slug_tokens - slug_years
        for f in ft_dir.glob("*.md"):
            name_tokens = {t.lower() for t in split_re.split(f.stem) if len(t) > 2}
            name_years = {t for t in name_tokens if t.isdigit() and len(t) == 4}
            name_authors = name_tokens - name_years
            # Require BOTH author overlap AND year match.
            # Year-only match → different paper, same year (false positive).
            # Author-only match → same author, different paper (false positive — e.g.
            # kounios-beeman-2009 vs beeman-2004 both share "beeman").
            if slug_authors & name_authors and slug_years & name_years:
                content = f.read_text()
                return (f"full-text ({f.name})", content[:30000])

    # Fallback: use the entire extraction file as context (quotes + surrounding)
    return (
        "abstract-only (extraction-derived; full source not in repo)",
        extraction_path.read_text()[:15000],
    )


# ---------------------------------------------------------------------------
# Gemini CoVE prompt + call
# ---------------------------------------------------------------------------

COVE_PROMPT = """You are an independent verifier. A researcher extracted a claim from an academic source. Your job is to independently judge whether the source supports the claim as stated.

SOURCE ({source_label}): {title} ({year})
---BEGIN SOURCE---
{source_text}
---END SOURCE---

EXTRACTED CLAIM: {claim_text}

SUPPORTING QUOTE (as recorded by the extractor):
"{quote}"

TASKS:

1. QUOTE_MATCH: does the supporting quote appear in the source (verbatim or very close paraphrase)?
   - VERBATIM: appears word-for-word
   - PARAPHRASE: close paraphrase of something in the source
   - NOT_FOUND: quote not in source (extractor may have fabricated it)

2. VERDICT: does the source support the extracted claim?
   - VERIFIED: claim accurately reproduces what the source says
   - CORRECTED: claim is directionally right but imprecise or overreaches; a better paraphrase exists
   - REFUTED: source says something that contradicts the claim
   - INSUFFICIENT: source does not address the claim enough to judge

3. CORRECTION: if CORRECTED, provide a more precise one-sentence paraphrase of what the source actually says.

4. REASONING: one sentence explaining the verdict.

Respond with ONLY a JSON object, no prose before or after:
{{
  "quote_match": "VERBATIM" | "PARAPHRASE" | "NOT_FOUND",
  "verdict": "VERIFIED" | "CORRECTED" | "REFUTED" | "INSUFFICIENT",
  "correction": "..." or null,
  "reasoning": "..."
}}"""


def run_gemini(prompt: str, timeout: int = 180, model: str | None = None) -> str:
    args = ["gemini", "-p", prompt, "--approval-mode", "plan"]
    if model:
        args += ["-m", model]
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return result.stdout + ("\nSTDERR:\n" + result.stderr if result.returncode != 0 else "")


def parse_json_from_output(text: str) -> dict | None:
    """Extract the first JSON object from gemini's output."""
    # Strip common wrappers: ```json ... ```
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        # Find first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < 0:
            return None
        candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Orchestrate
# ---------------------------------------------------------------------------


def load_done(out_path: Path) -> set[str]:
    done = set()
    if out_path.exists():
        for line in out_path.open():
            try:
                rec = json.loads(line)
            except Exception:
                continue
            done.add(rec["claim_id"])
    return done


def verify_stream(stream: str, limit: int | None = None, only: str | None = None) -> None:
    sd = STREAM_DIRS[stream]
    unverified_list = (
        (sd / "verification" / "unverified-cited.txt").read_text().strip().splitlines()
    )
    # Include other streams' extractions for cross-stream bridges
    src_idx = build_source_index(sd)
    for other_stream, other_sd in STREAM_DIRS.items():
        if other_stream == stream:
            continue
        for citekey, path in build_source_index(other_sd).items():
            src_idx.setdefault(citekey, path)
    out_path = sd / "verification" / "cove-gemini-round-2.jsonl"
    done = load_done(out_path)

    if only:
        unverified_list = [only]

    pending = [cl for cl in unverified_list if cl and cl not in done]
    if limit:
        pending = pending[:limit]

    print(f"stream={stream}  pending={len(pending)}  already-done={len(done)}", file=sys.stderr)

    for i, claim_id in enumerate(pending, 1):
        if ":" not in claim_id:
            continue
        citekey, cn = claim_id.split(":", 1)
        ext_path = src_idx.get(citekey)
        if not ext_path:
            rec = {"claim_id": claim_id, "error": "no-extraction-file", "citekey": citekey}
            _append(out_path, rec)
            print(f"[{i}/{len(pending)}] {claim_id} NO-EXTRACTION", file=sys.stderr)
            continue

        claim = load_claim(ext_path, cn)
        if not claim:
            rec = {
                "claim_id": claim_id,
                "error": "claim-not-found-in-file",
                "file": str(ext_path.name),
            }
            _append(out_path, rec)
            print(f"[{i}/{len(pending)}] {claim_id} NO-CLAIM-IN-FILE", file=sys.stderr)
            continue

        ctx_label, ctx_text = load_source_context(sd, claim["slug"], claim["source_type"], ext_path)

        prompt = COVE_PROMPT.format(
            source_label=ctx_label,
            title=claim["title"],
            year=claim["year"],
            source_text=ctx_text,
            claim_text=claim["claim_text"],
            quote=claim["quote"],
        )

        t0 = time.monotonic()
        try:
            raw = run_gemini(prompt)
        except subprocess.TimeoutExpired:
            rec = {"claim_id": claim_id, "error": "timeout"}
            _append(out_path, rec)
            print(f"[{i}/{len(pending)}] {claim_id} TIMEOUT", file=sys.stderr)
            continue
        dur = time.monotonic() - t0

        verdict = parse_json_from_output(raw)
        if not verdict:
            rec = {
                "claim_id": claim_id,
                "error": "unparseable",
                "raw": raw[:1000],
                "duration_s": round(dur, 2),
            }
            _append(out_path, rec)
            print(f"[{i}/{len(pending)}] {claim_id} UNPARSEABLE ({dur:.1f}s)", file=sys.stderr)
            continue

        rec = {
            "claim_id": claim_id,
            "verdict": verdict.get("verdict"),
            "quote_match": verdict.get("quote_match"),
            "correction": verdict.get("correction"),
            "reasoning": verdict.get("reasoning"),
            "context_label": ctx_label,
            "duration_s": round(dur, 2),
            "verifier": "gemini",
        }
        _append(out_path, rec)
        print(
            f"[{i}/{len(pending)}] {claim_id}  {verdict.get('verdict')}  "
            f"(quote:{verdict.get('quote_match')}  {dur:.1f}s)",
            file=sys.stderr,
        )


def _append(out_path: Path, rec: dict) -> None:
    with out_path.open("a") as f:
        f.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stream", choices=["a", "b", "c"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", type=str, default=None, help="single claim_id like nader2009:c9")
    args = ap.parse_args()
    verify_stream(args.stream, limit=args.limit, only=args.only)
