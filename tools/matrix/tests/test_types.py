"""Tests for Matrix types: Construct, Component."""

import pytest
from matrix import Component, Construct


class TestConstruct:
    def test_empty_creation(self):
        c = Construct()
        assert len(c) == 0
        assert c.kinds() == frozenset()

    def test_store_and_retrieve(self):
        c = Construct()
        c._results["probe.response"] = "hello"
        assert c["probe.response"] == "hello"

    def test_getitem_raises_on_missing(self):
        c = Construct()
        with pytest.raises(LookupError, match="No result for kind 'missing'"):
            c["missing"]

    def test_error_message_shows_available(self):
        c = Construct()
        c._results["probe.response"] = "hello"
        with pytest.raises(LookupError, match="probe.response"):
            c["missing"]

    def test_error_message_empty(self):
        c = Construct()
        with pytest.raises(LookupError, match=r"\(none\)"):
            c["missing"]

    def test_contains(self):
        c = Construct()
        assert "probe.response" not in c
        c._results["probe.response"] = "hello"
        assert "probe.response" in c

    def test_kinds(self):
        c = Construct()
        c._results["probe.response"] = 1
        c._results["sensor.grade"] = 2
        assert c.kinds() == frozenset({"probe.response", "sensor.grade"})

    def test_len(self):
        c = Construct()
        assert len(c) == 0
        c._results["probe.response"] = 1
        assert len(c) == 1
        c._results["sensor.grade"] = 2
        assert len(c) == 2

    def test_data_any_type(self):
        """Construct stores any type — no type constraints on values."""
        c = Construct()
        for i, data in enumerate(("str", 42, 3.14, True, None, (1, 2), {"nested": True}, [1, 2])):
            c._results[f"kind.{i}"] = data
            assert c[f"kind.{i}"] == data


class TestComponent:
    def test_satisfies_protocol(self):
        class MyProbe:
            name = "my-probe"
            requires: frozenset[str] = frozenset()
            provides = "probe.response"

            async def run(self, construct: Construct) -> str:
                return "Hello, world"

        assert isinstance(MyProbe(), Component)

    def test_with_dependencies(self):
        class MySensor:
            name = "my-sensor"
            requires = frozenset({"probe.response"})
            provides = "sensor.grade"

            async def run(self, construct: Construct) -> bool:
                response = construct["probe.response"]
                return len(response) > 0

        sensor = MySensor()
        assert isinstance(sensor, Component)
        assert sensor.requires == frozenset({"probe.response"})

    def test_incomplete_rejects(self):
        class Incomplete:
            name = "test"
            # missing requires, provides, run

        assert not isinstance(Incomplete(), Component)

    def test_dag_chain(self):
        """Three-node DAG: probe -> sensor -> scorer."""

        class Probe:
            name = "probe"
            requires: frozenset[str] = frozenset()
            provides = "probe.response"

            async def run(self, construct: Construct) -> str:
                return "Response"

        class Sensor:
            name = "sensor"
            requires = frozenset({"probe.response"})
            provides = "sensor.grade"

            async def run(self, construct: Construct) -> dict:
                response = construct["probe.response"]
                return {"passed": len(response) > 10, "score": 0.95}

        class Scorer:
            name = "scorer"
            requires = frozenset({"sensor.grade"})
            provides = "scorer.verdict"

            async def run(self, construct: Construct) -> str:
                grade = construct["sensor.grade"]
                return "pass" if grade["passed"] else "fail"

        for cls in (Probe, Sensor, Scorer):
            assert isinstance(cls(), Component)


class TestLifecycle:
    """End-to-end: empty Construct -> enriched Construct."""

    def test_manual_enrichment(self):
        """Simulate what the engine will do (without the engine)."""
        construct = Construct()

        # Engine runs component, stores result
        construct._results["probe.response"] = "Hello, world"

        assert construct["probe.response"] == "Hello, world"
        assert len(construct) == 1

    def test_multi_component_enrichment(self):
        """Simulate probe -> sensor -> scorer chain."""
        c = Construct()

        c._results["probe.response"] = "I can help with evals"
        c._results["sensor.grade"] = {"passed": True, "score": 1.0}
        c._results["scorer.verdict"] = "pass"

        assert len(c) == 3
        assert c["scorer.verdict"] == "pass"
        assert c.kinds() == frozenset({"probe.response", "sensor.grade", "scorer.verdict"})

    def test_parallel_batch_simulation(self):
        """Simulate parallel components in same batch."""
        c = Construct()

        # Batch 1: probe runs alone
        c._results["probe.response"] = "response"

        # Batch 2: sensor-a and sensor-b run in parallel
        c._results["sensor.accuracy"] = 0.95
        c._results["sensor.latency"] = 42

        assert len(c) == 3
        assert c["sensor.accuracy"] == 0.95
        assert c["sensor.latency"] == 42
