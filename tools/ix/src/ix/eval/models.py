"""Eval domain models — frozen Pydantic value objects for evaluation.

Experiment definition and result types.
Agent response types (AgentResponse) live in Matrix.
"""

from typing import Any

from pydantic import BaseModel

from ix.domain.types import Probe, Subject

# --- Expectation Constants ---
# Legacy: used by activation sensor experiments.
MUST_TRIGGER = "must_trigger"
SHOULD_NOT_TRIGGER = "should_not_trigger"
ACCEPTABLE = "acceptable"


class ExperimentConfig(BaseModel, frozen=True):
    """Experiment definition — loaded from YAML + MD files.

    agent config specifies the runtime:
      agent:
        model: sonnet
        max_tokens: 4096

    sensors is a list of config dicts, each with a type field:
      sensors:
        - type: activation
          expected_skill: build-eval
        - type: function-test

    Single sensor shorthand via `sensor` dict is still supported —
    normalized to a one-element `sensors` list by the model validator.
    """

    name: str
    description: str = ""
    subjects: tuple[Subject, ...] = ()
    agent: dict = {}
    sensor: dict = {}
    sensors: tuple[dict, ...] = ()
    trials: int = 5
    probes: tuple[Probe, ...] = ()

    def __init__(self, **data: Any) -> None:
        # Normalize: sensor (single) → sensors (list)
        if not data.get("sensors") and data.get("sensor"):
            data["sensors"] = (data["sensor"],)
        elif not data.get("sensors") and not data.get("sensor"):
            data["sensors"] = ({"type": "activation"},)
        super().__init__(**data)


class TrialRecord(BaseModel, frozen=True):
    """One trial of one probe: observation + sensor reading."""

    probe_id: str
    trial: int
    observation: Any = None
    reading: Any = None


class ProbeResult(BaseModel, frozen=True):
    """Aggregated result across all trials for one probe."""

    probe_id: str
    score: float
    passed: bool
    trial_scores: tuple[float, ...] = ()
    details: tuple[str, ...] = ()


class ExperimentResults(BaseModel, frozen=True):
    """Complete results for one experiment run."""

    experiment_name: str
    probe_results: tuple[ProbeResult, ...] = ()

    # Summary metrics
    mean_score: float = 0.0
    std_dev: float = 0.0
    min_score: float = 0.0
    max_score: float = 0.0

    # Interpretation
    status: str = "pending"
    issues: tuple[str, ...] = ()
    suggestions: tuple[str, ...] = ()
