"""Recon pipeline configuration + composition root.

Components are provided. Adapters are wired here. Compositions are configs.
Any client provides a ReconConfig → gets a running Orchestrator.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from matrix import Orchestrator

from recon.adapters._out.duckduckgo import DuckDuckGoAdapter
from recon.adapters._out.pdf_download import PdfDownloadAdapter
from recon.adapters._out.pdftotext import PdftotextAdapter
from recon.adapters._out.semantic_scholar import SemanticScholarAdapter
from recon.adapters._out.web_extractor import WebExtractorAdapter
from recon.components import (
    ConvertNode,
    DownloadNode,
    InventoryConfig,
    InventoryNode,
    OutputConfig,
    SearchConfig,
    SearchNode,
    WebFetchNode,
    WebInventoryNode,
    WebSearchConfig,
    WebSearchNode,
)


class ReconConfig(BaseModel, frozen=True):
    """Top-level config for a recon pipeline.

    Clients (CTS, Radix, craft-research, CLI) provide this.
    Components are fixed — the config selects and parameterizes them.
    """

    query: str
    output_dir: Path = Path(".")
    keep_pdf: bool = False

    academic: SearchConfig | None = None
    web: WebSearchConfig | None = None

    @classmethod
    def academic_preset(
        cls,
        query: str,
        output_dir: Path = Path("."),
        *,
        limit: int = 20,
        year_min: int | None = None,
        year_max: int | None = None,
        min_citations: int = 0,
        keep_pdf: bool = False,
    ) -> ReconConfig:
        return cls(
            query=query, output_dir=output_dir, keep_pdf=keep_pdf,
            academic=SearchConfig(
                query=query, limit=limit, year_min=year_min,
                year_max=year_max, min_citations=min_citations,
            ),
        )

    @classmethod
    def web_preset(
        cls,
        query: str,
        output_dir: Path = Path("."),
        *,
        limit: int = 10,
        keep_pdf: bool = False,
    ) -> ReconConfig:
        return cls(
            query=query, output_dir=output_dir, keep_pdf=keep_pdf,
            web=WebSearchConfig(query=query, limit=limit, output_dir=output_dir, keep_pdf=keep_pdf),
        )

    @classmethod
    def full_preset(
        cls,
        query: str,
        output_dir: Path = Path("."),
        *,
        academic_limit: int = 20,
        web_limit: int = 10,
        year_min: int | None = None,
        year_max: int | None = None,
        min_citations: int = 0,
        keep_pdf: bool = False,
    ) -> ReconConfig:
        return cls(
            query=query, output_dir=output_dir, keep_pdf=keep_pdf,
            academic=SearchConfig(
                query=query, limit=academic_limit, year_min=year_min,
                year_max=year_max, min_citations=min_citations,
            ),
            web=WebSearchConfig(
                query=query, limit=web_limit, output_dir=output_dir, keep_pdf=keep_pdf,
            ),
        )


def build_pipeline(config: ReconConfig) -> Orchestrator:
    """Build a matrix Orchestrator from config. Wires adapters to components."""
    components = []

    # Default adapter instances
    s2 = SemanticScholarAdapter()
    downloader = PdfDownloadAdapter()
    converter = PdftotextAdapter()
    ddg = DuckDuckGoAdapter()
    extractor = WebExtractorAdapter()

    out = OutputConfig(output_dir=config.output_dir, keep_pdf=config.keep_pdf)

    if config.academic:
        components.extend([
            SearchNode(config.academic, s2),
            DownloadNode(out, downloader),
            ConvertNode(out, converter),
            InventoryNode(InventoryConfig(output_dir=config.output_dir, query=config.query)),
        ])

    if config.web:
        components.extend([
            WebSearchNode(config.web, ddg),
            WebFetchNode(config.web, extractor, converter),
            WebInventoryNode(InventoryConfig(output_dir=config.output_dir, query=config.query)),
        ])

    if not components:
        raise ValueError("ReconConfig must enable at least one pipeline (academic or web)")

    return Orchestrator(components)
