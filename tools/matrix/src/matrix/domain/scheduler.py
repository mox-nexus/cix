"""DagScheduler — yields execution batches from compiled topology."""

from __future__ import annotations

import graphlib
from collections.abc import Iterator
from typing import Any


class DagScheduler:
    """Generates topological execution batches."""

    def __init__(
        self,
        registry: dict[str, Any],
        edges: dict[str, set[str]],
    ) -> None:
        self._registry = registry
        self._edges = edges

    def batches(self) -> Iterator[tuple[Any, ...]]:
        """Yield batches of components in topological order.

        Components within a batch are independent of each other.
        """
        sorter = graphlib.TopologicalSorter(self._edges)
        sorter.prepare()

        while sorter.is_active():
            ready_names = sorter.get_ready()
            yield tuple(self._registry[name] for name in ready_names)
            for name in ready_names:
                sorter.done(name)
