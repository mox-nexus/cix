"""Tests for Experiment — the orchestration service that runs eval experiments.

Covers:
- Pure analysis functions (aggregate_readings, compute_metrics)
- Full Experiment.run() integration with MockAgent
- Persistence verification

Source: ix/eval/experiment.py, ix/eval/analysis.py
"""

from pathlib import Path

import pytest
from ix.adapters._out.filesystem_store import FilesystemStore
from ix.adapters._out.mock_runtime import MockAgent
from ix.composition import make_run_trial
from ix.domain.types import Probe, Reading, Subject
from ix.eval.analysis import aggregate_readings, compute_metrics
from ix.eval.models import ExperimentConfig, ProbeResult
from ix.eval.sensors import ActivationSensor
from ix.eval.experiment import Experiment
from matrix import ComponentRegistry


# --- Helpers ---


def _r(probe_id: str, trial: int, passed: bool) -> Reading:
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


def _mock_registry() -> ComponentRegistry:
    registry = ComponentRegistry()
    registry.register(
        "matrix.agent.mock",
        lambda **kw: MockAgent(expected_skill="build-eval"),
    )
    return registry


@pytest.fixture
def service(tmp_path: Path) -> Experiment:
    return Experiment(
        registry=_mock_registry(),
        sensor=ActivationSensor(expected_skill="build-eval"),
        store=FilesystemStore(tmp_path),
        mock=True,
        run_trial=make_run_trial(),
    )


# --- aggregate_readings ---


class TestAggregateReadings:
    def test_groups_by_probe_and_computes_score(self):
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
        assert must.passed is True
        assert not_r.score == 0.0
        assert not_r.passed is False

    def test_majority_vote(self):
        """3 pass + 2 fail = pass (score 0.6 > 0.5 threshold)."""
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
        assert results[0].passed is True

    def test_callback_invoked_per_probe(self):
        probes = {
            "m1": _probe("m1", "eval?", "must_trigger"),
            "m2": _probe("m2", "metrics?", "must_trigger"),
        }
        readings = [_r("m1", 0, True), _r("m2", 0, False)]

        completed = []
        aggregate_readings(readings, probes, on_probe_complete=completed.append)
        assert len(completed) == 2
        assert {r.probe_id for r in completed} == {"m1", "m2"}


# --- compute_metrics ---


class TestComputeMetrics:
    def test_all_passed(self):
        results = [
            ProbeResult(probe_id="m1", score=1.0, passed=True, trial_scores=(1.0, 1.0)),
            ProbeResult(probe_id="m2", score=0.8, passed=True, trial_scores=(0.8, 0.8)),
            ProbeResult(probe_id="n1", score=0.9, passed=True, trial_scores=(0.9, 0.9)),
        ]
        metrics = compute_metrics(results)
        assert metrics["pass_rate"] == 1.0
        assert metrics["mean_score"] == pytest.approx(0.9, abs=0.01)
        assert metrics["min_score"] == 0.8
        assert metrics["max_score"] == 1.0

    def test_all_failed(self):
        results = [
            ProbeResult(probe_id="m1", score=0.2, passed=False, trial_scores=(0.2, 0.2)),
            ProbeResult(probe_id="n1", score=0.1, passed=False, trial_scores=(0.1, 0.1)),
        ]
        metrics = compute_metrics(results)
        assert metrics["pass_rate"] == 0.0
        assert metrics["mean_score"] == pytest.approx(0.15, abs=0.01)
        assert metrics["min_score"] == 0.1
        assert metrics["max_score"] == 0.2

    def test_mixed_results(self):
        """pass_rate: 2/3, mean_score: mean of [1.0, 0.8, 0.2]."""
        results = [
            ProbeResult(probe_id="m1", score=1.0, passed=True),
            ProbeResult(probe_id="m2", score=0.8, passed=True),
            ProbeResult(probe_id="n1", score=0.2, passed=False),
        ]
        metrics = compute_metrics(results)
        assert metrics["pass_rate"] == pytest.approx(2 / 3, abs=0.01)
        assert metrics["mean_score"] == pytest.approx(2 / 3, abs=0.01)

    def test_empty_results(self):
        metrics = compute_metrics([])
        assert metrics["pass_rate"] == 0.0
        assert metrics["mean_score"] == 0.0
        assert metrics["min_score"] == 0.0
        assert metrics["max_score"] == 0.0


# --- Experiment integration ---


class TestExperiment:
    async def test_produces_results_with_metrics(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "How do I write evals?", "must_trigger"),
                _probe("must-002", "What metrics for LLM?", "must_trigger"),
                _probe("not-001", "Write a Python function", "should_not_trigger"),
            ),
            trials=5,
        )
        results = await service.run(exp)

        assert 0.0 <= results.pass_rate <= 1.0
        assert 0.0 <= results.mean_score <= 1.0
        assert results.min_score <= results.max_score
        assert len(results.probe_results) == 3

    async def test_status_derived_from_pass_rate(self, service: Experiment):
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
            trials=3,
        )
        results = await service.run(exp)
        assert results.status in ("excellent", "good", "needs_work", "poor")

    async def test_runs_all_probes_regardless_of_metadata(self, service: Experiment):
        """All probes run including non-standard expectation values."""
        exp = _config(
            probes=(
                _probe("must-001", "evals?", "must_trigger"),
                _probe("edge-001", "test my code?", "acceptable"),
                _probe("not-001", "factorial?", "should_not_trigger"),
            ),
        )
        results = await service.run(exp)
        probe_ids = [pr.probe_id for pr in results.probe_results]
        assert "edge-001" in probe_ids
        assert len(results.probe_results) == 3

    async def test_callback_fires_per_probe(self, service: Experiment):
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

    async def test_results_persisted_to_store(self, service: Experiment, tmp_path: Path):
        exp = _config(
            probes=(_probe("must-001", "evals?", "must_trigger"),),
            trials=2,
        )
        await service.run(exp)

        latest = tmp_path / "test-activation" / "results" / "summary-latest.json"
        assert latest.exists()

    async def test_provenance_populated(self, service: Experiment):
        """Results carry config_hash and ix_version for reproducibility."""
        exp = _config(
            probes=(_probe("must-001", "evals?", "must_trigger"),),
            trials=1,
        )
        results = await service.run(exp)

        assert results.config_hash != ""
        assert len(results.config_hash) == 16
        assert results.ix_version != ""
        assert results.run_timestamp is not None

    async def test_mock_agent_high_pass_rate(self, service: Experiment):
        """MockAgent always activates -> high pass rate on must_trigger probes."""
        exp = _config(
            probes=tuple(
                _probe(f"must-{i:03d}", f"eval question {i}", "must_trigger")
                for i in range(1, 11)
            )
            + tuple(
                _probe(f"not-{i:03d}", f"non-eval question {i}", "should_not_trigger")
                for i in range(1, 6)
            ),
            trials=5,
        )
        results = await service.run(exp)
        assert results.pass_rate >= 0.5
