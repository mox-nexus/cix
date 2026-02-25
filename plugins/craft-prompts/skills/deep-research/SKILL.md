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

## Composed Research Instrument

The full research prompt structure. Not a template to fill — a **thinking instrument** that decomposes research into verifiable parts.

```markdown
# Research Instrument: [TOPIC]

## Date & Scope
Current date: [DATE]
Scope boundary: [what's IN and what's OUT]

## Research Mandate
You are conducting systematic research. Your obligation is to the evidence, not to comprehensiveness. An honest gap is worth more than a fabricated bridge.

## Pillar Decomposition
Break the research into 3-5 focused pillars. Each pillar has:
- A specific question (not "tell me about X")
- Source targets (where answers likely live)
- Expected evidence type (empirical, theoretical, case study, practitioner report)

### Pillar 1: [QUESTION]
Sources: [targeted venues, authors, systems]
Evidence type: [empirical | theoretical | case study | practitioner]

### Pillar 2: [QUESTION]
...

## Null Hypotheses
For each pillar, state the steel-man counterargument:
- Pillar 1 null: "[The opposite of what you expect to find]"
- Pillar 2 null: "..."

If evidence supports the null hypothesis, report it. Do not suppress inconvenient findings.

## Source Hierarchy (strictly enforce)
1. Peer-reviewed journals, A* conferences (core claims)
2. High-citation preprint >50 citations (supporting evidence)
3. Technical documentation, engineering blogs with credentials (implementation)
EXCLUDE: Marketing, LinkedIn posts, unattributed claims, SEO content

## Uncertainty Handling
- "INSUFFICIENT EVIDENCE" rather than guessing
- "CONFLICTING EVIDENCE: [A] claims X, [B] claims Y" when sources disagree
- "WEAK EVIDENCE (Tier 3 only)" when no authoritative sources exist
- Never fabricate citations to appear comprehensive

## Recency
- STRONG PREFERENCE: Past 2 years
- ACCEPTABLE: 3-4 years if foundational (>100 citations)
- FOUNDATIONAL ONLY: Older for established theory (explain why)

## Traceability Matrix
For every factual claim, provide:

| Claim | Source | Tier | Confidence | Falsification Condition |
|-------|--------|------|------------|------------------------|
| [claim] | [author, title, venue, year, DOI] | [1/2/3] | [HIGH/MEDIUM/LOW] | [what would make this wrong] |

Confidence levels:
- HIGH: Multiple Tier 1 sources, replicated
- MEDIUM: Single Tier 1 or multiple Tier 2
- LOW: Tier 3 only or single unreplicated study

## Anti-Bias Safeguards
- Report negative results (what you searched for and didn't find)
- Distinguish evidence levels explicitly (don't mix Tier 1 and Tier 3 as equal)
- Flag commercial interest (vendor-sponsored research, company blogs promoting own products)
- State search terms used (so the research is reproducible)

## Deliverables
1. Findings per pillar (with inline traceability)
2. Evidence table (the traceability matrix, filled)
3. Gaps identified (what couldn't be answered and why)
4. Synthesis (cross-pillar connections, emergent patterns)
5. Confidence summary (what's solid, what's shaky, what's missing)
```

---

## Multi-Agent Research Workflow

When research spans multiple disciplines or lenses, decompose across agents rather than overloading one.

### When to Decompose

| Situation | Approach |
|-----------|----------|
| Single domain, clear questions | One agent, multiple pillars |
| Cross-disciplinary (theory + practice + design) | Multiple agents, one lens each |
| Adversarial verification needed | Two agents: advocate + critic |
| Breadth survey | Multiple agents, then synthesis |

### Lens Decomposition

Each agent gets a **perspective**, not a slice. The same topic seen through different lenses produces richer findings than dividing the topic into non-overlapping chunks.

Example: Researching "control patterns for human-AI systems"
- Agent 1 (Theory lens): Control theory, cybernetics, stability
- Agent 2 (Systems lens): Software control planes, reconciliation, protocols
- Agent 3 (Human lens): Transparency, agency, cognitive ergonomics

Overlapping coverage is a feature — it reveals where lenses agree (high confidence) and where they diverge (interesting tensions).

### Agent Prompt Structure

Each agent receives:
1. The composed research instrument (above) with its specific pillars
2. A lens declaration: "You are researching from the perspective of [LENS]"
3. The structured output schema (below) so results are composable

### Synthesis Guidance

The orchestrator (you) does the following with multi-agent results:
1. **Convergence map**: Where do multiple lenses agree? (High confidence claims)
2. **Divergence map**: Where do lenses disagree or see different things? (Interesting tensions)
3. **Gap map**: What did no lens cover? (Blind spots)
4. **Cross-references**: Findings from Agent A that inform/challenge Agent B
5. **Integrated model**: The synthesis that no single lens could produce

---

## Structured Output Schema

What comes back from each research agent. This structure makes multi-agent results composable.

```markdown
# Research Report: [TOPIC] — [LENS] Perspective

## Executive Summary
[3-5 sentences: what was found, what wasn't, confidence level]

## Findings

### Finding 1: [TITLE]
**Claim:** [precise statement]
**Evidence:** [source with full citation]
**Confidence:** HIGH | MEDIUM | LOW
**Falsification:** [what would invalidate this]
**Implications:** [so what — why this matters for the research question]

### Finding 2: ...

## Evidence Table

| # | Claim | Source | Tier | Confidence | Falsification |
|---|-------|--------|------|------------|---------------|
| 1 | ... | ... | ... | ... | ... |

## Gaps
- [What was searched for but not found]
- [Questions that remain unanswered]
- [Areas where only weak evidence exists]

## Negative Results
- [Hypotheses that were not supported]
- [Expected findings that didn't materialize]

## Cross-References
- [Connections to other research pillars/lenses]
- [Findings that might inform adjacent research]

## Search Methodology
- Databases/tools used: [list]
- Search terms: [list]
- Date range: [range]
- Exclusion criteria: [what was filtered out and why]
```

---

## Quick Prompt Pattern

For single-agent, fast research (when the full instrument is overkill):

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
- Multi-agent research decomposition across lenses
