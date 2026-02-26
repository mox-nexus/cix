"""Post-DAG analysis — aggregate, metrics, interpret.

Pure functions operating on Reading types.
Generic — works with any sensor. The Reading is the contract.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from collections.abc import Callable

from ix.domain.types import Probe, Reading
from ix.eval.models import ProbeResult


def aggregate_readings(
    readings: list[Reading],
    probes: dict[str, Probe],
    on_probe_complete: Callable[[ProbeResult], None] | None = None,
) -> list[ProbeResult]:
    """Group readings by probe_id, average scores across trials.

    Sensor-agnostic. Uses Reading.score (continuous) when available,
    falls back to Reading.passed (binary).
    """
    by_probe: dict[str, list[Reading]] = defaultdict(list)
    for reading in readings:
        by_probe[reading.probe_id].append(reading)

    probe_results: list[ProbeResult] = []
    for probe_id, probe_readings in by_probe.items():
        if any(r.score is not None for r in probe_readings):
            score = sum(r.score for r in probe_readings if r.score is not None) / len(
                probe_readings
            )
        else:
            score = sum(1 for r in probe_readings if r.passed) / len(probe_readings)

        probe_result = ProbeResult(
            probe_id=probe_id,
            score=score,
            passed=score > 0.5,
            trial_scores=tuple(r.score or (1.0 if r.passed else 0.0) for r in probe_readings),
            details=tuple(r.details for r in probe_readings if r.details),
        )
        probe_results.append(probe_result)

        if on_probe_complete:
            on_probe_complete(probe_result)

    return probe_results


def compute_metrics(results: list[ProbeResult]) -> dict:
    """Compute summary metrics from probe results.

    Generic — computes mean score, std dev, min/max.
    """
    if not results:
        return {"mean_score": 0.0, "std_dev": 0.0, "min_score": 0.0, "max_score": 0.0}

    scores = [r.score for r in results]
    all_trial_scores = [s for r in results for s in r.trial_scores]

    return {
        "mean_score": statistics.mean(scores),
        "std_dev": statistics.stdev(all_trial_scores) if len(all_trial_scores) > 1 else 0.0,
        "min_score": min(all_trial_scores) if all_trial_scores else 0.0,
        "max_score": max(all_trial_scores) if all_trial_scores else 0.0,
    }


def interpret(metrics: dict) -> dict:
    """Interpret metrics."""
    mean = metrics.get("mean_score", 0.0)
    std = metrics.get("std_dev", 0.0)

    issues: list[str] = []
    suggestions: list[str] = []

    if mean < 0.10:
        issues.append(f"Floor effect — mean={mean:.1%}, task may be too hard")
    elif mean > 0.90:
        issues.append(f"Ceiling effect — mean={mean:.1%}, task may be too easy")

    if std > 0.25:
        issues.append(f"High variance — std={std:.3f}, results may be noisy")
        suggestions.append("Increase trial count or simplify task")

    if mean >= 0.85:
        status = "excellent"
    elif mean >= 0.70:
        status = "good"
    elif mean >= 0.50:
        status = "needs_work"
    else:
        status = "poor"

    return {
        "status": status,
        "issues": tuple(issues),
        "suggestions": tuple(suggestions),
    }
