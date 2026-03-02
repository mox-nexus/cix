---
name: synthesizing
description: "This skill should be used when the user asks to 'synthesize these findings', 'integrate across sources', 'map convergence and divergence', 'identify research gaps', or needs cross-source evidence integration with gap analysis."
version: 0.1.0
---

# Synthesizing

> Synthesis is not summarization. It's finding what no single source can show alone.

Synthesis integrates verified claims across sources to answer research questions. The output is findings — claims about the state of knowledge — grounded in the provenance chain. Every finding references specific verified claims. Every gap is named, not inferred.

## Contents

- [What Synthesis Does](#what-synthesis-does)
- [The Synthesis Protocol](#the-synthesis-protocol)
- [Convergence, Divergence, and Gaps](#convergence-divergence-and-gaps)
- [Evidence Weighting](#evidence-weighting)
- [Confidence Levels](#confidence-levels)
- [Gap Analysis](#gap-analysis)
- [Output Format](#output-format)
- [Anti-Patterns](#anti-patterns)

## What Synthesis Does

Synthesis answers: **given everything we know (verified claims), what can we say about this research question?**

It maps three things:
1. **Convergence** — where multiple sources agree (high confidence findings)
2. **Divergence** — where sources disagree (tensions, contradictions)
3. **Gaps** — what no source addresses (blind spots)

Synthesis does NOT:
- Add claims not in the verified set
- Infer findings beyond what sources state
- Resolve contradictions by choosing a side (it maps them)
- Fill gaps with speculation

## The Synthesis Protocol

### Inputs

- Verified claims from scrutiny (`.research/verification/` files)
- Research questions from scope.md
- Source inventory

### Per Research Question

1. **Gather** — collect all verified claims relevant to this question
2. **Cluster** — group claims by sub-topic or finding
3. **Map convergence** — identify where multiple sources agree
4. **Map divergence** — identify where sources disagree, with evidence weighting
5. **Map gaps** — identify what the question asks that no source addresses
6. **Synthesize** — write findings as integrated claims with provenance references
7. **Assign confidence** — based on convergence, tier, and evidence weight

### Provenance in Findings

Every finding must reference the specific verified claims it draws from:

```
FINDING: User control is the strongest predictor of co-production quality
         in human-AI collaboration.
EVIDENCE: [blaurock2025:c1] (β=0.507, RCT, n=654) — VERIFIED
          [lee2024:c3] (β=0.31, survey, n=312) — VERIFIED
          [wang2023:c7] (user control improved outcomes, d=0.45) — VERIFIED
CONFIDENCE: HIGH — 3 sources converge, includes RCT
```

The claim IDs (`[source:cN]`) link back through verification to extraction to source quotes. This is the provenance chain.

## Convergence, Divergence, and Gaps

### Convergence Map

Sources that agree strengthen confidence:

| Convergence Level | Evidence | Confidence Impact |
|-------------------|----------|-------------------|
| **Strong** | 3+ sources, including Tier 1 | HIGH |
| **Moderate** | 2 sources, or 3+ without Tier 1 | MEDIUM |
| **Weak** | Single source, any tier | LOW |

Agreement on different metrics is still convergence:
- Study A finds "X improves accuracy" (d=0.45)
- Study B finds "X improves task completion" (OR=2.3)
- Both point in the same direction → convergent

### Divergence Map

Sources that disagree create tensions. Don't resolve — map:

```
DIVERGENCE: Effect of engagement features on experienced users
SOURCE A: [blaurock2025:c3] — non-significant positive (b=0.090, ns)
SOURCE B: [hypothetical:c5] — significant negative (b=-0.23, p<0.05)
WEIGHTING: Source A (RCT, n=654) vs Source B (quasi-exp, n=89)
           Evidence favors Source A on design strength
SYNTHESIS: Evidence is mixed. Larger RCT finds null effect;
           smaller study finds negative. Requires replication.
```

### Gap Map

Gaps are what the research questions ask that no source addresses:

```
GAP: No studies examine control effects in non-Western populations
TYPE: Empirical
IMPACT: Current findings may not generalize across cultures
SOURCES CHECKED: [all sources in inventory — none address this]
```

## Evidence Weighting

When findings conflict, weight by research quality. This is not "choosing sides" — it's noting which evidence is stronger.

### Weighting Hierarchy

```
Meta-analysis / systematic review
  ↓
Randomized controlled trial (RCT)
  ↓
Quasi-experimental
  ↓
Longitudinal observational
  ↓
Cross-sectional survey
  ↓
Case study
  ↓
Expert opinion / practitioner report
```

### Weighting Factors

| Factor | Higher Weight | Lower Weight |
|--------|-------------|-------------|
| **Study design** | RCT, meta-analysis | Case study, opinion |
| **Sample size** | n > 500 | n < 50 |
| **Source tier** | Tier 1 (peer-reviewed) | Tier 3 (blog) |
| **Recency** | Past 2 years | > 5 years |
| **Replication** | Replicated finding | Single study |
| **Effect size** | Large, clinically meaningful | Small, borderline |

### When Weighting Is Insufficient

Some divergences can't be resolved by weighting:
- Both sources are high quality with large samples
- The findings are in genuinely different contexts
- The measures aren't directly comparable

In these cases, report the tension as an open question, not a resolved finding.

## Confidence Levels

Structural confidence based on evidence, not verbalized certainty:

| Level | Evidence Pattern | Language |
|-------|-----------------|----------|
| **HIGH** | 3+ converging sources, Tier 1 included, replicated | "Evidence consistently shows..." |
| **MEDIUM** | 2 converging sources, or single Tier 1 | "Evidence suggests..." |
| **LOW** | Single source, or conflicting evidence | "Limited evidence indicates..." |
| **INSUFFICIENT** | No verified claims address this question | "No evidence found for..." |

Confidence can only decrease through the pipeline. A LOW finding stays LOW even if "it makes sense" or "it's consistent with theory." New evidence upgrades confidence, not reasoning.

## Gap Analysis

Four layers for systematic gap identification:

| Layer | Questions | Example Gap |
|-------|-----------|-------------|
| **Theoretical** | What constructs lack formal definition? What models are missing? | "No formal model of control in human-AI dyads" |
| **Methodological** | What approaches haven't been tried? What designs are missing? | "No longitudinal studies — all cross-sectional" |
| **Empirical** | What populations/contexts unstudied? What data is missing? | "All samples WEIRD — no Global South data" |
| **Practical** | What implementations are missing? What hasn't been deployed? | "No production system implements these controls" |

### Gap Reporting

For each gap:
1. **Name** the gap specifically
2. **Classify** by layer (theoretical, methodological, empirical, practical)
3. **Impact** — what does this gap mean for the research question?
4. **Evidence of absence** — what sources were checked that don't cover this?

## Output Format

Per-question synthesis file:

```markdown
# Synthesis: [Research Question]

## Question
[The research question from scope.md]

## Findings

### Finding 1: [Title]
CLAIM: [integrated finding]
EVIDENCE:
  - [source1:cN] — [brief] — VERIFIED
  - [source2:cN] — [brief] — VERIFIED
CONFIDENCE: [HIGH/MEDIUM/LOW]

### Finding 2: [Title]
...

## Convergence Map
- [What multiple sources agree on, with claim references]

## Divergence Map
- [Where sources disagree, with evidence weighting]

## Gap Map

### Theoretical Gaps
- [gaps with classification and impact]

### Methodological Gaps
- [gaps]

### Empirical Gaps
- [gaps]

### Practical Gaps
- [gaps]

## Summary
- Total findings: [N]
- HIGH confidence: [n] | MEDIUM: [n] | LOW: [n]
- Key convergences: [1-2 sentences]
- Key divergences: [1-2 sentences]
- Critical gaps: [1-2 sentences]
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|--------------|-------------|------------|
| **Summarizing instead of synthesizing** | Retells each source separately | Integrate across sources per finding |
| **Filling gaps with inference** | Introduces ungrounded claims | Name gaps explicitly |
| **Resolving all tensions** | Forces false consensus | Map divergences, weight evidence |
| **Citing unverified claims** | Breaks provenance chain | Only use VERIFIED/CORRECTED claims |
| **Confidence inflation** | "Makes sense" is not evidence | Structural confidence from evidence pattern |
| **Single-source findings as HIGH** | One study is never HIGH confidence | HIGH requires convergence across sources |

## References

- `references/evidence-weighting.md` — Detailed weighting protocols, position bias mitigation, worked examples
