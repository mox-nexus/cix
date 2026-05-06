"""Collector — the single port in Recon's hexagon.

Transport-agnostic: could be HTTP, subprocess, or anything else.
Takes a collector entry + optional source, yields records.

The dispatch loop consumes the iterator and writes to JSONL line-by-line;
collectors that return a list should wrap it in `iter()`. Streaming
collectors yield as they produce, enabling bounded memory for large outputs.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Protocol

from recon.domain.models import CollectorEntry, SourceEntry


class Collector(Protocol):
    """Collect data, yield records.

    `raw_store` is an optional side-channel for preserving raw fetched bytes
    (HTTP body, CLI stdout) alongside the processed records. When provided,
    collectors capture the raw snapshot before/during processing. Callers that
    don't need raw preservation pass None (or rely on the default).
    """

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
        *,
        raw_store: Any | None = None,
    ) -> Iterator[dict[str, Any]]: ...
