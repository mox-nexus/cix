"""DuckDuckGo adapter — implements WebSearchPort."""

from __future__ import annotations

from duckduckgo_search import DDGS

from recon.domain.types import WebSource


class DuckDuckGoAdapter:
    """WebSearchPort implementation via DuckDuckGo. No API key needed."""

    def search(self, query: str, *, limit: int = 10) -> list[WebSource]:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=limit)

        return [
            WebSource(title=r["title"], url=r["href"], snippet=r["body"])
            for r in results
        ]
