"""Voice — internal sub-port of the cross_family mechanism.

This port is NOT a domain port. Voices are an implementation detail of how
the cross_family mechanism operates. Other mechanisms (Berry/SEP/debate) do
not use this port; they have their own internal sub-ports if any.
"""

from __future__ import annotations

from typing import Protocol

from assay.adapters._out.mechanisms.cross_family.config import CoVeDepth
from assay.domain.models import Claim


class VoiceReading:
    """One voice's reading on one claim at one CoVE depth.

    Internal to cross_family mechanism. Aggregated into a MechanismResult
    by the CrossFamilyMechanism.

    Verdict shape: 'agree' | 'disagree' | 'uncertain' | 'error'.
    """

    __slots__ = (
        "voice_name",
        "voice_model",
        "depth",
        "verdict",
        "reasoning",
        "extracted_value",
        "supporting_span",
        "elapsed_seconds",
        "raw_response",
    )

    def __init__(
        self,
        voice_name: str,
        voice_model: str,
        depth: CoVeDepth,
        verdict: str,
        reasoning: str,
        extracted_value: str | None,
        supporting_span: str | None,
        elapsed_seconds: float,
        raw_response: str,
    ) -> None:
        self.voice_name = voice_name
        self.voice_model = voice_model
        self.depth = depth
        self.verdict = verdict
        self.reasoning = reasoning
        self.extracted_value = extracted_value
        self.supporting_span = supporting_span
        self.elapsed_seconds = elapsed_seconds
        self.raw_response = raw_response

    def to_dict(self) -> dict:
        return {
            "voice_name": self.voice_name,
            "voice_model": self.voice_model,
            "depth": self.depth.value,
            "verdict": self.verdict,
            "reasoning": self.reasoning,
            "extracted_value": self.extracted_value,
            "supporting_span": self.supporting_span,
            "elapsed_seconds": self.elapsed_seconds,
            "raw_response": self.raw_response,  # chain-of-custody: preserve verbatim
        }


class Voice(Protocol):
    """A voice renders a VoiceReading on a Claim at a given CoVE depth."""

    name: str
    model: str

    def read(self, claim: Claim, depth: CoVeDepth) -> VoiceReading:
        """Render a reading. Must always return; on failure return a reading
        with verdict='error' and reasoning describing the cause.
        """
        ...
