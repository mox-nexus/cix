"""Tests for DagScheduler — topological batch generation."""

from matrix import DagCompiler, DagScheduler
from matrix_helpers import FakeComponent


def _compile(*components):
    """Compile components and return a DagScheduler."""
    registry, edges = DagCompiler.compile(list(components))
    return DagScheduler(registry, edges)


class TestDagScheduler:
    def test_linear_batches(self):
        """probe → sensor → scorer → 3 batches of 1."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade")
        scorer = FakeComponent("scorer", frozenset({"sensor.grade"}), "scorer.verdict")

        scheduler = _compile(probe, sensor, scorer)
        result = [tuple(c.name for c in batch) for batch in scheduler.batches()]

        assert len(result) == 3
        assert result[0] == ("probe",)
        assert result[1] == ("sensor",)
        assert result[2] == ("scorer",)

    def test_parallel_batch(self):
        """probe → [sensor_a, sensor_b] — sensors in same batch."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor_a = FakeComponent("sensor-a", frozenset({"probe.response"}), "sensor.accuracy")
        sensor_b = FakeComponent("sensor-b", frozenset({"probe.response"}), "sensor.latency")

        scheduler = _compile(probe, sensor_a, sensor_b)
        result = [tuple(sorted(c.name for c in batch)) for batch in scheduler.batches()]

        assert len(result) == 2
        assert result[0] == ("probe",)
        assert result[1] == ("sensor-a", "sensor-b")

    def test_diamond_batches(self):
        """probe → [sensor_a, sensor_b] → scorer — 3 levels."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor_a = FakeComponent("sensor-a", frozenset({"probe.response"}), "sensor.accuracy")
        sensor_b = FakeComponent("sensor-b", frozenset({"probe.response"}), "sensor.latency")
        scorer = FakeComponent(
            "scorer",
            frozenset({"sensor.accuracy", "sensor.latency"}),
            "scorer.verdict",
        )

        scheduler = _compile(probe, sensor_a, sensor_b, scorer)
        result = [tuple(sorted(c.name for c in batch)) for batch in scheduler.batches()]

        assert len(result) == 3
        assert result[0] == ("probe",)
        assert result[1] == ("sensor-a", "sensor-b")
        assert result[2] == ("scorer",)

    def test_single_component(self):
        """Single root component → 1 batch of 1."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        scheduler = _compile(probe)
        result = list(scheduler.batches())

        assert len(result) == 1
        assert len(result[0]) == 1
        assert result[0][0].name == "probe"

    def test_empty(self):
        """No components → no batches."""
        registry, edges = DagCompiler.compile([])
        scheduler = DagScheduler(registry, edges)
        result = list(scheduler.batches())
        assert result == []

    def test_yields_actual_components(self):
        """Batches contain actual component objects, not names."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        scheduler = _compile(probe)
        batch = next(scheduler.batches())
        assert batch[0] is probe
