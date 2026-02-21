"""Tests for Orchestrator — sequential DAG execution."""

import pytest
from matrix import Construct, Orchestrator
from matrix_helpers import FakeComponent


class ReadingComponent:
    """Component that reads upstream results."""

    def __init__(self, name: str, requires: frozenset[str], provides: str, read_kind: str):
        self.name = name
        self.requires = requires
        self.provides = provides
        self._read_kind = read_kind

    async def run(self, construct: Construct):
        upstream = construct[self._read_kind]
        return f"read:{upstream}"


class FailingComponent:
    """Component that raises an exception."""

    def __init__(self, name: str, requires: frozenset[str], provides: str):
        self.name = name
        self.requires = requires
        self.provides = provides

    async def run(self, construct: Construct):
        raise ValueError(f"{self.name} failed")


class TestOrchestrator:
    async def test_linear_execution(self):
        """probe -> sensor -> scorer produces 3 results in order."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade")
        scorer = FakeComponent("scorer", frozenset({"sensor.grade"}), "scorer.verdict")

        orch = Orchestrator([probe, sensor, scorer])
        construct = await orch.run()

        assert len(construct) == 3
        assert construct.kinds() == frozenset({"probe.response", "sensor.grade", "scorer.verdict"})

    async def test_construct_grows(self):
        """Construct starts empty and accumulates results."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade")

        orch = Orchestrator([probe, sensor])
        construct = await orch.run()

        assert len(construct) == 2
        assert construct.kinds() == frozenset({"probe.response", "sensor.grade"})

    async def test_component_reads_upstream(self):
        """Sensor reads probe's result via construct["kind"]."""
        probe = FakeComponent("probe", frozenset(), "probe.response", data="hello")
        sensor = ReadingComponent(
            "sensor",
            frozenset({"probe.response"}),
            "sensor.grade",
            read_kind="probe.response",
        )

        orch = Orchestrator([probe, sensor])
        construct = await orch.run()

        assert construct["sensor.grade"] == "read:hello"

    async def test_error_propagation(self):
        """Component exception propagates to caller."""
        probe = FakeComponent("probe", frozenset(), "probe.response")
        fail = FailingComponent("fail", frozenset({"probe.response"}), "fail.output")

        orch = Orchestrator([probe, fail])
        with pytest.raises(ValueError, match="fail failed"):
            await orch.run()

    async def test_empty_dag(self):
        """No components -> empty construct."""
        orch = Orchestrator([])
        construct = await orch.run()

        assert len(construct) == 0

    async def test_result_data(self):
        """Each result has correct data for the kind."""
        probe = FakeComponent("probe", frozenset(), "probe.response", data=42)

        orch = Orchestrator([probe])
        construct = await orch.run()

        assert construct["probe.response"] == 42
