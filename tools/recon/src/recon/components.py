"""Matrix components for the recon DAG.

Components are thin wrappers around port calls. Adapters are injected
via the composition root (config.py). Components never import adapters.

Two pipelines:
  Academic:  SearchNode → DownloadNode → ConvertNode → InventoryNode
  Web:       WebSearchNode → WebFetchNode → WebInventoryNode
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel
from matrix import Construct, TypedStruct

from recon.domain.ports import (
    ConvertPort,
    DownloadPort,
    SearchPort,
    WebFetchPort,
    WebSearchPort,
)
from recon.domain.types import Paper, WebSource


# ── Configs ──────────────────────────────────────────────────────────

class SearchConfig(BaseModel, frozen=True):
    """Config for academic search."""

    query: str
    limit: int = 20
    year_min: int | None = None
    year_max: int | None = None
    min_citations: int = 0


class WebSearchConfig(BaseModel, frozen=True):
    """Config for web search."""

    query: str
    limit: int = 10
    output_dir: Path = Path(".")
    keep_pdf: bool = False


class OutputConfig(BaseModel, frozen=True):
    """Config for output-producing nodes."""

    output_dir: Path = Path(".")
    keep_pdf: bool = False


class InventoryConfig(BaseModel, frozen=True):
    """Config for inventory generation."""

    output_dir: Path = Path(".")
    query: str = ""


# ── Academic Pipeline ────────────────────────────────────────────────

class SearchNode:
    """Search for papers via SearchPort. Root node.

    produces: recon.v1/papers
    """

    name = "search"
    consumes: frozenset[str] = frozenset()
    produces = "recon.v1/papers"

    def __init__(self, config: SearchConfig, adapter: SearchPort) -> None:
        self._config = config
        self._adapter = adapter

    async def run(self, construct: Construct) -> TypedStruct:
        papers = self._adapter.search(
            self._config.query,
            limit=self._config.limit,
            year_min=self._config.year_min,
            year_max=self._config.year_max,
            min_citations=self._config.min_citations,
        )
        return TypedStruct("recon.v1/papers", papers)


class DownloadNode:
    """Download PDFs via DownloadPort.

    consumes: recon.v1/papers
    produces: recon.v1/downloads
    """

    name = "download"
    consumes = frozenset({"recon.v1/papers"})
    produces = "recon.v1/downloads"

    def __init__(self, config: OutputConfig, adapter: DownloadPort) -> None:
        self._config = config
        self._adapter = adapter

    async def run(self, construct: Construct) -> TypedStruct:
        papers: list[Paper] = construct["recon.v1/papers"]
        results = [
            (paper, self._adapter.download(paper, self._config.output_dir))
            for paper in papers
        ]
        return TypedStruct("recon.v1/downloads", results)


class ConvertNode:
    """Convert PDFs to text via ConvertPort.

    consumes: recon.v1/downloads
    produces: recon.v1/texts
    """

    name = "convert"
    consumes = frozenset({"recon.v1/downloads"})
    produces = "recon.v1/texts"

    def __init__(self, config: OutputConfig, adapter: ConvertPort) -> None:
        self._config = config
        self._adapter = adapter

    async def run(self, construct: Construct) -> TypedStruct:
        downloads: list[tuple[Paper, Path | None]] = construct["recon.v1/downloads"]
        results: list[tuple[Paper, Path | None]] = []

        for paper, pdf_path in downloads:
            if pdf_path is None:
                results.append((paper, None))
                continue

            txt_path = self._adapter.to_text(pdf_path, self._config.output_dir)
            results.append((paper, txt_path))

            if txt_path and not self._config.keep_pdf:
                pdf_path.unlink(missing_ok=True)

        return TypedStruct("recon.v1/texts", results)


# ── Web Pipeline ─────────────────────────────────────────────────────

class WebSearchNode:
    """Search the web via WebSearchPort. Root node.

    produces: recon.v1/web.sources
    """

    name = "web_search"
    consumes: frozenset[str] = frozenset()
    produces = "recon.v1/web.sources"

    def __init__(self, config: WebSearchConfig, adapter: WebSearchPort) -> None:
        self._config = config
        self._adapter = adapter

    async def run(self, construct: Construct) -> TypedStruct:
        sources = self._adapter.search(self._config.query, limit=self._config.limit)
        return TypedStruct("recon.v1/web.sources", sources)


class WebFetchNode:
    """Fetch web sources via WebFetchPort + ConvertPort.

    consumes: recon.v1/web.sources
    produces: recon.v1/web.texts
    """

    name = "web_fetch"
    consumes = frozenset({"recon.v1/web.sources"})
    produces = "recon.v1/web.texts"

    def __init__(self, config: WebSearchConfig, web_adapter: WebFetchPort, convert_adapter: ConvertPort) -> None:
        self._config = config
        self._web = web_adapter
        self._convert = convert_adapter

    async def run(self, construct: Construct) -> TypedStruct:
        sources: list[WebSource] = construct["recon.v1/web.sources"]
        results: list[tuple[WebSource, Path | None]] = []

        for source in sources:
            path = self._web.fetch(source.url, self._config.output_dir)

            if path and path.suffix == ".pdf":
                txt_path = self._convert.to_text(path, self._config.output_dir)
                if txt_path and not self._config.keep_pdf:
                    path.unlink(missing_ok=True)
                results.append((source, txt_path))
            else:
                results.append((source, path))

        return TypedStruct("recon.v1/web.texts", results)


# ── Inventory ────────────────────────────────────────────────────────

class InventoryNode:
    """Write inventory.md for academic sources.

    consumes: recon.v1/papers, recon.v1/texts
    produces: recon.v1/inventory
    """

    name = "inventory"
    consumes = frozenset({"recon.v1/papers", "recon.v1/texts"})
    produces = "recon.v1/inventory"

    def __init__(self, config: InventoryConfig) -> None:
        self._config = config

    async def run(self, construct: Construct) -> TypedStruct:
        papers: list[Paper] = construct["recon.v1/papers"]
        texts: list[tuple[Paper, Path | None]] = construct["recon.v1/texts"]

        downloaded = [(p, path) for p, path in texts if path is not None]
        paywalled = [p for p, path in texts if path is None]

        inventory_path = self._config.output_dir / "inventory.md"
        inventory_path.write_text(
            _render_academic_inventory(self._config.query, papers, downloaded, paywalled)
        )
        return TypedStruct("recon.v1/inventory", inventory_path)


class WebInventoryNode:
    """Write inventory.md for web sources.

    consumes: recon.v1/web.sources, recon.v1/web.texts
    produces: recon.v1/web.inventory
    """

    name = "web_inventory"
    consumes = frozenset({"recon.v1/web.sources", "recon.v1/web.texts"})
    produces = "recon.v1/web.inventory"

    def __init__(self, config: InventoryConfig) -> None:
        self._config = config

    async def run(self, construct: Construct) -> TypedStruct:
        sources: list[WebSource] = construct["recon.v1/web.sources"]
        texts: list[tuple[WebSource, Path | None]] = construct["recon.v1/web.texts"]

        fetched = [(s, path) for s, path in texts if path is not None]
        failed = [s for s, path in texts if path is None]

        inventory_path = self._config.output_dir / "inventory.md"
        inventory_path.write_text(
            _render_web_inventory(self._config.query, sources, fetched, failed)
        )
        return TypedStruct("recon.v1/web.inventory", inventory_path)


# ── Renderers ────────────────────────────────────────────────────────

def _render_academic_inventory(
    query: str, all_papers: list[Paper],
    downloaded: list[tuple[Paper, Path]], paywalled: list[Paper],
) -> str:
    lines = ["# Source Inventory\n"]
    if downloaded:
        lines.append("## Downloaded\n")
        for paper, txt_path in downloaded:
            authors_str = ", ".join(paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += " et al."
            doi_str = f" DOI: {paper.doi}." if paper.doi else ""
            lines.append(
                f"- **{authors_str} ({paper.year}).** {paper.title}. "
                f"{paper.venue or 'Preprint'}.{doi_str} [text: {txt_path.name}]\n"
            )
    if paywalled:
        lines.append("\n## Paywalled (abstract only)\n")
        for paper in paywalled:
            authors_str = ", ".join(paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += " et al."
            doi_str = f" DOI: {paper.doi}." if paper.doi else ""
            lines.append(
                f"- **{authors_str} ({paper.year}).** {paper.title}. "
                f"{paper.venue or 'Preprint'}.{doi_str} [no PDF available]\n"
            )
    lines.append(f"\n## Search Log\n")
    lines.append(f'- Query: "{query}"\n')
    lines.append(f"- Results: {len(all_papers)} papers found\n")
    lines.append(f"- Downloaded: {len(downloaded)} (open access)\n")
    lines.append(f"- Paywalled: {len(paywalled)}\n")
    lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    return "".join(lines)


def _render_web_inventory(
    query: str, all_sources: list[WebSource],
    fetched: list[tuple[WebSource, Path]], failed: list[WebSource],
) -> str:
    lines = ["# Web Source Inventory\n"]
    if fetched:
        lines.append("## Fetched\n")
        for source, txt_path in fetched:
            lines.append(f"- **{source.title}** — {source.url} [text: {txt_path.name}]\n")
    if failed:
        lines.append("\n## Unreachable\n")
        for source in failed:
            lines.append(f"- **{source.title}** — {source.url}\n")
    lines.append(f"\n## Search Log\n")
    lines.append(f'- Query: "{query}"\n')
    lines.append(f"- Results: {len(all_sources)} sources found\n")
    lines.append(f"- Fetched: {len(fetched)}\n")
    lines.append(f"- Failed: {len(failed)}\n")
    lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    return "".join(lines)
