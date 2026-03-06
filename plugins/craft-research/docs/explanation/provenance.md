# Evidentiary Provenance: Why Every Claim Needs a Chain

This document explains why provenance — the unbroken chain from finding to source quote — is the central design constraint of craft-research, and why each link in the chain exists.

## The Problem Provenance Solves

When an AI says "research shows X (Smith 2023)," three things can go wrong:

1. **Smith 2023 doesn't exist.** The model fabricated the citation. This happens at rates of 1-in-5 for GPT-4o (Deakin University study).

2. **Smith 2023 exists but doesn't say X.** The model attributed a finding to the wrong source, or overgeneralized a specific finding. This is subtler and harder to catch — the citation resolves, but the claim it's attached to is wrong.

3. **Smith 2023 says X, but X is one study with n=42 in a specific population, and the model presents it as established fact.** The finding is technically correct but the confidence level is inflated. The reader has no way to evaluate the strength of the evidence.

Provenance solves all three by requiring an unbroken chain:

```
Source text (the actual paper)
  → Verbatim quote (exact words, with location)
  → Atomic claim (one fact, derived from the quote)
  → Verification verdict (independently confirmed)
  → Synthesized finding (with claim references and confidence)
```

Each link is independently checkable. A human can walk the chain backwards from any finding and verify every step.

## Why Verbatim Quotes

The first instinct is to paraphrase: "Blaurock et al. found that control matters most." But paraphrasing introduces interpretation at the earliest stage, and interpretation errors compound. Consider:

**Source**: "user control had the strongest effect on co-production quality (β=0.507, p<0.001)"

**Paraphrase 1**: "control matters most for quality" — loses the effect size, loses the specific construct

**Paraphrase 2**: "control is the strongest predictor" — changes "effect" to "predictor," a methodological distinction

**Paraphrase 3**: "user control improves co-production" — loses the comparative claim (strongest), adds causal implication the source doesn't make

Each paraphrase drifts from the source. By the time it passes through verification and synthesis, the drift may be undetectable — the claim "looks right" because it's plausible, but it no longer faithfully represents what the source said.

Verbatim quotes eliminate this. The quote is a fixed anchor. The claim is explicitly marked as an interpretation of the quote. Verification checks whether the interpretation is faithful. The two remain separate throughout.

## Why Atomic Claims

Compound claims hide partial truth. Consider:

**Compound**: "CoVE improves accuracy and reduces hallucination in research contexts."

This contains three claims:
1. CoVE improves accuracy
2. CoVE reduces hallucination
3. These effects hold in research contexts

Claim 1 might be well-supported. Claim 2 might be well-supported. Claim 3 might be speculative — the original study may have tested in general Q&A, not research specifically. But the compound claim presents all three as equally established.

Decomposition lets verification operate on each independently. Claim 1: VERIFIED. Claim 2: VERIFIED. Claim 3: INSUFFICIENT (original study didn't test research contexts). Now synthesis can use claims 1 and 2 with HIGH confidence while correctly noting that the research-specific application is extrapolation.

## Why Independent Verification

The most counterintuitive design choice: the verifier (scrutiny) must re-read the source *without seeing the extraction first*. This feels wasteful — why read the paper twice? But the independence is the mechanism.

When a verifier sees an extraction before reading the source, they anchor to the extraction. They read the source looking for confirmation, not contradiction. They find what they expect to find. This is textbook confirmation bias, and it's the failure mode of all "checking" that happens in the same context as the original work.

CoVE (Dhuliawala et al., 2023) demonstrated this empirically: independent verification achieves +23% F1 improvement over same-context verification. The improvement comes entirely from the independence — the verifier forms their own understanding, then compares.

In practice, this means:
1. Scrutiny reads the source paper
2. Scrutiny forms its own understanding of what the source says
3. *Only then* does scrutiny compare against extract's extraction
4. Discrepancies surface errors that same-context checking would miss

## Why Confidence Only Decreases

A verified claim from a single Tier 2 source gets MEDIUM confidence. It would be natural for synthesis to reason: "This is consistent with three other findings, it makes theoretical sense, and the mechanism is plausible — I'll upgrade it to HIGH."

This is not allowed. Reasoning does not constitute evidence. Only new verified claims from independent sources can increase confidence. Why?

Because LLMs excel at constructing coherent narratives. Given a claim and a request to justify it, the model will produce a plausible argument every time. This is the fundamental problem: the model can always explain why a claim should be true, regardless of whether it is. Allowing reasoning-based confidence upgrades would make every claim HIGH by default.

The constraint is a firewall against the model's own persuasiveness. Confidence tracks evidence, not plausibility.

## Why the Audit Exists

The audit agent walks provenance chains end-to-end after synthesis. This seems redundant — if extraction was good and verification was independent, shouldn't the findings be correct?

In principle, yes. In practice, three things go wrong:

### Chain Breaks

The most common: a synthesis finding cites a claim that was never verified, or a claim whose verification was INSUFFICIENT. The claim entered synthesis through a gap in the gate between verification and synthesis.

### Scope Inflation

Each layer preserves scope within its own operation but doesn't cross-check against previous layers. A source says "in US university settings." The extraction correctly notes this. Verification confirms it. But synthesis drops the scope qualifier when integrating across sources: "Control improves outcomes" instead of "Control improves outcomes (US university settings)."

The audit catches this by reading the finding *and* the source, checking whether the finding's scope is warranted by the evidence.

### Confidence Inflation

Similar to scope inflation: individual verifications are honest about confidence, but synthesis assigns a higher confidence than the evidence supports. The audit cross-checks confidence against the actual evidence pattern.

## The Workspace as Audit Trail

The `.research/` workspace isn't just a coordination mechanism — it's a permanent record of every stage in the pipeline. Months later, a reader can:

- Open `extraction/blaurock2025.md` and see every claim extracted from that paper, with verbatim quotes and locations
- Open `verification/blaurock2025.md` and see which claims were verified, corrected, or refuted
- Open `synthesis/control-effects.md` and see which verified claims support the finding about control effects
- Open `audit/report.md` and see whether the chains were intact

This transparency is the complement to accuracy. Even if the pipeline makes an error, the error is visible and traceable. A reader who disagrees with a finding can follow the chain to the specific claim, the specific quote, and the specific source — and form their own judgment.

## The Human's Role

The pipeline is designed so the human retains the generative steps:

1. **Scoping** — defining which questions matter and what's out of scope
2. **Reviewing** — evaluating whether findings answer the questions
3. **Deciding** — determining what to do with the findings

Agents handle the mechanical steps: extracting, verifying, integrating, auditing. These are high-effort, error-prone, and don't require the kind of judgment that scoping and deciding require.

This matches the CIX thesis: AI amplifies capability on mechanical tasks while the human retains agency over the tasks that require judgment. The human doesn't need to spend hours manually extracting claims from papers — but they absolutely need to decide which research questions to ask and whether the answers are satisfactory.
