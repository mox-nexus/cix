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
        """TrialNode returns one Reading per (probe x trial x sensor)."""
        agent = MockAgent(expected_skill="build-eval", seed=42)
        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(_probes(), agent, sensor, trials=3)

        construct = Construct()
        results = await node.run(construct)

        # 2 probes x 3 trials = 6 readings (one sensor per trial)
        assert len(results) == 6
        assert all(isinstance(r, Reading) for r in results)

    async def test_readings_have_identity(self):
        """Each reading traces back to its probe and trial."""
        agent = MockAgent(expected_skill="build-eval", seed=42)
        sensor = ActivationSensor(expected_skill="build-eval")
        node = TrialNode(_probes(), agent, sensor, trials=1)

        construct = Construct()
        results = await node.run(construct)

        assert len(results) == 2
        probe_ids = {r.probe_id for r in results}
        assert probe_ids == {"must-001", "not-001"}
        assert all(r.trial_index == 0 for r in results)
        assert all(r.sensor_name == "activation" for r in results)

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
        results = await node.run(construct)

        assert len(results) == 1
        assert results[0].passed is False
        assert results[0].probe_id == "err-001"
        assert "timeout" in results[0].details
