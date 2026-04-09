"""Tests for ActivationSensor — deterministic grader for skill activation.

Verifies exact match, partial match, keyword detection, expectation-aware
grading, and reading traceability. Source: ix/eval/sensors.py
"""

from ix.domain.ports import Sensor
from ix.domain.types import Trial
from ix.eval.sensors import ActivationSensor
from matrix import AgentResponse


def _trial_with_skill(skill: str, probe_id: str = "test-probe") -> Trial:
    return Trial(
        probe_id=probe_id,
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


class TestProtocol:
    def test_satisfies_sensor_protocol(self):
        assert isinstance(ActivationSensor(), Sensor)


class TestActivationSensor:
    def test_detects_exact_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.measure(_trial_with_skill("build-eval"))
        assert result[0].passed is True
        assert result[0].score == 1.0
        assert result[0].sensor_name == "activation"

    def test_detects_partial_match(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.measure(_trial_with_skill("build-evals:build-eval"))
        assert result[0].passed is True

    def test_no_activation_without_tools(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.measure(_trial_no_tools())
        assert result[0].passed is False
        assert result[0].score == 0.0

    def test_no_activation_wrong_skill(self):
        sensor = ActivationSensor(expected_skill="build-eval")
        result = sensor.measure(_trial_with_skill("data-store"))
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
        result = sensor.measure(trial)
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
        result = sensor.measure(trial)
        assert result[0].probe_id == "must-001"
        assert result[0].trial_index == 3


class TestExpectationAware:
    """ActivationSensor with expectations flips pass/fail for should_not_trigger."""

    def test_should_not_trigger_passes_when_not_activated(self):
        sensor = ActivationSensor(
            expected_skill="build-eval",
            expectations={"not-001": "should_not_trigger"},
        )
        trial = Trial(
            probe_id="not-001",
            trial_index=0,
            response=AgentResponse(content="direct answer"),
        )
        result = sensor.measure(trial)
        assert result[0].passed is True

    def test_should_not_trigger_fails_when_activated(self):
        sensor = ActivationSensor(
            expected_skill="build-eval",
            expectations={"not-001": "should_not_trigger"},
        )
        trial = _trial_with_skill("build-eval", probe_id="not-001")
        result = sensor.measure(trial)
        assert result[0].passed is False

    def test_acceptable_always_passes(self):
        sensor = ActivationSensor(
            expected_skill="build-eval",
            expectations={"edge-001": "acceptable"},
        )
        trial = Trial(
            probe_id="edge-001",
            trial_index=0,
            response=AgentResponse(content="direct answer"),
        )
        result = sensor.measure(trial)
        assert result[0].passed is True


class TestMultiSkill:
    """Per-probe expected_skill for multi-skill experiments."""

    def test_per_probe_skill_match(self):
        sensor = ActivationSensor(
            expected_skills={
                "crafting-001": "crafting",
                "research-001": "research",
            },
        )
        trial = _trial_with_skill("crafting", probe_id="crafting-001")
        result = sensor.measure(trial)
        assert result[0].passed is True

    def test_per_probe_skill_mismatch(self):
        sensor = ActivationSensor(
            expected_skills={
                "crafting-001": "crafting",
                "research-001": "research",
            },
        )
        # Probe expects "crafting" but agent activated "research"
        trial = _trial_with_skill("research", probe_id="crafting-001")
        result = sensor.measure(trial)
        assert result[0].passed is False

    def test_per_probe_overrides_default(self):
        sensor = ActivationSensor(
            expected_skill="build-eval",
            expected_skills={"crafting-001": "crafting"},
        )
        trial = _trial_with_skill("crafting", probe_id="crafting-001")
        result = sensor.measure(trial)
        assert result[0].passed is True

    def test_fallback_to_default_when_no_per_probe(self):
        sensor = ActivationSensor(
            expected_skill="build-eval",
            expected_skills={"crafting-001": "crafting"},
        )
        # Probe not in expected_skills — falls back to default
        trial = _trial_with_skill("build-eval", probe_id="other-001")
        result = sensor.measure(trial)
        assert result[0].passed is True

    def test_from_config_reads_probe_metadata(self):
        from ix.domain.types import Probe
        from ix.eval.sensors import ActivationSensorConfig

        config = ActivationSensorConfig(expected_skill="default-skill")
        probes = (
            Probe(id="a", prompt="test", metadata={"expected_skill": "crafting"}),
            Probe(id="b", prompt="test2", metadata={"expected_skill": "research"}),
            Probe(id="c", prompt="test3", metadata={}),
        )
        sensor = ActivationSensor.from_config(config, probes)
        assert sensor._expected_skills["a"] == "crafting"
        assert sensor._expected_skills["b"] == "research"
        assert sensor._expected_skills["c"] == "default-skill"

    def test_should_not_trigger_with_any_skill(self):
        """should_not_trigger fails if ANY skill is activated, regardless of match."""
        sensor = ActivationSensor(
            expected_skills={"not-001": "crafting"},
            expectations={"not-001": "should_not_trigger"},
        )
        # Agent activated a different skill — still a failure for should_not_trigger
        trial = _trial_with_skill("research", probe_id="not-001")
        result = sensor.measure(trial)
        assert result[0].passed is False
