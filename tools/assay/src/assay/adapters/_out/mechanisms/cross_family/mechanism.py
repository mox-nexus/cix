"""CrossFamilyMechanism — the Phase-1 sole mechanism implementation.

Implements the Mechanism port. Composes Voice sub-adapters internally.
Voice-level adjudication is internal; only the projected MechanismResult
crosses the domain boundary.

Other mechanisms (Berry, SEP, debate, linguistic) are sibling adapters at
the same architectural level; they implement the Mechanism port directly with
their own internal sub-ports.
"""

from __future__ import annotations

import time
from collections import Counter

from assay.adapters._out.mechanisms.cross_family.config import CrossFamilyConfig
from assay.adapters._out.mechanisms.cross_family.voice.port import Voice, VoiceReading
from assay.domain.models import Claim, MechanismResult, Verdict

_NAME = "cross_family"


def _project_to_verdict(readings: list[VoiceReading]) -> tuple[Verdict, bool, bool, int]:
    """Project voice readings to a domain Verdict.

    Returns (verdict, converged, diverged, error_count).
    """
    counts: Counter[str] = Counter(r.verdict for r in readings)
    error_count = counts.get("error", 0)
    agree = counts.get("agree", 0)
    disagree = counts.get("disagree", 0)
    uncertain = counts.get("uncertain", 0) + counts.get("unparsed", 0)
    non_error = agree + disagree + uncertain

    if non_error == 0:
        return Verdict.ERROR, False, False, error_count

    diverged = agree > 0 and disagree > 0
    converged = not diverged

    if diverged:
        return Verdict.UNCERTAIN, converged, diverged, error_count
    if agree > 0:
        return Verdict.AGREE, converged, diverged, error_count
    if disagree > 0:
        return Verdict.DISAGREE, converged, diverged, error_count
    return Verdict.UNCERTAIN, converged, diverged, error_count


class CrossFamilyMechanism:
    name = _NAME

    def __init__(self, voices: list[Voice], config: CrossFamilyConfig) -> None:
        if not voices:
            raise ValueError("cross_family mechanism requires at least one voice")
        self._voices = voices
        self._config = config

    def evaluate(self, claim: Claim) -> MechanismResult:
        t0 = time.time()
        readings: list[VoiceReading] = []
        for voice in self._voices:
            reading = voice.read(claim, self._config.depth)
            readings.append(reading)

        verdict, converged, diverged, error_count = _project_to_verdict(readings)

        # Confidence: fraction of non-error voices in the dominant verdict bucket.
        non_error = len([r for r in readings if r.verdict != "error"])
        if non_error == 0:
            confidence = None
        else:
            counts = Counter(r.verdict for r in readings if r.verdict != "error")
            top = counts.most_common(1)[0][1] if counts else 0
            confidence = top / non_error if non_error > 0 else None

        if diverged:
            summary = f"diverged: {error_count} error, voices split"
        elif converged and verdict is Verdict.AGREE:
            summary = f"converged AGREE across {non_error} voice(s)"
        elif converged and verdict is Verdict.DISAGREE:
            summary = f"converged DISAGREE across {non_error} voice(s)"
        elif verdict is Verdict.ERROR:
            summary = f"all {error_count} voice(s) errored"
        else:
            summary = f"uncertain across {non_error} voice(s)"

        return MechanismResult(
            claim_id=claim.id,
            claim_sha256=claim.sha256,
            mechanism=_NAME,
            verdict=verdict,
            confidence=confidence,
            summary=summary,
            evidence={
                "depth": self._config.depth.value,
                "voice_readings": [r.to_dict() for r in readings],
            },
            elapsed_seconds=time.time() - t0,
            metadata={"voice_count": len(self._voices)},
        )
