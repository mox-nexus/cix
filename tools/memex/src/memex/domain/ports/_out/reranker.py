"""Reranker port - interface for cross-encoder reranking.

Reranking improves precision by scoring query-document pairs with a
cross-encoder model after initial retrieval.
"""

from typing import Protocol

from memex.domain.models import Fragment


class RerankerPort(Protocol):
    """Port for reranking search results.

    Cross-encoders score (query, document) pairs directly, providing
    better relevance estimates than bi-encoder similarity. Use after
    initial retrieval to rerank top candidates.

    Typical flow: Retrieve 50-100 → Rerank to top 10-20
    """

    def rerank(
        self,
        query: str,
        candidates: list[Fragment],
        top_k: int = 10,
    ) -> list[tuple[Fragment, float]]:
        """Rerank candidates by relevance to query.

        Args:
            query: The search query
            candidates: Fragments to rerank (from initial retrieval)
            top_k: Number of top results to return

        Returns:
            List of (Fragment, score) tuples, sorted by relevance descending.
            Score semantics depend on implementation (typically 0-1 or logits).
        """
        ...

    @property
    def model_name(self) -> str:
        """Return the model name for display/logging."""
        ...
