"""Semantic Scholar adapter — implements SearchPort."""

from __future__ import annotations

from semanticscholar import SemanticScholar

from recon.domain.types import Paper

_FIELDS = [
    "title",
    "authors",
    "year",
    "externalIds",
    "abstract",
    "citationCount",
    "openAccessPdf",
    "venue",
]


class SemanticScholarAdapter:
    """SearchPort implementation backed by Semantic Scholar API."""

    def search(
        self,
        query: str,
        *,
        limit: int = 20,
        year_min: int | None = None,
        year_max: int | None = None,
        min_citations: int = 0,
    ) -> list[Paper]:
        sch = SemanticScholar()

        year_range = None
        if year_min or year_max:
            y_min = year_min or 1900
            y_max = year_max or 2030
            year_range = f"{y_min}-{y_max}"

        results = sch.search_paper(
            query,
            limit=limit,
            year=year_range,
            min_citation_count=min_citations,
            fields=_FIELDS,
        )

        return [_to_paper(r) for r in results]

    def get_by_id(self, paper_id: str) -> Paper | None:
        sch = SemanticScholar()

        try:
            r = sch.get_paper(paper_id, fields=_FIELDS)
        except Exception:
            return None

        return _to_paper(r)


def _to_paper(r) -> Paper:
    ext_ids = r.externalIds or {}
    oa_pdf = r.openAccessPdf or {}

    return Paper(
        title=r.title or "Untitled",
        authors=[a.name for a in (r.authors or [])],
        year=r.year,
        doi=ext_ids.get("DOI"),
        abstract=r.abstract,
        citation_count=r.citationCount or 0,
        open_access_url=oa_pdf.get("url"),
        arxiv_id=ext_ids.get("ArXiv"),
        s2_id=r.paperId,
        venue=r.venue,
    )
