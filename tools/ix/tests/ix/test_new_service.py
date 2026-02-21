"""Tests for Experiment (Four Pillars version).

Verifies full in-memory integration: mock agent -> service.run() -> ExperimentResults.
"""

from pathlib import Path

import pytest
from ix.adapters._out.filesystem_store import FilesystemStore
from ix.adapters._out.mock_runtime import MockAgent
from ix.domain.types import Probe, Reading, Subject
from ix.eval.analysis import aggregate_readings, compute_metrics, interpret
from ix.eval.models import ExperimentConfig, ProbeResult
from ix.eval.sensors import ActivationSensor
from ix.eval.service import Experiment


def _r(probe_id: str, trial: int, passed: bool) -> Reading:
    """Shorthand for test Reading construction."""
    return Reading(
        sensor_name="activation",
        probe_id=probe_id,
        trial_index=trial,
        passed=passed,
        score=1.0 if passed else 0.0,
    )


def _probe(id: str, prompt: str, expectation: str) -> Probe:
    return Probe(id=id, prompt=prompt, metadata={"expectation": expectation})


def _config(probes: tuple[Probe, ...], trials: int = 5) -> ExperimentConfig:
    return ExperimentConfig(
        name="test-activation",
        subjects=(Subject(name="build-eval"),),
        trials=trials,
        probes=probes,
    )


@pytest.fixture
def service(tmp_path: Path) -> Experiment:
    agent = MockAgent(expected_skill="build-eval", seed=42)
    return Experiment(
        agent=agent,
        sensor=ActivationSensor(expected_skill="build-eval"),
        store=FilesystemStore(tmp_path),
    )


# --- Analysis function tests ---


class TestAggregateReadings:
    def test_correct_metrics(self):
        """Synthetic data -> correct ProbeResults."""
        must_probe = _probe("m1", "eval?", "must_trigger")
        not_probe = _probe("n1", "sort?", "should_not_trigger")
        probes = {must_probe.id: must_probe, not_probe.id: not_probe}

        readings = [
            _r("m1", 0, True),
            _r("m1", 1, True),
            _r("n1", 0, False),
            _r("n1", 1, False),
        ]

        results = aggregate_readings(readings, probes)

        assert len(results) == 2
        must = next(r for r in results if r.probe_id == "m1")
        not_r = next(r for r in results if r.probe_id == "n1")
        assert must.score == 1.0
        assert must.correct is True
        assert not_r.score == 0.0
        assert not_r.correct is True

    def test_majority_vote(self):
        """3 pass + 2 fail = pass (score > 0.5)."""
        probe = _probe("m1", "eval?", "must_trigger")
        probes = {probe.id: probe}
        readings = [
            _r("m1", 0, True),
            _r("m1", 1, True),
            _r("m1", 2, True),
            _r("m1", 3, False),
            _r("m1", 4, False),
        ]

        results = aggregate_readings(readings, probes)
        assert results[0].score == 0.6
        assert results[0].correct is True

    def test_callback_fires(self):
        probe = _probe("m1", "eval?", "must_trigger")
        probes = {probe.id: probe}
        readings = [
            Reading(sensor_name="activation", probe_id="m1", trial_index=0, passed=True, score=1.0),
        ]

        completed = []
        aggregate_readings(readings, probes, on_probe_complete=completed.append)
        assert len(completed) == 1


class TestComputeMetrics:
    def test_perfect(self):
        results = [
            ProbeResult(probe_id="m1", expectation="must_trigger", score=1.0, correct=True),
            ProbeResult(probe_id="m2", expectation="must_trigger", score=0.8, correct=True),
            ProbeResult(probe_id="n1", expectation="should_not_trigger", score=0.0, correct=True),
        ]
        metrics = compute_metrics(results)
        assert metrics["f1"] == 1.0
        assert metrics["tp"] == 2
        assert metrics["tn"] == 1

    def test_all_wrong(self):
        results = [
            ProbeResult(probe_id="m1", expectation="must_trigger", score=0.2, correct=False),
            ProbeResult(probe_id="n1", expectation="should_not_trigger", score=0.8, correct=False),
        ]
        metrics = compute_metrics(results)
        assert metrics["f1"] == 0.0
        assert metrics["fn"] == 1
        assert metrics["fp"] == 1


class TestInterpret:
    def test_excellent(self):
        metrics = dict(precision=0.95, recall=0.93, f1=0.94, tp=14, fp=1, fn=1, tn=9)
        interp = interpret(metrics)
        assert interp["status"] == "excellent"

    def test_low_recall(self):
        metrics = dict(precision=0.9, recall=0.6, f1=0.72, tp=9, fp=1, fn=6, tn=9)
        interp = interpret(metrics)
        assert interp["status"] == "good"
        assert any("recall" in i.lower() for i in interp["issues"])

    def test_poor(self):
        metrics = dict(precision=0.3, recall=0.4, f1=0.34, tp=4, fp=9, fn=6, tn=1)
        interp = interpret(metrics)
        assert interp["status"] == "poor"


# --- Full service integration ---


class TestExperiment:
    async def test_produces_metrics(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "How do I write evals?", "must_trigger"),
                _probe("must-002", "What metrics for LLM?", "must_trigger"),
                _probe("not-001", "Write a Python function", "should_not_trigger"),
            ),
            trials=5,
        )
        results = await service.run(exp)

        assert 0.0 <= results.precision <= 1.0
        assert 0.0 <= results.recall <= 1.0
        assert 0.0 <= results.f1 <= 1.0
        assert results.tp + results.fn == 2
        assert results.fp + results.tn == 1

    async def test_interpretation(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
            trials=3,
        )
        results = await service.run(exp)

        assert results.status in ("excellent", "good", "needs_work", "poor")

    async def test_skips_acceptable(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("edge-001", "test my code?", "acceptable"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
        )
        results = await service.run(exp)
        probe_ids = [pr.probe_id for pr in results.probe_results]
        assert "edge-001" not in probe_ids
        assert len(results.probe_results) == 2

    async def test_callback_fires(self, service: Experiment):
        completed = []
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
            trials=1,
        )
        await service.run(exp, on_probe_complete=completed.append)
        assert len(completed) == 2

    async def test_results_persisted(self, service: Experiment, tmp_path: Path):
        exp = _config(
            probes=(_probe("must-001", "evals?", "must_trigger"),),
            trials=2,
        )
        await service.run(exp)

        latest = tmp_path / "test-activation" / "results" / "summary-latest.json"
        assert latest.exists()

    async def test_high_f1(self, service: Experiment):
        """Seed=42 with 90/10 mock rates -> high F1."""
        exp = _config(
            probes=tuple(
                _probe(f"must-{i:03d}", f"eval question {i}", "must_trigger") for i in range(1, 11)
            )
            + tuple(
                _probe(f"not-{i:03d}", f"non-eval question {i}", "should_not_trigger")
                for i in range(1, 6)
            ),
            trials=5,
        )
        results = await service.run(exp)
        assert results.f1 >= 0.7
