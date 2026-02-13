"""Last-results register for UUID friction resolution.

Saves search results so users can reference by display index.
Ace's recommendation: UUIDs kill usability. Short indices fix it.

Usage:
    memex dig "auth"       # Results show [1] [2] [3]...
    memex thread @3        # Opens conversation from result #3
"""

import json
from pathlib import Path

from memex.config.settings import settings


def _register_path() -> Path:
    """Path to the last-results register."""
    return settings.corpus_path.parent / "last_results.json"


def save_results(results: list[dict]) -> None:
    """Save result metadata for later reference.

    Args:
        results: List of dicts with at least 'id' and 'conversation_id'.
    """
    path = _register_path()
    path.write_text(json.dumps(results, default=str))


def load_results() -> list[dict]:
    """Load previously saved results."""
    path = _register_path()
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _resolve_entry(ref: str) -> dict | None:
    """Parse @N and return the full register entry."""
    try:
        index = int(ref[1:]) - 1  # 1-indexed for humans
    except ValueError:
        return None

    results = load_results()
    if 0 <= index < len(results):
        return results[index]
    return None


def resolve_fragment_ref(ref: str) -> str | None:
    """Resolve @N to fragment_id, or pass through raw ID.

    Args:
        ref: Either a direct fragment ID or "@N" where N is 1-indexed.

    Returns:
        Fragment ID string, or None if not found.
    """
    if not ref.startswith("@"):
        return ref
    entry = _resolve_entry(ref)
    return entry.get("id") if entry else None


def resolve_conversation_ref(ref: str) -> str | None:
    """Resolve @N to conversation_id, or pass through raw ID.

    Args:
        ref: Either a direct conversation ID or "@N" where N is 1-indexed.

    Returns:
        conversation_id string, or None if not found.
    """
    if not ref.startswith("@"):
        return ref
    entry = _resolve_entry(ref)
    return entry.get("conversation_id") if entry else None


# Backward compat alias — use resolve_conversation_ref for new code
resolve_reference = resolve_conversation_ref
