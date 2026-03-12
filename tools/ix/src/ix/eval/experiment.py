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
from ix.eval.analysis import aggregate_readings, compute_metrics
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
    ) -> ExperimentResults:
        """Execute the experiment: inner DAG loop then post-loop aggregation."""
        active_subject = subject or Subject(name="default")

        # Override runtime to mock if --mock flag
        if self._mock:
            subject_config = dict(active_subject.config)
            subject_config["runtime"] = {"type": "mock"}
            active_subject = active_subject.model_copy(
                update={"config": subject_config},
            )

        readings: list[Reading] = []

        for probe in config.probes:
            for trial_idx in range(config.trials):
                trial_readings = await self._run_trial(
                    probe,
                    active_subject,
                    self._sensor,
                    self._registry,
                    trial_idx,
                )
                readings.extend(trial_readings)

        probe_map = {p.id: p for p in config.probes}
        probe_results = aggregate_readings(readings, probe_map, on_probe_complete)
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
            config_hash=config_hash,
            run_timestamp=datetime.now(UTC),
            ix_version=__version__,
        )
        self._store.save_summary(config.name, results)
        return results
