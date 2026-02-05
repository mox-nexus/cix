---
name: deep-research
description: "Use when: 'design a research prompt', 'reduce hallucinations', 'create a deep research prompt', 'citation accuracy', 'source verification', 'academic research with AI', or needing traceability and hallucination reduction in AI-assisted research."
---

# Deep Research

AI-assisted research with traceability and hallucination reduction.

**The problem:** 50-90% of LLM responses not fully supported by cited sources. No single platform is reliable alone.

---

## Platform Reality

| Platform | Hallucination Rate | Best For |
|----------|-------------------|----------|
| Perplexity | <3.5% | Quick fact-checking |
| Claude | ~6% | Synthesis, explicit uncertainty |
| GPT-5 | 8% | Multi-source analysis |
| Gemini Deep Research | 88%* | Comprehensive (verify everything) |

*High accuracy but hallucinates supporting details.

---

## Multi-Tool Strategy

| Phase | Tool | Why |
|-------|------|-----|
| Discovery | Elicit, Consensus | Academic DBs (138M+ papers) |
| Verification | Scite.ai | 1.5B citations classified |
| Synthesis | Claude | Lowest hallucination, explicit uncertainty |
| Fact-check | Perplexity | Best rate when constrained |

---

## Core Techniques

### Chain-of-Verification (CoVe) — +23% F1

1. Draft response
2. Generate verification questions
3. Answer questions independently (no peeking at draft)
4. Revise based on verification

### Source Hierarchy

Specify explicitly in prompts:

| Tier | Source | Use For |
|------|--------|---------|
| 1 (Gold) | Peer-reviewed, A* conferences | Core claims |
| 2 (Silver) | High-citation preprint (>50) | Supporting evidence |
| 3 (Bronze) | Tech blogs, docs | Implementation details |
| Exclude | Marketing, LinkedIn, unattributed | Never cite |

### Abstention Permission

```
If uncertain, state "INSUFFICIENT EVIDENCE" rather than guessing.
If sources conflict, state "CONFLICTING EVIDENCE: [A] claims X, [B] claims Y."
```

### Recency Enforcement

```
Current date: ${DATE}
Prefer past 2 years. 3-4 years if foundational. Older only for established theory.
```

---

## Quick Prompt Pattern

```markdown
Current date: [DATE]

Research: [TOPIC]

Source hierarchy:
1. Peer-reviewed (preferred)
2. High-citation preprint (>50)
3. Technical docs (note as LIMITED)
EXCLUDE: Marketing, unattributed

Uncertainty handling:
- "INSUFFICIENT EVIDENCE" rather than guessing
- Never fabricate citations

For each claim: Author, Title, Venue, Year, DOI
Classify: [VERIFIED] / [NEEDS VERIFICATION]
```

---

## References

- `references/deep-research.md` — Complete framework, verification protocols, example prompts

---

## When to Use

- AI-assisted academic research
- Reducing hallucinations in research outputs
- Citation accuracy requirements
- Multi-source verification workflows
- Systematic literature reviews
