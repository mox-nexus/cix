"""Tests for ix DAG components — TrialNode (execute + sense)."""

from ix.adapters._out.components import TrialNode
from ix.adapters._out.mock_runtime import MockAgent
from ix.domain.types import Probe, Reading
from ix.eval.sensors import ActivationSensor
from matrix import Component, Construct

# --- Helpers ---


def _probes() -> list[Probe]:
    return [
        Probe(
            id="must-001", prompt="How do I write evals?", metadata={"expectation": "must_trigger"}
        ),
        Probe(
            id="not-001",
            prompt="Write a Python function",
            metadata={"expectation": "should_not_trigger"},
        ),
    ]


# --- Protocol Tests ---


class TestProtocol:
    def test_trial_node_satisfies_component(self):
        agent = MockAgent(expected_skill="build-eval", seed=42)
        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(_probes(), agent, sensor)
        assert isinstance(node, Component)


# --- TrialNode Tests ---


class TestTrialNode:
    async def test_produces_readings(self):
        """TrialNode returns TypedStruct with one Reading per (probe x trial x sensor)."""
        agent = MockAgent(expected_skill="build-eval", seed=42)
        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(_probes(), agent, sensor, trials=3)

        construct = Construct()
        result = await node.run(construct)

        assert result.type_url == "ix.v1/experiment.readings"
        # 2 probes x 3 trials = 6 readings (one sensor per trial)
        assert len(result.value) == 6
        assert all(isinstance(r, Reading) for r in result.value)

    async def test_readings_have_identity(self):
        """Each reading traces back to its probe and trial."""
        agent = MockAgent(expected_skill="build-eval", seed=42)
        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(_probes(), agent, sensor, trials=1)

        construct = Construct()
        result = await node.run(construct)
        readings = result.value

        assert len(readings) == 2
        probe_ids = {r.probe_id for r in readings}
        assert probe_ids == {"must-001", "not-001"}
        assert all(r.trial_index == 0 for r in readings)
        assert all(r.sensor_name == "activation" for r in readings)

    async def test_error_trial_produces_failed_reading(self):
        """Runtime errors produce failed readings, not exceptions."""

        class FailingAgent:
            async def run(self, prompt: str):
                raise RuntimeError("timeout")

        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(
            [Probe(id="err-001", prompt="fail")],
            FailingAgent(),
            sensor,
        )

        construct = Construct()
        result = await node.run(construct)
        readings = result.value

        assert len(readings) == 1
        assert readings[0].passed is False
        assert readings[0].probe_id == "err-001"
        assert "timeout" in readings[0].details
