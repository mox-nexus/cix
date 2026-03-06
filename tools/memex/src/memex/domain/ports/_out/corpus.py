"""Corpus port - interface for persistence and search.

No SQL in port contract (Karman) - that's implementation detail.
Uses domain types only (Burner).

Edge operations → GraphPort (graph.py)
Trail operations → TrailPort (trail.py)
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Protocol

from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    EmbeddingConfig,
    Fragment,
    FragmentSchema,
)


class CorpusPort(Protocol):
    """Protocol for corpus storage and search.

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
        """Search fragments by content (all words must match)."""
        ...

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        """Search fragments by semantic similarity."""
        ...

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation."""
        ...

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[ConversationSummary]:
        """List conversations with summary info, most recent first."""
        ...

    def stats(self) -> CorpusStats:
        """Get corpus statistics."""
        ...

    def schema(self) -> FragmentSchema:
        """Return schema information for introspection."""
        ...

    def backfill_embeddings(
        self,
        embedder_stream: Callable[[Iterator[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings for existing fragments using streaming embedding."""
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

    def rebuild_search_index(self) -> None:
        """Rebuild search index after data changes."""
        ...

    def embedding_dimensions(self) -> int | None:
        """Return stored embedding dimensions, or None if unknown."""
        ...

    def record_embedding_config(self, config: EmbeddingConfig) -> None:
        """Record the embedding model used for this corpus."""
        ...

    def close(self) -> None:
        """Close connection."""
        ...
