"""Corpus port - interface for persistence.

No SQL in port contract (Karman) - that's implementation detail.
Uses domain types only (Burner).
"""

from collections.abc import Callable, Iterable
from typing import Protocol

from memex.domain.models import Fragment


class CorpusPort(Protocol):
    """Protocol for corpus storage.

    Stores Fragments, returns Fragments.
    Implementation details (SQL, DataFrame) stay in adapters.
    """

    def store(self, fragments: Iterable[Fragment]) -> int:
        """Store fragments. Returns count of new fragments."""
        ...

    def store_with_embeddings(
        self,
        fragments: Iterable[Fragment],
        embedder: Callable[[str], list[float]],
    ) -> int:
        """Store fragments with embeddings. Returns count of new fragments."""
        ...

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        """Search fragments by content (all words must match).

        Args:
            query: Search terms (space-separated, all must match)
            limit: Maximum results
            source_kind: Optional filter by source type
        """
        ...

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        """Search fragments by semantic similarity.

        Args:
            query_embedding: Query vector
            limit: Maximum results
            source_kind: Optional filter by source type
            min_score: Minimum cosine similarity threshold

        Returns:
            List of (Fragment, score) tuples.
        """
        ...

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation."""
        ...

    def stats(self) -> dict:
        """Get corpus statistics."""
        ...

    def schema(self) -> dict:
        """Return schema information for introspection."""
        ...

    def skill(self) -> str:
        """Return skill documentation for this corpus backend."""
        ...

    def backfill_embeddings(
        self,
        embedder_batch: Callable[[list[str]], list[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings for existing fragments using batch embedding."""
        ...

    def count_without_embeddings(self) -> int:
        """Count fragments without embeddings."""
        ...

    def has_semantic_search(self) -> bool:
        """Check if semantic search is available."""
        ...

    def has_keyword_search(self) -> bool:
        """Check if full-text search (BM25) is available."""
        ...

    def rebuild_fts_index(self) -> None:
        """Rebuild FTS index after data changes.

        No-op for backends that auto-update their indexes.
        """
        ...

    def embedding_dimensions(self) -> int | None:
        """Return stored embedding dimensions, or None if unknown.

        Used for validating embedder compatibility.
        """
        ...

    def close(self) -> None:
        """Close connection."""
        ...
