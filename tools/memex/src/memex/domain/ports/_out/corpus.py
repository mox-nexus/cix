"""Corpus port - interface for persistence.

No SQL in port contract (Karman) - that's implementation detail.
Uses domain types only (Burner).
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Protocol

from memex.domain.models import Fragment

# Type alias for progress callbacks (processed, total)
ProgressCallback = Callable[[int, int], None] | None


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

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[dict]:
        """List conversations with summary info.

        Returns:
            List of dicts with: conversation_id, message_count, first_timestamp,
            last_timestamp, source_kind, preview (first user message).
        """
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
        embedder_stream: Callable[[list[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings for existing fragments using streaming embedding.

        embedder_stream yields one embedding at a time from a generator,
        allowing write-as-you-go without materializing all vectors.
        """
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

    # --- Edge methods ---

    def find_similar(self, fragment_id: str, limit: int = 10) -> list[tuple[Fragment, float]]:
        """Find similar fragments via SIMILAR_TO edges."""
        ...

    def build_follows_edges(self) -> int:
        """Materialize FOLLOWS edges from conversation ordering."""
        ...

    def build_similar_edges(
        self,
        threshold: float = 0.8,
        k: int = 5,
        on_progress: ProgressCallback = None,
    ) -> int:
        """Build SIMILAR_TO edges from embedding similarity.

        Args:
            threshold: Minimum cosine similarity (0-1)
            k: Max similar neighbors per fragment
            on_progress: Callback(processed, total) for progress updates

        Returns:
            Count of edges created.
        """
        ...

    def edge_stats(self) -> dict:
        """Get edge statistics by type."""
        ...

    # --- Trail methods ---

    def create_trail(self, name: str, description: str = "") -> str:
        """Create a named trail. Returns trail ID."""
        ...

    def add_to_trail(self, trail_name: str, fragment_id: str, note: str = "") -> int:
        """Add fragment to trail. Returns position."""
        ...

    def get_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        """Get trail entries in order. Returns (Fragment, note) tuples."""
        ...

    def list_trails(self) -> list[dict]:
        """List all trails."""
        ...

    def delete_trail(self, trail_name: str) -> bool:
        """Delete a trail."""
        ...

    def close(self) -> None:
        """Close connection."""
        ...
