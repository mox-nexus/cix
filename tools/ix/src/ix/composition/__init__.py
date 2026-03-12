"""Composition root — unified registry for all component types.

One registry, one pattern: type_url → factory → Component.
Sensors, agents, probes, trials — all resolve the same way.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from matrix import ComponentRegistry
from matrix import Orchestrator as _Orchestrator

from ix.adapters._out.components import ProbeNode, SensorNode, SubjectNode, TrialNode
from ix.adapters._out.filesystem_store import FilesystemStore
from ix.adapters._out.mock_runtime import MockAgent
from ix.config.settings import find_lab
from ix.domain.ports import Sensor as _Sensor
from ix.domain.types import Probe, Reading, Subject
from ix.eval.experiment import Experiment
from ix.eval.models import ACCEPTABLE, MUST_TRIGGER
from ix.eval.sensors import (
    ActivationSensor,
    ActivationSensorConfig,
    FunctionTestSensor,
    FunctionTestSensorConfig,
    OutcomeSensor,
    OutcomeSensorConfig,
    ToolUsageSensor,
    ToolUsageSensorConfig,
)
from ix.eval.sensors_deepeval import DeepEvalSensor, DeepEvalSensorConfig

if TYPE_CHECKING:
    from ix.domain.ports import Sensor
    from ix.eval.models import ExperimentConfig


# --- Sensor Types ---

_SENSOR_TYPES: dict[str, tuple[type, type]] = {
    "ix.sensor.activation": (ActivationSensor, ActivationSensorConfig),
    "ix.sensor.function-test": (FunctionTestSensor, FunctionTestSensorConfig),
    "ix.sensor.deepeval": (DeepEvalSensor, DeepEvalSensorConfig),
    "ix.sensor.tool-usage": (ToolUsageSensor, ToolUsageSensorConfig),
    "ix.sensor.outcome": (OutcomeSensor, OutcomeSensorConfig),
}


def _make_sensor_factory(sensor_cls: type, config_cls: type):
    """Registry-compatible factory that validates config through Pydantic.

    Passes registry to from_config — each sensor resolves its own
    dependencies (e.g. DeepEval creates its judge agent from the registry).
    """

    def factory(*, probes: tuple[Probe, ...] = (), registry: Any = None, **raw_config: Any):
        config = config_cls.model_validate(raw_config)
        return sensor_cls.from_config(config, probes, registry=registry)

    return factory


# --- Agent Factories ---


def _anthropic_factory(*, system_prompt: str | None = None, **kw: Any):
    """Factory for AnthropicAgent — single-turn API calls."""
    from matrix.adapters._out.runtime.anthropic_agent import AnthropicAgent

    kw.pop("type", None)
    kw.pop("trial_index", None)
    return AnthropicAgent(system_prompt=system_prompt, **kw)


def _claude_factory(*, system_prompt: str | None = None, **kw: Any):
    """Factory for ClaudeAgent — Agent SDK, multi-turn."""
    from matrix.adapters._out.runtime.claude import ClaudeAgent

    kw.pop("type", None)
    kw.pop("trial_index", None)
    return ClaudeAgent(system_prompt=system_prompt, **kw)


def _make_mock_factory(
    expected_skill: str = "build-eval",
    base_seed: int | None = None,
    expectations: dict[str, bool] | None = None,
):
    """Build a mock factory with captured test config.

    Derives per-trial seed from (base_seed, trial_index) so each trial
    is deterministic but independent.
    """

    def factory(*, trial_index: int = 0, **kw: Any):
        effective_seed = (base_seed * 1000 + trial_index) if base_seed is not None else None
        return MockAgent(
            expected_skill=expected_skill,
            seed=effective_seed,
            expectations=expectations or {},
        )

    return factory


# --- Unified Registry ---


def build_registry(
    *,
    mock: bool = False,
    skill: str = "build-eval",
    seed: int | None = None,
    experiment: ExperimentConfig | None = None,
) -> ComponentRegistry:
    """Build the unified ComponentRegistry — sensors + agent runtimes.

    All component types resolve through this single registry.
    Mock config is captured in the mock factory closure.
    """
    registry = ComponentRegistry()

    # Sensors
    for type_url, (cls, config_cls) in _SENSOR_TYPES.items():
        registry.register(type_url, _make_sensor_factory(cls, config_cls))

    # Agent runtimes
    registry.register("matrix.agent.anthropic", _anthropic_factory)
    registry.register("matrix.agent.claude", _claude_factory)

    expectations = _build_expectations(experiment) if experiment and mock else {}
    registry.register(
        "matrix.agent.mock",
        _make_mock_factory(
            expected_skill=skill,
            base_seed=seed,
            expectations=expectations,
        ),
    )

    return registry


# --- Sensor Wiring ---


def _build_one_sensor(
    sensor_config: dict,
    probes: tuple[Probe, ...],
    registry: ComponentRegistry,
    experiment_cwd: str | None = None,
) -> Sensor:
    """Build a single sensor from its config dict via registry."""
    sensor_config = dict(sensor_config)
    sensor_type = sensor_config.get("type", "activation")
    type_url = f"ix.sensor.{sensor_type}"

    # Resolve graders_module path relative to experiment directory
    if "graders_module" in sensor_config and experiment_cwd:
        graders_path = Path(experiment_cwd) / sensor_config["graders_module"]
        sensor_config["graders_module"] = str(graders_path.resolve())

    if type_url not in registry:
        valid = sorted(
            t.removeprefix("ix.sensor.") for t in registry.types() if t.startswith("ix.sensor.")
        )
        raise ValueError(f"Unknown sensor type: {sensor_type!r}. Valid types: {', '.join(valid)}")

    return registry.create(
        type_url,
        {**sensor_config, "probes": probes, "registry": registry},
    )


def create_sensor(
    experiment: ExperimentConfig,
    registry: ComponentRegistry,
    experiment_cwd: str | None = None,
) -> Sensor:
    """Build sensor(s) from experiment config via registry.

    Multiple sensors are wrapped in CompositeSensor.
    """
    from ix.eval.sensors import CompositeSensor

    sensors = [
        _build_one_sensor(sc, experiment.probes, registry, experiment_cwd)
        for sc in experiment.sensors
    ]

    if len(sensors) == 1:
        return sensors[0]
    return CompositeSensor(sensors)


# --- Trial Runner ---


def make_run_trial(experiment_cwd: str | None = None):
    """Build the default trial runner using concrete DAG Components.

    This is the composition root's job — wiring concrete implementations.
    The service layer only knows the callable signature, not the node classes.
    """

    async def _run(
        probe: Probe,
        subject: Subject,
        sensor: _Sensor,
        registry: ComponentRegistry,
        trial_index: int,
    ) -> list[Reading]:
        orchestrator = _Orchestrator(
            [
                ProbeNode(probe),
                SubjectNode(subject),
                TrialNode(
                    registry=registry, trial_index=trial_index, experiment_cwd=experiment_cwd
                ),
                SensorNode(sensor=sensor),
            ]
        )
        construct = await orchestrator.run()
        return construct["sensor.reading"]

    return _run


# --- Service Wiring ---


def create_service(
    mock: bool = False,
    skill: str = "build-eval",
    lab: Path | None = None,
    seed: int | None = None,
    experiment: ExperimentConfig | None = None,
    experiment_cwd: str | None = None,
) -> Experiment:
    """Wire up the experiment service with unified registry.

    Everything resolves through one ComponentRegistry.
    --mock overrides subject runtime to use MockAgent.
    """
    registry = build_registry(
        mock=mock,
        skill=skill,
        seed=seed,
        experiment=experiment,
    )
    sensor = (
        create_sensor(experiment, registry, experiment_cwd)
        if experiment
        else ActivationSensor(expected_skill=skill)
    )
    store = FilesystemStore(lab or find_lab())

    return Experiment(
        registry=registry,
        sensor=sensor,
        store=store,
        mock=mock,
        run_trial=make_run_trial(experiment_cwd=experiment_cwd),
    )


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


__all__ = ["build_registry", "create_sensor", "create_service", "create_store", "make_run_trial"]
