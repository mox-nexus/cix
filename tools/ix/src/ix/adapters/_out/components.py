"""DAG components — ProbeNode, SubjectNode, TrialNode, SensorNode.

Four-node inner DAG topology:
  ProbeNode ──┐
              ├──▶ TrialNode ──▶ SensorNode
  SubjectNode ┘

Each is a Matrix Component: name, consumes, produces, async run(construct) → TypedStruct.
All resolve through ComponentRegistry — no special cases.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from matrix import Construct, TypedStruct

from ix.domain.ports import Sensor
from ix.domain.types import Probe, Reading, Subject, Trial

if TYPE_CHECKING:
    from matrix import ComponentRegistry

logger = logging.getLogger(__name__)


class ProbeNode:
    """Data node — provides one probe stimulus.

    Root node, no upstream dependencies. Returns the Probe as-is.
    One probe per Orchestrator run. The Experiment loop iterates probes.
    """

    name = "probe"
    consumes: frozenset[str] = frozenset()
    produces = "probe.stimulus"

    def __init__(self, probe: Probe) -> None:
        self._probe = probe

    async def run(self, construct: Construct) -> TypedStruct:
        return TypedStruct(type_url="probe.stimulus", value=self._probe)


class SubjectNode:
    """Data node — provides subject configuration.

    Root node, no upstream dependencies. Returns the Subject's config dict
    which includes system_prompt, runtime config, and any other identity.
    """

    name = "subject"
    consumes: frozenset[str] = frozenset()
    produces = "subject.config"

    def __init__(self, subject: Subject) -> None:
        self._subject = subject

    async def run(self, construct: Construct) -> TypedStruct:
        return TypedStruct(type_url="subject.config", value=self._subject.config)


class TrialNode:
    """Agent node — executes one probe against one subject.

    Reads probe stimulus and subject config from Construct.
    Creates an Agent via the ComponentRegistry from subject's runtime config.
    Runs the probe through the agent. Returns one Trial (observation or error).
    """

    name = "trial"
    consumes: frozenset[str] = frozenset({"probe.stimulus", "subject.config"})
    produces = "trial.observation"

    def __init__(
        self,
        registry: ComponentRegistry,
        trial_index: int = 0,
        experiment_cwd: str | None = None,
    ) -> None:
        self._registry = registry
        self._trial_index = trial_index
        self._experiment_cwd = experiment_cwd

    async def run(self, construct: Construct) -> TypedStruct:
        probe: Probe = construct["probe.stimulus"]
        subject_config: dict = construct["subject.config"]

        try:
            agent = self._build_agent(subject_config)
            response = await agent.run(probe.prompt)
            trial = Trial(
                probe_id=probe.id,
                trial_index=self._trial_index,
                response=response,
            )
        except Exception as e:
            logger.warning("Trial failed for probe %s: %s", probe.id, e)
            trial = Trial(
                probe_id=probe.id,
                trial_index=self._trial_index,
                error=str(e),
            )

        return TypedStruct(type_url="trial.observation", value=trial)

    def _build_agent(self, subject_config: dict):
        """Create an Agent from subject config via registry."""
        runtime_config = dict(subject_config.get("runtime", {}))
        runtime_type = runtime_config.pop("type", "anthropic")
        type_url = f"matrix.agent.{runtime_type}"

        # Inject experiment cwd for runtimes that support it (e.g. ClaudeAgent)
        if self._experiment_cwd and "cwd" not in runtime_config:
            runtime_config["cwd"] = self._experiment_cwd

        return self._registry.create(
            type_url,
            {
                "system_prompt": subject_config.get("system_prompt"),
                "trial_index": self._trial_index,
                **runtime_config,
            },
        )


class SensorNode:
    """Logic node — grades a trial via a Sensor, produces readings.

    Downstream of TrialNode. Reads one Trial from Construct, runs the
    Sensor protocol on it, returns readings.
    """

    name = "sensor"
    consumes: frozenset[str] = frozenset({"trial.observation"})
    produces = "sensor.reading"

    def __init__(self, sensor: Sensor) -> None:
        self._sensor = sensor

    async def run(self, construct: Construct) -> TypedStruct:
        trial: Trial = construct["trial.observation"]
        readings = self._measure(trial)
        return TypedStruct(type_url="sensor.reading", value=readings)

    def _measure(self, trial: Trial) -> list[Reading]:
        """Measure a trial. Error trials and sensor failures produce failed readings."""
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
            return self._sensor.measure(trial)
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
