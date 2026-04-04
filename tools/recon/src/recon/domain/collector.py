"""Collector — the single port in Recon's hexagon.

Transport-agnostic: could be subprocess, HTTP, or anything else.
Takes a collector entry + optional source, returns records.
The dispatch loop handles file I/O — collectors are pure data processors.
"""

from __future__ import annotations

from typing import Any, Protocol

from recon.domain.models import CollectorEntry, SourceEntry


class Collector(Protocol):
    """Collect data and return records."""

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
    ) -> list[dict[str, Any]]: ...
