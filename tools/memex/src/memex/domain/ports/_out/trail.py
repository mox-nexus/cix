"""Trail port - interface for curated fragment collections.

Trails are named, ordered, annotated paths through fragments.
Bush's associative trails made concrete.
"""

from typing import Protocol

from memex.domain.models import Fragment, TrailSummary


class TrailPort(Protocol):
    """Protocol for trail operations."""

    def create_trail(self, name: str, description: str = "") -> str:
        """Create a named trail. Returns trail ID."""
        ...

    def add_to_trail(self, trail_name: str, fragment_id: str, note: str = "") -> int:
        """Add fragment to trail. Returns position."""
        ...

    def get_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        """Get trail entries in order. Returns (Fragment, note) tuples."""
        ...

    def list_trails(self) -> list[TrailSummary]:
        """List all trails."""
        ...

    def delete_trail(self, trail_name: str) -> bool:
        """Delete a trail."""
        ...
