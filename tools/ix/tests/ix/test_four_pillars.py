"""Tests for core engine — generic, eval-free.

Uses pure-Python dummy implementations to prove the engine
works with any domain, not just eval. Registers a DummyAgent
in the ComponentRegistry to exercise the unified type → registry path.
"""

from ix.adapters._out.components import ProbeNode, SensorNode, SubjectNode, TrialNode
from ix.domain.ports import Sensor
from ix.domain.types import Probe, Reading, Subject, Trial
from matrix import Artifact, Component, ComponentRegistry, Construct, Orchestrator

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

    def measure(self, trial: Trial) -> list[Reading]:
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


def _subject(runtime_type: str = "dummy") -> Subject:
    return Subject(name="test", config={"runtime": {"type": runtime_type}})


def _registry(agent_factory=None) -> ComponentRegistry:
    registry = ComponentRegistry()
    factory = agent_factory or (lambda **kw: DummyAgent())
    registry.register("matrix.agent.dummy", factory)
    return registry


def _construct_with_trial(trial: Trial) -> Construct:
    """Pre-populate a Construct with one trial for isolated SensorNode tests."""
    construct = Construct()
    construct.append(Artifact.create(type_url="trial.observation", producer="trial", data=trial))
    return construct


# --- Protocol conformance ---


class TestProtocolConformance:
    def test_threshold_sensor_satisfies_protocol(self):
        assert isinstance(ThresholdSensor(), Sensor)

    def test_probe_node_satisfies_component(self):
        assert isinstance(ProbeNode(Probe(id="1", prompt="1")), Component)

    def test_subject_node_satisfies_component(self):
        assert isinstance(SubjectNode(_subject()), Component)

    def test_trial_node_satisfies_component(self):
        assert isinstance(TrialNode(_registry()), Component)

    def test_sensor_node_satisfies_component(self):
        assert isinstance(SensorNode(sensor=ThresholdSensor()), Component)


# --- TrialNode ---


class TestTrialNode:
    async def test_produces_trial_with_response(self):
        """DummyAgent: int(prompt) * 10."""
        reg = _registry()
        probe = _probes(5)[0]

        construct = Construct()
        construct.append(Artifact.create(type_url="probe.stimulus", producer="probe", data=probe))
        construct.append(
            Artifact.create(type_url="subject.config", producer="subject", data=_subject().config)
        )

        node = TrialNode(registry=reg, trial_index=0)
        result = await node.run(construct)

        assert result.type_url == "trial.observation"
        assert result.value.response == 50
        assert result.value.probe_id == "5"

    async def test_captures_errors(self):
        reg = _registry(agent_factory=lambda **kw: FailingAgent())

        construct = Construct()
        construct.append(
            Artifact.create(type_url="probe.stimulus", producer="probe", data=_probes(1)[0])
        )
        construct.append(
            Artifact.create(type_url="subject.config", producer="subject", data=_subject().config)
        )

        node = TrialNode(registry=reg, trial_index=0)
        result = await node.run(construct)

        assert result.value.error == "SUT crashed"
        assert result.value.response is None


# --- SensorNode ---


class TestSensorNode:
    async def test_produces_readings_from_trial(self):
        trial = Trial(probe_id="5", trial_index=0, response=50)
        construct = _construct_with_trial(trial)
        node = SensorNode(sensor=ThresholdSensor(threshold=15))
        result = await node.run(construct)

        assert result.type_url == "sensor.reading"
        assert len(result.value) == 1
        assert result.value[0].passed is True
        assert result.value[0].score == 50.0

    async def test_below_threshold_fails(self):
        trial = Trial(probe_id="1", trial_index=0, response=10)
        construct = _construct_with_trial(trial)
        node = SensorNode(sensor=ThresholdSensor(threshold=15))
        result = await node.run(construct)

        assert result.value[0].passed is False
        assert result.value[0].score == 10.0

    async def test_error_trial_produces_failed_reading(self):
        trial = Trial(probe_id="err", trial_index=0, error="SUT crashed")
        construct = _construct_with_trial(trial)
        node = SensorNode(sensor=ThresholdSensor())
        result = await node.run(construct)

        assert len(result.value) == 1
        assert result.value[0].passed is False
        assert "SUT crashed" in result.value[0].details


# --- Full 4-node DAG integration ---


class TestFullDag:
    async def test_four_node_dag(self):
        """Orchestrator runs the full inner DAG with DummyAgent."""
        reg = _registry()
        probe = _probes(3)[0]  # DummyAgent returns 30
        subject = _subject()
        sensor = ThresholdSensor(threshold=15)

        orchestrator = Orchestrator(
            [
                ProbeNode(probe),
                SubjectNode(subject),
                TrialNode(registry=reg, trial_index=0),
                SensorNode(sensor),
            ]
        )
        construct = await orchestrator.run()

        trial = construct["trial.observation"]
        assert trial.response == 30

        readings = construct["sensor.reading"]
        assert len(readings) == 1
        assert readings[0].passed is True  # 30 > 15
        assert readings[0].score == 30.0

    async def test_below_threshold_probe(self):
        """Probe with value 1 → response 10 → fails threshold 15."""
        reg = _registry()

        orchestrator = Orchestrator(
            [
                ProbeNode(_probes(1)[0]),
                SubjectNode(_subject()),
                TrialNode(registry=reg, trial_index=0),
                SensorNode(ThresholdSensor(threshold=15)),
            ]
        )
        construct = await orchestrator.run()

        readings = construct["sensor.reading"]
        assert readings[0].passed is False
        assert readings[0].score == 10.0
