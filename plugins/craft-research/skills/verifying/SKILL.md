---
name: verifying
description: "This skill should be used when the user asks to 'verify these claims', 'check this against the source', 'run CoVE', 'fact-check these findings', or needs independent verification of extracted claims against source material."
version: 0.1.0
---

# Verifying

> Verification is adversarial by design. The goal is to break claims, not confirm them.

Verification is the integrity checkpoint. Extracted claims are hypotheses about what a source says. Verification tests those hypotheses independently — re-reading the source without seeing the extraction, then comparing. Claims that survive are verified. Claims that don't are corrected or refuted.

Confidence can only decrease through verification, never increase without new evidence.

## Contents

- [Chain-of-Verification (CoVE)](#chain-of-verification-cove)
- [Verification Verdicts](#verification-verdicts)
- [The Protocol](#the-protocol)
- [Independence Requirement](#independence-requirement)
- [Verification Questions](#verification-questions)
- [Output Format](#output-format)
- [Anti-Patterns](#anti-patterns)

## Chain-of-Verification (CoVE)

The most validated hallucination reduction technique (+23% F1, Meta Research). Four steps:

1. **Draft** — the extracted claim exists (from extract)
2. **Plan verification** — generate questions that would confirm or refute the claim
3. **Independent verification** — answer questions by re-reading the source, without seeing the extraction
4. **Verdict** — compare independent findings against the extracted claim

The critical step is **independence**. The verifier must re-read the source and form their own understanding before comparing against the extraction. Seeing the extraction first anchors judgment and defeats the purpose.

## Verification Verdicts

Each claim receives exactly one verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **VERIFIED** | Claim accurately represents the source quote. Numbers, direction, and scope match. | Passes to synthesis unchanged |
| **CORRECTED** | Claim has a factual error but the core finding exists. Specific correction provided. | Corrected version passes to synthesis |
| **REFUTED** | Claim misrepresents the source. The source says something materially different. | Removed from pipeline. Refutation documented. |
| **INSUFFICIENT** | Cannot verify — source ambiguous, quote not found, or methodology unclear. | Flagged. Does not pass to synthesis without human review. |

### Correction vs. Refutation

**Corrected**: "β=0.51" when source says "β=0.507" — the finding exists, the number was rounded.

**Refuted**: "positive effect" when source says "negative effect" — the claim is directionally wrong.

The boundary: does the claim preserve the source's meaning? If yes but with errors, CORRECTED. If no, REFUTED.

## The Protocol

### Per Claim

1. **Read the source quote** from the extraction file
2. **Locate the quote** in the original source — confirm it's verbatim
3. **Read surrounding context** — 2-3 paragraphs before and after
4. **Generate verification questions** (see below)
5. **Answer questions independently** — from the source, not the extraction
6. **Compare** independent answers against the extracted claim
7. **Assign verdict** — VERIFIED, CORRECTED, REFUTED, or INSUFFICIENT
8. **Document** — record the verdict with evidence

### Verification Order

- Verify claims in source order (as they appear in the paper), not extraction order
- This reduces anchoring to the extractor's organizational choices
- High-tier claims (Tier 1) get more thorough verification than Tier 3

## Independence Requirement

The verifier MUST:
- Re-read the source independently
- Form their own understanding of what the source says
- Only then compare against the extracted claim

The verifier MUST NOT:
- Read the extraction before the source
- Accept the claim as default-true
- Skip re-reading because the quote "looks right"
- Verify only the quote match without checking the claim interpretation

Independence is not optional. It is the mechanism by which CoVE achieves its +23% F1 improvement.

## Verification Questions

For each claim, generate questions that would confirm or refute it:

### Factual Claims

- Does the source contain this exact number/statistic?
- Is the direction (positive/negative/neutral) correct?
- Is the sample size correctly reported?
- Is the statistical test correctly identified?
- Is the effect attributed to the correct variable?

### Methodological Claims

- Does the source describe this method?
- Are the conditions/steps correctly enumerated?
- Are limitations or caveats accurately represented?

### Scope Claims

- Does the source claim this generality?
- Are there boundary conditions the extraction omitted?
- Is the population correctly described?

### Causal Claims

- Does the source claim causation or correlation?
- Is the claim's causal language warranted by the study design?
- Are confounds acknowledged?

## Output Format

Per-source verification file:

```markdown
# Verification: [Source Short Name]

## Source Confirmed
- **Title**: [verified title]
- **DOI**: [verified — resolves: yes/no]

## Claim Verification

### [source]:c1 — VERIFIED
ORIGINAL CLAIM: [from extraction]
VERIFICATION: Confirmed. Source states "[relevant quote]" in [location].
No discrepancies found.

### [source]:c2 — CORRECTED
ORIGINAL CLAIM: [from extraction]
CORRECTION: [what changed and why]
CORRECTED CLAIM: [new claim text]
EVIDENCE: Source states "[relevant quote]" in [location].

### [source]:c3 — REFUTED
ORIGINAL CLAIM: [from extraction]
REFUTATION: [why this is wrong]
SOURCE ACTUALLY SAYS: "[what the source actually states]"
LOCATION: [where in source]

### [source]:c4 — INSUFFICIENT
ORIGINAL CLAIM: [from extraction]
REASON: [why verification failed — ambiguous source, quote not found, etc.]
RECOMMENDATION: [human review needed / check original PDF / etc.]

## Summary
- Total claims verified: [N]
- VERIFIED: [n] | CORRECTED: [n] | REFUTED: [n] | INSUFFICIENT: [n]
- Verification rate: [VERIFIED + CORRECTED] / Total
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|--------------|-------------|------------|
| Confirming instead of verifying | Anchoring bias — you expect the claim to be true | Default to doubt. Read source first. |
| Verifying quotes but not claims | Quote can be correct while claim misinterprets it | Verify the CLAIM against the source, not just the quote |
| Skipping context | Quotes out of context can mean the opposite | Read 2-3 paragraphs of surrounding context |
| "Looks right" verification | Pattern matching is not verification | Generate specific verification questions |
| Batch verification | Quality degrades with volume | One claim at a time, full protocol |
| Upgrading confidence | "The finding makes sense" is not evidence | Confidence only decreases through verification |

## References

- `references/cove.md` — CoVE protocol details, prompt patterns, verification examples
