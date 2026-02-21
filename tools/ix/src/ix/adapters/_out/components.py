"""DAG components — TrialNode.

Driven adapter: bridges ix domain protocols (ExperimentRuntime, Sensor)
to Matrix's Component protocol and Construct store.

Sensing is embedded in execution — each trial is immediately measured.
The component returns list[Reading], not raw trials.
"""

from __future__ import annotations

import logging

from matrix import Construct

from ix.domain.ports import ExperimentRuntime, Sensor
from ix.domain.types import Probe, Reading, Trial

logger = logging.getLogger(__name__)


class TrialNode:
    """Executes probes via an Agent, senses each response immediately.

    The agent already knows its identity (system prompt, config).
    TrialNode sends probe.prompt, collects responses, and runs the
    sensor inline — no separate SensorNode needed.

    requires: frozenset() — root node
    provides: "experiment.readings"
    """

    name = "trial"
    requires: frozenset[str] = frozenset()
    provides = "experiment.readings"

    def __init__(
        self,
        probes: list[Probe],
        runtime: ExperimentRuntime,
        sensor: Sensor,
        trials: int = 1,
    ) -> None:
        self._probes = probes
        self._runtime = runtime
        self._sensor = sensor
        self._trials = trials

    async def run(self, construct: Construct) -> list[Reading]:
        """Fire all probes across all trials, sense each immediately."""
        readings: list[Reading] = []

        for trial_idx in range(self._trials):
            for probe in self._probes:
                trial = await self._execute(probe, trial_idx)
                readings.extend(self._sense(trial))

        return readings

    async def _execute(self, probe: Probe, trial_idx: int) -> Trial:
        """Run one probe, return Trial (success or error)."""
        try:
            response = await self._runtime.run(probe.prompt)
            return Trial(
                probe_id=probe.id,
                trial_index=trial_idx,
                response=response,
            )
        except Exception as e:
            return Trial(
                probe_id=probe.id,
                trial_index=trial_idx,
                error=str(e),
            )

    def _sense(self, trial: Trial) -> list[Reading]:
        """Measure a trial via the sensor. Error trials produce failed readings."""
        if trial.error:
            return [
                Reading(
                    sensor_name=self._sensor.name,
                    probe_id=trial.probe_id,
                    trial_index=trial.trial_index,
                    passed=False,
                    score=0.0,
                    details=f"error: {trial.error}",
                )
            ]

        try:
            return self._sensor.sense(trial)
        except Exception as e:
            logger.warning(
                "Sensor %s failed on trial %s/%d: %s",
                self._sensor.name,
                trial.probe_id,
                trial.trial_index,
                e,
            )
            return [
                Reading(
                    sensor_name=self._sensor.name,
                    probe_id=trial.probe_id,
                    trial_index=trial.trial_index,
                    passed=False,
                    score=0.0,
                    details=f"sensor error: {e}",
                )
            ]
