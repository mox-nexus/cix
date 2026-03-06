# Chain-of-Verification (CoVE) — Reference

Extended reference for the CoVE verification protocol applied to research claim verification.

---

## Origins

Chain-of-Verification (Dhuliawala et al., 2023, arXiv:2309.11495) is the most validated hallucination reduction technique in current literature. Meta Research demonstrated +23% F1 improvement when CoVE is applied to factual claims.

The mechanism: when a model generates a claim and then verifies it in the same context, it anchors to its own output. When verification questions are answered independently (without seeing the original claim), the model draws from source material rather than its own prior assertion.

---

## The Four Steps in Research Context

### Step 1: Draft (from extraction)

The extracted claim from the extract phase serves as the draft. The verifier receives:
- The claim text
- The source quote
- The source metadata (author, title, venue, year)

### Step 2: Plan Verification

Generate 3-5 verification questions per claim. These questions should be:
- Answerable from the source alone
- Specific enough to confirm or refute the claim
- Independent of the claim's phrasing

**Example claim**: "CoVE improves F1 by 23% on factual claim verification"

**Verification questions**:
1. What metric does the paper report for CoVE's improvement? (F1, accuracy, precision, recall?)
2. What is the exact improvement figure? (23%, or something else?)
3. What baseline is the improvement measured against? (standard prompting, CoT, something else?)
4. What task/dataset is this result from?
5. Are there conditions where the improvement doesn't hold?

### Step 3: Independent Verification

Answer each verification question by reading the source material directly. Key rules:

- **Do NOT re-read the claim before answering** — this defeats independence
- **Read the relevant sections of the source** — not just the quote
- **Note exactly what the source says** — verbatim where possible
- **If the source doesn't answer a question** — note "NOT FOUND IN SOURCE"

### Step 4: Verdict

Compare independent answers against the claim:

| Comparison | Verdict |
|-----------|---------|
| All answers consistent with claim | VERIFIED |
| Minor discrepancies (rounding, phrasing) | CORRECTED |
| Material disagreement (direction, magnitude, scope) | REFUTED |
| Questions unanswerable from source | INSUFFICIENT |

---

## Verification Depth by Tier

Not all claims warrant the same verification depth:

| Claim Tier | Verification Depth | Questions |
|-----------|-------------------|-----------|
| **Tier 1 (Gold)** | Full CoVE — all 4 steps, 5 questions | Comprehensive |
| **Tier 2 (Silver)** | Standard — 3 questions, spot-check | Key facts |
| **Tier 3 (Bronze)** | Light — quote verification + 1 question | Existence check |

### Escalation

If a Tier 2 claim fails light verification, escalate to full CoVE. If a Tier 3 claim is critical to a synthesis finding, escalate to standard.

---

## Common Verification Failures

### Number Errors

The most common extraction error. Specific checks:
- Is the decimal correct? (0.507 vs 0.057)
- Is the sign correct? (positive vs negative)
- Is the statistic type correct? (β vs b vs r vs d)
- Is the sample size from this study or a cited study?
- Is the p-value exact or a threshold? (p=0.03 vs p<0.05)

### Scope Errors

Claims often overstate the scope of a finding:
- Study of undergraduates → extracted as "people generally"
- Results in English → extracted without language caveat
- One dataset → extracted as "consistently"
- Controlled experiment → extracted as "in practice"

### Causal Errors

Claims upgrade correlation to causation:
- Source: "X is associated with Y" → Extracted as: "X causes Y"
- Source: "X predicts Y" → Extracted as: "X leads to Y"
- Check study design: only RCTs and controlled experiments support causal claims

### Attribution Errors

Claims attribute findings to wrong source:
- "Smith (2023) found X" but X was actually found by Jones (2022), cited by Smith
- Check: is the finding from this paper's original research, or from a paper they cited?

---

## Prompt Patterns

### For generating verification questions

```
Given this extracted claim from [Source]:
CLAIM: [claim text]
QUOTE: [source quote]

Generate 5 verification questions that would confirm or refute this claim.
Each question must be answerable from the source paper alone.
Questions should test: the exact numbers, the direction of the effect,
the scope of the finding, the methodology, and any caveats.
```

### For independent verification

```
Source paper: [title, author, year]

Answer these questions using ONLY the source paper.
Do NOT refer to any prior extraction or claim.
For each answer, quote the relevant text from the source.

1. [question]
2. [question]
...
```

### For verdict assignment

```
EXTRACTED CLAIM: [claim]
INDEPENDENT FINDINGS:
1. [answer to q1]
2. [answer to q2]
...

Compare the extracted claim against the independent findings.
Assign a verdict: VERIFIED, CORRECTED, REFUTED, or INSUFFICIENT.

If CORRECTED: state the exact correction needed.
If REFUTED: state what the source actually says.
If INSUFFICIENT: state what additional information is needed.
```

---

## Verification Checklist

Before assigning VERIFIED:

- [ ] Quote is verbatim (checked against source)
- [ ] Numbers match exactly (not rounded, not approximated)
- [ ] Direction is correct (positive/negative/null)
- [ ] Scope is not overstated (population, conditions, generality)
- [ ] Causal language matches study design
- [ ] Attribution is to the correct source (not a cited source)
- [ ] Caveats and limitations are preserved
- [ ] Statistical test type is correctly identified
