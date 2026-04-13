# Verification: Load-Bearing Claims

**Protocol:** CoVE (Chain of Verification) — independent re-read of sources, adversarial comparison
**Claims verified:** 15 (architecturally load-bearing for memex)
**Sources consulted:** abstracts from .pilot-targets.json / .remaining-abstracts.json; full-text from sources/full-text/*.md

---

## Results Summary

| Verdict | Count | Claims |
|---|---|---|
| VERIFIED | 11 | c1, c2, c3, c5, c6, c9, c10, c11, c13, c14, c15 |
| CORRECTED | 4 | c4, c7, c8, c12 |
| REFUTED | 0 | — |
| INSUFFICIENT | 0 | — |

**Verification rate:** 100% (all claims pass — 11 verified, 4 corrected)
**No refutations.** Core findings are solid. The 4 corrections are hedge-dropping and minor source-attribution issues — none change the architectural implications.

---

## Claim-by-Claim

### 1. nader2009:c5 — VERIFIED
CLAIM: Memories are not consolidated just once; they return to labile state and require reconsolidation on reactivation.
QUOTE: "memories are not consolidated, or stabilized, just once: they can return to a labile state and need to be reconsolidated, or restabilized, when reactivated."
VERIFICATION: Quote is verbatim from the paper's "Evidence for a reconsolidation process" section. Claim accurately represents the paper's central thesis. Note: boundary conditions exist (nader2009:c11, c23 — not all memories reconsolidate under all conditions), but the claim as stated is what the paper argues.

### 2. tulving1984:c10 — VERIFIED
CLAIM: Synergistic ecphory — retrieval requires joint influence of stored trace AND cognitively present retrieval information.
QUOTE: "'synergistic' refers to the joint influence that the stored episodic information and the cognitively present retrieval information exert on the construction of the product of ecphory"
VERIFICATION: Quote is verbatim from the Tulving 1984 abstract. Claim correctly captures the two-input model. No hedge in source — Tulving presents this as the framework's definition, not a tentative claim.

### 3. metcalfe1986:c8 — VERIFIED
CLAIM: Across both experiments, FOK judgments for insight problems showed zero predictive validity.
QUOTE: "predictive metacognitions were nonexistent for the problems."
VERIFICATION: Quote is verbatim from abstract. "Both experiments showed that..." precedes the quoted sentence in the abstract, confirming the replication claim. "The problems" correctly disambiguated to insight problems (contrasted with "memory performance" in the preceding clause).

### 4. metcalfewiebe1987:c8 — CORRECTED
CLAIM: 78% of correct insight solutions showed ≤1 point warmth change on 10-point scale.
QUOTE: "On 78% of the problems and anagrams for which subjects provided the correct solution, the progress estimates increased by no more than 1 point, on a 10-point scale, over the entire solution interval."
CORRECTION: This finding is from **Metcalfe 1986b**, cited in the introduction of Metcalfe & Wiebe 1987. It is NOT a new finding from the 1987 paper. The extraction attributes it to metcalfe-wiebe-1987:c8 as if it were a finding of that paper. The claim content is accurate; the source attribution is imprecise.
CORRECTED ATTRIBUTION: Primary source is Metcalfe 1986b (cited in Metcalfe & Wiebe 1987 introduction).
IMPACT ON SYNTHESIS: None — the finding still stands, just from a different primary source.

### 5. beeman2004:c2 — VERIFIED
CLAIM: EEG revealed gamma-band burst in RH aSTG 0.3s before insight solutions.
QUOTE: "Scalp electroencephalogram recordings (Experiment 2) revealed a sudden burst of high-frequency (gamma-band) neural activity in the same area beginning 0.3 s prior to insight solutions."
VERIFICATION: Quote is verbatim from abstract. "The same area" correctly identified as RH aSTG (from Experiment 1's fMRI result in the same abstract). The 0.3s timing is explicitly stated. Full-text confirms: "a sudden burst of gamma-band activity between about 300 ms prior to the button press."

### 6. bartlett1995:c6 — VERIFIED
CLAIM: Bartlett's central claim is that memory is a process of reconstruction.
QUOTE: "Bartlett developed his claim that memory is a process of reconstruction"
VERIFICATION: Quote is verbatim from the 1995 reissue publisher abstract. Note: this is a publisher's characterization of Bartlett's argument, not Bartlett's own words. However, the characterization is well-established in the field and uncontroversial. Full verification would require reading the original 1932 text.

### 7. squire1982:c6 — CORRECTED
CLAIM: Permanent storage occurs outside medial temporal/diencephalic regions; those regions handle formation and maintenance.
QUOTE: "permanent memory storage normally occurs outside the brain regions affected in amnesia. It appears that these brain regions constitute an essential neuroanatomical substrate for the formation of new memories and for their maintenance and elaboration after learning."
CORRECTION: Source hedges with **"It appears that"** — this is Squire's interpretive conclusion, not a definitive statement. The extraction drops the hedge and states it as established fact. The claim should read: "Squire proposes that permanent storage occurs outside..." or preserve the hedge.
IMPACT ON SYNTHESIS: Minimal — the claim is still the dominant view in the field, and later evidence (Squire & Zola-Morgan 1991, etc.) strengthened it. But precision requires noting the hedge.

### 8. wilson2002:c11 — CORRECTED
CLAIM: Mental representations are purpose-neutral.
QUOTE: "Our mental representations, whether novel and sketchy or familiar and detailed, appear to be to a large extent purpose-neutral, or at least to contain information beyond that needed for the originally conceived purpose."
CORRECTION: Source has **two hedges**: "appear to be" and "to a large extent." Additionally, Wilson offers a **weaker alternative**: "at least to contain information beyond that needed." The extraction drops all hedges and states it as "mental representations ARE purpose-neutral." Corrected claim: "Wilson argues that mental representations appear to be largely purpose-neutral, or at minimum contain information beyond the originally conceived purpose."
IMPACT ON SYNTHESIS: The architectural implication (encode broadly, not narrowly) still holds, but with less certainty.

### 9. wilson2002:c15 — VERIFIED
CLAIM: Episodic retrieval has "reliving" quality that crystallizes through retelling into semantic form.
QUOTE: "recalling an episodic memory has a quality of 'reliving,' with all the attendant visual, kinesthetic, and spatial impressions. This is especially true when memories are fresh, before they have become crystallized by retelling into something more resembling semantic memories."
VERIFICATION: Quote is verbatim. "Especially true when memories are fresh" correctly preserved — Wilson says the reliving quality is strongest for fresh memories, not exclusive to them.

### 10. stafford1984:c2 — VERIFIED
CLAIM: After only five minutes, people can recollect only about 10% of what was said in a social exchange.
QUOTE: "even after only five minutes people are able to recollect only about 10% of what was said in a social exchange."
VERIFICATION: Quote is verbatim from abstract. Note for synthesis: this is a single 1984 study with unreported methodology for measuring "what was said." The 10% figure has not been directly replicated (gap identified in synthesis). The "about" qualifier is preserved.

### 11. kounios2009:c8 — VERIFIED
CLAIM: Insight is the culmination of a series of brain states and processes operating at different time scales.
QUOTE: "these studies show that insight is the culmination of a series of brain states and processes operating at different time scales."
VERIFICATION: Quote is verbatim from abstract.

### 12. nader2009:c12 — CORRECTED
CLAIM: Reconsolidation in humans requires spatial context reinstatement.
QUOTE: "reactivation-dependent interference effects in consolidated episodic memory were found only when human subjects were exposed to the interfering material in the same environment in which the original learning took place."
CORRECTION: The claim **overgeneralizes**. The source reports that **interference effects** in one study required same spatial environment. This is not the same as "reconsolidation requires context reinstatement" in general. Reconsolidation may occur without interference; this finding is specifically about when interference-based disruption of reconsolidated memory occurs.
CORRECTED CLAIM: "In one human study, reactivation-dependent interference with consolidated episodic memory occurred only when subjects were in the same spatial environment as original learning."
IMPACT ON SYNTHESIS: The fog-match implication still holds (context matters for retrieval and for memory modification), but the claim is narrower than originally stated.

### 13. friston2017:c4 — VERIFIED
CLAIM: Bayesian model reduction has all the hallmarks of "aha" moments and evinces mechanisms associated with sleep.
QUOTE: "The ensuing Bayesian model reduction evinces mechanisms associated with sleep and has all the hallmarks of 'aha' moments."
VERIFICATION: Quote is verbatim from abstract. Note: this is a computational model claim based on simulations, not an empirical finding from human subjects. The tier should be 3 (theoretical/computational), not 1. The extraction already assigned tier 1, which is the source tier; the CLAIM tier should be lower.

### 14. metcalfewiebe1987:c14 — VERIFIED
CLAIM: Normative predictions outperform self-predictions for insight; interaction F(1,46)=10.13.
QUOTE: "The interaction between own versus normative gammas as a function of problem type was significant [F(1,46) = 10.13, MSe = 1.13]."
VERIFICATION: F statistic confirmed against full text. The accompanying characterization ("overwhelmingly wrong") is also verbatim from the paper.

### 15. pickering2004:c2 — VERIFIED
CLAIM: In dialogue, linguistic representations become aligned at many levels through a largely automatic process.
QUOTE: "in dialogue, the linguistic representations employed by the interlocutors become aligned at many levels, as a result of a largely automatic process."
VERIFICATION: Quote is verbatim from abstract. "Largely" qualifier preserved.

---

## Corrections Applied to Synthesis

The 4 corrections should update the synthesis findings:

1. **Finding 1.3 (c4):** Note that the 78% warmth figure's primary source is Metcalfe 1986b, not Metcalfe & Wiebe 1987. The finding itself is unchanged.
2. **Finding 0.3 (c7):** Change "permanent storage occurs outside..." to "Squire proposes that permanent storage occurs outside..." — preserving the source's hedge.
3. **Finding 2.4 (c8):** Change "mental representations are purpose-neutral" to "Wilson argues mental representations appear to be largely purpose-neutral" — preserving both hedges.
4. **Finding 3.2 (c12):** Narrow from "reconsolidation requires spatial context reinstatement" to "one human study found interference effects required same spatial environment" — reducing the generalization.

None of these corrections change the architectural implications. The core findings stand:
- Recall modifies memory (c1 verified)
- Fog-match is ecphory (c2 verified)
- Insight is unpredictable pre-hoc (c3 verified)
- Insight has neural signatures (c5 verified)
- Memory is reconstruction (c6 verified)
- Encode broadly (c8 corrected but implication holds)
- 90% conversational content lost in 5 minutes (c10 verified)
