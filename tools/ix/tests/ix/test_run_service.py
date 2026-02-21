"""Tests for Experiment — verifies metrics match expected shape."""

from pathlib import Path

import pytest
from ix.adapters._out.filesystem_store import FilesystemStore
from ix.adapters._out.mock_runtime import MockAgent
from ix.domain.types import Probe, Subject
from ix.eval.analysis import compute_metrics, interpret
from ix.eval.models import ExperimentConfig, ProbeResult
from ix.eval.sensors import ActivationSensor
from ix.eval.service import Experiment


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


class TestExperiment:
    async def test_produces_metrics_shape(self, service: Experiment):
        """End-to-end: dry-run produces precision/recall/F1/confusion matrix."""
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

    async def test_interpretation_shape(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
            trials=3,
        )
        results = await service.run(exp)

        assert results.status in ("excellent", "good", "needs_work", "poor")
        assert isinstance(results.issues, tuple)
        assert isinstance(results.suggestions, tuple)

    async def test_skips_acceptable_probes(self, service: Experiment):
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

    async def test_dry_run_high_f1(self, service: Experiment):
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

        latest_path = tmp_path / "test-activation" / "results" / "summary-latest.json"
        assert latest_path.exists()


class TestMetricsComputation:
    def test_perfect_metrics(self):
        results = [
            ProbeResult(probe_id="m1", expectation="must_trigger", score=0.8, correct=True),
            ProbeResult(probe_id="m2", expectation="must_trigger", score=1.0, correct=True),
            ProbeResult(probe_id="n1", expectation="should_not_trigger", score=0.0, correct=True),
        ]
        metrics = compute_metrics(results)
        assert metrics["precision"] == 1.0
        assert metrics["recall"] == 1.0
        assert metrics["f1"] == 1.0

    def test_all_wrong(self):
        results = [
            ProbeResult(probe_id="m1", expectation="must_trigger", score=0.2, correct=False),
            ProbeResult(probe_id="n1", expectation="should_not_trigger", score=0.8, correct=False),
        ]
        metrics = compute_metrics(results)
        assert metrics["f1"] == 0.0


class TestInterpretation:
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
