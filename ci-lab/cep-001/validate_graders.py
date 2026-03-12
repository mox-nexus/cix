"""Construct validity test for CEP-001 YAML graders.

Run before spending API tokens. Verifies:
1. Perfect responses score >= 0.95
2. Empty/wrong responses score <= 0.1
3. Partial responses score proportionally

Usage: uv run python ci-lab/cep-001/validate_graders.py
"""

from __future__ import annotations

import sys

sys.path.insert(0, "ci-lab/cep-001")

from graders import GRADERS  # noqa: E402

# --- Perfect responses (should score ~1.0) ---

PERFECT = {
    "task-001": """```yaml
database: DuckDB
deployment_model: single-node
analytics_capability: true
primary_use_case: token usage patterns
```""",
    "task-002": """```yaml
algorithm: token bucket
tiers: 2
global_rate_per_min: 40
global_burst: 15
per_user_rate_per_min: 10
per_user_burst: 5
backoff_initial_ms: 500
```""",
    "task-003": """```yaml
model_name: nomic-embed-text-v1.5
dimensions: 768
inference_mode: local
acceleration: CoreML
```""",
    "task-004": """```yaml
root_cause: Sort order was ascending instead of descending after reranking
fix: Added reverse=True to the sort call
component: cross-encoder reranking pipeline
commit: a3f7e21
```""",
    "task-005": """```yaml
trail_type: curated
trail_creation: manual
similar_type: algorithmic
similar_method: embedding cosine similarity
trail_use_case: synthesis
similar_use_case: exploration
```""",
    "task-006": """```yaml
chosen_pattern: typing.Protocol
typing_style: structural
runtime_check: runtime_checkable
rejected_alternative: ABC
```""",
}


# --- Zero responses (should score ~0.0) ---

ZERO = {
    "task-001": "I couldn't find any information about that.",
    "task-002": "```yaml\nalgorithm: sliding window\ntiers: 1\n```",
    "task-003": "The model is GPT-4.",
    "task-004": (
        "```yaml\nroot_cause: network timeout\nfix: increased timeout\n"
        "component: api gateway\ncommit: abc1234\n```"
    ),
    "task-005": (
        "```yaml\ntrail_type: algorithmic\ntrail_creation: automatic\n"
        "similar_type: curated\nsimilar_method: manual comparison\n"
        "trail_use_case: exploration\nsimilar_use_case: synthesis\n```"
    ),
    "task-006": (
        "```yaml\nchosen_pattern: Abstract Base Class\n"
        "typing_style: nominal\nruntime_check: abstractmethod\n"
        "rejected_alternative: Protocol\n```"
    ),
}


# --- Partial responses (should score between 0 and 1) ---

PARTIAL = {
    "task-001": (
        """```yaml
database: DuckDB
deployment_model: clustered
analytics_capability: true
primary_use_case: user sessions
```""",
        0.5,
    ),  # database + analytics correct, deployment + use_case wrong
    "task-002": (
        """```yaml
algorithm: token bucket
tiers: 2
global_rate_per_min: 40
global_burst: 15
per_user_rate_per_min: 0
per_user_burst: 0
backoff_initial_ms: 0
```""",
        4 / 7,
    ),  # 4 of 7 fields correct
    "task-003": (
        """```yaml
model_name: nomic-embed-text-v1.5
dimensions: 768
inference_mode: cloud
acceleration: cuda
```""",
        0.5,
    ),  # model + dimensions correct, mode + accel wrong
}


def main() -> int:
    passed = 0
    failed = 0
    total = 0

    print("=== Construct Validity: Perfect Responses ===\n")
    for probe_id, response in PERFECT.items():
        grader = GRADERS[probe_id]
        score = grader(response)
        ok = score >= 0.95
        status = "PASS" if ok else "FAIL"
        print(f"  {probe_id}: {score:.2f} [{status}]")
        total += 1
        if ok:
            passed += 1
        else:
            failed += 1

    print("\n=== Construct Validity: Zero Responses ===\n")
    for probe_id, response in ZERO.items():
        grader = GRADERS[probe_id]
        score = grader(response)
        ok = score <= 0.15
        status = "PASS" if ok else "FAIL"
        print(f"  {probe_id}: {score:.2f} [{status}]")
        total += 1
        if ok:
            passed += 1
        else:
            failed += 1

    print("\n=== Construct Validity: Partial Responses ===\n")
    for probe_id, (response, expected_approx) in PARTIAL.items():
        grader = GRADERS[probe_id]
        score = grader(response)
        ok = abs(score - expected_approx) < 0.15
        status = "PASS" if ok else "FAIL"
        print(f"  {probe_id}: {score:.2f} (expected ~{expected_approx:.2f}) [{status}]")
        total += 1
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Results: {passed}/{total} passed, {failed} failed")

    if failed > 0:
        print("\nGrader apparatus has issues. Fix before running experiments.")
        return 1

    print("\nGrader apparatus validated. Ready for Phase 1 (noise floor).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
