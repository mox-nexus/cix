"""ix core types — domain-agnostic value objects.

These types express any experiment: eval, benchmark, load test.
No eval-specific concepts leak here.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Subject(BaseModel, frozen=True):
    """A Subject Under Test — one variant being compared."""

    name: str
    description: str = ""
    config: dict = {}


class Probe(BaseModel, frozen=True):
    """A task prompt — the stimulus sent to a Subject.

    id + prompt are universal. Everything else (expectation, test_cases,
    repo, entry_point) goes in metadata — the sensor/scorer reads what it needs.
    """

    id: str
    prompt: str
    metadata: dict = {}


class Trial(BaseModel, frozen=True):
    """One execution of a probe against a subject.

    Pipeline data: pairs probe identity with the response (or error).
    The sensor gets trial.response. The scorer uses trial.probe_id
    to look up ground truth.
    """

    probe_id: str
    trial_index: int
    response: Any = None
    error: str | None = None


class Reading(BaseModel, frozen=True):
    """Result of a sensor measuring a trial.

    Sensors produce readings, like instruments. Each reading traces
    back to its trial via probe_id + trial_index, enabling joins
    across the Construct's artifact ledger.
    """

    sensor_name: str
    probe_id: str
    trial_index: int
    passed: bool
    score: float | None = None
    metrics: dict = {}
    details: str = ""
