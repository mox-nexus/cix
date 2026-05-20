"""Voice-output parsing — extract VERDICT / EXTRACTED / SUPPORTING SPAN / REASON.

Internal to cross_family mechanism. Used by every voice adapter to turn a
raw model response into a structured reading.

Phase 1 uses Python regex. xuma rule-tree replacement deferred (see
roadmap notes in README).
"""

from __future__ import annotations

import re

_VERDICT_RX = re.compile(r"VERDICT:\s*(AGREE|DISAGREE|UNCERTAIN)\b", re.IGNORECASE)
_EXTRACTED_RX = re.compile(r"EXTRACTED:\s*(.+?)(?:\n[A-Z][A-Z _]+:|\Z)", re.IGNORECASE | re.DOTALL)
_SPAN_RX = re.compile(r"SUPPORTING SPAN:\s*(.+?)(?:\n[A-Z][A-Z _]+:|\Z)", re.IGNORECASE | re.DOTALL)
_REASON_RX = re.compile(r"REASON:\s*(.+?)(?:\n[A-Z][A-Z _]+:|\Z)", re.IGNORECASE | re.DOTALL)


def parse_response(raw: str) -> dict:
    """Extract structured fields from a voice response.

    Returns a dict with keys: verdict (str: 'agree'|'disagree'|'uncertain'|'unparsed'),
    extracted (str|None), supporting_span (str|None), reason (str).
    """
    verdict_m = _VERDICT_RX.search(raw)
    verdict = verdict_m.group(1).lower() if verdict_m else "unparsed"

    extracted_m = _EXTRACTED_RX.search(raw)
    extracted = _strip(extracted_m.group(1)) if extracted_m else None

    span_m = _SPAN_RX.search(raw)
    span = _strip(span_m.group(1)) if span_m else None
    if span and span.upper() == "NONE":
        span = None

    reason_m = _REASON_RX.search(raw)
    reason = _strip(reason_m.group(1)) if reason_m else raw[:200].strip()

    return {
        "verdict": verdict,
        "extracted": extracted,
        "supporting_span": span,
        "reason": reason,
    }


def _strip(s: str) -> str:
    return s.strip().rstrip(".").strip()
