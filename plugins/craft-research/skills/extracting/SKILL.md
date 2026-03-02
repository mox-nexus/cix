---
name: extracting
description: "This skill should be used when the user asks to 'extract claims from a paper', 'claimify this source', 'decompose into atomic claims', 'pull findings from this paper', or needs structured claim extraction with source quotes and evidence tiers."
version: 0.1.0
---

# Extracting

> Every claim traces to a quote. Every quote has a location. No exceptions.

Extraction is the foundation of evidentiary provenance. A claim without a source quote is an assertion. A source quote without a location is unverifiable. The entire downstream pipeline — verification, synthesis, audit — depends on extraction quality.

## Contents

- [The Provenance Unit](#the-provenance-unit)
- [The Claimify Pipeline](#the-claimify-pipeline)
- [Source Tiers](#source-tiers)
- [Extraction Protocol](#extraction-protocol)
- [Output Format](#output-format)
- [Position Bias Mitigation](#position-bias-mitigation)
- [Anti-Patterns](#anti-patterns)

## The Provenance Unit

The atomic unit of research is a **claim with provenance**:

```
QUOTE: "[verbatim text from source]"
LOCATION: [page, section, paragraph — enough to find it]
CLAIM: [atomic, verifiable statement derived from the quote]
TIER: [1-Gold | 2-Silver | 3-Bronze]
```

The quote is verbatim. The claim is your interpretation. Keeping them separate lets verification check whether the claim actually follows from the quote.

## The Claimify Pipeline

Three stages. Each serves a distinct purpose. Do not skip stages.

### Stage 1: Selection

Filter non-factual content before processing:

**Keep:**
- Empirical findings with data
- Methodological descriptions
- Defined constructs and frameworks
- Measured outcomes with effect sizes

**Remove:**
- Opinions ("We believe...", "It seems...")
- Meta-commentary ("As discussed above...")
- Hedged speculation ("might", "could potentially")
- Marketing language, promotional claims

### Stage 2: Disambiguation

Resolve all references to specific entities:

| Ambiguous | Disambiguated |
|-----------|---------------|
| "it" | "the CoVE protocol" |
| "this approach" | "chain-of-verification" |
| "the method" | "dual-LLM cross-critique" |
| "their study" | "Dhuliawala et al. (2023)" |
| "significant" | "statistically significant (p<0.05)" or "practically significant (d=0.86)" |

Every pronoun, every "this/that", every abbreviation — resolved on first occurrence. A claim that requires context from elsewhere in the paper to understand is not yet atomic.

### Stage 3: Decomposition

Split compound claims into atomic facts:

| Compound | Atomic |
|----------|--------|
| "CoVE improves accuracy and reduces hallucination" | "CoVE improves F1 by 23%" AND "CoVE reduces hallucination rate" |
| "The system is fast and accurate" | "System latency is X ms" AND "System accuracy is Y%" |
| "Results were significant across all conditions" | One claim per condition with its specific result |

Each atomic claim is independently true or false. No conjunctions joining separate facts.

## Source Tiers

Assign on extraction. Tier determines how the claim can be used downstream.

| Tier | Source Type | Downstream Use |
|------|------------|----------------|
| **1 (Gold)** | Peer-reviewed journal, A* conference | Core claims, theoretical foundation |
| **2 (Silver)** | High-citation preprint (>50), industry with metrics | Supporting evidence |
| **3 (Bronze)** | Technical blogs, talks, documentation | Implementation details only |
| **Exclude** | Marketing, LinkedIn, unattributed | Never extract — flag and skip |

When uncertain about tier: check venue, citation count, author credentials. If still uncertain, assign the lower tier.

## Extraction Protocol

### Per Source

1. **Identify source metadata**: author, title, venue, year, DOI
2. **Read the full source** — not just abstract
3. **Stage 1 (Select)**: Mark factual claims, skip non-factual
4. **Stage 2 (Disambiguate)**: Resolve all references
5. **Stage 3 (Decompose)**: Split compounds into atoms
6. **For each atomic claim**: Record QUOTE + LOCATION + CLAIM + TIER
7. **Count**: Report total claims extracted, broken down by tier

### What to Extract

| Extract | Skip |
|---------|------|
| Findings with effect sizes | Background/context reviews |
| Methodological innovations | Literature review summaries |
| Defined frameworks with components | Acknowledgments |
| Measured outcomes | Future work speculation |
| Stated limitations | Related work (extract from originals instead) |
| Replication results | Reformulations of others' work |

### Handling Uncertainty

- If a quote is ambiguous, extract the conservative interpretation
- If a finding lacks effect sizes, note "NO EFFECT SIZE REPORTED"
- If methodology is unclear, note "METHODOLOGY UNCLEAR: [what's missing]"
- Never infer what wasn't stated — extraction is faithful, not creative

## Output Format

Per-source extraction file:

```markdown
# Extraction: [Source Short Name]

## Source
- **Author**: [full names]
- **Title**: [complete title]
- **Venue**: [journal/conference]
- **Year**: [year]
- **DOI**: [doi or URL]
- **Tier**: [1/2/3]

## Claims

### [source]:c1
QUOTE: "[verbatim]"
LOCATION: [section, page, paragraph]
CLAIM: [atomic statement]
TIER: [1/2/3]

### [source]:c2
QUOTE: "[verbatim]"
LOCATION: [section, page, paragraph]
CLAIM: [atomic statement]
TIER: [1/2/3]

...

## Summary
- Total claims: [N]
- Tier 1: [n] | Tier 2: [n] | Tier 3: [n]
- Key findings: [1-3 sentence summary of most important claims]
```

Claim IDs follow the pattern `[source-short-name]:c[N]`. These IDs persist through the entire pipeline — verification, synthesis, and audit reference them.

## Position Bias Mitigation

LLMs weight information by position, not importance. Countermeasures:

1. **Extract per-source first** — never synthesize across sources during extraction
2. **Full source reading** — don't stop after abstract/introduction
3. **Explicit completeness check** — after extraction, scan for findings in results/discussion that were missed
4. **No ordering effects** — extraction quality shouldn't depend on which source was read first

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|--------------|-------------|------------|
| Extracting from abstracts only | Misses nuance, limitations, actual effect sizes | Read full paper |
| Paraphrasing instead of quoting | Breaks provenance — can't verify | Verbatim quotes |
| Compound claims | Hides partial truth | Decompose to atoms |
| Inferring beyond the text | Introduces hallucination at source | Extract only what's stated |
| Skipping tier assignment | Downstream can't weight evidence | Assign tier on extraction |
| "The authors found..." | Attribution without quote | QUOTE + CLAIM separation |

## References

- `references/claimify.md` — Claimify pipeline details, dual-LLM cross-critique, worked examples
