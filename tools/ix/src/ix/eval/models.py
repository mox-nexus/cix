"""Eval domain models — frozen Pydantic value objects for evaluation.

Experiment definition and result types (TrialRecord, ProbeResult, ExperimentResults).
Agent response types (AgentResponse) live in Matrix.
"""

from typing import Any

from pydantic import BaseModel

from ix.domain.types import Probe, Reading, Subject

# --- Expectation Constants ---
# Single source of truth for probe expectation values.
# Used in analysis, service, and composition layers.

MUST_TRIGGER = "must_trigger"
SHOULD_NOT_TRIGGER = "should_not_trigger"
ACCEPTABLE = "acceptable"


class ExperimentConfig(BaseModel, frozen=True):
    """Experiment definition — loaded from YAML + MD files.

    sensors is a list of config dicts, each with a type field:
      sensors:
        - type: activation
          expected_skill: build-eval
        - type: deepeval
          metric: answer_relevancy

    Single sensor shorthand via `sensor` dict is still supported —
    normalized to a one-element `sensors` list by the model validator.
    """

    name: str
    description: str = ""
    subjects: tuple[Subject, ...] = ()
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
    reading: Reading | None = None


class ProbeResult(BaseModel, frozen=True):
    """Aggregated result across all trials for one probe."""

    probe_id: str
    expectation: str
    score: float
    correct: bool
    trials: tuple[TrialRecord, ...] = ()


class ExperimentResults(BaseModel, frozen=True):
    """Complete results for one experiment run.

    Metrics and interpretation are flat — no nested sub-models.
    """

    experiment_name: str
    probe_results: tuple[ProbeResult, ...] = ()

    # Classification metrics (from compute_metrics)
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0

    # Interpretation (from interpret)
    status: str = "pending"
    issues: tuple[str, ...] = ()
    suggestions: tuple[str, ...] = ()
