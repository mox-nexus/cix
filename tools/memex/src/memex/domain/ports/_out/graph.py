"""Graph port - interface for fragment relationships.

Edges connect fragments: FOLLOWS (temporal), SIMILAR_TO (semantic).
"""

from collections.abc import Callable
from typing import Protocol

from memex.domain.models import EdgeTypeStats, Fragment

ProgressCallback = Callable[[int, int], None] | None


class GraphPort(Protocol):
    """Protocol for graph operations on fragments."""

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
        """Build SIMILAR_TO edges from embedding similarity."""
        ...

    def edge_stats(self) -> dict[str, EdgeTypeStats]:
        """Get edge statistics by type."""
        ...

    def traverse(
        self,
        fragment_id: str,
        max_hops: int = 2,
        edge_type: str | None = None,
        limit: int = 20,
    ) -> list[tuple[Fragment, int, str]]:
        """Multi-hop graph traversal from a fragment.

        Returns (Fragment, hops, edge_type) tuples sorted by distance.
        """
        ...
