"""YAML-based graders for CEP-001 task probes.

Each grader validates whether the agent's YAML config contains the correct
field values from the corpus ground truth. Deterministic, no paraphrase variance.

Each function takes the response content (str) and returns a float [0, 1].

Architecture: _extract_yaml → _field_match → _grade_yaml → per-probe wrapper.
"""

from __future__ import annotations

import re
from typing import Any

import yaml


def _extract_yaml(response: str) -> dict | None:
    """Extract YAML from ```yaml code blocks or raw content.

    Takes the last ```yaml block (the final version if the agent iterates).
    Falls back to raw yaml.safe_load on the full response.
    Returns None if unparseable.
    """
    # Try ```yaml blocks
    blocks = re.findall(r"```ya?ml\s*\n(.*?)```", response, re.DOTALL)
    if blocks:
        try:
            return yaml.safe_load(blocks[-1])
        except yaml.YAMLError:
            pass

    # Try any ``` blocks
    blocks = re.findall(r"```\s*\n(.*?)```", response, re.DOTALL)
    if blocks:
        try:
            return yaml.safe_load(blocks[-1])
        except yaml.YAMLError:
            pass

    # Fall back to raw parse
    try:
        parsed = yaml.safe_load(response)
        if isinstance(parsed, dict):
            return parsed
    except yaml.YAMLError:
        pass

    return None


def _field_match(actual: Any, expected: Any, match_type: str) -> bool:
    """Compare one field value against ground truth.

    Match types:
      exact:    str equality (case-insensitive, stripped)
      contains: expected substring in actual (case-insensitive)
      numeric:  numeric equality (int or float)
      boolean:  bool interpretation matches
      any:      list of expected values, any match counts
    """
    if actual is None:
        return False

    if match_type == "exact":
        return str(actual).lower().strip() == str(expected).lower().strip()

    if match_type == "contains":
        return str(expected).lower() in str(actual).lower()

    if match_type == "numeric":
        try:
            return float(actual) == float(expected)
        except (ValueError, TypeError):
            return False

    if match_type == "boolean":
        if isinstance(actual, bool):
            return actual == expected
        truthy = {"true", "yes", "1"}
        return (str(actual).lower().strip() in truthy) == expected

    if match_type == "any":
        # expected is a list of acceptable values
        actual_lower = str(actual).lower()
        return any(str(e).lower() in actual_lower for e in expected)

    return False


def _grade_yaml(
    response: str,
    field_specs: list[tuple[str, Any, float, str]],
) -> float:
    """Universal YAML grader.

    field_specs: list of (field_name, expected_value, weight, match_type)
    Returns: weighted score [0.0, 1.0]
    """
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    total_weight = sum(w for _, _, w, _ in field_specs)
    if total_weight == 0:
        return 0.0

    earned = 0.0
    for field_name, expected, weight, match_type in field_specs:
        actual = parsed.get(field_name)
        if actual is not None and _field_match(actual, expected, match_type):
            earned += weight

    return earned / total_weight


# --- Per-Probe Graders ---


def grade_task_001(response: str) -> float:
    """Auth token storage: DuckDB, single-node, analytics, token usage.

    Corpus: conv-001-auth-duckdb.md
    """
    return _grade_yaml(response, [
        ("database", "duckdb", 1.0, "contains"),
        ("deployment_model", "single-node", 1.0, "any"),  # also accept "single node", "single-file"
        ("analytics_capability", True, 1.0, "boolean"),
        ("primary_use_case", "token", 1.0, "contains"),
    ])


def _grade_task_001_deployment(actual: Any) -> bool:
    """Flexible matching for deployment model."""
    if actual is None:
        return False
    a = str(actual).lower()
    return any(t in a for t in [
        "single-node", "single node", "single-file", "single file",
        "embedded", "serverless", "no server", "one machine",
    ])


# Override task-001 to use flexible deployment matching
def grade_task_001(response: str) -> float:  # noqa: F811
    """Auth token storage: DuckDB, single-node, analytics, token usage."""
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    score = 0.0
    total = 4.0

    if _field_match(parsed.get("database"), "duckdb", "contains"):
        score += 1.0
    if _grade_task_001_deployment(parsed.get("deployment_model")):
        score += 1.0
    if _field_match(parsed.get("analytics_capability"), True, "boolean"):
        score += 1.0
    if _field_match(parsed.get("primary_use_case"), "token", "contains"):
        score += 1.0

    return score / total


def grade_task_002(response: str) -> float:
    """Rate limiting: token bucket, 2 tiers, 40/min burst 15, 10/min burst 5, 500ms backoff.

    Corpus: conv-002-rate-limiting.md
    """
    return _grade_yaml(response, [
        ("algorithm", "token bucket", 1.0, "contains"),
        ("tiers", 2, 1.0, "numeric"),
        ("global_rate_per_min", 40, 1.0, "numeric"),
        ("global_burst", 15, 1.0, "numeric"),
        ("per_user_rate_per_min", 10, 1.0, "numeric"),
        ("per_user_burst", 5, 1.0, "numeric"),
        ("backoff_initial_ms", 500, 1.0, "numeric"),
    ])


def grade_task_003(response: str) -> float:
    """Embedding model: nomic-embed-text-v1.5, 768-dim, local, CoreML.

    Corpus: conv-003-embedding-model.md
    """
    return _grade_yaml(response, [
        ("model_name", "nomic", 1.0, "contains"),
        ("dimensions", 768, 1.0, "numeric"),
        ("inference_mode", "local", 1.0, "contains"),
        ("acceleration", "coreml", 1.0, "any"),
    ])


# Override task-003 for flexible acceleration matching
def grade_task_003(response: str) -> float:  # noqa: F811
    """Embedding model: nomic-embed-text-v1.5, 768-dim, local, CoreML."""
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    score = 0.0
    total = 4.0

    if _field_match(parsed.get("model_name"), "nomic", "contains"):
        score += 1.0
    if _field_match(parsed.get("dimensions"), 768, "numeric"):
        score += 1.0
    if _field_match(parsed.get("inference_mode"), "local", "contains"):
        score += 1.0

    accel = str(parsed.get("acceleration", "")).lower()
    if any(t in accel for t in ["coreml", "core ml", "core_ml", "metal", "apple"]):
        score += 1.0

    return score / total


def grade_task_004(response: str) -> float:
    """Reranking bug: ascending sort, reverse=True fix, cross-encoder, commit a3f7e21.

    Corpus: conv-006-reranking-bug.md
    """
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    score = 0.0
    total = 4.0

    # root_cause should mention ascending/descending/inverted/reverse
    rc = str(parsed.get("root_cause", "")).lower()
    if any(t in rc for t in ["ascending", "descending", "invert", "reverse", "wrong order", "sort order"]):
        score += 1.0

    # fix should mention reverse
    fix = str(parsed.get("fix", "")).lower()
    if any(t in fix for t in ["reverse", "descending", "reverse=true"]):
        score += 1.0

    # component should mention reranking/cross-encoder
    comp = str(parsed.get("component", "")).lower()
    if any(t in comp for t in ["rerank", "re-rank", "cross-encoder", "cross encoder"]):
        score += 1.0

    # commit must be exact (prefix match)
    commit = str(parsed.get("commit", "")).strip()
    if commit.startswith("a3f7e21"):
        score += 1.0

    return score / total


def grade_task_005(response: str) -> float:
    """Trails vs similar: curated/manual vs algorithmic/cosine, synthesis vs exploration.

    Corpus: conv-008-trail-architecture.md
    """
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    score = 0.0
    total = 6.0

    tt = str(parsed.get("trail_type", "")).lower()
    if any(t in tt for t in ["curated", "manual", "intentional", "user"]):
        score += 1.0

    tc = str(parsed.get("trail_creation", "")).lower()
    if any(t in tc for t in ["manual", "user", "human", "curated", "intentional"]):
        score += 1.0

    st = str(parsed.get("similar_type", "")).lower()
    if any(t in st for t in ["algorithmic", "automatic", "computed", "machine"]):
        score += 1.0

    sm = str(parsed.get("similar_method", "")).lower()
    if any(t in sm for t in ["cosine", "embedding", "vector", "semantic"]):
        score += 1.0

    tu = str(parsed.get("trail_use_case", "")).lower()
    if any(t in tu for t in ["synthesis", "narrative", "research", "deep dive", "understanding"]):
        score += 1.0

    su = str(parsed.get("similar_use_case", "")).lower()
    if any(t in su for t in ["exploration", "discovery", "discover", "browsing", "serendipity"]):
        score += 1.0

    return score / total


def grade_task_006(response: str) -> float:
    """Hexagonal ports: Protocol, structural typing, runtime_checkable, rejected ABC.

    Corpus: conv-004-hexagonal-ports.md
    """
    parsed = _extract_yaml(response)
    if parsed is None:
        return 0.0

    score = 0.0
    total = 4.0

    cp = str(parsed.get("chosen_pattern", "")).lower()
    if "protocol" in cp:
        score += 1.0

    ts = str(parsed.get("typing_style", "")).lower()
    if any(t in ts for t in ["structural", "duck", "implicit"]):
        score += 1.0

    rc = str(parsed.get("runtime_check", "")).lower()
    if any(t in rc for t in ["runtime_checkable", "runtime checkable", "isinstance"]):
        score += 1.0

    ra = str(parsed.get("rejected_alternative", "")).lower()
    if any(t in ra for t in ["abc", "abstract base class", "abstract class"]):
        score += 1.0

    return score / total


# Registry: probe_id -> grader function
GRADERS: dict[str, callable] = {
    "task-001": grade_task_001,
    "task-002": grade_task_002,
    "task-003": grade_task_003,
    "task-004": grade_task_004,
    "task-005": grade_task_005,
    "task-006": grade_task_006,
}
