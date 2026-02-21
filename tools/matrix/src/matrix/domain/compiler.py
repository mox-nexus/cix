"""DagCompiler — static topology validation from Component declarations.

Infers edges from requires/provides, detects cycles and missing producers.
"""

from __future__ import annotations

import graphlib
from typing import Any, Protocol, runtime_checkable


class CompilationError(Exception):
    """Raised when topology validation fails."""


@runtime_checkable
class _Compilable(Protocol):
    """Minimal interface for compilation."""

    name: str
    requires: frozenset[str]
    provides: str


class DagCompiler:
    """Validates component topology and builds adjacency edges."""

    @staticmethod
    def compile(
        components: list[Any],
    ) -> tuple[dict[str, Any], dict[str, set[str]]]:
        """Validate topology and return (registry, edges).

        Raises CompilationError on missing producer, duplicate output, or cycle.
        """
        registry: dict[str, Any] = {}
        kind_producers: dict[str, str] = {}

        for component in components:
            name = component.name
            if name in registry:
                raise CompilationError(f"Duplicate component name: {name!r}")
            registry[name] = component

            kind = component.provides
            if kind in kind_producers:
                raise CompilationError(
                    f"Duplicate output kind {kind!r}: "
                    f"produced by both {kind_producers[kind]!r} and {name!r}"
                )
            kind_producers[kind] = name

        edges: dict[str, set[str]] = {}
        for component in components:
            deps: set[str] = set()
            for required_kind in component.requires:
                if required_kind not in kind_producers:
                    raise CompilationError(
                        f"Component {component.name!r} requires kind "
                        f"{required_kind!r}, but no component provides it"
                    )
                deps.add(kind_producers[required_kind])
            edges[component.name] = deps

        sorter = graphlib.TopologicalSorter(edges)
        try:
            sorter.prepare()
        except graphlib.CycleError as e:
            raise CompilationError(f"Cycle detected: {e}") from e

        return registry, edges
