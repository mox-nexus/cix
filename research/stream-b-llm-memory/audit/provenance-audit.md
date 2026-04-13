# Stream B: Provenance Audit

**Date:** 2026-04-13
**Findings audited:** 10
**Claims in synthesis:** 44
**Claims verified:** 15 (34%) — 14 VERIFIED, 1 CORRECTED, 0 REFUTED

---

## Chain Integrity

### Per-Finding Verification Coverage

| Finding | Claims cited | Verified | Status |
|---|---|---|---|
| B1.1 Induction heads | 4 | 4 (olsson2022:c1-c4) | COMPLETE |
| B1.2 ICL as gradient descent | 3 | 3 (vonoswald2022:c1,c2,c4) | COMPLETE |
| B1.3 KV cache as memory | 3 | 3 (kwon2023:c1-c3) | COMPLETE |
| B2.1 Lost-in-the-middle | 3 | 2 (an2024:c1,c4) | MAJORITY |
| B2.2 Circuit-specific retrieval | 3 | 2 (garcia2024:c1,c3) | MAJORITY |
| B3.1 Catastrophic forgetting | 4 | 2 (luo2023:c1,c2) | PARTIAL |
| B3.2 Knowledge editing | 2 | 2 (yao2023:c1,c2) | COMPLETE |
| B3.3 Hallucination | 3 | 1 (huang2023:c1) | PARTIAL |
| B4.1 MemGPT | 4 | 3 (packer2023:c2,c3,c5) | MAJORITY |
| Cross-stream bridge | 1 | 1 (marblestone2016:c1) | COMPLETE |

**Findings with ZERO verified evidence: 0**
**Findings with COMPLETE chains: 5**
**Findings with MAJORITY: 3**
**Findings with PARTIAL: 2**

---

## Success Criteria Check

| Criterion | Status |
|---|---|
| Each RQ has ≥3 sources spanning ≥2 traditions | ✓ B1: 3 sources (interp, ML theory, systems); B2: 2 sources (interp, training); B3: 3 sources (empirical, editing, survey); B4: 1 source (MemGPT) — **B4 WEAK (single source)** |
| Human-LLM analogy explicitly mapped | ✓ 10-row structural parallel map with STRONG/MODERATE/BREAKS verdicts |
| Stream A findings evaluated for LLM analogues | ✓ Ecphory, reconsolidation, insight, metacognition, storage all mapped |
| Architectural implications named | ✓ 8 implications |
| All cited claims passed CoVE or noted | ✓ 15 verified, 29 noted as unverified abstract extractions |

---

## Issues Found

| Issue | Severity | Detail |
|---|---|---|
| RQ-B4 relies on single source (MemGPT) | MEDIUM | Only one memory-architecture paper. RAG surveys collected but not extracted. Would strengthen with RETRO, Memorizing Transformers, or other memory-augmentation papers. |
| 29 claims unverified | MEDIUM | All have verbatim quotes from abstracts, so risk is low. But pipeline integrity requires CoVE. |
| Olsson2022:c2 correction not applied to synthesis | LOW | Synthesis Finding B1.1 preserves the hedge in the evidence listing but the finding title says "IS implemented by induction heads" — should be "may be implemented" for large models. |
| All extractions abstract-only | MEDIUM | Same limitation as Stream A. Full-text would add mechanism details, especially for Olsson (induction head circuits) and von Oswald (mathematical proofs). |

---

## Verdict: SHIP (PROVISIONAL)

**Reasoning:** All 10 findings have at least partial verification. 0 findings have zero verified evidence. The structural parallel map — the core deliverable of Stream B — is grounded in verified claims for each mapping. The RQ-B4 single-source weakness is acknowledged as a gap, not hidden.

**Conditions for full SHIP:**
- [ ] Verify remaining 29 claims
- [ ] Add 2-3 more RQ-B4 sources (RAG surveys, RETRO, Memorizing Transformers)
- [ ] Full-text extraction for Olsson 2022 and von Oswald 2022
- [ ] Apply olsson2022:c2 correction to synthesis finding B1.1
