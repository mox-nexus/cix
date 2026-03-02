# Claimify Pipeline — Reference

Extended reference for the Claimify structured claim extraction pipeline.

---

## Origins

The Claimify pipeline achieves 99% claim entailment through structured decomposition (Selection → Disambiguation → Decomposition). Originally developed for fact-checking at scale, adapted here for research provenance.

The key insight: most extraction failures happen because compound, ambiguous claims enter verification. Fix the input shape, and downstream accuracy follows.

---

## Stage Detail: Selection

### Decision Framework

For each statement in the source, classify:

| Classification | Action | Example |
|---------------|--------|---------|
| **Empirical finding** | EXTRACT | "CoVE improved F1 by 23% (p<0.01)" |
| **Methodological claim** | EXTRACT | "We used stratified sampling across 3 conditions" |
| **Definitional** | EXTRACT | "We define control as the user's ability to..." |
| **Opinion** | SKIP | "We believe this approach is promising" |
| **Hedge** | SKIP (or extract as WEAK) | "This might suggest..." |
| **Meta-commentary** | SKIP | "As we discussed in Section 2..." |
| **Citation of others** | EXTRACT FROM ORIGINAL | "Smith (2023) found..." → go to Smith |

### Edge Cases

**Hedged findings**: "Results suggest X (p=0.04)" — extract the finding with the p-value. The hedge is the author being cautious, but the data speaks.

**Negative results**: "We found no significant effect of X on Y" — always extract. Negative results are findings.

**Limitations sections**: Extract specific limitations ("sample was limited to US undergraduates"), skip meta-limitations ("more research is needed").

---

## Stage Detail: Disambiguation

### Pronoun Resolution Table

| Pronoun Pattern | Resolution Strategy |
|----------------|-------------------|
| "it", "this", "that" | Replace with the specific noun from nearest antecedent |
| "the method/approach" | Replace with the named method |
| "they/their" (referring to researchers) | Replace with "Author et al." |
| "they/their" (referring to participants) | Replace with "participants" or specific population |
| "significant" | Specify: statistically (p-value) or practically (effect size) |
| "large/small effect" | Replace with actual effect size if available |

### Abbreviation Handling

- Expand on first occurrence per extraction file
- Include original abbreviation in parentheses: "Chain-of-Verification (CoVE)"
- After first expansion, abbreviation alone is acceptable

---

## Stage Detail: Decomposition

### Splitting Rules

**Conjunction split**: "X and Y" → two claims (unless X and Y are a defined pair)

**Conditional split**: "When A, then B" → keep as single conditional claim (splitting loses the relationship)

**Comparative split**: "X outperforms Y on tasks A, B, and C" → three claims (one per task)

**Quantified split**: "Results improved across all N conditions" → N claims (one per condition with its specific result)

### When NOT to Split

- Defined compound constructs: "precision and recall" as a pair
- Causal chains where splitting loses the mechanism
- Conditional relationships where the condition is essential

---

## Dual-LLM Cross-Critique

For high-stakes extraction (systematic reviews, meta-analyses), use dual extraction:

### Protocol

```
1. Model A extracts claims from source (full Claimify pipeline)
2. Model B extracts claims from same source (independently, no visibility to A)
3. Concordance check:
   - Agreement → HIGH CONFIDENCE claim
   - Disagreement → Cross-critique phase
4. Cross-critique:
   - Show A's extraction to B: "What's wrong with this?"
   - Show B's extraction to A: "What's wrong with this?"
   - 51% of discordant pairs resolve
5. Remaining disagreements → flag for human review
```

### Results (validated)

- 0.94 accuracy on concordant extractions
- 51% resolution of initial disagreements through critique
- Remaining disagreements are genuine ambiguities that require human judgment

### When to Use Dual Extraction

| Situation | Single extraction | Dual extraction |
|-----------|------------------|-----------------|
| Quick survey | Yes | Overkill |
| Systematic review | No | Yes |
| High-stakes claims | No | Yes |
| Well-structured paper | Yes | Optional |
| Dense/ambiguous paper | No | Yes |

---

## Worked Example

### Source Text (excerpt)

> "Our randomized controlled trial (n=654) found that user control had the strongest effect on co-production quality (β=0.507, p<0.001), followed by transparency (β=0.415, p<0.001). Surprisingly, engagement features showed a negative but non-significant effect (b=0.090, ns) for experienced users."

### Stage 1: Selection

All three sentences are empirical findings. Keep all.

### Stage 2: Disambiguation

- "Our randomized controlled trial" → "Blaurock et al. (2025) randomized controlled trial"
- "co-production quality" → already specific
- "engagement features" → resolve if paper defines specific features
- "experienced users" → resolve if paper defines experience threshold

### Stage 3: Decomposition

```
CLAIM 1: User control has the strongest effect on co-production quality
         (β=0.507, p<0.001) in the Blaurock et al. (2025) RCT (n=654).
CLAIM 2: Transparency has the second-strongest effect on co-production quality
         (β=0.415, p<0.001) in the Blaurock et al. (2025) RCT (n=654).
CLAIM 3: Engagement features show a non-significant effect (b=0.090, ns)
         for experienced users in the Blaurock et al. (2025) RCT (n=654).
```

Each claim is independently verifiable. Each traces to the same quote. Each carries the specific statistical evidence.

---

## Common Extraction Errors

| Error | Example | Fix |
|-------|---------|-----|
| **Rounding** | Source says β=0.507, extraction says "about 0.5" | Use exact numbers |
| **Sign flip** | Source says negative, extraction says positive | Double-check direction |
| **Sample confusion** | Report n from wrong study | Verify n matches the specific finding |
| **Venue confusion** | Attribute finding to wrong paper | Verify author + finding match |
| **Effect type confusion** | Report β as b or r | Preserve the exact statistic type |
| **p-value inflation** | Source says p<0.05, extraction says "highly significant" | Report exact p-value |
