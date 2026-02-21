"""Container — composition root that wires config, registry, and runtime.

The only place that combines domain concepts with concrete adapters.
DI happens at registration time (factory closures capture dependencies).
The Container orchestrates: read specs → resolve through registry → build Orchestrator.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from matrix.domain.config import Config
from matrix.domain.orchestrator import Orchestrator
from matrix.domain.registry import ComponentRegistry


class Container:
    """Composition root — wires config + registry → Orchestrator.

    Usage::

        # Registration captures dependencies (DI at registration time)
        registry = (
            ComponentRegistry()
            .register("app.probe", lambda **kw: MyProbe(**kw))
            .register("app.sensor", lambda **kw: MySensor(**kw))
        )

        # Container wires everything
        container = Container(config=config, registry=registry)
        orchestrator = container.build_orchestrator([
            ("app.probe", {"template": "..."}),
            ("app.sensor", None),
        ])

        construct = await orchestrator.run()
    """

    def __init__(
        self,
        config: Config[Any],
        registry: ComponentRegistry,
        runtime: Any | None = None,
    ) -> None:
        self._config = config
        self._registry = registry
        self._runtime = runtime

    @property
    def config(self) -> Config[Any]:
        return self._config

    @property
    def registry(self) -> ComponentRegistry:
        return self._registry

    @property
    def runtime(self) -> Any | None:
        return self._runtime

    def create_component(self, type_url: str, config: dict[str, Any] | None = None) -> Any:
        """Create a single component from the registry."""
        return self._registry.create(type_url, config)

    def build_orchestrator(
        self,
        component_specs: Sequence[tuple[str, dict[str, Any] | None]],
    ) -> Orchestrator:
        """Resolve component specs through the registry, return a wired Orchestrator.

        Args:
            component_specs: Sequence of (type_url, config_dict) pairs.
                Each type_url is resolved through the registry.
                Config dict is passed as **kwargs to the factory.
        """
        components = [
            self._registry.create(type_url, config) for type_url, config in component_specs
        ]
        return Orchestrator(components)
