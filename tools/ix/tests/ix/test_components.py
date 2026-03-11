"""Tests for ix DAG components — ProbeNode, SubjectNode, TrialNode, SensorNode.

Four-node inner DAG:
  ProbeNode → TrialNode ← SubjectNode
                 ↓
             SensorNode
"""

from matrix import Artifact, Component, ComponentRegistry, Construct, AgentResponse, Orchestrator

from ix.adapters._out.components import ProbeNode, SensorNode, SubjectNode, TrialNode
from ix.domain.types import Probe, Reading, Subject, Trial
from ix.eval.sensors import ActivationSensor


# --- Test Helpers ---


class _EchoAgent:
    """Test agent — echoes prompt as content, adds a tool call."""

    async def run(self, prompt: str) -> AgentResponse:
        return AgentResponse(
            content=f"echo: {prompt}",
            tool_calls=({"name": "Skill", "input": {"skill": "build-eval"}},),
        )


class _FailingAgent:
    """Test agent — always raises."""

    async def run(self, prompt: str):
        raise RuntimeError("timeout")


def _test_registry(agent_type: str = "test", agent_factory=None) -> ComponentRegistry:
    """Build a registry with a test agent."""
    registry = ComponentRegistry()
    factory = agent_factory or (lambda **kw: _EchoAgent())
    registry.register(f"matrix.agent.{agent_type}", factory)
    return registry


def _probe(id: str = "must-001", prompt: str = "How do I write evals?") -> Probe:
    return Probe(id=id, prompt=prompt, metadata={"expectation": "must_trigger"})


def _subject(runtime_type: str = "test") -> Subject:
    return Subject(
        name="test-subject",
        config={"system_prompt": "You are helpful.", "runtime": {"type": runtime_type}},
    )


def _construct_with_trial(trial: Trial) -> Construct:
    """Pre-populate a Construct with one trial for isolated SensorNode tests."""
    construct = Construct()
    construct.append(
        Artifact.create(type_url="trial.observation", producer="trial", data=trial)
    )
    return construct


# --- Protocol Tests ---


class TestProtocol:
    def test_probe_node_satisfies_component(self):
        assert isinstance(ProbeNode(_probe()), Component)

    def test_subject_node_satisfies_component(self):
        assert isinstance(SubjectNode(_subject()), Component)

    def test_trial_node_satisfies_component(self):
        assert isinstance(TrialNode(_test_registry()), Component)

    def test_sensor_node_satisfies_component(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        assert isinstance(SensorNode(sensor), Component)


# --- ProbeNode Tests ---


class TestProbeNode:
    async def test_produces_stimulus(self):
        probe = _probe()
        node = ProbeNode(probe)
        result = await node.run(Construct())

        assert result.type_url == "probe.stimulus"
        assert result.value is probe

    async def test_root_node_no_consumes(self):
        assert ProbeNode(_probe()).consumes == frozenset()


# --- SubjectNode Tests ---


class TestSubjectNode:
    async def test_produces_config(self):
        subject = _subject()
        node = SubjectNode(subject)
        result = await node.run(Construct())

        assert result.type_url == "subject.config"
        assert result.value == subject.config
        assert result.value["system_prompt"] == "You are helpful."

    async def test_root_node_no_consumes(self):
        assert SubjectNode(_subject()).consumes == frozenset()


# --- TrialNode Tests ---


class TestTrialNode:
    async def test_produces_observation(self):
        registry = _test_registry()
        probe = _probe()
        subject = _subject()

        # Build construct with probe + subject
        construct = Construct()
        construct.append(Artifact.create(type_url="probe.stimulus", producer="probe", data=probe))
        construct.append(
            Artifact.create(type_url="subject.config", producer="subject", data=subject.config)
        )

        node = TrialNode(registry=registry, trial_index=0)
        result = await node.run(construct)

        assert result.type_url == "trial.observation"
        trial = result.value
        assert isinstance(trial, Trial)
        assert trial.probe_id == "must-001"
        assert trial.trial_index == 0
        assert trial.error is None

    async def test_creates_agent_from_registry(self):
        """TrialNode resolves agent type through registry."""
        created_with = {}

        def capturing_factory(**kw):
            created_with.update(kw)
            return _EchoAgent()

        registry = _test_registry(agent_factory=capturing_factory)

        construct = Construct()
        construct.append(
            Artifact.create(type_url="probe.stimulus", producer="probe", data=_probe())
        )
        construct.append(
            Artifact.create(
                type_url="subject.config",
                producer="subject",
                data={"system_prompt": "Be precise.", "runtime": {"type": "test"}},
            )
        )

        node = TrialNode(registry=registry, trial_index=3)
        await node.run(construct)

        assert created_with["system_prompt"] == "Be precise."
        assert created_with["trial_index"] == 3

    async def test_error_captured_not_raised(self):
        """Runtime errors produce error trials, not exceptions."""
        registry = _test_registry(agent_factory=lambda **kw: _FailingAgent())

        construct = Construct()
        construct.append(
            Artifact.create(type_url="probe.stimulus", producer="probe", data=_probe("err-001"))
        )
        construct.append(
            Artifact.create(
                type_url="subject.config",
                producer="subject",
                data={"runtime": {"type": "test"}},
            )
        )

        node = TrialNode(registry=registry)
        result = await node.run(construct)

        trial = result.value
        assert trial.error == "timeout"
        assert trial.probe_id == "err-001"
        assert trial.response is None


# --- SensorNode Tests ---


class TestSensorNode:
    async def test_produces_readings(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = Trial(
            probe_id="must-001",
            trial_index=0,
            response=AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "build-eval"}},),
            ),
        )

        construct = _construct_with_trial(trial)
        node = SensorNode(sensor)
        result = await node.run(construct)

        assert result.type_url == "sensor.reading"
        assert len(result.value) == 1
        assert result.value[0].passed is True
        assert result.value[0].sensor_name == "activation"

    async def test_error_trial_produces_failed_reading(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        error_trial = Trial(probe_id="err-001", trial_index=0, error="timeout")

        construct = _construct_with_trial(error_trial)
        node = SensorNode(sensor)
        result = await node.run(construct)

        readings = result.value
        assert len(readings) == 1
        assert readings[0].passed is False
        assert "timeout" in readings[0].details


# --- Full 4-Node DAG Integration ---


class TestInnerDag:
    async def test_four_node_dag(self):
        """Orchestrator runs ProbeNode → TrialNode ← SubjectNode → SensorNode."""
        registry = _test_registry()
        probe = _probe()
        subject = _subject()
        sensor = ActivationSensor(expected_skill="build-eval")

        probe_node = ProbeNode(probe)
        subject_node = SubjectNode(subject)
        trial_node = TrialNode(registry=registry, trial_index=0)
        sensor_node = SensorNode(sensor)

        orchestrator = Orchestrator([probe_node, subject_node, trial_node, sensor_node])
        construct = await orchestrator.run()

        # Trial was produced
        trial = construct["trial.observation"]
        assert isinstance(trial, Trial)
        assert trial.probe_id == "must-001"
        assert trial.response.content == "echo: How do I write evals?"

        # Sensor graded it
        readings = construct["sensor.reading"]
        assert len(readings) == 1
        assert readings[0].passed is True
