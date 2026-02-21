"""Composition root — wires adapters to ports via Matrix registry.

Config-driven. Each sensor has a typed Pydantic config model.
experiment.yaml sensor dict is validated through the model at creation time.
Typos and bad values fail fast with clear Pydantic errors.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from matrix import ComponentRegistry

from ix.adapters._out.filesystem_store import FilesystemStore
from ix.adapters._out.mock_runtime import MockAgent
from ix.config.settings import find_lab
from ix.domain.types import Probe
from ix.eval.models import ACCEPTABLE, MUST_TRIGGER
from ix.eval.sensors import (
    ActivationSensor,
    ActivationSensorConfig,
    FunctionTestSensor,
    FunctionTestSensorConfig,
)
from ix.eval.service import Experiment

if TYPE_CHECKING:
    from ix.domain.ports import Sensor
    from ix.eval.models import ExperimentConfig


# --- Sensor Registry ---

# Each entry: type_url → (SensorClass, ConfigModel)
# The factory validates config through the Pydantic model,
# then delegates to SensorClass.from_config(validated_config, probes).

from ix.eval.sensors_deepeval import DeepEvalSensor, DeepEvalSensorConfig

_SENSOR_TYPES: dict[str, tuple[type, type]] = {
    "ix.sensor.activation": (ActivationSensor, ActivationSensorConfig),
    "ix.sensor.function-test": (FunctionTestSensor, FunctionTestSensorConfig),
    "ix.sensor.deepeval": (DeepEvalSensor, DeepEvalSensorConfig),
}


def _make_factory(sensor_cls: type, config_cls: type):
    """Create a registry-compatible factory that validates config through Pydantic.

    Extracts infrastructure deps (judge) before Pydantic validation,
    then passes both config and deps to from_config.
    """

    def factory(*, probes: tuple[Probe, ...] = (), judge: Any = None, **raw_config: Any):
        config = config_cls.model_validate(raw_config)
        return sensor_cls.from_config(config, probes, judge=judge)

    return factory


_sensor_registry = ComponentRegistry()
for _type_url, (_cls, _config_cls) in _SENSOR_TYPES.items():
    _sensor_registry.register(_type_url, _make_factory(_cls, _config_cls))


def _build_one_sensor(sensor_config: dict, probes: tuple[Probe, ...]) -> Sensor:
    """Build a single sensor from its config dict via registry."""
    sensor_config = dict(sensor_config)
    sensor_type = sensor_config.get("type", "activation")
    type_url = f"ix.sensor.{sensor_type}"

    if type_url not in _sensor_registry:
        valid = sorted(t.removeprefix("ix.sensor.") for t in _sensor_registry.types())
        raise ValueError(f"Unknown sensor type: {sensor_type!r}. Valid types: {', '.join(valid)}")

    # Create judge agent for deepeval sensors when model is specified
    judge = None
    if sensor_type == "deepeval" and sensor_config.get("model"):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        judge = ClaudeAgent(model=sensor_config["model"], max_turns=1)

    return _sensor_registry.create(
        type_url,
        {**sensor_config, "probes": probes, "judge": judge},
    )


def create_sensor(experiment: ExperimentConfig) -> Sensor:
    """Build sensor(s) from experiment config via registry.

    Reads experiment.sensors (list of config dicts). Each is built
    independently via the registry. Multiple sensors are wrapped
    in a CompositeSensor — caller sees one Sensor either way.

    For deepeval sensors with a model specified, creates a judge Agent
    and routes DeepEval's LLM calls through Matrix's Agent protocol.
    """
    from ix.eval.sensors import CompositeSensor

    sensors = [_build_one_sensor(sc, experiment.probes) for sc in experiment.sensors]

    if len(sensors) == 1:
        return sensors[0]
    return CompositeSensor(sensors)


# --- Service Wiring ---


def create_service(
    mock: bool = False,
    skill: str = "build-eval",
    lab: Path | None = None,
    seed: int | None = None,
    experiment: ExperimentConfig | None = None,
) -> Experiment:
    """Wire up the experiment service with adapters.

    In mock mode, MockAgent produces structured AgentResponse directly.
    In live mode, ClaudeAgent extracts structured data from the SDK.
    No EvalRuntime shim needed — agents return AgentResponse natively.
    """
    if mock:
        expectations = _build_expectations(experiment) if experiment else {}
        agent = MockAgent(expected_skill=skill, seed=seed, expectations=expectations)
    else:
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent(max_turns=1)

    sensor = create_sensor(experiment) if experiment else ActivationSensor(expected_skill=skill)
    store = FilesystemStore(lab or find_lab())

    return Experiment(agent=agent, sensor=sensor, store=store)


def create_store(lab: Path | None = None) -> FilesystemStore:
    """Direct store access for CLI commands that only need persistence."""
    return FilesystemStore(lab or find_lab())


def _build_expectations(experiment: ExperimentConfig) -> dict[str, bool]:
    """Map probe prompts to activation expectations for mock runtime."""
    return {
        probe.prompt: probe.metadata.get("expectation") == MUST_TRIGGER
        for probe in experiment.probes
        if probe.metadata.get("expectation") != ACCEPTABLE
    }


__all__ = ["create_sensor", "create_service", "create_store"]
