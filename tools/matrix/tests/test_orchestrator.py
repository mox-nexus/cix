"""Tests for Orchestrator — sequential DAG execution."""

import pytest
from matrix import Artifact, Construct, ContractError, Orchestrator, TypedStruct
from matrix_helpers import FakeComponent


class ReadingComponent:
    """Component that reads upstream results."""

    def __init__(self, name: str, consumes: frozenset[str], produces: str, read_kind: str):
        self.name = name
        self.consumes = consumes
        self.produces = produces
        self._read_kind = read_kind

    async def run(self, construct: Construct) -> TypedStruct:
        upstream = construct[self._read_kind]
        return TypedStruct(type_url=self.produces, value=f"read:{upstream}")


class FailingComponent:
    """Component that raises an exception."""

    def __init__(self, name: str, consumes: frozenset[str], produces: str):
        self.name = name
        self.consumes = consumes
        self.produces = produces

    async def run(self, construct: Construct) -> TypedStruct:
        raise ValueError(f"{self.name} failed")


class MismatchComponent:
    """Component that declares one type_url but returns another."""

    def __init__(self, name: str, produces: str, actual_type_url: str):
        self.name = name
        self.consumes: frozenset[str] = frozenset()
        self.produces = produces
        self._actual = actual_type_url

    async def run(self, construct: Construct) -> TypedStruct:
        return TypedStruct(type_url=self._actual, value="data")


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

    async def test_ledger_contains_artifacts(self):
        """Construct ledger has proper Artifacts with type_url, producer, id, timestamp."""
        probe = FakeComponent("probe", frozenset(), "probe.response", data="hello")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade", data=True)

        orch = Orchestrator([probe, sensor])
        construct = await orch.run()

        ledger = construct.ledger
        assert len(ledger) == 2

        assert isinstance(ledger[0], Artifact)
        assert ledger[0].type_url == "probe.response"
        assert ledger[0].producer == "probe"
        assert ledger[0].data == "hello"
        assert ledger[0].id  # UUID present
        assert ledger[0].timestamp  # timestamp present

        assert ledger[1].type_url == "sensor.grade"
        assert ledger[1].producer == "sensor"
        assert ledger[1].data is True

    async def test_contract_error_on_type_url_mismatch(self):
        """Orchestrator raises ContractError when type_url != produces."""
        bad = MismatchComponent(
            name="liar",
            produces="declared.type",
            actual_type_url="actual.type",
        )

        orch = Orchestrator([bad])
        with pytest.raises(ContractError, match="declared produces='declared.type'"):
            await orch.run()

    async def test_contract_error_message(self):
        """ContractError message includes component name and both type_urls."""
        bad = MismatchComponent(
            name="broken",
            produces="expected.v1/foo",
            actual_type_url="wrong.v1/bar",
        )

        orch = Orchestrator([bad])
        with pytest.raises(ContractError) as exc_info:
            await orch.run()

        msg = str(exc_info.value)
        assert "'broken'" in msg
        assert "expected.v1/foo" in msg
        assert "wrong.v1/bar" in msg
