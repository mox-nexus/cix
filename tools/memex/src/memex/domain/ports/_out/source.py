"""Source port - interface for ingesting different formats.

Adapters produce Iterator[Fragment], the canonical domain entity (Karman).
No infrastructure types (DataFrame) in port contracts (Burner).
"""

from collections.abc import Iterator
from pathlib import Path
from typing import Protocol

from memex.domain.models import Fragment


class SourcePort(Protocol):
    """Protocol for source adapters.

    Produces Fragments from source-specific formats.
    """

    def can_handle(self, path: Path) -> bool:
        """Check if this adapter can handle the given path."""
        ...

    def ingest(self, path: Path) -> Iterator[Fragment]:
        """Ingest source file and yield Fragments."""
        ...

    def source_kind(self) -> str:
        """Return the source kind this adapter handles."""
        ...
