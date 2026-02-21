"""Tests for Container — composition root wiring."""

import pytest
from matrix.composition.container import Container
from matrix.domain.config import Config
from matrix.domain.registry import ComponentRegistry
from matrix_helpers import FakeComponent
from pydantic import BaseModel, ConfigDict


class StubClientConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    trials: int = 5


def make_probe(**config):
    return FakeComponent(
        name=config.get("name", "probe"),
        requires=frozenset(),
        provides="probe.response",
    )


def make_sensor(**config):
    return FakeComponent(
        name=config.get("name", "sensor"),
        requires=frozenset({"probe.response"}),
        provides="sensor.grade",
    )


@pytest.fixture
def registry():
    return (
        ComponentRegistry().register("test.probe", make_probe).register("test.sensor", make_sensor)
    )


@pytest.fixture
def config():
    return Config(client=StubClientConfig())


@pytest.fixture
def container(config, registry):
    return Container(config=config, registry=registry)


class TestContainer:
    def test_exposes_config(self, container, config):
        assert container.config is config

    def test_exposes_registry(self, container, registry):
        assert container.registry is registry

    def test_exposes_runtime(self, config, registry):
        runtime = object()
        container = Container(config=config, registry=registry, runtime=runtime)
        assert container.runtime is runtime

    def test_runtime_defaults_none(self, container):
        assert container.runtime is None

    def test_create_component(self, container):
        component = container.create_component("test.probe")
        assert component.name == "probe"
        assert component.provides == "probe.response"

    def test_create_component_with_config(self, container):
        component = container.create_component("test.probe", {"name": "custom-probe"})
        assert component.name == "custom-probe"


class TestBuildOrchestrator:
    def test_builds_from_specs(self, container):
        orchestrator = container.build_orchestrator(
            [
                ("test.probe", None),
                ("test.sensor", None),
            ]
        )
        assert orchestrator is not None

    @pytest.mark.anyio
    async def test_orchestrator_runs(self, container):
        orchestrator = container.build_orchestrator(
            [
                ("test.probe", None),
                ("test.sensor", None),
            ]
        )
        construct = await orchestrator.run()
        assert len(construct) == 2
        assert "probe.response" in construct
        assert "sensor.grade" in construct

    @pytest.mark.anyio
    async def test_config_passed_through(self, container):
        orchestrator = container.build_orchestrator(
            [
                ("test.probe", {"name": "my-probe"}),
                ("test.sensor", {"name": "my-sensor"}),
            ]
        )
        construct = await orchestrator.run()
        # Components ran and stored results
        assert "probe.response" in construct
        assert "sensor.grade" in construct

    def test_unknown_type_raises(self, container):
        with pytest.raises(KeyError, match="Unknown component type"):
            container.build_orchestrator([("nonexistent.type", None)])

    def test_empty_specs(self, container):
        orchestrator = container.build_orchestrator([])
        assert orchestrator is not None


class TestDIPattern:
    """Verify the factory-captures-dependency pattern works."""

    def test_factory_captures_runtime(self, config):
        """Factories close over shared dependencies at registration time."""
        captured_runtime = object()

        def make_runtime_probe(**kw):
            return FakeComponent(
                name=kw.get("name", "runtime-probe"),
                requires=frozenset(),
                provides="probe.response",
                data=f"used-runtime-{id(captured_runtime)}",
            )

        registry = ComponentRegistry().register("test.runtime-probe", make_runtime_probe)
        container = Container(config=config, registry=registry, runtime=captured_runtime)
        component = container.create_component("test.runtime-probe")
        assert component._data == f"used-runtime-{id(captured_runtime)}"
