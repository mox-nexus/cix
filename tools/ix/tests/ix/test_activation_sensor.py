"""Tests for ActivationSensor — evaluative sensor that checks tool calls."""

from ix.domain.types import Trial
from ix.eval.sensors import ActivationSensor
from matrix import AgentResponse


def _trial_with_skill(skill: str) -> Trial:
    return Trial(
        probe_id="test-probe",
        trial_index=0,
        response=AgentResponse(
            tool_calls=({"name": "Skill", "input": {"skill": skill}},),
        ),
    )


def _trial_no_tools() -> Trial:
    return Trial(
        probe_id="test-probe",
        trial_index=0,
        response=AgentResponse(content="just text, no tools"),
    )


class TestActivationSensor:
    def test_detects_exact_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.sense(_trial_with_skill("build-eval"))
        assert result[0].passed is True
        assert result[0].score == 1.0

    def test_detects_partial_match(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.sense(_trial_with_skill("build-evals:build-eval"))
        assert result[0].passed is True

    def test_detects_eval_keyword(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.sense(_trial_with_skill("eval-1337"))
        assert result[0].passed is True

    def test_no_activation_without_tools(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.sense(_trial_no_tools())
        assert result[0].passed is False
        assert result[0].score == 0.0

    def test_no_activation_wrong_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.sense(_trial_with_skill("data-store"))
        assert result[0].passed is False

    def test_non_skill_tool_ignored(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = Trial(
            probe_id="test-probe",
            trial_index=0,
            response=AgentResponse(
                tool_calls=({"name": "Read", "input": {"path": "/foo"}},),
            ),
        )
        result = sensor.sense(trial)
        assert result[0].passed is False

    def test_reading_carries_trial_identity(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        trial = Trial(
            probe_id="must-001",
            trial_index=3,
            response=AgentResponse(
                tool_calls=({"name": "Skill", "input": {"skill": "build-eval"}},),
            ),
        )
        result = sensor.sense(trial)
        assert result[0].probe_id == "must-001"
        assert result[0].trial_index == 3
