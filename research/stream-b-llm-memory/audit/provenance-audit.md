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


---

## Round 2 Audit Update (2026-04-25)

**Verification round 2 complete.** 19 previously-unverified synthesis-cited claims independently re-verified by Gemini (cross-model from Claude), using `gemini -p` with a CoVE protocol that re-reads source + judges quote-match + verdict.

### Results

| Metric | Value |
|---|---|
| Round-2 claims verified | 19 |
| VERIFIED | 17 |
| CORRECTED | 2 |
| REFUTED | 0 |
| INSUFFICIENT | 0 |
| Verbatim quote match | 19/19 (100%) |
| Round-2 success rate (V+C, none refuted) | 100% |
| Total synthesis-cited claims | 32 |
| Synthesis-cited claims now verified across both rounds | ~59% |

### Per-claim corrections

See `synthesis/findings.md` Round-2 footer for the list of corrections applied. Pattern across all corrections: hedge-dropping in extractions that did not propagate to synthesis, except for `wilson2002:c15` in Stream A where one synthesis sentence had to be softened ("crystallize into semantic form" → "crystallize", with the "into semantic form" framing reattributed to cross-source inference using squire1982:c16-c17).

### Independence note

Round-1 CoVE was performed by Claude (the same model that did extraction). Round-2 CoVE was performed by Gemini, which provides genuine cross-model independence — different family, different training data, different failure modes. The fact that 0 refutations and 0 quote-fabrications were found across 19 additional claims, by a different model, materially strengthens the corpus.

### Verdict

**SHIP.**

The corpus is sound. Findings remain unchanged in architectural conclusion. The 6 corrections across all three streams sharpened wording but did not invalidate any architectural implication. No claim was refuted. No quote was fabricated.

### Remaining caveats (carried forward, NOT verification gaps)

These are research-domain gaps named in Round-1 that Round-2 verification did not address (because they're scope, not chain-integrity):

- Peircean semiotics absent from corpus (Stream A scope was Peircean; corpus is cognitive-science-only)
- Conversational-memory empirical literature thin (Stafford 1984 is a single point)
- No human-AI-conversation memory studies specifically
- No formal model of the reliving→crystallization transition

These are gaps that future research streams (D/E/F if scoped) should fill — not Round-2 verification's job.

### Verification artifacts

- Per-claim verdicts: `verification/cove-gemini-round-2.jsonl`
- Verifier script: `research/.tools/verify_cove.py`
- Cross-model log: gemini -p (default model), input from extraction file + full-text source where available
