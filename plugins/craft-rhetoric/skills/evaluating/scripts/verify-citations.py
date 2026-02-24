# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "rich-click>=1.8"]
# ///
"""Citation verification with triangulated LLM grounding.

Pipeline: extract claims -> paper lookup (Scholar + OpenAlex) -> dual-model verification.

    uv run verify-citations.py article.md
    uv run verify-citations.py article.md --no-llm
    uv run verify-citations.py article.md -m google/gemma-3-27b-it:free
    uv run verify-citations.py article.md -o report.md
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

SCHOLAR = "https://api.semanticscholar.org/graph/v1"
SCHOLAR_FIELDS = "title,authors,year,abstract,citationCount,paperId"
OPENALEX = "https://api.openalex.org"

DEFAULT_MODELS = [
    "arcee-ai/trinity-large-preview:free",
    "deepseek/deepseek-r1-0528:free",
]


# -- Models -------------------------------------------------------


@dataclass
class Claim:
    text: str
    level: str
    citation: str
    author: str
    year: str | None


@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int | None
    abstract: str | None
    citations: int
    source: str  # "doi", "scholar", "openalex"


@dataclass
class ModelVerdict:
    model: str
    supported: bool | None
    confidence: str
    reasoning: str


@dataclass
class Verdict:
    claim: Claim
    paper: Paper | None
    model_verdicts: list[ModelVerdict] = field(default_factory=list)

    @property
    def consensus(self) -> bool | None:
        """True if all models agree supported, False if all agree not, else None."""
        verdicts = [v.supported for v in self.model_verdicts if v.supported is not None]
        if not verdicts:
            return None
        if all(v is True for v in verdicts):
            return True
        if all(v is False for v in verdicts):
            return False
        return None

    @property
    def divergent(self) -> bool:
        """True if models disagree."""
        verdicts = [v.supported for v in self.model_verdicts if v.supported is not None]
        if len(verdicts) < 2:
            return False
        return len(set(verdicts)) > 1


# -- Extraction ----------------------------------------------------

_EV_RE = re.compile(r'<span\s+class="ev\s+ev-(\w+)"\s+title="([^"]+)">[^<]*</span>')
_SKIP = {"same", "this", "above", "see", "compare"}


def extract_claims(markdown: str) -> list[Claim]:
    claims = []
    for m in _EV_RE.finditer(markdown):
        level, citation = m.group(1), m.group(2)

        # Grab preceding sentence as claim text
        window = markdown[max(0, m.start() - 500) : m.start()]
        for sep in [". ", ".\n", "\n\n"]:
            idx = window.rfind(sep)
            if idx != -1:
                window = window[idx + len(sep) :]
                break
        text = re.sub(r"<[^>]+>", "", window).strip()
        text = re.sub(r"\s+", " ", text)[-300:]

        author_m = re.match(r"([A-Z][a-z]+)", citation)
        year_m = re.search(r"((?:19|20)\d{2})", citation)
        if not author_m or author_m.group(1).lower() in _SKIP:
            continue

        year = year_m.group(1) if year_m else None
        claims.append(Claim(text, level, citation, author_m.group(1), year))
    return claims


# -- Bibliography (format-agnostic) --------------------------------


@dataclass
class BiblioEntry:
    author: str
    year: str
    title: str
    url: str


# Multiple patterns to match common bibliography formats
_BIB_PATTERNS = [
    # Standard: Author (Year). [Title](URL)
    re.compile(r"([A-Z][a-z]+).*?\((\d{4})\).*?\[([^\]]+)\]\(([^)]+)\)"),
    # Paragraph: Author, X. et al. (Year). "Title." ... DOI/URL
    re.compile(
        r"([A-Z][a-z]+),?\s+\w.*?\((\d{4})\)\.\s*"
        r'["""]([^"""\n]{10,})["""].*?(https?://\S+|10\.\d{4,}/\S+)'
    ),
    # Simple: Author (Year). Title. URL
    re.compile(
        r"([A-Z][a-z]+).*?\((\d{4})\)\.\s*"
        r"([^.\n]{10,})\.\s*(?:.*?)(https?://\S+)"
    ),
]


def load_bibliography(path: Path) -> list[BiblioEntry]:
    """Extract bibliography entries using multiple format patterns."""
    if not path.exists():
        return []
    text = path.read_text()
    entries: dict[tuple[str, str], BiblioEntry] = {}

    for pattern in _BIB_PATTERNS:
        for m in pattern.finditer(text):
            author, year = m.group(1), m.group(2)
            title = m.group(3).strip().rstrip(".")
            url = m.group(4).strip().rstrip(".")
            key = (author.lower(), year)
            if key not in entries:
                entries[key] = BiblioEntry(author, year, title, url)

    # Also extract standalone DOIs from the entire file
    for doi_m in re.finditer(r"(10\.\d{4,}/[^\s)\"'>]+)", text):
        doi = doi_m.group(1).rstrip(".")
        # Find nearest author/year context
        context = text[max(0, doi_m.start() - 200) : doi_m.start()]
        a = re.search(r"([A-Z][a-z]+)", context)
        y = re.search(r"\((\d{4})\)", context)
        if a and y:
            key = (a.group(1).lower(), y.group(1))
            if key not in entries:
                url = f"https://doi.org/{doi}"
                entries[key] = BiblioEntry(a.group(1), y.group(1), "", url)

    return list(entries.values())


def _bib_match(claim: Claim, entries: list[BiblioEntry]) -> BiblioEntry | None:
    for e in entries:
        if e.author.lower() == claim.author.lower() and e.year == claim.year:
            return e
    return None


# -- Paper Lookup --------------------------------------------------


def _doi_from_url(url: str) -> str | None:
    m = re.search(r"(10\.\d{4,}/[^\s)\"'>]+)", url)
    return m.group(1).rstrip(".") if m else None


def _parse_scholar(d: dict, source: str) -> Paper:
    authors = [a.get("name", "") for a in d.get("authors", [])]
    return Paper(
        d.get("title", ""),
        authors,
        d.get("year"),
        d.get("abstract"),
        d.get("citationCount", 0),
        source,
    )


def _scholar_doi(doi: str, client: httpx.Client) -> Paper | None:
    try:
        r = client.get(
            f"{SCHOLAR}/paper/DOI:{doi}",
            params={"fields": SCHOLAR_FIELDS},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        return _parse_scholar(r.json(), "doi")
    except httpx.HTTPError:
        return None


def _scholar_search(query: str, client: httpx.Client) -> Paper | None:
    try:
        r = client.get(
            f"{SCHOLAR}/paper/search",
            params={"query": query, "limit": 3, "fields": SCHOLAR_FIELDS},
            timeout=10,
        )
        if r.status_code == 429:
            time.sleep(3)
            r = client.get(
                f"{SCHOLAR}/paper/search",
                params={
                    "query": query,
                    "limit": 3,
                    "fields": SCHOLAR_FIELDS,
                },
                timeout=10,
            )
        if r.status_code != 200:
            return None
        data = r.json().get("data", [])
        if not data:
            return None
        return _parse_scholar(data[0], "scholar")
    except httpx.HTTPError:
        return None


def _reconstruct_abstract(inv: dict) -> str:
    words: dict[int, str] = {}
    for w, positions in inv.items():
        for p in positions:
            words[p] = w
    return " ".join(words[i] for i in sorted(words))


def _openalex(
    claim: Claim,
    title_hint: str | None,
    client: httpx.Client,
) -> Paper | None:
    """Search OpenAlex with title hint or keywords from citation."""
    if title_hint:
        query = title_hint
    else:
        # Extract searchable keywords from citation text
        q = re.sub(
            r"[A-Z][a-z]+\s+et al\.?|et al\.?"
            r"|\d{4}|n=[\d,]+|[—,().●◐○◌]",
            " ",
            claim.citation,
        )
        query = " ".join(w for w in q.split() if len(w) > 2)
    if not query.strip():
        return None
    year_filter = f"publication_year:{claim.year}" if claim.year else ""

    try:
        r = client.get(
            f"{OPENALEX}/works",
            params={
                "search": query,
                "filter": year_filter,
                "per_page": 5,
            },
            headers={"User-Agent": "verify-citations/0.2 (cix)"},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        results = r.json().get("results", [])
        if not results:
            return None

        for work in results:
            authorships = work.get("authorships", [])[:10]
            authors = [a.get("author", {}).get("display_name", "") for a in authorships]
            if any(claim.author.lower() in a.lower() for a in authors):
                inv = work.get("abstract_inverted_index")
                abstract = _reconstruct_abstract(inv) if inv else None
                return Paper(
                    work.get("title", ""),
                    authors[:5],
                    work.get("publication_year"),
                    abstract,
                    work.get("cited_by_count", 0),
                    "openalex",
                )
        return None
    except httpx.HTTPError:
        return None


def _build_search_query(claim: Claim) -> str:
    """Build a search query from citation metadata."""
    # Extract venue and topic keywords from citation
    parts = re.split(r"[,;—]", claim.citation)
    keywords = []
    for part in parts:
        part = part.strip()
        # Skip author/year/sample-size fragments
        if re.match(r"^[A-Z][a-z]+ et al", part):
            continue
        if re.match(r"^\d{4}$", part):
            continue
        if re.match(r"^n[=≈]", part):
            continue
        cleaned = re.sub(r"[()]", "", part).strip()
        if cleaned and len(cleaned) > 2:
            keywords.append(cleaned)
    query = f"{claim.author} {' '.join(keywords)}"
    if claim.year:
        query += f" {claim.year}"
    return query


def find_paper(
    claim: Claim,
    biblio: list[BiblioEntry],
    client: httpx.Client,
) -> Paper | None:
    """Find paper: bibliography DOI -> Scholar search -> OpenAlex."""
    # 1. Try bibliography DOI
    bib = _bib_match(claim, biblio)
    if bib:
        doi = _doi_from_url(bib.url)
        if doi:
            p = _scholar_doi(doi, client)
            if p:
                return p
        if bib.title:
            p = _scholar_search(bib.title, client)
            if p:
                return p

    # 2. Search Scholar directly from citation metadata
    query = _build_search_query(claim)
    p = _scholar_search(query, client)
    if p:
        return p

    # 3. OpenAlex fallback
    return _openalex(claim, bib.title if bib else None, client)


# -- LLM Verification (Triangulated) ------------------------------

_VERIFY_PROMPT = """\
You are a citation fact-checker. Verify whether this academic claim is \
accurate based on your knowledge of the cited paper.

CLAIM: {claim}
CITATION: {citation}
PAPER: {paper_info}

Respond with JSON only, no other text:
{{"supported": true/false/null, "confidence": "high"/"medium"/"low", \
"reasoning": "1-2 sentences"}}

Rules:
- true = the claim accurately represents findings from this paper
- false = the claim misrepresents the paper (wrong numbers, wrong conclusion, wrong attribution)
- null = you don't have enough knowledge of this specific paper to verify
- Check specific numbers: if the claim says β=0.507 or 17% or n=654, verify those
- Check attribution: is this finding actually from this author/paper?
- If you're unsure, say null — don't guess"""


def _ask_llm(
    claim: Claim,
    paper: Paper | None,
    client: httpx.Client,
    base_url: str,
    api_key: str,
    model: str,
) -> tuple[bool | None, str, str]:
    """Returns (supported, reasoning, confidence)."""
    paper_info = ""
    if paper:
        paper_info = f"Title: {paper.title}\n"
        paper_info += f"Authors: {', '.join(paper.authors[:5])}\n"
        paper_info += f"Year: {paper.year}\n"
        paper_info += f"Citations: {paper.citations}\n"
        if paper.abstract:
            paper_info += f"Abstract: {paper.abstract}\n"
    else:
        paper_info = "(Paper not found in databases — verify from your knowledge)"

    prompt = _VERIFY_PROMPT.format(
        claim=claim.text,
        citation=claim.citation,
        paper_info=paper_info,
    )
    try:
        r = client.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 300,
            },
            timeout=60,
        )
        if r.status_code != 200:
            return None, f"API error {r.status_code}", "low"
        content = r.json()["choices"][0]["message"]["content"]
        # Strip reasoning model think tags (DeepSeek R1, etc.)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        # Extract JSON from markdown code blocks if present
        if "```" in content:
            m = re.search(
                r"```(?:json)?\s*(\{.*?\})\s*```",
                content,
                re.DOTALL,
            )
            if m:
                content = m.group(1)
        # Try to find JSON object in response
        json_m = re.search(r"\{[^{}]*\}", content, re.DOTALL)
        if json_m:
            content = json_m.group(0)
        result = json.loads(content)
        return (
            result.get("supported"),
            result.get("reasoning", ""),
            result.get("confidence", "medium"),
        )
    except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
        return None, str(e), "low"


def _triangulate(
    claim: Claim,
    paper: Paper | None,
    models: list[str],
    client: httpx.Client,
    base_url: str,
    api_key: str,
    console: Console,
) -> list[ModelVerdict]:
    """Run claim against multiple models, return all verdicts."""
    verdicts: list[ModelVerdict] = []

    for model in models:
        short = model.split("/")[-1].split(":")[0][:12]
        supported, reasoning, confidence = _ask_llm(claim, paper, client, base_url, api_key, model)
        verdicts.append(ModelVerdict(model, supported, confidence, reasoning))
        style = _verdict_style(supported)
        console.print(f"[dim]{short}[/]={style}", end=" ")
        time.sleep(0.5)  # rate limit courtesy

    return verdicts


# -- Orchestration -------------------------------------------------


def _verdict_style(supported: bool | None) -> str:
    if supported is True:
        return "[green]yes[/]"
    if supported is False:
        return "[red]no[/]"
    return "[yellow]?[/]"


def verify_all(
    claims: list[Claim],
    biblio: list[BiblioEntry],
    models: list[str],
    skip_llm: bool,
    console: Console,
) -> list[Verdict]:
    base_url = os.environ.get("VERIFY_BASE_URL", "https://openrouter.ai/api/v1")
    api_key = os.environ.get("VERIFY_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
    has_llm = bool(api_key) and not skip_llm
    verdicts: list[Verdict] = []

    with httpx.Client() as client:
        for i, claim in enumerate(claims):
            prefix = f"  [{i + 1}/{len(claims)}]"
            label = f"{claim.author} {claim.year or ''}"
            console.print(f"{prefix} {label}...", end=" ")
            time.sleep(0.3)

            paper = find_paper(claim, biblio, client)
            if paper:
                cit = f"{paper.citations} cit."
                console.print(
                    f"[green]found[/] via {paper.source} ({cit})",
                    end=" ",
                )
            else:
                console.print("[yellow]db miss[/]", end=" ")

            if has_llm:
                model_verdicts = _triangulate(
                    claim, paper, models, client, base_url, api_key, console
                )
                console.print()
                verdicts.append(Verdict(claim, paper, model_verdicts))
            else:
                console.print("[dim]skipped[/]")
                verdicts.append(Verdict(claim, paper))

    return verdicts


# -- Report --------------------------------------------------------


def _consensus_label(v: Verdict) -> str:
    if not v.paper:
        return "[red]NOT FOUND[/]"
    if not v.model_verdicts:
        return "[yellow]PARTIAL[/]"
    if v.divergent:
        return "[yellow]DIVERGENT[/]"
    c = v.consensus
    if c is True:
        return "[green]VERIFIED[/]"
    if c is False:
        return "[red]CONTRADICTED[/]"
    return "[yellow]INCONCLUSIVE[/]"


def render_report(
    verdicts: list[Verdict],
    filepath: str,
    console: Console,
) -> None:
    found = sum(1 for v in verdicts if v.paper)
    verified = sum(1 for v in verdicts if v.consensus is True)
    contradicted = sum(1 for v in verdicts if v.consensus is False)
    divergent = sum(1 for v in verdicts if v.divergent)

    summary = (
        f"[bold]{Path(filepath).name}[/]\n"
        f"{len(verdicts)} claims  ·  {found} found  ·  "
        f"[green]{verified} verified[/]  ·  "
        f"[red]{contradicted} contradicted[/]"
    )
    if divergent:
        summary += f"  ·  [yellow]{divergent} divergent[/]"

    console.print()
    console.print(Panel(summary, title="Citation Verification", border_style="blue"))

    table = Table(show_lines=True, expand=True)
    table.add_column("#", width=3, justify="right")
    table.add_column("Citation", width=22)
    table.add_column("Paper", width=36)
    table.add_column("Verdict", width=14)
    table.add_column("Models", ratio=1)

    for i, v in enumerate(verdicts, 1):
        cite = f"[bold]{v.claim.author}[/] {v.claim.year or ''}\n[dim]{v.claim.level}[/]"
        if v.paper:
            title = v.paper.title
            if len(title) > 55:
                title = title[:55] + "..."
            paper_col = f"{title}\n[dim]{v.paper.citations} cit · {v.paper.source}[/]"
        else:
            paper_col = "[red]Not found[/]"

        model_col = ""
        for mv in v.model_verdicts:
            short = mv.model.split("/")[-1].split(":")[0][:12]
            style = _verdict_style(mv.supported)
            model_col += f"[dim]{short}[/]: {style}\n"
            if mv.reasoning:
                reason = mv.reasoning[:80]
                model_col += f"[dim]{reason}[/]\n"

        table.add_row(str(i), cite, paper_col, _consensus_label(v), model_col)

    console.print(table)


def save_report(
    verdicts: list[Verdict],
    filepath: str,
    output: Path,
) -> None:
    lines = [
        f"# Citation Verification: {Path(filepath).name}\n",
        "| # | Citation | Found | Consensus | Models |",
        "|---|----------|-------|-----------|--------|",
    ]
    for i, v in enumerate(verdicts, 1):
        if v.divergent:
            label = "DIVERGENT"
        elif v.consensus is True:
            label = "VERIFIED"
        elif v.consensus is False:
            label = "CONTRADICTED"
        elif v.paper:
            label = "PARTIAL"
        else:
            label = "NOT FOUND"
        found = "Yes" if v.paper else "No"
        year = v.claim.year or ""

        model_notes = []
        for mv in v.model_verdicts:
            short = mv.model.split("/")[-1].split(":")[0]
            sup = {True: "yes", False: "no", None: "?"}[mv.supported]
            reason = mv.reasoning.replace("|", "/")[:60]
            model_notes.append(f"{short}={sup}: {reason}")
        models = "; ".join(model_notes) if model_notes else "-"

        lines.append(f"| {i} | {v.claim.author} {year} | {found} | {label} | {models} |")
    output.write_text("\n".join(lines) + "\n")


# -- CLI -----------------------------------------------------------


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "-m",
    "--model",
    multiple=True,
    help="LLM model(s) for verification. Repeat for triangulation.",
)
@click.option("--no-llm", is_flag=True, help="Paper lookup only")
@click.option(
    "-b",
    "--bibliography",
    type=click.Path(exists=True),
    help="Bibliography file (any markdown format with DOIs/URLs)",
)
@click.option("-o", "--output", type=click.Path(), help="Save markdown report")
def cli(
    filepath: str,
    model: tuple[str, ...],
    no_llm: bool,
    bibliography: str | None,
    output: str | None,
) -> None:
    """Verify evidence-tagged citations in a markdown article.

    \b
    Extracts <span class="ev ..."> evidence spans, finds the cited papers
    via Semantic Scholar + OpenAlex, then verifies claims against paper
    abstracts using multiple LLMs for triangulated confidence.

    \b
    Default models: arcee-ai/trinity-large-preview:free + deepseek/deepseek-r1-0528:free
    Env: OPENROUTER_API_KEY or VERIFY_API_KEY + VERIFY_BASE_URL
    """
    console = Console()
    md = Path(filepath).read_text()

    # Resolve models
    models = list(model) if model else DEFAULT_MODELS

    console.print(f"\n[bold]Extracting claims from[/] {filepath}")
    claims = extract_claims(md)
    console.print(f"  Found [bold]{len(claims)}[/] evidence-tagged claims")

    # Try to find bibliography (format-agnostic)
    bib_path = (
        Path(bibliography)
        if bibliography
        else Path(filepath).parent.parent / "reference" / "bibliography.md"
    )
    biblio = load_bibliography(bib_path) if bib_path.exists() else []
    if biblio:
        console.print(f"  Loaded [bold]{len(biblio)}[/] bibliography entries from {bib_path.name}")

    if not no_llm:
        model_names = ", ".join(m.split("/")[-1].split(":")[0] for m in models)
        console.print(f"  Models: [bold]{model_names}[/]")
    console.print()

    if not claims:
        console.print("[yellow]No evidence spans found.[/]")
        return

    api_key = os.environ.get("VERIFY_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
    if not no_llm and not api_key:
        console.print("[yellow]No API key — paper lookup only.[/]\n")
        no_llm = True

    verdicts = verify_all(claims, biblio, models, no_llm, console)
    render_report(verdicts, filepath, console)

    if output:
        save_report(verdicts, filepath, Path(output))
        console.print(f"\n[dim]Saved to {output}[/]")


if __name__ == "__main__":
    cli()
