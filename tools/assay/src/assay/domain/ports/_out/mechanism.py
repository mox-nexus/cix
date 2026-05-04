"""Mechanism — the primary outbound port for assay.

A Mechanism is a verification approach that produces a MechanismResult on a
Claim. The five known mechanism families (in roadmap order):

  - cross_family       — independent LLM voices reconciled (Phase 1)
  - trace_budget       — logprob-based "did the cite condition the claim" (Phase 3)
  - semantic_entropy   — hidden-state per-claim uncertainty score (Phase 3)
  - debate             — multi-round voice-vs-voice with critique (Phase 3)
  - linguistic         — deterministic NLP checks: verb fidelity, hedge detection,
                          numeric normalization, citation-span alignment (Phase 3)

Each mechanism adapter implements this port. The InquiryRunner depends on the
port, never on a specific mechanism.

The port returns a MechanismResult (never raises). On failure, the result
carries Verdict.ERROR with a summary describing the cause; this lets the
inquiry continue and the user see exactly what failed.
"""

from __future__ import annotations

from typing import Protocol

from assay.domain.models import Claim, MechanismResult


class Mechanism(Protocol):
    """A mechanism renders a MechanismResult on a Claim.

    Adapters implement this; composition wires them. Never raises.
    """

    name: str

    def evaluate(self, claim: Claim) -> MechanismResult:
        """Render a MechanismResult on the claim. Must always return; on
        failure, return a MechanismResult with verdict=Verdict.ERROR.
        """
        ...
