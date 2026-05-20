"""InquiryRunner — orchestrates a verification inquiry.

For each claim from the ClaimStore, evaluate every configured Mechanism and
adjudicate the results. Persists each MechanismResult and Adjudication to the
VerdictStore as work proceeds (resumable; partial-failure tolerant).

Pure orchestration over ports — depends on no specific mechanism, no specific
storage. Composition root wires the actual implementations.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from assay.domain.models import Adjudication, Claim, MechanismResult
from assay.domain.ports._out.claim_store import ClaimStore
from assay.domain.ports._out.mechanism import Mechanism
from assay.domain.ports._out.verdict_store import VerdictStore
from assay.domain.services.adjudication import adjudicate


@dataclass
class InquiryProgress:
    """Per-claim progress emitted to a callback for live CLI output."""

    claim: Claim
    mechanism_results: list[MechanismResult]
    adjudication: Adjudication


@dataclass
class InquirySummary:
    """End-of-run summary statistics."""

    claim_count: int
    converged_count: int
    diverged_count: int
    error_only_count: int
    elapsed_seconds: float


class InquiryRunner:
    def __init__(
        self,
        claim_store: ClaimStore,
        mechanisms: list[Mechanism],
        verdict_store: VerdictStore,
        sleep_seconds_between_claims: float = 0.0,
    ) -> None:
        if not mechanisms:
            raise ValueError("at least one mechanism is required")
        self._claims = claim_store
        self._mechanisms = mechanisms
        self._store = verdict_store
        self._sleep = sleep_seconds_between_claims

    def run(
        self,
        on_progress: Callable[[InquiryProgress], None] | None = None,
        only_claim_id: str | None = None,
    ) -> InquirySummary:
        t0 = time.time()
        claim_count = 0
        converged = 0
        diverged = 0
        error_only = 0

        claims: Iterable[Claim]
        if only_claim_id:
            single = self._claims.get(only_claim_id)
            if single is None:
                raise KeyError(f"no claim with id {only_claim_id!r} in store")
            claims = [single]
        else:
            claims = self._claims.iter_claims()

        for claim in claims:
            claim_count += 1
            results: list[MechanismResult] = []
            for mech in self._mechanisms:
                result = mech.evaluate(claim)
                self._store.write_mechanism_result(result)
                results.append(result)

            adj = adjudicate(claim.id, claim.sha256, results)
            self._store.write_adjudication(adj)

            if adj.converged and adj.error_count < len(results):
                converged += 1
            if adj.diverged:
                diverged += 1
            if adj.error_count == len(results):
                error_only += 1

            if on_progress:
                on_progress(
                    InquiryProgress(claim=claim, mechanism_results=results, adjudication=adj)
                )

            if self._sleep > 0:
                time.sleep(self._sleep)

        return InquirySummary(
            claim_count=claim_count,
            converged_count=converged,
            diverged_count=diverged,
            error_only_count=error_only,
            elapsed_seconds=time.time() - t0,
        )
