"""Phase 1 noise floor analysis for CEP-001 task-based probes.

Reads the latest results JSON and checks rollback triggers:
  - Mean = 0.0 on all trials (floor — task impossible)
  - Mean = 1.0 on all trials (ceiling — task trivial)
  - SD > 0.35 (too noisy for N=5 discrimination)
  - YAML extraction fails > 50% of trials (inferred from score=0.0 trials)

Usage:
    uv run python ci-lab/cep-001/analyze_phase1.py
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


def analyze(results_path: Path) -> None:
    data = json.loads(results_path.read_text())

    subject = data.get("subject", "unknown")
    print(f"Subject: {subject}")
    print(f"Experiment: {data['experiment_name']}")
    print(f"Overall: mean={data['mean_score']:.1%}, pass_rate={data['pass_rate']:.1%}")
    print(f"Range: [{data['min_score']:.1%}, {data['max_score']:.1%}]")
    print()

    triggers = []

    for pr in data["probe_results"]:
        probe_id = pr["probe_id"]
        scores = pr["trial_scores"]
        n = len(scores)
        mean = statistics.mean(scores)
        sd = statistics.stdev(scores) if n > 1 else 0.0
        lo, hi = min(scores), max(scores)
        zeros = sum(1 for s in scores if s == 0.0)

        print(f"  {probe_id}: mean={mean:.3f}, sd={sd:.3f}, range=[{lo:.2f}, {hi:.2f}], n={n}, zeros={zeros}")

        # Check rollback triggers
        probe_triggers = []
        if mean == 0.0:
            probe_triggers.append("FLOOR (mean=0.0 — task impossible)")
        if mean == 1.0 and sd == 0.0:
            probe_triggers.append("CEILING (mean=1.0 — task trivial)")
        if sd > 0.35:
            probe_triggers.append(f"NOISY (sd={sd:.3f} > 0.35)")
        if zeros / n > 0.5:
            probe_triggers.append(f"YAML_FAIL ({zeros}/{n} = {zeros/n:.0%} zero scores)")

        if probe_triggers:
            for t in probe_triggers:
                print(f"    ⚠ ROLLBACK: {t}")
            triggers.append((probe_id, probe_triggers))

    print()
    print("=" * 60)
    n_triggered = len(triggers)
    if n_triggered == 0:
        print("PASS: 0/6 probes triggered rollback. Proceed to Phase 2.")
    elif n_triggered <= 2:
        print(f"PARTIAL: {n_triggered}/6 probes triggered rollback. Redesign those probes.")
        for pid, ts in triggers:
            for t in ts:
                print(f"  {pid}: {t}")
    else:
        print(f"FAIL: {n_triggered}/6 probes triggered rollback. Fundamental rethink needed.")
        for pid, ts in triggers:
            for t in ts:
                print(f"  {pid}: {t}")


if __name__ == "__main__":
    results_dir = Path("ci-lab/cep-001/results")
    latest = results_dir / "summary-latest.json"

    if not latest.exists():
        # Try from argument
        if len(sys.argv) > 1:
            latest = Path(sys.argv[1])
        else:
            print(f"No results found at {latest}")
            sys.exit(1)

    analyze(latest)
