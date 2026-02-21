"""Post-DAG analysis — aggregate, metrics, interpret.

Pure functions operating on Reading types.
Groups by probe_id from the DAG artifacts.
Scoring (comparing readings against ground truth) happens here.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from ix.domain.types import Probe, Reading
from ix.eval.models import MUST_TRIGGER, SHOULD_NOT_TRIGGER, ProbeResult


def aggregate_readings(
    readings: list[Reading],
    probes: dict[str, Probe],
    on_probe_complete: Callable[[ProbeResult], None] | None = None,
) -> list[ProbeResult]:
    """Group readings by probe_id, majority vote across trials.

    Scoring: compares sensor readings against probe ground truth
    (probe.metadata["expectation"]).

    Readings already carry probe_id + trial_index — no join needed.
    """
    by_probe: dict[str, list[Reading]] = defaultdict(list)
    for reading in readings:
        by_probe[reading.probe_id].append(reading)

    probe_results: list[ProbeResult] = []
    for probe_id, probe_readings in by_probe.items():
        score = sum(1 for r in probe_readings if r.passed) / len(probe_readings)
        activated = score > 0.5
        probe = probes[probe_id]
        expectation = probe.metadata.get("expectation", MUST_TRIGGER)
        correct = activated == (expectation == MUST_TRIGGER)

        probe_result = ProbeResult(
            probe_id=probe_id,
            expectation=expectation,
            score=score,
            correct=correct,
        )
        probe_results.append(probe_result)

        if on_probe_complete:
            on_probe_complete(probe_result)

    return probe_results


def compute_metrics(results: list[ProbeResult]) -> dict:
    """Compute confusion matrix and F1.

    Returns a dict suitable for spreading into ExperimentResults(**metrics).
    """
    must = [r for r in results if r.expectation == MUST_TRIGGER]
    should_not = [r for r in results if r.expectation == SHOULD_NOT_TRIGGER]

    tp = sum(1 for r in must if r.score > 0.5)
    fn = sum(1 for r in must if r.score <= 0.5)
    fp = sum(1 for r in should_not if r.score > 0.5)
    tn = sum(1 for r in should_not if r.score <= 0.5)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return dict(
        precision=precision,
        recall=recall,
        f1=f1,
        tp=tp,
        fp=fp,
        fn=fn,
        tn=tn,
    )


def interpret(metrics: dict) -> dict:
    """Interpret metrics and suggest tuning.

    Returns a dict suitable for spreading into ExperimentResults(**interp).
    """
    issues: list[str] = []
    suggestions: list[str] = []

    if metrics["recall"] < 0.8:
        issues.append("Low recall - skill not activating enough")
        suggestions.append("Broaden skill description keywords")
        suggestions.append("Add more trigger phrases to description")

    if metrics["precision"] < 0.8:
        issues.append("Low precision - skill activating too much")
        suggestions.append("Tighten skill description to be more specific")
        suggestions.append("Add exclusion phrases")

    if metrics["f1"] >= 0.85:
        status = "excellent"
    elif metrics["f1"] >= 0.70:
        status = "good"
    elif metrics["f1"] >= 0.50:
        status = "needs_work"
    else:
        status = "poor"

    return dict(
        status=status,
        issues=tuple(issues),
        suggestions=tuple(suggestions),
    )
