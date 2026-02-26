---
name: mapping
description: "This skill should be used when the user asks to 'survey these sources', 'map what we have', 'create a map of contents', 'inventory these papers', or needs to understand what sources exist before going deep."
version: 0.1.0
---

# Mapping

> Survey the landscape. Synthesize what it says. Map how it connects.

Three stages: survey (what exists), synthesis (what it says, with proof), mapping (how it connects).

## Contents

- [Survey](#survey)
- [Synthesis](#synthesis)
- [Map of Contents](#map-of-contents)
- [Confidence Tiers](#confidence-tiers)
- [Anti-Patterns](#anti-patterns)

## Survey

Enumerate every source in the landscape. Skim — don't comprehend. Enough to classify, not enough to understand.

Per source:
- **Type**: paper, codebase, documentation, conversation, experience
- **Location**: file path, URL
- **Scope**: what it covers (one sentence)
- **Strength**: primary / secondary / tertiary / anecdotal
- **Confidence**: Solid / Probable / Uncertain / Unknown (see [Confidence Tiers](#confidence-tiers))

Survey both the evidence base (papers, research) AND the implementation (code, docs, architecture) when the project spans both. The ground truth tells you what matters.

## Synthesis

Extract claims from sources with provenance. Every claim traces to a verbatim quote.

### Quote-anchored claims

```
QUOTE: "exact verbatim text" (Source, section/page)
CLAIM: What this establishes
```

Quotes are verifiable by string matching. Paraphrases are where hallucination hides. Cross-source claims need quotes from BOTH sources.

### Extraction pipeline

Per source, four stages:

1. **Select** — passages with verifiable propositions. Skip hedges, boilerplate, methodology without findings.
2. **Disambiguate** — multiple interpretations and context doesn't resolve? **Exclude, don't guess.** Flag for deep reading.
3. **Decompose** — compound claims into atomic, self-contained, verifiable units. Don't over-decompose — noise degrades verification.
4. **Align** — each claim to its **specific supporting passage**, not the whole source.

### Factored verification

After extracting claims, verify with CoVe using **factored execution**:

1. **Draft** — produce claims/clusters/connections
2. **Question** — "Does Source X actually say Y?" "Is the effect size Z?"
3. **Verify independently** — re-read the source passage. **No access to the draft.**
4. **Revise** — correct based on verification

The independence in step 3 is the mechanism.

| Verify | Skip |
|--------|------|
| Effect sizes, specific numbers | Source type classifications |
| Causal claims | Author names, venues |
| Cross-source connections | Gap identifications |
| Claims anchoring downstream decisions | Methodological descriptions |

### Evidence weighting

When sources conflict, weight by: study design (RCT > observational > case study > review) > sample size > replication > recency > venue.

Report conflicts explicitly. "INSUFFICIENT EVIDENCE" over guessing. "CONFLICTING EVIDENCE" over picking a winner.

## Map of Contents

The output is a `map/` directory with an MOC and per-cluster synthesis files.

```
map/
├── MOC.md                    # index — inventory, clusters, connections, gaps
├── cluster-<name>.md         # per-cluster synthesis with quote-anchored claims
└── ...
```

**MOC.md** — the index. Source inventory, cluster summaries, connection map, gaps. References point to cluster files and to actual source locations.

**Cluster files** — the evidence. Quote-anchored claims, evidence weighting, confidence tiers, references to source material.

Downstream agents read MOC.md to orient → follow references to cluster files for evidence → follow source references for depth.

### MOC.md structure

```
## Inventory
[Each entry: type, location, scope, strength, confidence tier]

## Clusters
[Summary per cluster with link to cluster file]
[Coverage: dense / adequate / thin / gap]

## Connections
[Reinforcement, tension, dependency between clusters]
[Reading order]

## Gaps
[Coverage, evidence, connection, recency gaps]
[Impact on the project]
```

### Cluster file structure

```
# Cluster: <name>

## Sources
[Which sources contribute]

## Claims
[QUOTE + CLAIM format, each with confidence tier]

## Internal tensions
[Where sources disagree]

## Open questions
[What this cluster doesn't resolve]
```

### MOC types

| Context | What it maps |
|---------|-------------|
| Research + implementation | Evidence base AND codebase |
| Papers only | Sources by claim, evidence connections, gaps |
| Codebase only | Modules, dependencies, patterns |
| Existing content | What exists, reading paths, redundancies |

## Confidence Tiers

Structural, never verbalized. Tiers are **behavioral instructions** for downstream agents.

| Tier | Signal | Downstream instruction |
|------|--------|----------------------|
| **Solid** | Quote + factored verification passed | Trust directly |
| **Probable** | Quote extracted, not independently verified | Verify during deep reading |
| **Uncertain** | No quote — inferred from skim | MUST deep-read, may reclassify |
| **Unknown** | Source couldn't be read/parsed | Decide: acquire or proceed without |

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Paraphrase instead of quote | Verbatim text, verifiable by grep |
| Verifier sees the draft | Factored execution — verify in isolation |
| Over-decomposition | Atomic units, not smaller |
| Full-context verification | Align evidence at passage level |
| "I'm confident" | Structural basis only |
| Resolving ambiguity by guessing | Exclude and flag |
| Internal consistency = truth | Verify against source text |

## References

- `references/synthesis-techniques.md` — CoVe, Claimify, ReClaim, FActScore, self-correction boundaries
- `references/verification-methods.md` — 0.95^N problem, typed schemas, confidence calibration
