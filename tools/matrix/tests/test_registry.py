"""Tests for ComponentRegistry — type URL to factory mapping."""

import pytest
from matrix.domain.registry import ComponentRegistry
from matrix_helpers import FakeComponent


def make_probe(**config):
    """Factory that creates a FakeComponent probe."""
    return FakeComponent(
        name=config.get("name", "probe"),
        requires=frozenset(),
        provides="probe.response",
    )


def make_sensor(**config):
    """Factory that creates a FakeComponent sensor."""
    return FakeComponent(
        name=config.get("name", "sensor"),
        requires=frozenset({"probe.response"}),
        provides="sensor.grade",
    )


class TestRegistration:
    def test_register_and_create(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        component = registry.create("test.probe")
        assert component.name == "probe"
        assert component.provides == "probe.response"

    def test_chaining(self):
        registry = (
            ComponentRegistry()
            .register("test.probe", make_probe)
            .register("test.sensor", make_sensor)
        )
        assert len(registry) == 2

    def test_duplicate_raises(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        with pytest.raises(ValueError, match="Duplicate registration"):
            registry.register("test.probe", make_sensor)

    def test_class_as_factory(self):
        """Python classes are callables — can register directly."""
        registry = ComponentRegistry().register(
            "test.fake",
            lambda **kw: FakeComponent(
                name=kw.get("name", "direct"),
                requires=frozenset(),
                provides="fake.output",
            ),
        )
        component = registry.create("test.fake", {"name": "custom"})
        assert component.name == "custom"


class TestCreation:
    def test_unknown_type_raises(self):
        registry = ComponentRegistry()
        with pytest.raises(KeyError, match="Unknown component type"):
            registry.create("nonexistent.type")

    def test_config_passed_to_factory(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        component = registry.create("test.probe", {"name": "custom-probe"})
        assert component.name == "custom-probe"

    def test_none_config_uses_defaults(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        component = registry.create("test.probe")
        assert component.name == "probe"

    def test_empty_config_uses_defaults(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        component = registry.create("test.probe", {})
        assert component.name == "probe"


class TestIntrospection:
    def test_contains(self):
        registry = ComponentRegistry().register("test.probe", make_probe)
        assert "test.probe" in registry
        assert "test.missing" not in registry

    def test_len(self):
        registry = (
            ComponentRegistry()
            .register("test.probe", make_probe)
            .register("test.sensor", make_sensor)
        )
        assert len(registry) == 2

    def test_types(self):
        registry = (
            ComponentRegistry()
            .register("test.probe", make_probe)
            .register("test.sensor", make_sensor)
        )
        assert registry.types() == frozenset({"test.probe", "test.sensor"})

    def test_empty_registry(self):
        registry = ComponentRegistry()
        assert len(registry) == 0
        assert registry.types() == frozenset()
