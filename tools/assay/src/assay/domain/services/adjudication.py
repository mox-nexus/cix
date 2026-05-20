"""Cross-mechanism adjudication.

Pure logic — no I/O. Given a list of MechanismResults on the same Claim,
produce an Adjudication that captures convergence/divergence on Verdict.

The adjudication does not reason over mechanism-specific evidence (logprob
traces, voice readings, etc.). That reasoning belongs to the human reviewer
(or, in Phase 3, to a meta-adjudicator service that operates on the
mechanism-specific evidence dicts). Phase 1 stays disciplined: this layer
sees only Verdicts.

Convergence rules:
  - All non-error mechanisms return AGREE → converged on AGREE
  - All non-error mechanisms return DISAGREE → converged on DISAGREE
    (a real outcome — every mechanism agrees the claim is wrong)
  - Mix of AGREE and DISAGREE → diverged → final UNCERTAIN
  - UNCERTAIN counts as soft-non-vote
  - Errors tracked separately; do not block convergence if all non-error agree
"""

from __future__ import annotations

from collections import Counter

from assay.domain.exceptions import AdjudicationError
from assay.domain.models import Adjudication, MechanismResult, Verdict


def adjudicate(claim_id: str, claim_sha256: str, results: list[MechanismResult]) -> Adjudication:
    if not results:
        raise AdjudicationError(f"no mechanism results to adjudicate for claim {claim_id}")

    counts: Counter[Verdict] = Counter(r.verdict for r in results)
    error_count = counts.get(Verdict.ERROR, 0)
    agree = counts.get(Verdict.AGREE, 0)
    disagree = counts.get(Verdict.DISAGREE, 0)
    uncertain = counts.get(Verdict.UNCERTAIN, 0)
    non_error = agree + disagree + uncertain

    if non_error == 0:
        return Adjudication(
            claim_id=claim_id,
            claim_sha256=claim_sha256,
            mechanism_results=results,
            converged=False,
            diverged=False,
            error_count=error_count,
            final_verdict=Verdict.ERROR,
            notes="all mechanisms errored; no judgment possible",
        )

    diverged = agree > 0 and disagree > 0
    converged = not diverged

    if diverged:
        final = Verdict.UNCERTAIN
    elif agree > 0:
        final = Verdict.AGREE
    elif disagree > 0:
        final = Verdict.DISAGREE
    else:
        final = Verdict.UNCERTAIN

    notes_parts: list[str] = []
    if uncertain > 0:
        notes_parts.append(f"{uncertain} uncertain")
    if error_count > 0:
        notes_parts.append(f"{error_count} errored")
    if diverged:
        notes_parts.append(f"split: {agree} agree vs {disagree} disagree")
    notes = "; ".join(notes_parts) if notes_parts else None

    return Adjudication(
        claim_id=claim_id,
        claim_sha256=claim_sha256,
        mechanism_results=results,
        converged=converged,
        diverged=diverged,
        error_count=error_count,
        final_verdict=final,
        notes=notes,
    )
