"""Recon domain types — pure, no external dependencies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Paper:
    """Paper metadata. Source-agnostic — works for S2, OpenAlex, or self-hosted."""

    title: str
    authors: list[str]
    year: int | None
    doi: str | None
    abstract: str | None
    citation_count: int
    open_access_url: str | None
    arxiv_id: str | None
    s2_id: str
    venue: str | None

    @property
    def slug(self) -> str:
        """Generate filename slug: author-year-short-title."""
        first_author = self.authors[0].split()[-1].lower() if self.authors else "unknown"
        year = self.year or "undated"
        words = (self.title or "untitled").lower().split()[:4]
        title_slug = "-".join(w for w in words if w.isalnum())
        return f"{first_author}-{year}-{title_slug}"

    @property
    def citation(self) -> str:
        """One-line citation string."""
        authors_str = self.authors[0] if len(self.authors) == 1 else f"{self.authors[0]} et al."
        return f"{authors_str} ({self.year}). {self.title}. {self.venue or 'Preprint'}."


@dataclass
class WebSource:
    """A source discovered via web search."""

    title: str
    url: str
    snippet: str
