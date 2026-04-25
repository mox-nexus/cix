#!/usr/bin/env python3
"""Light verification of Round 3 Inquiries doc — gemini cross-eval of load-bearing claims.

Not full CoVE: source papers are not in the repo. We give gemini the claim, the cited
references (URL + reference number), and ask it to (a) evaluate plausibility against its
own knowledge of those refs, (b) flag whether the cited literature actually supports the
claim as stated. This is weaker than source-grounded CoVE but stronger than no scrutiny.

Output: research/round-3-inquiries/verification.jsonl
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "round-3-inquiries"
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / "verification.jsonl"

# Five load-bearing claims with their cited refs (paraphrased from doc + reference list)
CLAIMS = [
    {
        "id": "R3-I1-stafford-task-oriented",
        "inquiry": "Inquiry 1: Conversational Memory Decay",
        "claim": (
            "Empirical measurements of problem-solving dyads show participants retain "
            "approximately 40.66% to 43.69% of informational units immediately following "
            "the interaction — a fourfold increase over Stafford & Daly's ~10% figure for "
            "casual social exchange."
        ),
        "refs": [
            "Ref 1: Stafford 1984 (researchgate)",
            "Ref 7: Remembering and Retelling Stories in Individual and Collaborative Contexts (PMC2843526)",
        ],
        "consequence": (
            "If true, refutes the architectural assumption of catastrophic conversation "
            "amnesia. Memex's value proposition shifts from 'compensate for amnesia' to "
            "'augment functional cognition + recover the lost 60% of nuance.'"
        ),
    },
    {
        "id": "R3-I2-qkv-as-ecphory",
        "inquiry": "Inquiry 2: Context-Dependent Retrieval / QKV-as-Ecphory",
        "claim": (
            "The QKV (Query-Key-Value) attention mechanism in Transformers is "
            "mathematically equivalent to ecphoric memory retrieval as defined by "
            "Tulving's Encoding Specificity Principle. Queries function as the context "
            "cue, Keys index trace memory, Values store content; perturbing Key matrix "
            "weights directly impairs memory retrieval."
        ),
        "refs": [
            "Ref 20: Memory Retrieval in Transformers: Insights from The Encoding Specificity Principle (researchgate)",
            "Ref 21: arxiv 2601.20282 (same paper, January 2026 preprint)",
            "Ref 22-23: Dentate spikes and external control of hippocampal function (PMC8369486 + biorxiv)",
        ],
        "consequence": (
            "If true, ecphoric retrieval is computationally native to Transformer attention. "
            "Standard RAG with external flat-vector cosine similarity bypasses this. Architecture "
            "should leverage attention rather than treat it as a black box. Underpins new "
            "Implication #28 (Triadic Retrieval)."
        ),
    },
    {
        "id": "R3-I3-trail-interaction-cost",
        "inquiry": "Inquiry 3: Failure of Curated Trails",
        "claim": (
            "Across decades of personal-information-management research, user-authored trail "
            "curation has consistently failed due to interaction cost. Specific evidence: "
            "Trigg's NoteCards (~1987) failed to allow casual users to maintain archives; "
            "Marshall's longitudinal PIM studies show 'benign neglect' as the dominant pattern; "
            "modern PKM tools (Obsidian, Roam, Notion) exhibit 'curation burden' and the "
            "'Ball of Wool' graph problem; users fall victim to 'Collector's Fallacy.'"
        ),
        "refs": [
            "Ref 25: Tool Support for Knowledge Foraging (CMU-HCII-23-105)",
            "Ref 28-29: Halasz, Reflections on NoteCards / Trigg PhD",
            "Ref 30-32: Obsidian forum + PKM critiques",
            "Ref 35-37: Marshall's PIM/personal-archives papers",
        ],
        "consequence": (
            "If true, refutes any architecture that requires user-authored trails. Trails must "
            "emerge from implicit signals (navigation, reading time, query chains), with at "
            "most low-cost confirmation. Underpins new Implication #27 (Curation Interaction "
            "Cost Threshold)."
        ),
    },
    {
        "id": "R3-I4-format-affects-llm-utilization",
        "inquiry": "Inquiry 4: RAG Content Form Effects",
        "claim": (
            "The format of retrieved content (instruction-formatted, semantic-tagged, "
            "hierarchically-structured) substantially affects LLM utilization in long contexts, "
            "flattening the U-shaped lost-in-the-middle attention curve. Specific quantitative "
            "claim: semantic tagging improves question-answering accuracy by over 17% in "
            "long-context environments."
        ),
        "refs": [
            "Ref 40: Tagging-Augmented Generation (ACL 2025 industry paper)",
            "Ref 41-49: instruction-formatted retrieval, structural cues, hierarchical formatting, decoupled granularity",
            "Ref 45: Lost in the Middle (Liu et al, Stanford 2023)",
        ],
        "consequence": (
            "If true, format is a load-bearing architectural variable. A presentation layer "
            "between retrieval and context injection is mandatory, not optional. Underpins "
            "new Implication #29 (Decoupled Retrieval and Injection Granularity)."
        ),
    },
    {
        "id": "R3-I5-peirce-triadic-retrieval",
        "inquiry": "Inquiry 5: Peircean Semiotics",
        "claim": (
            "Peirce's triadic sign-interpretant-object framework provides architectural "
            "leverage beyond Tulving's dyadic cue-trace ecphory. Specifically, the 'interpretant' "
            "(interpretive schema applied at retrieval time) is a computationally distinct third "
            "input that must be passed alongside query and trace to the attention mechanism. "
            "Computational implementations exist (Sowa's Conceptual Graphs, de Souza's Semiotic "
            "Engineering, SemJudge / Hierarchical Semiosis Graphs)."
        ),
        "refs": [
            "Ref 51: A Semiotically Oriented Cognitive Model of Knowledge Representation",
            "Ref 54: de Souza, Semiotic Engineering",
            "Ref 56: arxiv 2604.08641 — On Semiotic-Grounded Interpretive Evaluation of Generative Art (SemJudge)",
        ],
        "consequence": (
            "If true, retrieval architecture must be triadic (Q, O, I), not dyadic (Q, K). "
            "Underpins new Implication #28. The engineering pathway — what computational form "
            "the 'interpretant' takes — is unspecified in the source doc."
        ),
    },
]

PROMPT_TEMPLATE = """You are an independent reviewer evaluating a research claim. The claim was synthesized by another model from cited references. Your job is to assess whether the claim is plausible given what you know about the cited literature, and to flag any concerns.

INQUIRY: {inquiry}

CLAIM:
{claim}

CITED REFERENCES (paraphrased):
{refs}

ARCHITECTURAL CONSEQUENCE IF TRUE:
{consequence}

YOUR TASKS:

1. PLAUSIBILITY: Based on what you know about this research area and the cited authors/papers, is this claim plausible?
   - LIKELY_TRUE: well-established in the literature, multiple convergent sources, and your knowledge supports it
   - LIKELY_TRUE_WITH_CAVEATS: directionally right, but you'd want to flag specific caveats or scope limits
   - UNCERTAIN: insufficient evidence in your knowledge to evaluate; could be true but you can't confirm
   - LIKELY_OVERSTATED: the cited literature probably supports a weaker version of this claim
   - LIKELY_FALSE: contradicts what you know about the field

2. SPECIFIC_NUMBERS: If the claim contains specific numerical figures (percentages, gains), do those numbers match what you know? Or are they suspicious?

3. LOAD_BEARING_RISK: How risky is it to make architectural decisions on this claim alone? Consider whether the cited refs are well-established, whether the inferential leap from refs to claim is large, and whether the claim is doing more work than the evidence supports.

4. RESERVATIONS: 1-3 specific concerns or things you'd want verified before treating this as architecture-grade.

Respond with ONLY a JSON object, no prose before or after:
{{
  "plausibility": "LIKELY_TRUE" | "LIKELY_TRUE_WITH_CAVEATS" | "UNCERTAIN" | "LIKELY_OVERSTATED" | "LIKELY_FALSE",
  "numbers_check": "MATCH" | "SUSPICIOUS" | "NO_NUMBERS" | "CANT_VERIFY",
  "load_bearing_risk": "LOW" | "MEDIUM" | "HIGH",
  "reservations": ["...", "..."]
}}
"""


def run_gemini(prompt: str, timeout: int = 180) -> str:
    result = subprocess.run(
        ["gemini", "-p", prompt, "--approval-mode", "plan"],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout + ("\nSTDERR:\n" + result.stderr if result.returncode != 0 else "")


def parse_json(text: str) -> dict | None:
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        s, e = text.find("{"), text.rfind("}")
        if s < 0 or e < 0:
            return None
        candidate = text[s : e + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def main() -> int:
    done = set()
    if OUT_PATH.exists():
        for line in OUT_PATH.open():
            try:
                done.add(json.loads(line)["id"])
            except Exception:
                continue

    for c in CLAIMS:
        if c["id"] in done:
            print(f"skip (already done): {c['id']}", file=sys.stderr)
            continue

        prompt = PROMPT_TEMPLATE.format(
            inquiry=c["inquiry"],
            claim=c["claim"],
            refs="\n".join(f"- {r}" for r in c["refs"]),
            consequence=c["consequence"],
        )

        t0 = time.monotonic()
        try:
            raw = run_gemini(prompt)
        except subprocess.TimeoutExpired:
            rec = {"id": c["id"], "error": "timeout"}
        else:
            verdict = parse_json(raw)
            dur = round(time.monotonic() - t0, 2)
            if not verdict:
                rec = {"id": c["id"], "error": "unparseable", "raw": raw[:1000], "duration_s": dur}
            else:
                rec = {
                    "id": c["id"],
                    "inquiry": c["inquiry"],
                    "plausibility": verdict.get("plausibility"),
                    "numbers_check": verdict.get("numbers_check"),
                    "load_bearing_risk": verdict.get("load_bearing_risk"),
                    "reservations": verdict.get("reservations", []),
                    "duration_s": dur,
                    "verifier": "gemini",
                }

        with OUT_PATH.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        plaus = rec.get("plausibility", rec.get("error", "?"))
        risk = rec.get("load_bearing_risk", "-")
        print(f"  {c['id']:<40} {plaus:<25} risk={risk}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
