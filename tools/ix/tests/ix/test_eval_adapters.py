"""Tests for eval domain adapters — MockAgent, ActivationSensor.

Verifies that eval-specific adapters correctly implement the core
protocols and produce the right types.
"""

from ix.adapters._out.components import TrialNode
from ix.adapters._out.mock_runtime import MockAgent
from ix.domain.ports import ExperimentRuntime, Sensor
from ix.domain.types import Probe, Trial
from ix.eval.sensors import ActivationSensor
from matrix import AgentResponse, Orchestrator

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


# --- Protocol conformance ---


class TestProtocolConformance:
    def test_mock_agent_satisfies_experiment_runtime(self):
        assert isinstance(MockAgent(), ExperimentRuntime)

    def test_activation_sensor_satisfies_sensor(self):
        assert isinstance(ActivationSensor(), Sensor)


# --- MockAgent ---


class TestMockAgent:
    async def test_returns_agent_response(self):
        agent = MockAgent(expected_skill="build-eval")
        response = await agent.run("How do evals work?")

        assert isinstance(response, AgentResponse)
        assert "build-eval" in response.content

    async def test_always_activates_without_expectations(self):
        agent = MockAgent(expected_skill="build-eval")
        response = await agent.run("anything")

        assert len(response.tool_calls) == 1
        assert response.tool_calls[0]["name"] == "Skill"
        assert response.tool_calls[0]["input"]["skill"] == "build-eval"

    async def test_deterministic_with_seed(self):
        agent1 = MockAgent(expected_skill="build-eval", seed=42, expectations={"q": True})
        agent2 = MockAgent(expected_skill="build-eval", seed=42, expectations={"q": True})

        r1 = await agent1.run("q")
        r2 = await agent2.run("q")

        assert r1 == r2

    async def test_no_tool_calls_when_not_activated(self):
        # seed=7 with should_not_trigger (10% rate) should NOT activate
        agent = MockAgent(
            expected_skill="build-eval",
            seed=7,
            expectations={"hello": False},
        )
        response = await agent.run("hello")

        assert len(response.tool_calls) == 0


# --- ActivationSensor ---


class TestActivationSensor:
    def _trial(self, response: AgentResponse) -> Trial:
        return Trial(probe_id="test", trial_index=0, response=response)

    def test_detects_exact_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = self._trial(
            AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "build-eval"}},),
            )
        )
        readings = sensor.sense(trial)

        assert len(readings) == 1
        assert readings[0].passed is True
        assert readings[0].score == 1.0
        assert readings[0].sensor_name == "activation"

    def test_detects_partial_match(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = self._trial(
            AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "build-evals:build-eval"}},),
            )
        )
        assert sensor.sense(trial)[0].passed is True

    def test_detects_eval_keyword(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = self._trial(
            AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "eval-1337"}},),
            )
        )
        assert sensor.sense(trial)[0].passed is True

    def test_no_activation_without_tools(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = self._trial(AgentResponse(content="just text"))
        readings = sensor.sense(trial)

        assert readings[0].passed is False
        assert readings[0].score == 0.0

    def test_no_activation_wrong_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = self._trial(
            AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "data-store"}},),
            )
        )
        assert sensor.sense(trial)[0].passed is False


# --- Full DAG integration ---


class TestEvalDagIntegration:
    async def test_full_eval_dag(self):
        """Orchestrator([TrialNode(sensor=ActivationSensor)])
        produces correct Readings.
        """
        probes = _probes()

        trial_node = TrialNode(
            probes=probes,
            runtime=MockAgent(expected_skill="build-eval"),
            sensor=ActivationSensor(expected_skill="build-eval"),
            trials=2,
        )

        orchestrator = Orchestrator([trial_node])
        construct = await orchestrator.run()

        readings = construct["experiment.readings"]

        assert len(readings) == 4  # 2 probes x 2 trials

        # MockAgent always activates build-eval (no expectations set)
        # So both must_trigger and should_not_trigger get activated
        assert all(r.passed for r in readings)
        assert all(r.sensor_name == "activation" for r in readings)
