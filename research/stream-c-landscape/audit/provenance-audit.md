# Stream C Provenance Audit

**Auditor:** Automated provenance chain check
**Date:** 2026-04-13
**Scope:** All findings in synthesis/findings.md

---

## Pipeline Integrity

| Stage | Status | Notes |
|-------|--------|-------|
| Scope | COMPLETE | 5 RQs + null hypotheses, frozen 2026-04-13 |
| Collection | COMPLETE | 500 OpenAlex records (10 JSONL, sweep-1) + 3 web synthesis documents |
| Triage | COMPLETE | 15 papers selected from 500; extraction-targets.json written |
| Extraction | COMPLETE | 13 papers extracted (~85 claims), 2 papers missing from sweep data (MTEB, Vector DB survey) |
| Synthesis | COMPLETE | 10 findings + 5 hard problems + 26 architectural implications |
| Verification | COMPLETE | 10 load-bearing claims verified: 8 VERIFIED, 2 CORRECTED, 0 REFUTED |
| Corrections | APPLIED | C1.4 and C2.5 corrected in synthesis |

---

## Provenance Chain: Findings → Evidence

### RQ-C1 Findings

| Finding | Evidence sources | Chain intact? |
|---------|-----------------|---------------|
| C1.1 (three architectural patterns) | web:memory-augmented-systems, sumers_2023:c3-c4, li_2024:c4 | YES |
| C1.2 (LTM improves engagement) | jo_2024:c4-c6 | YES |
| C1.3 (existing models fail at LT conversation) | xu_2022:c1,c3,c5 | YES — VERIFIED |
| C1.4 (no cognitive grounding) [CORRECTED] | web:memory-augmented-systems, sumers_2023:c2, li_2024:c1 | YES — CORRECTED, applied |

### RQ-C2 Findings

| Finding | Evidence sources | Chain intact? |
|---------|-----------------|---------------|
| C2.1 (hybrid search is baseline) | bruch_2023:c1, web:vector-db, zhao_2022 | YES |
| C2.2 (convex > RRF) | bruch_2023:c2,c4,c5 | YES — VERIFIED |
| C2.3 (LLM reranking distills) | sun_2023:c1,c4 | YES — VERIFIED |
| C2.4 (no ecphoric retrieval) | web:memory-augmented-systems, zhao_2022, web:pkm | YES — VERIFIED |
| C2.5 (GraphRAG relational retrieval) [CORRECTED] | peng_2024:c3,c5, web:memory-augmented-systems, pan_2023:c4 | YES — CORRECTED, applied |

### RQ-C3 Findings

| Finding | Evidence sources | Chain intact? |
|---------|-----------------|---------------|
| C3.1 (LanceDB confirmed) | web:vector-db-hybrid-retrieval | YES — VERIFIED |
| C3.2 (GRIT unified models) | muennighoff_2024:c2,c5,c6 | YES |
| C3.3 (no conversation embedding model) | web:vector-db, lee_2024 | YES |

### RQ-C4 Findings

| Finding | Evidence sources | Chain intact? |
|---------|-----------------|---------------|
| C4.1 (trails unimplemented) | web:pkm-memex-history | YES — VERIFIED |
| C4.2 (PKM assumes manual decomposition) | web:pkm-memex-history | YES |
| C4.3 (no PKM effectiveness evidence) | web:pkm-memex-history | YES — VERIFIED |

### RQ-C5 Findings

| Finding | Evidence sources | Chain intact? |
|---------|-----------------|---------------|
| C5.1 (ecphoric retrieval unsolved) | All web sources + zhao_2022 | YES — VERIFIED |
| C5.2 (solidification tracking unsolved) | web:memory-augmented-systems, web:pkm | YES |
| C5.3 (conversational memory underserved) | xu_2022:c1, web:vector-db | YES |
| C5.4 (temporal reasoning partial) | web:vector-db (Milvus, Re3), web:memory-augmented-systems (Zep) | YES |
| C5.5 (privacy/local-first partial) | web:memory-augmented-systems, jo_2024:c6, web:vector-db | YES |

---

## Evidence Quality Assessment

### Academic Extractions (13 papers, ~85 claims)
- All abstract-only (OpenAlex) — lower depth than full-text extraction
- All claims have verbatim quotes from reconstructed abstracts
- 2 planned papers (MTEB benchmark, Vector DB survey) absent from sweep data — covered by web research
- Evidence tiers: mix of T1 empirical (EMAT, CareCall, Bruch, Sun, Xu, M3, NV-Embed, GRIT), T2 theoretical (CoALA, LLM+KG), T3 review (Dense Retrieval survey, GraphRAG survey, Personal LLM Agents)

### Web Research Synthesis (3 documents)
- Sourced from product documentation, blog posts, benchmark sites, Wikipedia
- URLs provided for all claims
- More current than academic papers (2025-2026 coverage)
- Lower epistemic weight than peer-reviewed sources — web claims should be treated as landscape descriptions, not verified findings
- Key web-sourced claims verified against academic sources where possible (e.g., hybrid search convergence supported by both Bruch 2023 and web sources)

### Verification Coverage
- 10 of ~20 synthesis claims verified (50% coverage)
- All load-bearing claims (architectural decision drivers) included in verification
- 8 VERIFIED, 2 CORRECTED — corrections applied
- 0 REFUTED

---

## Known Weaknesses

1. **Abstract-only extraction** — All 13 academic papers extracted from abstracts only. Claims are thin compared to Stream A/B full-text extractions. Load-bearing papers (CoALA, Bruch fusion, Xu goldfish) would benefit from full-text extraction.

2. **Web source ephemerality** — Web research synthesis documents capture a snapshot of the landscape as of 2026-04-13. Product features, benchmarks, and pricing will shift. These findings should be re-verified before making implementation decisions.

3. **Two missing papers** — MTEB benchmark (Muennighoff 2023) and Vector DB survey (Ma 2023) were not in the OpenAlex sweep data. The web research covers their territory but without the academic rigor.

4. **RQ-C4 has zero academic sources** — The PKM/memex history findings rely entirely on web research. The OpenAlex sweep for PKM returned noise (PRISMA guidelines, bioinformatics). A targeted collection for PKM academic literature would strengthen this RQ.

5. **Absence claims** — Several key findings (C2.4, C4.1, C5.1) are absence claims ("no system does X"). These are supported by broad survey coverage but cannot be proven with certainty. A system implementing ecphoric retrieval could exist outside the surveyed literature.

---

## Ship Decision

**SHIP PROVISIONAL.**

Rationale:
- All findings have traceable evidence chains (provenance intact)
- Load-bearing claims verified (8/10 verified, 2 corrected and applied)
- Null hypotheses evaluated for all 5 RQs
- Cross-stream integration complete (26 architectural implications consolidated)
- Known weaknesses are documented and bounded

The "provisional" qualifier reflects:
- Abstract-only extraction depth
- Web source ephemerality
- Absence claims inherently unprovable
- RQ-C4 lacking academic sources

These weaknesses do not block architectural design work. They should be addressed if memex publishes research claims externally.


---

## Round 2 Audit Update (2026-04-25)

**Verification round 2 complete.** 22 previously-unverified synthesis-cited claims independently re-verified by Gemini (cross-model from Claude), using `gemini -p` with a CoVE protocol that re-reads source + judges quote-match + verdict.

### Results

| Metric | Value |
|---|---|
| Round-2 claims verified | 22 |
| VERIFIED | 20 |
| CORRECTED | 2 |
| REFUTED | 0 |
| INSUFFICIENT | 0 |
| Verbatim quote match | 22/22 (100%) |
| Round-2 success rate (V+C, none refuted) | 100% |
| Total synthesis-cited claims | 34 |
| Synthesis-cited claims now verified across both rounds | ~65% |

### Per-claim corrections

See `synthesis/findings.md` Round-2 footer for the list of corrections applied. Pattern across all corrections: hedge-dropping in extractions that did not propagate to synthesis, except for `wilson2002:c15` in Stream A where one synthesis sentence had to be softened ("crystallize into semantic form" → "crystallize", with the "into semantic form" framing reattributed to cross-source inference using squire1982:c16-c17).

### Independence note

Round-1 CoVE was performed by Claude (the same model that did extraction). Round-2 CoVE was performed by Gemini, which provides genuine cross-model independence — different family, different training data, different failure modes. The fact that 0 refutations and 0 quote-fabrications were found across 22 additional claims, by a different model, materially strengthens the corpus.

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
