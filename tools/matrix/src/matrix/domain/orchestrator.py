"""Orchestrator — sequential DAG execution using Construct."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from opentelemetry import trace

from .compiler import DagCompiler
from .scheduler import DagScheduler
from .types import Artifact, Construct, ContractError

_tracer = trace.get_tracer("matrix")
logger = logging.getLogger("matrix.orchestrator")

# Callback signature: (component_name, event) where event is "start" or "done".
NodeCallback = Callable[[str, str], None]


class Orchestrator:
    """Compiles and executes a DAG of components sequentially."""

    def __init__(
        self,
        components: list[Any],
        on_node: NodeCallback | None = None,
    ) -> None:
        self._registry, self._edges = DagCompiler.compile(components)
        self._on_node = on_node

    async def run(self) -> Construct:
        """Execute the DAG. Returns the Construct with all results."""
        with _tracer.start_as_current_span("matrix.dag.run") as dag_span:
            construct = Construct()
            scheduler = DagScheduler(self._registry, self._edges)

            for batch in scheduler.batches():
                for component in batch:
                    await self._run_component(component, construct)

            dag_span.set_attribute("matrix.dag.artifact_count", len(construct.ledger))
            return construct

    async def _run_component(self, component: Any, construct: Construct) -> None:
        """Execute one component: trace, validate contract, append artifact."""
        name = component.name

        if self._on_node:
            self._on_node(name, "start")

        logger.debug("Running %s", name)

        with _tracer.start_as_current_span(
            "matrix.component.run",
            attributes={
                "matrix.component.name": name,
                "matrix.component.produces": component.produces,
            },
        ) as span:
            result = await component.run(construct)

            if result.type_url != component.produces:
                error = ContractError(
                    f"{name!r} declared produces={component.produces!r} "
                    f"but returned type_url={result.type_url!r}"
                )
                span.record_exception(error)
                span.set_status(trace.StatusCode.ERROR, str(error))
                raise error

            artifact = Artifact.create(
                type_url=result.type_url,
                producer=name,
                data=result.value,
            )
            construct.append(artifact)

        if self._on_node:
            self._on_node(name, "done")
