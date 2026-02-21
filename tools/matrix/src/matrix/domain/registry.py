"""ComponentRegistry — type URL to factory mapping.

Inspired by x.uma's xds typed config registry: type URL string maps to
a factory callable that takes a config dict and returns a Component instance.

Simple things first: the factory is any callable(**config) -> Component.
Typed config validation (Pydantic per-component) is a future evolution.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ComponentFactory(Protocol):
    """Anything callable that produces a Component from keyword args."""

    def __call__(self, **config: Any) -> Any: ...


class ComponentRegistry:
    """Type URL → Component factory mapping.

    Usage::

        registry = (
            ComponentRegistry()
            .register("ix.probe.prompt", PromptProbe)
            .register("ix.sensor.activation", ActivationSensor)
        )

        probe = registry.create("ix.probe.prompt", {"template": "..."})
    """

    def __init__(self) -> None:
        self._factories: dict[str, ComponentFactory] = {}

    def register(self, type_url: str, factory: ComponentFactory) -> ComponentRegistry:
        """Register a factory for a type URL. Returns self for chaining.

        Raises ValueError on duplicate registration.
        """
        if type_url in self._factories:
            raise ValueError(f"Duplicate registration: {type_url!r} is already registered")
        self._factories[type_url] = factory
        return self

    def create(self, type_url: str, config: dict[str, Any] | None = None) -> Any:
        """Create a component instance from type URL + config dict.

        Raises KeyError if type URL is not registered.
        """
        factory = self._factories.get(type_url)
        if factory is None:
            raise KeyError(f"Unknown component type: {type_url!r}")
        return factory(**(config or {}))

    def __contains__(self, type_url: str) -> bool:
        return type_url in self._factories

    def __len__(self) -> int:
        return len(self._factories)

    def types(self) -> frozenset[str]:
        """Return all registered type URLs."""
        return frozenset(self._factories)
