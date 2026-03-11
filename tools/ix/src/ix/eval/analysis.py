"""Post-DAG analysis — aggregate readings into results.

Pure functions. The sensor is the grader — passed=True means correct.
Analysis just counts.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from ix.domain.types import Probe, Reading
from ix.eval.models import ProbeResult


def aggregate_readings(
    readings: list[Reading],
    probes: dict[str, Probe],
    on_probe_complete: Callable[[ProbeResult], None] | None = None,
) -> list[ProbeResult]:
    """Group readings by probe_id, compute pass rate per probe."""
    by_probe: dict[str, list[Reading]] = defaultdict(list)
    for reading in readings:
        by_probe[reading.probe_id].append(reading)

    probe_results: list[ProbeResult] = []
    for probe_id, probe_readings in by_probe.items():
        trial_scores = tuple(r.score for r in probe_readings)
        score = sum(trial_scores) / len(trial_scores) if trial_scores else 0.0

        probe_result = ProbeResult(
            probe_id=probe_id,
            score=score,
            passed=score > 0.5,
            trial_scores=trial_scores,
            details=tuple(r.details for r in probe_readings if r.details),
        )
        probe_results.append(probe_result)

        if on_probe_complete:
            on_probe_complete(probe_result)

    return probe_results


def compute_metrics(results: list[ProbeResult]) -> dict:
    """Compute pass rate and mean score across all probes.

    pass_rate: fraction of probes that passed (binary).
    mean_score: mean of continuous per-probe scores (preserves resolution).
    """
    if not results:
        return {"pass_rate": 0.0, "mean_score": 0.0, "min_score": 0.0, "max_score": 0.0}

    scores = [r.score for r in results]
    n_passed = sum(1 for r in results if r.passed)

    return {
        "pass_rate": n_passed / len(results),
        "mean_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
    }


