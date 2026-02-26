---
name: evaluating
description: "This skill should be used when the user asks to 'is this ready to ship', 'does this content work', 'evaluate this piece', 'check evidence quality', or needs propagation testing and evidence verification."
version: 0.1.0
---

# Evaluating

> The quality gate is "does understanding propagate?" — not "is this well-crafted?"

## Contents

- [The Propagation Test](#the-propagation-test)
- [Structural Confidence Categories](#structural-confidence-categories)
- [Three Doors Traversal](#three-doors-traversal)
- [Evidence Verification](#evidence-verification)
- [Accuracy Standards](#accuracy-standards)
- [Comprehension Verification Tests](#comprehension-verification-tests)

## The Propagation Test

Ebert's primary evaluation criterion. After reading the content:

1. **Can the reader explain it to someone else?** Not repeat it — explain it. Can they reconstruct the reasoning in their own words?
2. **Does understanding survive one hop?** If the reader explains it to a third person, does the third person understand? Content that can't survive forwarding is information, not understanding.
3. **Can the reader apply it to a novel case?** Understanding transfers. Memorization doesn't.

If all three pass, understanding propagates. If any fails, the content informs but doesn't teach.

This is the difference between failure mode #3 (spectacle — reader is impressed but can't explain) and genuine understanding transfer.

## Structural Confidence Categories

Replace verbalized confidence with structural assessment. Verbalized confidence ("I'm 90% sure") is unreliable in LLMs (Xiong et al. ICLR 2024). Use convergence-based categories instead:

| Category | Meaning | Based on |
|----------|---------|----------|
| **Solid** | Multiple independent verification paths converge | Cross-reference, multiple sources agree, mechanism understood |
| **Probable** | Most paths converge, minor uncertainty remains | Single quality source, or converging indirect evidence |
| **Uncertain** | Paths diverge, gaps exist | Sources disagree, mechanism unclear, small sample |
| **Unknown** | Cannot verify from available material | No source, outside domain, genuine ignorance |

**Rule**: Never present "uncertain" claims as "solid." Never use verbalized confidence alone. Always pair with structural checks.

## Three Doors Traversal

When reviewing content, check each door:

### Door 1 (Principle)
- Can the principle-seeker pull their thread from any passage?
- What's the universal this rests on? Could someone state it?
- In 5 years, what from this explanation still holds?

### Door 2 (Concretions)
- Who is this for? Can I name the constituency?
- What was this decided *against*? Is contrast present?
- Would this land differently for a different audience?

### Door 3 (Ground)
- Can the ground-seeker find something solid at every point?
- What would someone actually carry away?
- Does this have weight, or is it just clarity?

### Dimensional Shift
- Does the explanation cross doors at least once?
- Is there a moment where the abstract becomes undeniable?
- Could someone read this and stay in one door the entire time?

### Encoding Assessment
- Which doors are present, which are missing?
- Is it woven or sequenced? (Three doors in a trench coat?)
- Does a dimensional shift happen? What shift would fix it?

## Evidence Verification

### Evidence Labeling

Every cited claim must carry an evidence level:

| Level | Description | Language |
|-------|-------------|----------|
| **Strong** | Meta-analyses, replicated | "Research consistently shows..." |
| **Moderate** | Several studies | "Studies suggest..." |
| **Weak** | Single study, preprint | "One study found..." |
| **Speculative** | Theory only | "In principle..." |

### Verification Pipeline

1. **Bibliography check** — Every cited paper must have a bibliography entry with DOI or URL
2. **Tool verification** — Run `scripts/verify-citations.py` on the article
3. **Interpret results** — VERIFIED, CONTRADICTED, PARTIAL, NOT FOUND

Missing bibliography entries are the #1 cause of unverifiable claims. Fix bibliography first, then verify content.

## Accuracy Standards

Teaching wrong things effectively is worse than not teaching at all. Verification precedes craft.

- State what was measured, not what you infer
- Label evidence levels explicitly
- Separate findings from interpretation
- Acknowledge contradictory evidence
- Every cited number must trace to a specific paper — if unverifiable, don't cite it

### Common Failures

| Failure | Fix |
|---------|-----|
| Inference as finding | State what was actually measured |
| Selective citation | Acknowledge contradictory evidence |
| Mechanism invention | "Correlates with" not "causes" when mechanism unknown |
| Implication overreach | Separate findings from interpretation |
| Framing bias | Label philosophy as philosophy |

## Comprehension Verification Tests

When evaluating whether content carries genuine understanding (not just information):

1. **Rephrase test**: Can the key ideas be stated without the source's phrasing?
2. **Implication test**: What follows from this? What does this predict?
3. **Contradiction test**: What would disprove this? Strongest counterargument?
4. **Boundary test**: Where does this apply and where does it break down?
5. **Novelty test**: Can you generate an example the source doesn't include?

## What Evaluating Does Not Do

Evaluating checks content completeness and accuracy. It does NOT check:
- Voice quality, LLM tells, rhythm (voicing skill — orwell handles this)
- Visual design (figures skill)
- Collection structure (arranging skill)
- Staging and pacing (staging skill)

This separation is intentional — attention economics. Ebert's context contains zero noise about voice craft. His attention stays focused on whether understanding propagates.

## References

Load for detail:
- `references/accuracy-integrity.md` — Why accuracy is foundational, CoVe pattern, evidence labeling
- `references/evidence-verification.md` — Verification workflow, evidence spans, bibliography hygiene
- `scripts/verify-citations.py` — Automated citation verification tool
