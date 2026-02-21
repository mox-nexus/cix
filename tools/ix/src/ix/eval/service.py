"""Experiment — DAG execution + post-DAG aggregation.

DAG:      TrialNode (execute + sense)
Post-DAG: aggregate_readings, compute_metrics, interpret
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Protocol

from matrix import Orchestrator

from ix.adapters._out.components import TrialNode
from ix.domain.ports import ExperimentRuntime, Sensor
from ix.domain.types import Reading
from ix.eval.analysis import aggregate_readings, compute_metrics, interpret
from ix.eval.models import (
    ACCEPTABLE,
    ExperimentConfig,
    ExperimentResults,
    ProbeResult,
    TrialRecord,
)


class Storage(Protocol):
    """Persistence boundary for experiments and eval results."""

    def load_experiment(self, path: Path) -> ExperimentConfig: ...

    def list_experiments(self, base: Path) -> list[Path]: ...

    def append_result(self, experiment_name: str, result: TrialRecord) -> None: ...

    def save_summary(self, experiment_name: str, results: ExperimentResults) -> Path: ...


class Experiment:
    """An experiment you run.

    Constructed with infrastructure (agent, sensor, store).
    The agent already knows its identity (system prompt, config).
    Call run(config) to execute.
    """

    def __init__(
        self,
        agent: ExperimentRuntime,
        sensor: Sensor,
        store: Storage,
    ) -> None:
        self._agent = agent
        self._sensor = sensor
        self._store = store

    async def run(
        self,
        config: ExperimentConfig,
        on_probe_complete: Callable[[ProbeResult], None] | None = None,
    ) -> ExperimentResults:
        """Execute the experiment: DAG phase then post-DAG aggregation."""
        # Filter probes — skip "acceptable" expectations (scoring concern)
        active_probes = [p for p in config.probes if p.metadata.get("expectation") != ACCEPTABLE]

        trial_node = TrialNode(
            probes=active_probes,
            runtime=self._agent,
            sensor=self._sensor,
            trials=config.trials,
        )

        orchestrator = Orchestrator([trial_node])
        construct = await orchestrator.run()

        readings: list[Reading] = construct["experiment.readings"]

        probe_map = {p.id: p for p in active_probes}
        probe_results = aggregate_readings(readings, probe_map, on_probe_complete)
        metrics = compute_metrics(probe_results)
        interp = interpret(metrics)

        results = ExperimentResults(
            experiment_name=config.name,
            probe_results=tuple(probe_results),
            **metrics,
            **interp,
        )
        self._store.save_summary(config.name, results)
        return results
