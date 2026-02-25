"""Orchestrator — sequential DAG execution using Construct."""

from __future__ import annotations

from typing import Any

from .compiler import DagCompiler
from .scheduler import DagScheduler
from .types import Construct


class Orchestrator:
    """Compiles and executes a DAG of components sequentially."""

    def __init__(self, components: list[Any]) -> None:
        self._registry, self._edges = DagCompiler.compile(components)

    async def run(self) -> Construct:
        """Execute the DAG. Returns the Construct with all results."""
        construct = Construct()

        scheduler = DagScheduler(self._registry, self._edges)

        for batch in scheduler.batches():
            for component in batch:
                data = await component.run(construct)
                construct._results[component.provides] = data

        return construct
