"""Recon ports — interfaces for driven adapters.

Implementation-agnostic. Domain speaks these protocols.
Adapters in `adapters/_out/` implement them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from recon.domain.types import Paper, WebSource


class SearchPort(Protocol):
    """Search for academic papers."""

    def search(
        self,
        query: str,
        *,
        limit: int = 20,
        year_min: int | None = None,
        year_max: int | None = None,
        min_citations: int = 0,
    ) -> list[Paper]: ...

    def get_by_id(self, paper_id: str) -> Paper | None: ...


class DownloadPort(Protocol):
    """Download paper PDFs from open access sources."""

    def download(self, paper: Paper, output_dir: Path) -> Path | None: ...


class ConvertPort(Protocol):
    """Convert PDF to text."""

    def to_text(self, pdf_path: Path, output_dir: Path | None = None) -> Path | None: ...


class WebSearchPort(Protocol):
    """Search the web."""

    def search(self, query: str, *, limit: int = 10) -> list[WebSource]: ...


class WebFetchPort(Protocol):
    """Fetch and extract text from web URLs."""

    def fetch(self, url: str, output_dir: Path) -> Path | None: ...
