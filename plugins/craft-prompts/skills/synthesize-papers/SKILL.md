---
name: synthesize-papers
description: "Use when: 'analyze these papers', 'synthesize research findings', 'extract claims from papers', 'compare methodologies', 'literature review', 'research gap analysis', or analyzing/synthesizing multiple academic papers."
---

# Synthesize Papers

Analyzing and synthesizing academic papers with LLMs.

**The problem:** 75% of content in multi-document summaries can be hallucinated. LLMs over-sensitive to input ordering.

---

## Core Techniques

### Dual-LLM Cross-Critique — 0.94 accuracy

1. Two models extract independently
2. Concordance check (agreement = high confidence)
3. Cross-critique discordant responses
4. 51% become concordant after critique

### Plan-Based Synthesis (LitLLMs)

1. Generate structured outline first
2. Execute synthesis following the plan
3. Fewer hallucinations than direct generation

### Claimify Pipeline — 99% claim entailment

1. **Selection**: Filter non-factual content
2. **Disambiguation**: Resolve pronouns/ambiguity
3. **Decomposition**: Atomic, verifiable claims

---

## Gap Analysis Framework

Four layers to identify research gaps:

| Layer | Questions |
|-------|-----------|
| **Theoretical** | What constructs lack formal definition? |
| **Methodological** | What approaches haven't been tried? |
| **Empirical** | What populations/contexts unstudied? |
| **Practical** | What implementations missing? |

---

## Evidence Weighting

When findings conflict, weight by:

1. Study design (RCT > observational > case study)
2. Sample size
3. Recency
4. Replication status

```
[Study A] (n=1000, RCT, 2024) finds X
[Study B] (n=50, case study, 2020) finds Y
Weight toward Study A due to design and sample.
```

---

## Quick Prompt Pattern

```markdown
Papers to synthesize:
1. [Paper 1 - paste abstract or full text]
2. [Paper 2]
3. [Paper 3]

Tasks:
1. Extract key claims from each (atomic, verifiable)
2. Identify agreements and conflicts
3. Weight conflicting findings by study design + sample size
4. Synthesize into coherent narrative
5. Identify gaps across all four layers (theoretical, methodological, empirical, practical)

For each claim, cite: Author (Year), specific finding.
Flag conflicts as: "CONFLICTING: [A] vs [B]"
```

---

## References

- `references/paper-synthesis.md` — Complete patterns, Claimify details, gap analysis templates

---

## When to Use

- Literature review synthesis
- Comparing methodologies across studies
- Extracting and verifying claims
- Identifying research gaps
- Multi-paper analysis for thesis/publication
