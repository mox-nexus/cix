"""CLI for paper scout — thin driving adapter, config-driven."""

from __future__ import annotations

import asyncio
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from recon.config import ReconConfig, build_pipeline
from recon.adapters._out.pdftotext import PdftotextAdapter
from recon.adapters._out.pdf_download import PdfDownloadAdapter
from recon.adapters._out.semantic_scholar import SemanticScholarAdapter
from recon.domain.types import Paper, WebSource

console = Console()


@click.group()
def main() -> None:
    """Paper scout for craft-research."""


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--year-min", type=int, help="Earliest publication year")
@click.option("--year-max", type=int, help="Latest publication year")
@click.option("--min-citations", type=int, default=0, help="Minimum citation count")
def search(query: str, limit: int, year_min: int | None, year_max: int | None, min_citations: int) -> None:
    """Search Semantic Scholar for papers."""
    s2 = SemanticScholarAdapter()
    with console.status("Searching Semantic Scholar..."):
        papers = s2.search(query, limit=limit, year_min=year_min, year_max=year_max, min_citations=min_citations)

    if not papers:
        console.print("[yellow]No results found.[/yellow]")
        return

    _print_results_table(papers)
    console.print(f"\n[dim]{len(papers)} results[/dim]")


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=10, help="Max results")
@click.option("--output", "-o", type=click.Path(), default=".", help="Output directory")
@click.option("--year-min", type=int, help="Earliest publication year")
@click.option("--year-max", type=int, help="Latest publication year")
@click.option("--min-citations", type=int, default=0, help="Minimum citation count")
@click.option("--keep-pdf", is_flag=True, help="Keep PDF files after conversion")
def fetch(
    query: str, limit: int, output: str,
    year_min: int | None, year_max: int | None,
    min_citations: int, keep_pdf: bool,
) -> None:
    """Search, download, and convert papers via matrix DAG."""
    config = ReconConfig.academic_preset(
        query, Path(output), limit=limit, year_min=year_min,
        year_max=year_max, min_citations=min_citations, keep_pdf=keep_pdf,
    )
    construct = _run(config)
    _print_academic_summary(construct["recon.v1/papers"], construct["recon.v1/texts"])


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=10, help="Max results")
@click.option("--output", "-o", type=click.Path(), default=".", help="Output directory")
@click.option("--keep-pdf", is_flag=True, help="Keep PDF files")
def web(query: str, limit: int, output: str, keep_pdf: bool) -> None:
    """Search the web, fetch and extract content."""
    config = ReconConfig.web_preset(query, Path(output), limit=limit, keep_pdf=keep_pdf)
    construct = _run(config)
    _print_web_summary(construct["recon.v1/web.sources"], construct["recon.v1/web.texts"])


@main.command()
@click.argument("paper_id")
@click.option("--output", "-o", type=click.Path(), default=".", help="Output directory")
@click.option("--keep-pdf", is_flag=True, help="Keep PDF after conversion")
def get(paper_id: str, output: str, keep_pdf: bool) -> None:
    """Fetch a specific paper by DOI, arXiv ID, or S2 ID."""
    s2 = SemanticScholarAdapter()
    downloader = PdfDownloadAdapter()
    converter = PdftotextAdapter()
    output_dir = Path(output)

    with console.status("Looking up paper..."):
        paper = s2.get_by_id(paper_id)

    if not paper:
        console.print(f"[red]Paper not found: {paper_id}[/red]")
        raise SystemExit(1)

    console.print(f"[green]Found:[/green] {paper.citation}\n")

    pdf_path = downloader.download(paper, output_dir)
    if not pdf_path:
        console.print("[yellow]No open access PDF available.[/yellow]")
        return

    txt_path = converter.to_text(pdf_path, output_dir)
    if txt_path:
        console.print(f"[green]✓[/green] {txt_path.name}")
        if not keep_pdf:
            pdf_path.unlink(missing_ok=True)
    else:
        console.print("[yellow]PDF downloaded but conversion failed.[/yellow]")


@main.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output directory (default: same as PDF)")
def convert(pdf_path: str, output: str | None) -> None:
    """Convert a local PDF to text."""
    converter = PdftotextAdapter()
    txt_path = converter.to_text(Path(pdf_path), Path(output) if output else None)
    if txt_path:
        console.print(f"[green]✓[/green] {txt_path}")
    else:
        console.print("[red]Conversion failed.[/red]")
        raise SystemExit(1)


# ── Internals ────────────────────────────────────────────────────────

def _run(config: ReconConfig):
    pipeline = build_pipeline(config)
    with console.status("Running recon pipeline..."):
        return asyncio.run(pipeline.run())


def _print_academic_summary(papers: list[Paper], texts: list[tuple[Paper, Path | None]]) -> None:
    downloaded = [(p, path) for p, path in texts if path is not None]
    paywalled = [p for p, path in texts if path is None]

    for paper, txt_path in downloaded:
        label = f"{paper.authors[0].split()[-1] if paper.authors else '?'} {paper.year}"
        console.print(f"  [green]✓[/green] {label} → {txt_path.name}")
    for paper in paywalled:
        label = f"{paper.authors[0].split()[-1] if paper.authors else '?'} {paper.year}"
        console.print(f"  [dim]✗ {label} — no open access PDF[/dim]")

    console.print(f"\n[bold]Summary:[/bold] {len(downloaded)} converted, {len(paywalled)} unavailable, {len(papers)} total")


def _print_web_summary(sources: list[WebSource], texts: list[tuple[WebSource, Path | None]]) -> None:
    fetched = [(s, path) for s, path in texts if path is not None]
    failed = [s for s, path in texts if path is None]

    for source, txt_path in fetched:
        console.print(f"  [green]✓[/green] {source.title[:60]} → {txt_path.name}")
    for source in failed:
        console.print(f"  [dim]✗ {source.title[:60]}[/dim]")

    console.print(f"\n[bold]Summary:[/bold] {len(fetched)} fetched, {len(failed)} failed, {len(sources)} total")


def _print_results_table(papers: list[Paper]) -> None:
    table = Table(show_lines=False)
    table.add_column("#", style="dim", width=3)
    table.add_column("Year", width=4)
    table.add_column("Authors", max_width=25)
    table.add_column("Title", max_width=55)
    table.add_column("Cite", justify="right", width=5)
    table.add_column("OA", width=3)

    for i, p in enumerate(papers, 1):
        authors = p.authors[0].split()[-1] if p.authors else "?"
        if len(p.authors) > 1:
            authors += " et al."
        oa = "[green]✓[/green]" if p.open_access_url or p.arxiv_id else "[dim]✗[/dim]"
        table.add_row(str(i), str(p.year or "?"), authors, p.title[:55], str(p.citation_count), oa)

    console.print(table)
