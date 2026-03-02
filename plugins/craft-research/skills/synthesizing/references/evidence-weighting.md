# Evidence Weighting — Reference

Extended reference for evidence weighting in cross-source synthesis.

---

## The Problem

When sources conflict, the natural instinct is to pick the one that "makes more sense." This is selection bias. Evidence weighting replaces intuition with systematic quality assessment.

75% of multi-document summary content can be hallucinated (synthesis research, 2024). The primary cause: LLMs fill gaps between sources with plausible-sounding but ungrounded claims. Weighting forces the synthesizer to stay within the evidence.

---

## The Evidence Pyramid

Research quality forms a hierarchy. Higher designs control for more threats to validity:

```
          ┌──────────┐
          │  Meta-    │  Aggregates across studies
          │ analysis  │  Controls for: study-level bias
          ├──────────┤
          │   RCT    │  Random assignment
          │          │  Controls for: selection bias
          ├──────────┤
          │  Quasi-  │  Comparison without randomization
          │  exp.    │  Controls for: temporal trends
          ├──────────┤
          │  Longit. │  Repeated measurement
          │  obs.    │  Controls for: one-time effects
          ├──────────┤
          │  Cross-  │  Snapshot measurement
          │  section │  Controls for: nothing (descriptive)
          ├──────────┤
          │  Case    │  Single instance
          │  study   │  Controls for: nothing
          ├──────────┤
          │  Expert  │  Professional judgment
          │  opinion │  Controls for: nothing
          └──────────┘
```

Higher ≠ better in all cases. An excellent case study can be more informative than a poor RCT. But when evidence conflicts, higher designs get more weight by default.

---

## Multi-Factor Weighting

When two sources disagree, evaluate across all factors:

### Worked Example

**Claim conflict**: Effect of AI transparency on user trust

Study A: Transparency increases trust (d=0.62)
- Design: RCT, n=400, Tier 1 (CHI 2024), not yet replicated
- Score: Design=5, Sample=4, Tier=5, Recency=5, Replication=1

Study B: Transparency decreases trust when explanations are complex (d=-0.31)
- Design: Quasi-experimental, n=150, Tier 1 (CSCW 2023), replicated once
- Score: Design=4, Sample=3, Tier=5, Recency=4, Replication=3

**Synthesis**: Not a contradiction. Study B identifies a boundary condition (complexity) that Study A didn't test for. The synthesized finding: "Transparency increases trust when explanations are simple (Study A), but may decrease trust when explanations are complex (Study B). Explanation complexity moderates the transparency-trust relationship."

This is synthesis — finding what neither study alone reveals.

---

## Position Bias in Synthesis

LLMs weight information by position in the prompt, not by evidence quality. Countermeasures:

### 1. Per-Source Extraction First

Never synthesize across raw papers. Always work from extracted, verified claims. Claims are position-independent.

### 2. Explicit Quality Ordering

When presenting claims for synthesis, annotate each with quality metadata:

```
CLAIM: [text] (Design: RCT, n=400, Tier 1, 2024, unreplicated)
```

This forces attention to quality, not position.

### 3. Multiple Orderings (for critical syntheses)

Run synthesis 3 times with different claim orderings:
- Chronological
- Reverse chronological
- By evidence strength (strongest first)

Only include findings that appear in all 3 syntheses.

### 4. Adversarial Challenge

After synthesis, generate the strongest counterargument:
- "What evidence would overturn this finding?"
- "Which source most threatens this conclusion?"
- "What's the steel-man case against this finding?"

---

## When Sources Aren't Comparable

Not all divergences are contradictions. Check for:

### Different Populations
- Study A: undergraduates in US
- Study B: professionals in EU
- → Different populations, not conflicting findings

### Different Measures
- Study A: measures satisfaction (survey)
- Study B: measures performance (task completion)
- → Different constructs, not conflicting findings

### Different Timeframes
- Study A: immediate effect (post-task survey)
- Study B: longitudinal effect (6-month follow-up)
- → Different temporal windows, not conflicting findings

### Different Contexts
- Study A: laboratory setting
- Study B: field deployment
- → Different ecological validity, not conflicting findings

When studies aren't comparable, say so:

```
FINDING: Effect of X on Y may differ by [population/measure/timeframe/context].
Study A finds [result] in [context]. Study B finds [result] in [context].
These are not directly comparable because [specific reason].
CONFIDENCE: INSUFFICIENT for integrated finding. Separate findings reported.
```

---

## Handling Negative Results

Negative results (no significant effect found) are findings, not failures:

- Report them at the same evidence level as positive results
- A well-powered RCT finding no effect is HIGH confidence evidence of no effect
- A small study finding no effect is LOW confidence — could be underpowered
- Asymmetry: publication bias means negative results are likely underrepresented

### The File Drawer Problem

For every published positive finding, multiple null findings may be unpublished. Note this:

```
CAVEAT: Positive findings may be overrepresented due to publication bias.
        The true effect may be smaller than the published literature suggests.
```

---

## Synthesis Quality Checks

Before finalizing synthesis:

- [ ] Every finding references specific verified claim IDs
- [ ] No claims from outside the verified set
- [ ] Convergences noted with number of supporting sources
- [ ] Divergences mapped with evidence weighting
- [ ] Gaps named with type and impact
- [ ] Confidence levels based on evidence pattern, not intuition
- [ ] Negative results included at appropriate evidence level
- [ ] Position bias mitigated (claims extracted per-source, not from raw papers)
- [ ] Boundary conditions noted where applicable
