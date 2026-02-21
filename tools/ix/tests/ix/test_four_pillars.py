"""Tests for core engine — generic, eval-free.

Uses pure-Python dummy implementations to prove the engine
works with any domain, not just eval.
"""

from ix.adapters._out.components import TrialNode
from ix.domain.ports import ExperimentRuntime, Sensor
from ix.domain.types import Probe, Reading, Trial
from matrix import Component, Construct, Orchestrator

# --- Dummy implementations (no eval awareness) ---


class DummyAgent:
    """Returns int(prompt) * 10 as the observation."""

    async def run(self, prompt: str) -> int:
        return int(prompt) * 10


class FailingAgent:
    """Always raises an error."""

    async def run(self, prompt: str):
        raise RuntimeError("SUT crashed")


class ThresholdSensor:
    """Checks if response exceeds a threshold."""

    def __init__(self, threshold: int = 15):
        self._threshold = threshold

    @property
    def name(self) -> str:
        return "threshold"

    def sense(self, trial: Trial) -> list[Reading]:
        passed = trial.response > self._threshold
        return [
            Reading(
                sensor_name=self.name,
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=passed,
                score=float(trial.response),
                details=f"obs={trial.response}, threshold={self._threshold}",
            )
        ]


def _probes(*values: int) -> list[Probe]:
    """Create probes from integer values."""
    return [Probe(id=str(v), prompt=str(v)) for v in values]


# --- Protocol conformance ---


class TestProtocolConformance:
    def test_dummy_agent_satisfies_protocol(self):
        assert isinstance(DummyAgent(), ExperimentRuntime)

    def test_threshold_sensor_satisfies_protocol(self):
        assert isinstance(ThresholdSensor(), Sensor)

    def test_trial_node_satisfies_component(self):
        node = TrialNode(
            probes=_probes(1),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(),
        )
        assert isinstance(node, Component)


# --- TrialNode ---


class TestTrialNode:
    async def test_produces_correct_reading_count(self):
        """probes x trials = readings (one sensor reading per trial)."""
        node = TrialNode(
            probes=_probes(1, 2, 3),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(threshold=15),
            trials=2,
        )
        construct = Construct()
        results = await node.run(construct)

        assert len(results) == 6  # 3 probes x 2 trials
        assert all(isinstance(r, Reading) for r in results)

    async def test_readings_reflect_sensor_logic(self):
        """ThresholdSensor: resp > threshold → pass."""
        node = TrialNode(
            probes=_probes(1, 5),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(threshold=15),
            trials=1,
        )
        construct = Construct()
        results = await node.run(construct)

        # probe "1" → resp=10 (fail, 10 < 15)
        # probe "5" → resp=50 (pass, 50 > 15)
        assert results[0].passed is False
        assert results[0].score == 10.0
        assert results[1].passed is True
        assert results[1].score == 50.0

    async def test_trial_indices_are_correct(self):
        node = TrialNode(
            probes=_probes(1),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(),
            trials=3,
        )
        construct = Construct()
        results = await node.run(construct)

        assert [r.trial_index for r in results] == [0, 1, 2]

    async def test_captures_errors_as_failed_readings(self):
        """Runtime errors are captured as failed readings, not raised."""
        node = TrialNode(
            probes=_probes(1, 2),
            runtime=FailingAgent(),
            sensor=ThresholdSensor(),
        )
        construct = Construct()
        results = await node.run(construct)

        assert len(results) == 2
        for r in results:
            assert r.passed is False
            assert "SUT crashed" in r.details

    async def test_preserves_probe_id(self):
        node = TrialNode(
            probes=_probes(42),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(),
        )
        construct = Construct()
        results = await node.run(construct)

        assert results[0].probe_id == "42"


# --- Full DAG integration ---


class TestFullDag:
    async def test_orchestrator_single_node_dag(self):
        """Orchestrator compiles and runs TrialNode (execute + sense)."""
        trial_node = TrialNode(
            probes=_probes(1, 2, 3),
            runtime=DummyAgent(),
            sensor=ThresholdSensor(threshold=15),
            trials=2,
        )

        orchestrator = Orchestrator([trial_node])
        construct = await orchestrator.run()

        readings = construct["experiment.readings"]

        assert len(readings) == 6  # 3 probes x 2 trials

        # probe "1" -> resp=10 (fail), "2" -> resp=20 (pass), "3" -> resp=30 (pass)
        passed_count = sum(1 for r in readings if r.passed)
        assert passed_count == 4  # "2" and "3" pass, each x 2 trials
