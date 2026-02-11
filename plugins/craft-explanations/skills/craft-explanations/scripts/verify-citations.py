# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "rich-click>=1.8"]
# ///
"""Citation verification for CIX library articles.

Pipeline: extract claims -> bibliography DOI -> OpenAlex -> LLM grounding.

    uv run scripts/verify-citations.py article.md --no-llm
    uv run scripts/verify-citations.py article.md -m google/gemini-2.0-flash-001
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

import httpx
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

SCHOLAR = "https://api.semanticscholar.org/graph/v1"
SCHOLAR_FIELDS = "title,authors,year,abstract,citationCount,paperId"
OPENALEX = "https://api.openalex.org"


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
    source: str  # "doi", "title", "openalex"


@dataclass
class Verdict:
    claim: Claim
    paper: Paper | None
    supported: bool | None  # True/False/None
    reasoning: str


@dataclass
class BiblioEntry:
    author: str
    year: str
    title: str
    url: str


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


# -- Bibliography --------------------------------------------------

_BIB_RE = re.compile(r"([A-Z][a-z]+).*?\((\d{4})\).*?\[([^\]]+)\]\(([^)]+)\)")


def load_bibliography(path: Path) -> list[BiblioEntry]:
    if not path.exists():
        return []
    return [
        BiblioEntry(m.group(1), m.group(2), m.group(3), m.group(4))
        for m in _BIB_RE.finditer(path.read_text())
    ]


def _bib_match(claim: Claim, entries: list[BiblioEntry]) -> BiblioEntry | None:
    for e in entries:
        if e.author.lower() == claim.author.lower() and e.year == claim.year:
            return e
    return None


# -- Paper Lookup --------------------------------------------------


def _doi_from_url(url: str) -> str | None:
    m = re.search(r"(10\.\d{4,}/[^\s)]+)", url)
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


def _scholar_search(title: str, client: httpx.Client) -> Paper | None:
    params = {
        "query": title,
        "limit": 3,
        "fields": SCHOLAR_FIELDS,
    }
    try:
        r = client.get(
            f"{SCHOLAR}/paper/search",
            params=params,
            timeout=10,
        )
        if r.status_code == 429:
            time.sleep(3)
            r = client.get(
                f"{SCHOLAR}/paper/search",
                params=params,
                timeout=10,
            )
        if r.status_code != 200:
            return None
        data = r.json().get("data", [])
        if not data:
            return None
        return _parse_scholar(data[0], "title")
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
    """Search OpenAlex with title hint or topic keywords."""
    if title_hint:
        query = title_hint
    else:
        q = re.sub(
            r"[A-Z][a-z]+\s+et al\.?|et al\.?"
            r"|\d{4}|n=[\d,]+|[—,().●]",
            " ",
            claim.citation,
        )
        query = " ".join(w for w in q.split() if len(w) > 2)
    year_filter = f"publication_year:{claim.year}" if claim.year else ""

    try:
        r = client.get(
            f"{OPENALEX}/works",
            params={
                "search": query,
                "filter": year_filter,
                "per_page": 5,
            },
            headers={
                "User-Agent": "verify-citations/0.1 (cix)",
            },
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


def find_paper(
    claim: Claim,
    biblio: list[BiblioEntry],
    client: httpx.Client,
) -> Paper | None:
    """Bibliography DOI -> Semantic Scholar title -> OpenAlex."""
    bib = _bib_match(claim, biblio)
    if bib:
        doi = _doi_from_url(bib.url)
        if doi:
            p = _scholar_doi(doi, client)
            if p:
                return p
        p = _scholar_search(bib.title, client)
        if p:
            return p

    return _openalex(claim, bib.title if bib else None, client)


# -- LLM Verification ---------------------------------------------

_VERIFY_PROMPT = """\
You verify citations. Given a CLAIM and the cited paper's \
ABSTRACT, does the abstract support the claim?

CLAIM: {claim}
CITATION: {citation}
ABSTRACT: {abstract}

JSON only: {{"supported": true/false/null, \
"confidence": "high"/"medium"/"low", \
"reasoning": "1-2 sentences"}}
- true = abstract supports direction and approximate magnitude
- false = abstract contradicts the claim
- null = not enough info to verify"""


def _ask_llm(
    claim: Claim,
    abstract: str,
    client: httpx.Client,
    base_url: str,
    api_key: str,
    model: str,
) -> tuple[bool | None, str]:
    prompt = _VERIFY_PROMPT.format(
        claim=claim.text,
        citation=claim.citation,
        abstract=abstract,
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
            return None, f"API error {r.status_code}"
        content = r.json()["choices"][0]["message"]["content"]
        if "```" in content:
            m = re.search(
                r"```(?:json)?\s*({.*?})\s*```",
                content,
                re.DOTALL,
            )
            if m:
                content = m.group(1)
        result = json.loads(content)
        return result.get("supported"), result.get("reasoning", "")
    except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
        return None, str(e)


# -- Orchestration -------------------------------------------------


def _verdict_style(supported: bool | None) -> str:
    if supported is True:
        return "[green]supported[/]"
    if supported is False:
        return "[red]contradicted[/]"
    return "[yellow]inconclusive[/]"


def verify_all(
    claims: list[Claim],
    biblio: list[BiblioEntry],
    model: str,
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
            if not paper:
                _handle_not_found(claim, biblio, verdicts, console)
                continue

            cit = f"{paper.citations} cit."
            console.print(
                f"[green]found[/] via {paper.source} ({cit})",
                end=" ",
            )

            supported, reasoning = _verify_paper(
                claim,
                paper,
                has_llm,
                client,
                base_url,
                api_key,
                model,
                console,
            )
            verdicts.append(Verdict(claim, paper, supported, reasoning))

    return verdicts


def _handle_not_found(
    claim: Claim,
    biblio: list[BiblioEntry],
    verdicts: list[Verdict],
    console: Console,
) -> None:
    same_year = [
        e.author
        for e in biblio
        if e.year == claim.year and e.author.lower() != claim.author.lower()
    ]
    if same_year:
        names = ", ".join(same_year[:5])
        hint = f"Not found. Bib has {claim.year}: {names} — misattribution?"
        console.print(f"[red]not found[/] [dim]({claim.year} bib: {names})[/]")
    else:
        hint = "Not found"
        console.print("[red]not found[/]")
    verdicts.append(Verdict(claim, None, None, hint))


def _verify_paper(
    claim: Claim,
    paper: Paper,
    has_llm: bool,
    client: httpx.Client,
    base_url: str,
    api_key: str,
    model: str,
    console: Console,
) -> tuple[bool | None, str]:
    if has_llm and paper.abstract:
        supported, reasoning = _ask_llm(
            claim,
            paper.abstract,
            client,
            base_url,
            api_key,
            model,
        )
        console.print(_verdict_style(supported))
        return supported, reasoning
    if paper.abstract:
        console.print("[dim]skipped[/]")
        return None, "LLM skipped"
    console.print("[yellow]no abstract[/]")
    return None, "No abstract"


# -- Report --------------------------------------------------------


def _label(v: Verdict) -> str:
    if v.supported is True:
        return "[green]VERIFIED[/]"
    if v.supported is False:
        return "[red]CONTRADICTED[/]"
    if v.paper:
        return "[yellow]PARTIAL[/]"
    return "[red]NOT FOUND[/]"


def render_report(
    verdicts: list[Verdict],
    filepath: str,
    console: Console,
) -> None:
    found = sum(1 for v in verdicts if v.paper)
    ok = sum(1 for v in verdicts if v.supported is True)
    bad = sum(1 for v in verdicts if v.supported is False)

    summary = (
        f"[bold]{Path(filepath).name}[/]\n"
        f"{len(verdicts)} claims  ·  {found} found  ·  "
        f"[green]{ok} supported[/]  ·  "
        f"[red]{bad} contradicted[/]"
    )
    console.print()
    console.print(
        Panel(
            summary,
            title="Citation Verification",
            border_style="blue",
        )
    )

    table = Table(show_lines=True, expand=True)
    table.add_column("#", width=3, justify="right")
    table.add_column("Citation", width=24)
    table.add_column("Paper", width=40)
    table.add_column("Verdict", width=13)
    table.add_column("Reasoning", ratio=1)

    for i, v in enumerate(verdicts, 1):
        cite = f"[bold]{v.claim.author}[/] {v.claim.year or ''}\n[dim]{v.claim.level}[/]"
        if v.paper:
            title = v.paper.title
            if len(title) > 65:
                title = title[:65] + "..."
            paper = f"{title}\n[dim]{v.paper.citations} cit · {v.paper.source}[/]"
        else:
            paper = "[red]Not found[/]"
        table.add_row(str(i), cite, paper, _label(v), v.reasoning)

    console.print(table)


def save_report(
    verdicts: list[Verdict],
    filepath: str,
    output: Path,
) -> None:
    header = f"# Citation Verification: {Path(filepath).name}\n"
    cols = "| # | Citation | Found | Verdict | Reasoning |"
    sep = "|---|----------|-------|---------|-----------|"
    lines = [header, cols, sep]
    for i, v in enumerate(verdicts, 1):
        if v.supported is True:
            label = "VERIFIED"
        elif v.supported is False:
            label = "CONTRADICTED"
        elif v.paper:
            label = "PARTIAL"
        else:
            label = "NOT FOUND"
        found = "Yes" if v.paper else "No"
        reason = v.reasoning.replace("|", "/")
        year = v.claim.year or ""
        lines.append(f"| {i} | {v.claim.author} {year} | {found} | {label} | {reason} |")
    output.write_text("\n".join(lines) + "\n")


# -- CLI -----------------------------------------------------------


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "-m",
    "--model",
    default="moonshotai/kimi-k2.5",
    show_default=True,
    help="LLM model (OpenRouter or OpenAI-compatible)",
)
@click.option(
    "--no-llm",
    is_flag=True,
    help="Paper lookup only",
)
@click.option(
    "-b",
    "--bibliography",
    type=click.Path(exists=True),
    help="Bibliography with [Title](URL) entries",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Save markdown report",
)
def cli(
    filepath: str,
    model: str,
    no_llm: bool,
    bibliography: str | None,
    output: str | None,
) -> None:
    """Verify citations in a CIX library article.

    \b
    Env: OPENROUTER_API_KEY or VERIFY_API_KEY + VERIFY_BASE_URL
    """
    console = Console()
    md = Path(filepath).read_text()

    console.print(f"\n[bold]Extracting claims from[/] {filepath}")
    claims = extract_claims(md)
    console.print(f"  Found [bold]{len(claims)}[/] evidence-tagged claims")

    bib_path = (
        Path(bibliography)
        if bibliography
        else Path(filepath).parent.parent / "reference" / "bibliography.md"
    )
    biblio = load_bibliography(bib_path) if bib_path.exists() else []
    if biblio:
        console.print(f"  Loaded [bold]{len(biblio)}[/] bibliography entries from {bib_path.name}")
    console.print()

    if not claims:
        console.print("[yellow]No evidence spans found.[/]")
        return

    api_key = os.environ.get("VERIFY_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
    if not no_llm and not api_key:
        console.print("[yellow]No API key — paper lookup only.[/]\n")
        no_llm = True

    verdicts = verify_all(claims, biblio, model, no_llm, console)
    render_report(verdicts, filepath, console)

    if output:
        save_report(verdicts, filepath, Path(output))
        console.print(f"\n[dim]Saved to {output}[/]")


if __name__ == "__main__":
    cli()
