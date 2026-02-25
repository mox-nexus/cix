"""Tests for ix domain and eval models."""

import pytest
from ix.domain.types import Probe, Reading, Subject, Trial
from ix.eval.models import (
    ExperimentConfig,
    ExperimentResults,
    TrialRecord,
)
from matrix import AgentResponse
from pydantic import ValidationError


class TestProbe:
    def test_basic(self):
        p = Probe(id="must-001", prompt="test prompt")
        assert p.id == "must-001"
        assert p.metadata == {}

    def test_with_metadata(self):
        p = Probe(id="must-001", prompt="test", metadata={"expectation": "must_trigger"})
        assert p.metadata["expectation"] == "must_trigger"

    def test_frozen(self):
        p = Probe(id="x", prompt="p")
        with pytest.raises(ValidationError):
            p.id = "y"  # type: ignore[misc]


class TestSubject:
    def test_basic(self):
        s = Subject(name="build-eval")
        assert s.name == "build-eval"
        assert s.description == ""
        assert s.config == {}

    def test_with_config(self):
        s = Subject(name="build-eval", description="Eval skill", config={"version": "1.0"})
        assert s.description == "Eval skill"
        assert s.config["version"] == "1.0"

    def test_frozen(self):
        s = Subject(name="build-eval")
        with pytest.raises(ValidationError):
            s.name = "other"  # type: ignore[misc]


class TestTrial:
    def test_basic(self):
        t = Trial(probe_id="must-001", trial_index=0, response="hello")
        assert t.probe_id == "must-001"
        assert t.response == "hello"
        assert t.error is None

    def test_with_error(self):
        t = Trial(probe_id="must-001", trial_index=0, error="boom")
        assert t.error == "boom"
        assert t.response is None


class TestExperimentConfig:
    def test_minimal(self):
        exp = ExperimentConfig(name="test")
        assert exp.name == "test"
        assert exp.trials == 5
        assert exp.probes == ()
        assert exp.sensors == ({"type": "activation"},)

    def test_sensor_normalized_to_sensors(self):
        """Single sensor dict is normalized to one-element sensors tuple."""
        exp = ExperimentConfig(name="test", sensor={"type": "latency"})
        assert exp.sensors == ({"type": "latency"},)

    def test_with_probes(self):
        probes = (
            Probe(id="a", prompt="p1", metadata={"expectation": "must_trigger"}),
            Probe(id="b", prompt="p2", metadata={"expectation": "should_not_trigger"}),
        )
        exp = ExperimentConfig(
            name="test",
            subjects=(Subject(name="build-eval"),),
            probes=probes,
        )
        assert len(exp.probes) == 2
        assert exp.subjects[0].name == "build-eval"

    def test_explicit_subjects(self):
        subjects = (Subject(name="build-eval"), Subject(name="data-store"))
        exp = ExperimentConfig(name="test", subjects=subjects)
        assert len(exp.subjects) == 2

    def test_sensors_list(self):
        exp = ExperimentConfig(
            name="test",
            sensors=(
                {"type": "activation", "expected_skill": "build-eval"},
                {"type": "deepeval", "metric": "answer_relevancy"},
            ),
        )
        assert len(exp.sensors) == 2
        assert exp.sensors[0]["type"] == "activation"
        assert exp.sensors[1]["type"] == "deepeval"


class TestAgentResponseInMatrix:
    """Verify AgentResponse (Matrix type) works in ix context."""

    def test_with_tool_calls(self):
        r = AgentResponse(
            content="response text",
            tool_calls=({"name": "Skill", "input": {"skill": "build-eval"}},),
        )
        assert len(r.tool_calls) == 1
        assert r.tool_calls[0]["name"] == "Skill"

    def test_defaults(self):
        r = AgentResponse()
        assert r.content == ""
        assert r.tool_calls == ()
        assert r.tokens_input == 0
        assert r.cost_usd is None
        assert r.num_turns == 0


class TestTrialRecord:
    def test_basic(self):
        v = TrialRecord(
            probe_id="must-001",
            trial=0,
            observation=AgentResponse(content="hi"),
            reading=Reading(
                sensor_name="activation",
                probe_id="must-001",
                trial_index=0,
                passed=True,
                score=1.0,
            ),
        )
        assert v.probe_id == "must-001"
        assert v.reading.passed is True


class TestExperimentResults:
    def test_with_metrics(self):
        results = ExperimentResults(
            experiment_name="skill-activation",
            precision=0.9,
            recall=0.8,
            f1=0.85,
            tp=12,
            fp=1,
            fn=3,
            tn=9,
            status="good",
            issues=("Low recall",),
            suggestions=("Broaden triggers",),
        )
        assert results.f1 == 0.85
        assert results.status == "good"

    def test_defaults(self):
        results = ExperimentResults(experiment_name="test")
        assert results.precision == 0.0
        assert results.status == "pending"
        assert results.issues == ()

    def test_serialization_roundtrip(self):
        results = ExperimentResults(
            experiment_name="test",
            precision=0.9,
            recall=0.8,
            f1=0.85,
            tp=12,
            fp=1,
            fn=3,
            tn=9,
            status="good",
        )
        data = results.model_dump()
        restored = ExperimentResults.model_validate(data)
        assert restored == results
