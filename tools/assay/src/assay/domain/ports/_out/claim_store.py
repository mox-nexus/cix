"""ClaimStore — outbound port for claim source loading."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from assay.domain.models import Claim


class ClaimStore(Protocol):
    """Loads claims from a configured source (JSONL file, directory, etc.)."""

    def iter_claims(self) -> Iterator[Claim]:
        """Yield each Claim. Order is implementation-defined."""
        ...

    def get(self, claim_id: str) -> Claim | None:
        """Return one claim by id, or None if not found. Used for --claim debug."""
        ...
