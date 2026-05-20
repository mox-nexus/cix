"""Core domain models for assay.

The domain knows about Claims (assertions bound to PrimarySources), Mechanisms
(verification approaches that produce MechanismResults), and Adjudications
(cross-mechanism reconciliation of MechanismResults for one claim).

The domain does NOT know about Voices, CoVE depths, logprobs, hidden states,
or debate transcripts. Those are mechanism-specific concerns owned by mechanism
adapters.

Pure domain — no I/O, no API specifics, no DuckDB. Adapters bring those.
"""

from __future__ import annotations

import hashlib
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

# --- Verdict shape ---


class Verdict(StrEnum):
    """The discrete shape every mechanism must project its result to.

    Mechanisms also attach mechanism-specific evidence (logprob trace,
    voice readings, debate transcript, etc.) via MechanismResult.evidence.
    """

    AGREE = "agree"
    DISAGREE = "disagree"
    UNCERTAIN = "uncertain"
    ERROR = "error"


# --- Source ---


class PrimarySource(BaseModel):
    """A primary public document with chain-of-custody attestation.

    Forensic discipline: every claim is bound to a primary source, and the
    source itself carries provenance (accession, retrieval timestamp, hash)
    so that re-runs are reproducible and tampering is detectable.
    """

    id: str = Field(
        description="Stable source identifier (e.g., '10-K 0001324424-26-000008 Note 9')"
    )
    accession: str | None = Field(default=None, description="EDGAR accession number, if applicable")
    section: str | None = Field(
        default=None, description="Section / note / item locator within the source"
    )
    excerpt: str = Field(
        description="Verbatim excerpt of the source containing or relevant to the claim"
    )
    retrieved_at: str | None = Field(default=None, description="ISO-8601 retrieval timestamp")
    sha256: str | None = Field(
        default=None, description="SHA-256 of the full source document at retrieval"
    )
    fetch_url: str | None = Field(default=None, description="URL the source was fetched from")


# --- Claim ---


class Claim(BaseModel):
    """A verifiable assertion bound to a primary source.

    The statement is what is asserted. The source contains (or contradicts)
    the assertion. The question (optional) phrases what to ask the voice
    cold under BLIND depth. The expected_value (optional) is the asserted
    numeric/textual value if the claim is value-bearing.

    Mechanical extraction outputs are claims too (the assertion is "this
    XBRL concept tag at this period equals this value").
    """

    id: str = Field(description="Stable identifier for the claim (e.g., 'F003-cap-rate-FY2025')")
    statement: str = Field(description="The assertion as written")
    source: PrimarySource
    question: str | None = Field(
        default=None,
        description="Question for BLIND-depth verification, derived from statement if absent.",
    )
    expected_value: str | None = Field(
        default=None,
        description="Asserted value if value-bearing (e.g., '19.9%', '$296M').",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def sha256(self) -> str:
        """Content hash of the claim — enables re-run detection across edits."""
        h = hashlib.sha256()
        h.update(self.statement.encode("utf-8"))
        h.update(b"\x00")
        h.update(self.source.id.encode("utf-8"))
        h.update(b"\x00")
        h.update(self.source.excerpt.encode("utf-8"))
        h.update(b"\x00")
        h.update((self.expected_value or "").encode("utf-8"))
        return h.hexdigest()


# --- Mechanism result (the domain's primary contract) ---


class MechanismResult(BaseModel):
    """One mechanism's reading on one claim.

    Every mechanism (cross-family voice triangulation, Berry trace-budget,
    semantic-entropy probe, multi-agent debate, linguistic deterministic
    checks) projects to a Verdict on this contract. Mechanism-specific
    payload (voice readings, KL divergence scores, sample variances,
    debate transcripts) attaches via `evidence`.

    This is the seam that admits new mechanisms without domain surgery.
    """

    claim_id: str
    claim_sha256: str = Field(
        description="Content hash of the claim at the time of mechanism execution"
    )
    mechanism: str = Field(
        description="Mechanism family identifier (e.g., 'cross_family', 'trace_budget')"
    )
    verdict: Verdict
    confidence: float | None = Field(
        default=None,
        description="Mechanism-specific confidence in [0, 1] if applicable; None if not.",
    )
    summary: str = Field(description="One-sentence summary of what the mechanism concluded")
    evidence: dict[str, Any] = Field(
        default_factory=dict,
        description="Mechanism-specific payload (voice readings, KL trace, sample variance, etc.)",
    )
    elapsed_seconds: float
    metadata: dict[str, Any] = Field(default_factory=dict)


# --- Adjudication (cross-mechanism reconciliation) ---


class Adjudication(BaseModel):
    """Cross-mechanism reconciliation of all MechanismResults for one claim.

    Adjudication operates over the MechanismResult contract — it does not
    know about voices, logprobs, or any mechanism's internal evidence.
    Convergence is judged on Verdict alone; divergence triggers human
    review of the mechanism-specific evidence stored in each result.
    """

    claim_id: str
    claim_sha256: str = Field(description="Content hash; detects re-runs against edited claims")
    mechanism_results: list[MechanismResult]
    converged: bool = Field(description="True iff all non-error mechanisms agree on Verdict")
    diverged: bool = Field(description="True iff at least one mechanism disagrees with another")
    error_count: int
    final_verdict: Verdict = Field(
        description="Aggregate verdict; UNCERTAIN if diverged or all errored"
    )
    notes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# --- Inquiry (the YAML-driven mission spec) ---


class MechanismSpec(BaseModel):
    """Configuration for one mechanism in an Inquiry.

    Type-loose `config` dict is mechanism-specific; each mechanism adapter
    parses its own typed schema (Antifragile typed-schema inversion).
    """

    name: str = Field(description="Mechanism family identifier")
    config: dict[str, Any] = Field(default_factory=dict)


class InquiryConfig(BaseModel):
    """An Inquiry — the YAML-driven verification specification."""

    name: str
    description: str | None = None
    mechanisms: list[MechanismSpec]
    claims_path: str = Field(
        description="Path to JSONL file of claims, or directory of claim JSONs"
    )
    output_dir: str = Field(
        default=".cix/assay", description="Where verdicts and adjudications land"
    )
    sleep_seconds_between_calls: float = 0.5
