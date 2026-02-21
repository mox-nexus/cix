"""Tests for DagCompiler — topology validation from requires/provides."""

import pytest
from matrix import CompilationError, DagCompiler
from matrix_helpers import FakeComponent

# --- Helpers ---


def _probe(name: str = "probe", output: str = "probe.response") -> FakeComponent:
    return FakeComponent(name=name, requires=frozenset(), provides=output)


def _sensor(
    name: str = "sensor",
    inputs: frozenset[str] | None = None,
    output: str = "sensor.grade",
) -> FakeComponent:
    return FakeComponent(
        name=name,
        requires=inputs or frozenset({"probe.response"}),
        provides=output,
    )


def _scorer(
    name: str = "scorer",
    inputs: frozenset[str] | None = None,
    output: str = "scorer.verdict",
) -> FakeComponent:
    return FakeComponent(
        name=name,
        requires=inputs or frozenset({"sensor.grade"}),
        provides=output,
    )


# --- Tests ---


class TestDagCompiler:
    def test_linear_chain(self):
        """probe -> sensor -> scorer compiles to correct edges."""
        probe = _probe()
        sensor = _sensor()
        scorer = _scorer()

        registry, edges = DagCompiler.compile([probe, sensor, scorer])

        assert registry == {"probe": probe, "sensor": sensor, "scorer": scorer}
        assert edges["probe"] == set()
        assert edges["sensor"] == {"probe"}
        assert edges["scorer"] == {"sensor"}

    def test_parallel_sensors(self):
        """probe -> [sensor_a, sensor_b] — both read probe.response."""
        probe = _probe()
        sensor_a = _sensor(name="sensor-a", output="sensor.accuracy")
        sensor_b = _sensor(name="sensor-b", output="sensor.latency")

        registry, edges = DagCompiler.compile([probe, sensor_a, sensor_b])

        assert edges["probe"] == set()
        assert edges["sensor-a"] == {"probe"}
        assert edges["sensor-b"] == {"probe"}

    def test_diamond(self):
        """probe -> [sensor_a, sensor_b] -> scorer (reads both sensor kinds)."""
        probe = _probe()
        sensor_a = _sensor(name="sensor-a", output="sensor.accuracy")
        sensor_b = _sensor(name="sensor-b", output="sensor.latency")
        scorer = _scorer(
            inputs=frozenset({"sensor.accuracy", "sensor.latency"}),
        )

        registry, edges = DagCompiler.compile([probe, sensor_a, sensor_b, scorer])

        assert edges["scorer"] == {"sensor-a", "sensor-b"}
        assert edges["sensor-a"] == {"probe"}
        assert edges["sensor-b"] == {"probe"}

    def test_missing_producer_raises(self):
        """Component needs a kind nobody produces -> CompilationError."""
        orphan = _sensor(inputs=frozenset({"nonexistent.kind"}))

        with pytest.raises(CompilationError, match="nonexistent.kind"):
            DagCompiler.compile([orphan])

    def test_cycle_raises(self):
        """A -> B -> A -> CycleError."""
        a = FakeComponent(
            name="a",
            requires=frozenset({"b.output"}),
            provides="a.output",
        )
        b = FakeComponent(
            name="b",
            requires=frozenset({"a.output"}),
            provides="b.output",
        )

        with pytest.raises(CompilationError, match="[Cc]ycle"):
            DagCompiler.compile([a, b])

    def test_root_nodes(self):
        """Component with empty requires has no dependencies."""
        root = _probe()
        _, edges = DagCompiler.compile([root])
        assert edges["probe"] == set()

    def test_duplicate_provides(self):
        """Two components provide same kind -> CompilationError."""
        a = _probe(name="probe-a", output="probe.response")
        b = _probe(name="probe-b", output="probe.response")

        with pytest.raises(CompilationError, match="Duplicate output kind"):
            DagCompiler.compile([a, b])

    def test_duplicate_name(self):
        """Two components with same name -> CompilationError."""
        a = _probe(name="probe")
        b = FakeComponent(
            name="probe",
            requires=frozenset(),
            provides="other.kind",
        )

        with pytest.raises(CompilationError, match="Duplicate component name"):
            DagCompiler.compile([a, b])

    def test_single_component(self):
        """Single root component compiles fine."""
        probe = _probe()
        registry, edges = DagCompiler.compile([probe])

        assert len(registry) == 1
        assert edges["probe"] == set()

    def test_empty_list(self):
        """Empty component list compiles to empty results."""
        registry, edges = DagCompiler.compile([])
        assert registry == {}
        assert edges == {}
