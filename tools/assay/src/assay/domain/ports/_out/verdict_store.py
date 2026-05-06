"""VerdictStore — outbound port for persisting MechanismResults + Adjudications."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from assay.domain.models import Adjudication, MechanismResult


class VerdictStore(Protocol):
    """Persists MechanismResults and Adjudications for later query."""

    def write_mechanism_result(self, result: MechanismResult) -> None:
        """Append one MechanismResult to the run's store."""
        ...

    def write_adjudication(self, adjudication: Adjudication) -> None:
        """Append one Adjudication to the run's store."""
        ...

    def query(self, sql: str) -> Iterable[dict]:
        """Run a query against the store; returns row dicts. Implementation
        determines the SQL dialect (DuckDB by default).
        """
        ...
