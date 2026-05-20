"""CoVE-depth prompt construction for cross-family voices.

Internal to cross_family mechanism. Pure depth dispatch.

ANCHORED  — voice sees claim + source; checks for textual support.
REEXTRACT — voice sees source + question; re-derives value, compares to asserted.
BLIND     — voice sees source + question cold; no claim, no expected value;
            answers independently. Comparison happens in CrossFamilyMechanism.
"""

from __future__ import annotations

from assay.adapters._out.mechanisms.cross_family.config import CoVeDepth
from assay.domain.models import Claim

_HEADER = """You are an independent verification voice for a forensic verification harness.
Be precise; cite the source span; reply in the exact format requested.
Never speculate beyond what the source supports."""


def build_prompt(claim: Claim, depth: CoVeDepth) -> str:
    if depth is CoVeDepth.ANCHORED:
        return _anchored(claim)
    if depth is CoVeDepth.REEXTRACT:
        return _reextract(claim)
    if depth is CoVeDepth.BLIND:
        return _blind(claim)
    raise ValueError(f"unknown depth: {depth}")


def _anchored(claim: Claim) -> str:
    return f"""{_HEADER}

CLAIM: {claim.statement}
SOURCE ID: {claim.source.id}
SOURCE EXCERPT:
{claim.source.excerpt}

Does the source excerpt support the claim as written?

Reply in this exact format (one line each):

VERDICT: AGREE | DISAGREE | UNCERTAIN
SUPPORTING SPAN: <verbatim phrase from the source that supports your verdict, or NONE>
REASON: <one sentence>
"""


def _reextract(claim: Claim) -> str:
    question = claim.question or f"Per the source, what is the value relevant to: {claim.statement}"
    return f"""{_HEADER}

You will see a primary-source excerpt and a question. Re-extract the relevant
value from the source independently. Then compare to the asserted value.

QUESTION: {question}
ASSERTED VALUE: {claim.expected_value or "(see CLAIM)"}
CLAIM (for comparison): {claim.statement}
SOURCE ID: {claim.source.id}
SOURCE EXCERPT:
{claim.source.excerpt}

Reply in this exact format:

EXTRACTED: <the value you extracted from the source>
SUPPORTING SPAN: <verbatim phrase from the source that supports your extraction>
VERDICT: AGREE | DISAGREE | UNCERTAIN
REASON: <one or two sentences>
"""


def _blind(claim: Claim) -> str:
    """BLIND — Dhuliawala CoVE form. Voice does not see the claim or asserted value."""
    question = claim.question
    if not question:
        # Best-effort neutral question if mission did not provide one.
        question = f"What does the source disclose about: {claim.statement}"

    return f"""{_HEADER}

You will see a primary-source excerpt and a question. Answer the question
based ONLY on what the source discloses. Do not speculate beyond the source.
Do not assume any expected answer.

QUESTION: {question}
SOURCE ID: {claim.source.id}
SOURCE EXCERPT:
{claim.source.excerpt}

Reply in this exact format:

EXTRACTED: <the value or fact the source discloses, in your own words>
SUPPORTING SPAN: <the verbatim phrase or sentence from the source that supports your answer>
"""
