"""Corpus port - interface for persistence.

No SQL in port contract (Karman) - that's implementation detail.
Uses domain types only (Burner).
"""

from typing import Iterable, Protocol

from memex.domain.models import Fragment


class CorpusPort(Protocol):
    """Protocol for corpus storage.

    Stores Fragments, returns Fragments.
    Implementation details (SQL, DataFrame) stay in adapters.
    """

    def store(self, fragments: Iterable[Fragment]) -> int:
        """Store fragments. Returns count of new fragments."""
        ...

    def search(self, query: str, limit: int = 20) -> list[Fragment]:
        """Search fragments by content."""
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

    def close(self) -> None:
        """Close connection."""
        ...
