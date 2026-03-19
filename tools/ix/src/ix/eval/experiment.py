"""Experiment — inner DAG loop + post-loop aggregation.

Inner DAG (per probe × trial):
  ProbeNode → TrialNode ← SubjectNode
                 ↓
             SensorNode

Experiment loops over probes × trials, runs the inner DAG each time.
Post-loop: aggregate all readings → metrics.

NOTE: This module does NOT import concrete Components (ProbeNode, TrialNode, etc.).
Node construction is injected via `run_trial` from the composition root.
"""

from __future__ import annotations

import hashlib
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from matrix import ComponentRegistry

from ix import __version__
from ix.domain.ports import Sensor
from ix.domain.types import Probe, Reading, Subject
from ix.eval.analysis import (
    aggregate_readings,
    build_confusion_matrix,
    compute_metrics,
    compute_noise_floor,
)
from ix.eval.models import (
    ExperimentConfig,
    ExperimentResults,
    ProbeResult,
    TrialRecord,
)

# Callable that runs one probe×trial iteration, returns readings.
# The composition root provides this — it knows the concrete Components.
RunTrial = Callable[
    [Probe, Subject, "Sensor", ComponentRegistry, int],
    Awaitable[list[Reading]],
]


class Storage(Protocol):
    """Persistence boundary for experiments and eval results."""

    def load_experiment(self, path: Path) -> ExperimentConfig: ...

    def list_experiments(self, base: Path) -> list[Path]: ...

    def append_result(self, experiment_name: str, result: TrialRecord) -> None: ...

    def save_summary(self, experiment_name: str, results: ExperimentResults) -> Path: ...


class Experiment:
    """An experiment you run.

    Constructed with infrastructure (registry, sensor, store).
    The registry resolves agent runtimes from subject config.
    Call run(config, subject) to execute.
    """

    def __init__(
        self,
        registry: ComponentRegistry,
        sensor: Sensor,
        store: Storage,
        mock: bool = False,
        *,
        run_trial: RunTrial,
    ) -> None:
        self._registry = registry
        self._sensor = sensor
        self._store = store
        self._mock = mock
        self._run_trial = run_trial

    async def run(
        self,
        config: ExperimentConfig,
        subject: Subject | None = None,
        on_probe_complete: Callable[[ProbeResult], None] | None = None,
        on_run_complete: Callable[[int, float], None] | None = None,
    ) -> ExperimentResults:
        """Execute the experiment: inner DAG loop then post-loop aggregation.

        When config.repeats > 1, runs the full probe×trial matrix N times
        and computes noise floor (sd of pass_rate across runs) + confusion matrix.
        """
        active_subject = subject or Subject(name="default")

        # Override runtime to mock if --mock flag
        if self._mock:
            subject_config = dict(active_subject.config)
            subject_config["runtime"] = {"type": "mock"}
            active_subject = active_subject.model_copy(
                update={"config": subject_config},
            )

        all_readings: list[Reading] = []
        per_run_pass_rates: list[float] = []

        for run_idx in range(config.repeats):
            run_readings: list[Reading] = []

            for probe in config.probes:
                for trial_idx in range(config.trials):
                    trial_readings = await self._run_trial(
                        probe,
                        active_subject,
                        self._sensor,
                        self._registry,
                        trial_idx,
                    )
                    run_readings.extend(trial_readings)

            all_readings.extend(run_readings)

            # Per-run metrics for noise floor
            probe_map = {p.id: p for p in config.probes}
            run_probe_results = aggregate_readings(run_readings, probe_map)
            run_metrics = compute_metrics(run_probe_results)
            per_run_pass_rates.append(run_metrics["pass_rate"])

            if on_run_complete:
                on_run_complete(run_idx, run_metrics["pass_rate"])

        # Final aggregation across all runs
        probe_map = {p.id: p for p in config.probes}
        callback = on_probe_complete if config.repeats == 1 else None
        probe_results = aggregate_readings(all_readings, probe_map, callback)
        metrics = compute_metrics(probe_results)

        config_json = config.model_dump_json(exclude={"probes"})
        config_hash = hashlib.sha256(config_json.encode()).hexdigest()[:16]

        results = ExperimentResults(
            experiment_name=config.name,
            subject=active_subject.name,
            probe_results=tuple(probe_results),
            pass_rate=metrics["pass_rate"],
            mean_score=metrics["mean_score"],
            min_score=metrics["min_score"],
            max_score=metrics["max_score"],
            repeats=config.repeats,
            per_run_pass_rates=tuple(per_run_pass_rates),
            noise_floor_sd=compute_noise_floor(per_run_pass_rates),
            confusion_matrix=build_confusion_matrix(all_readings),
            config_hash=config_hash,
            run_timestamp=datetime.now(UTC),
            ix_version=__version__,
        )
        self._store.save_summary(config.name, results)
        return results
