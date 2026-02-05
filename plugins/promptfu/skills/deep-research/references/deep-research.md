# Deep Research Prompting

Engineering prompts for AI-assisted research with traceability, quality filtering, and hallucination reduction.

> **Sources:** Academic papers, platform documentation, empirical studies (2024-2026)

---

## The Problem

| Finding | Source |
|---------|--------|
| 50-90% of LLM responses not fully supported by cited sources | Nature Communications 2025 |
| 1 in 5 academic citations fabricated by GPT-4o | Deakin University study |
| 100+ hallucinated citations entered NeurIPS 2025 official record | Fortune |
| 66% DOI error rate in Gemini Deep Research | Omniscience Index benchmark |

**No single AI platform is sufficient for academic-quality research.**

---

## Platform Capabilities

### Hallucination Rates

| Platform | Rate | Best For |
|----------|------|----------|
| Perplexity | <3.5% | Quick fact-checking |
| Claude | ~6% | Synthesis, explicit uncertainty |
| GPT-5 | 8% | Multi-source analysis |
| Gemini Deep Research | 88%* | Comprehensive reports (verify all) |

*High accuracy (53%) but hallucinates supporting details.

### Citation Accuracy

| Platform | Accuracy | Caveat |
|----------|----------|--------|
| Claude | ~90% precision | 5-10% need manual validation |
| Perplexity | 78% claim-sourced | Heavy Reddit reliance in social mode |
| Gemini | 66% DOI errors | Study/year often correct, DOI wrong |
| OpenAI | 62% claim-sourced | Prefers SEO-spam over authoritative |

### Multi-Tool Strategy

| Phase | Tool | Why |
|-------|------|-----|
| **Discovery** | Elicit, Consensus | Academic DBs (138M+ papers) |
| **Verification** | Scite.ai | 1.5B citations classified |
| **Synthesis** | Claude | Lowest hallucination, explicit uncertainty |
| **Fact-check** | Perplexity | Best rate when constrained |
| **Reports** | Gemini Deep Research | Comprehensive, but verify everything |

---

## Validated Prompt Techniques

### What Works

| Technique | Evidence | Effect |
|-----------|----------|--------|
| **Chain-of-Verification (CoVe)** | Meta Research | +23% F1 |
| **Explicit abstention permission** | OpenAI research | Reduces confident wrong answers |
| **Tree-of-Thought** | Princeton/DeepMind | 74% vs 49% (CoT) vs 33% (standard) |
| **Source hierarchy specification** | Practitioner guides | 80-90% compliance |
| **Date range constraints** | Multiple studies | Reduces knowledge cutoff issues |

### What Doesn't Work

| Technique | Finding | Source |
|-----------|---------|--------|
| **Role prompting** | "Little to no effect on correctness" | Academic meta-analysis |
| **Examples with advanced models** | o1 performs worse with examples | Lenny's Newsletter 2025 |
| **Over-detailed prompts** | Counterproductive with sophisticated models | 1,500 paper analysis |

---

## The Deep Research Prompt Framework

### Structure

```
1. RESEARCH OBJECTIVE
   - Specific, measurable outcomes
   - Practical application context
   - Scope boundaries

2. PRIMARY QUESTIONS (3-5)
   - What are the validated [patterns/approaches] for [domain]?
   - How do [contexts] adapt [concepts] to [constraints]?
   - What are the measurable [impacts/trade-offs]?
   - What [failure modes] determine [outcomes]?
   - How does [theory] translate to [practice]?

3. SOURCE SPECIFICATION
   - Academic targets (foundational + recent)
   - Industry targets (companies, systems)
   - Quality tiers (explicit)

4. ANALYSIS REQUIREMENTS
   - Per source type
   - Cross-reference methodology

5. DELIVERABLES
   - Concrete outputs
   - Quality standards

6. VERIFICATION PROTOCOL
   - Hallucination reduction
   - Citation validation
```

---

## Chain-of-Verification (CoVe)

The most validated hallucination reduction technique.

### The Four Steps

1. **Draft** — Generate initial response
2. **Plan Verification** — Create fact-checking questions
3. **Independent Verification** — Answer questions *without seeing initial response*
4. **Final Response** — Generate verified output

### Prompt Pattern

```
Phase 1: Generate initial answer to [question].

Phase 2: Without referencing the answer, generate 5 verification
questions that would confirm or refute key claims in a response to [question].

Phase 3: Answer each verification question independently, citing sources.

Phase 4: Compare initial answer against verification answers.
Revise any claims that are contradicted or unsupported. Flag remaining
uncertainty as [UNVERIFIED].
```

---

## Source Quality Tiers

Specify explicitly in prompts.

| Tier | Source Type | Use For |
|------|-------------|---------|
| **1 (Gold)** | Peer-reviewed journals, A* conferences | Core claims, theoretical foundation |
| **2 (Silver)** | High-citation preprint (>50), industry with metrics | Supporting evidence |
| **3 (Bronze)** | Technical blogs, talks, documentation | Implementation details |
| **Exclude** | Marketing, LinkedIn posts, unverified claims | Never cite |

### Prompt Pattern

```
Source hierarchy (strictly enforce):
1. Peer-reviewed: ICSE, NeurIPS, ACL, Nature, Science (preferred)
2. Preprints: arXiv with >50 citations or established research groups
3. Technical: Official documentation, engineering blogs with author credentials
4. EXCLUDE: Marketing materials, LinkedIn posts, unattributed claims

For each source, state its tier. If only Tier 3 sources exist for a claim,
explicitly note "LIMITED EVIDENCE - industry sources only."
```

---

## Recency Enforcement

LLMs default to parametric (memorized) knowledge. Force recency explicitly.

### Prompt Pattern

```
Current date: ${DATE}

Recency requirements:
- STRONG PREFERENCE: Publications from past 2 years
- ACCEPTABLE: 3-4 years old if foundational or >100 citations
- FOUNDATIONAL ONLY: Older works for established theory

If citing older work, explain why newer sources don't exist or aren't relevant.
```

**Note:** Use `${DATE}` as a variable — supply current date at prompt execution time.

---

## Abstention Permission

Models hallucinate because "I don't know" scores zero in training. Grant explicit permission to abstain.

### Prompt Pattern

```
Uncertainty handling:
- If evidence is insufficient, state "INSUFFICIENT EVIDENCE" rather than guessing
- If sources conflict, state "CONFLICTING EVIDENCE: [Source A] claims X, [Source B] claims Y"
- If only weak sources exist, state "WEAK EVIDENCE (Tier 3 only)"
- Never fabricate citations to appear comprehensive
```

---

## Citation Requirements

### Prompt Pattern

```
Citation format (required for every factual claim):
- Full author names (not "et al." for <4 authors)
- Complete title
- Publication venue with volume/issue
- Year
- DOI or stable URL

For each citation, classify:
- [VERIFIED] - DOI resolves, content matches claim
- [NEEDS VERIFICATION] - Cannot confirm DOI or content
- [NO SOURCE] - Claim made without supporting citation
```

---

## Verification Protocol

### Pre-Research
1. Define explicit date ranges
2. Specify source hierarchy
3. Include abstention permission

### During Research
4. Require inline citations with DOIs
5. Apply CoVe (generate verification questions)
6. Require multi-source corroboration for key claims

### Post-Research
7. Spot-check citations with verification tools
8. Validate DOIs resolve to claimed content
9. Cross-reference against authoritative databases

### Prompt Pattern

```
After completing research:

1. List the 5 most important claims in the response
2. For each claim, provide:
   - The exact citation supporting it
   - Whether the DOI was verified to resolve
   - Confidence: HIGH (multiple Tier 1 sources) / MEDIUM (single Tier 1 or multiple Tier 2) / LOW (Tier 3 only)
3. List any claims that lack adequate sourcing as [UNVERIFIED]
```

---

## PRISMA-trAIce (2025)

For systematic literature reviews with AI assistance.

14-item extension to PRISMA 2020:
- Distinguishes human vs AI exclusions in flow diagram
- Requires documentation of AI tool identification
- Mandates human-AI interaction description
- Includes AI performance evaluation criteria

**Key finding:** "PRISMA method continues to exhibit clear superiority in reproducibility and accuracy... active participation of the researcher throughout the entire process is still crucial."

Use for: Formal literature reviews, thesis research, publication-quality surveys.

---

## Verification Tools

| Tool | Function | Access |
|------|----------|--------|
| **Scite.ai** | Smart citations (supporting/opposing/mentioning) | scite.ai |
| **SemanticCite** | 4-class verification (Supported/Partial/Unsupported/Uncertain) | arXiv:2511.16198 |
| **Elicit** | Academic paper search (138M+ papers) | elicit.com |
| **Consensus** | Research agreement visualization | consensus.app |
| **Citely** | Real-time citation verification | citely.ai |

---

## Complete Example Prompt

```markdown
# Research Task: [TOPIC]

## Current Date
${DATE}

## Objective
Conduct systematic analysis to [specific outcome] for [practical application].

## Primary Questions
1. What validated approaches exist for [X], supported by peer-reviewed evidence?
2. How do production systems implement [Y]?
3. What are the measurable trade-offs between [A] and [B]?

## Source Requirements

### Academic (target 10-15)
- Foundational: [Key papers if known]
- Recent: [Venues] proceedings from past 2-3 years
- Quality: Minimum 20 citations for preprints

### Industry (target 5-10)
- Companies: [Relevant organizations]
- Evidence: Production deployment required

### Source Hierarchy
1. Peer-reviewed (ICSE, NeurIPS, ACL)
2. High-citation preprint (>50)
3. Technical documentation
EXCLUDE: Marketing, unattributed claims

## Recency
- Prefer past 2 years
- 3-4 years if foundational
- Older only for established theory (explain why)

## Uncertainty Handling
- "INSUFFICIENT EVIDENCE" rather than guessing
- "CONFLICTING EVIDENCE" when sources disagree
- Never fabricate citations

## Citation Format
For each claim: Author(s), Title, Venue, Year, DOI
Classify: [VERIFIED] / [NEEDS VERIFICATION] / [NO SOURCE]

## Deliverables
1. [Specific output 1]
2. [Specific output 2]
3. Evidence gap analysis

## Verification
After completing:
1. List 5 most important claims with supporting citations
2. State confidence level for each (HIGH/MEDIUM/LOW)
3. List any [UNVERIFIED] claims explicitly
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| "Find all research on X" | Unbounded, invites fabrication | Specify source targets and limits |
| "Be comprehensive" | Encourages filling gaps with hallucination | "If fewer than N sources, state gap" |
| Trust any single platform | All have significant error rates | Multi-tool verification |
| Skip DOI validation | 66% error rate on Gemini alone | Spot-check critical citations |
| Role prompt for accuracy | No effect on correctness | Use CoVe instead |

---

## Sources

### Platform Research
- Nature Communications 2025 — LLM citation accuracy study
- Fortune — NeurIPS hallucinated citations
- Omniscience Index — Gemini reliability benchmark
- Deakin University — GPT-4o citation fabrication study

### Techniques
- Meta Research — Chain-of-Verification (arXiv:2309.11495)
- Princeton/DeepMind — Tree-of-Thought study
- OpenAI — "Why Language Models Hallucinate"
- Sebastian Raschka — "State of LLMs 2025"

### Frameworks
- PRISMA-trAIce 2025 (PMC12694947)
- SemanticCite (arXiv:2511.16198)
- Scite.ai Smart Citations

### Meta-Analysis
- Aakash Gupta — 1,500 papers on prompt engineering
- Lenny's Newsletter — Prompt engineering 2025
