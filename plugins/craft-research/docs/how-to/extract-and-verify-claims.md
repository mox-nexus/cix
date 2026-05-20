# How to Extract and Verify Claims from a Paper

A focused guide for the extract-then-verify workflow on a single source. You start with a paper and end with a set of verified atomic claims, each traceable to a verbatim quote. This is the core loop of the provenance chain.

## When to Use This

- You have a specific paper and want to know exactly what it claims
- You're adding a source to an existing literature review
- You need verified claims before citing a paper in your own work
- You suspect a number or finding is misrepresented somewhere

## Prerequisites

- The source material accessible to Claude (PDF on disk, URL, or text)
- A `.research/` workspace (or you can create extraction/verification files anywhere)
- Optionally: a `scope.md` for relevance filtering

## Part 1: Extract

### Prepare the Source

Identify the source metadata first:

- Author(s), title, venue, year, DOI
- Source tier: **Tier 1** (peer-reviewed journal, A* conference), **Tier 2** (high-citation preprint, industry with metrics), or **Tier 3** (blog, talk, documentation)
- If you have a `scope.md`, note which research questions this source is relevant to

### Run the Claimify Pipeline

Ask Claude to extract claims from the source. The extract agent runs three stages:

**Stage 1 — Selection.** Filters non-factual content. Keeps empirical findings with data, methodological descriptions, defined frameworks, measured outcomes. Removes opinions ("We believe..."), hedges ("might suggest..."), meta-commentary ("As discussed above..."), and marketing language.

**Stage 2 — Disambiguation.** Resolves all references to specific entities. Every "it", "this approach", "the method", "their study" becomes a named entity. A claim should be understandable without reading the surrounding text.

| Before | After |
|--------|-------|
| "it improved accuracy" | "the CoVE protocol improved F1 accuracy" |
| "significant" | "statistically significant (p<0.05)" |
| "their study" | "Dhuliawala et al. (2023)" |

**Stage 3 — Decomposition.** Splits compound claims into atomic facts. Each atomic claim is independently true or false. No conjunctions joining separate findings.

| Before | After |
|--------|-------|
| "CoVE improves accuracy and reduces hallucination" | Claim 1: "CoVE improves F1 by 23%." Claim 2: "CoVE reduces hallucination rate." |
| "Results were significant across all conditions" | One claim per condition with its specific result |

### What the Output Looks Like

For each atomic claim, you get a provenance unit:

```markdown
### dhuliawala2023:c1
QUOTE: "Chain-of-Verification achieves a +23% improvement in F1 score"
LOCATION: Abstract, paragraph 1
CLAIM: Chain-of-Verification (CoVE) achieves a +23% F1 improvement over baseline verification methods.
TIER: 1
```

The claim ID (`dhuliawala2023:c1`) follows this claim through the entire pipeline. When you see it referenced in a synthesis finding later, you can trace it back here.

The extraction file goes to `.research/extraction/[source-name].md`.

### Check Your Extraction

Before moving to verification, check:

- [ ] Every claim has a **verbatim** QUOTE (not paraphrased)
- [ ] Every quote has a LOCATION (section, page, paragraph — enough to find it)
- [ ] Every claim is **atomic** (one fact, not "X and Y")
- [ ] Source tier is assigned
- [ ] Completeness: scan the results and discussion sections for findings not yet extracted

**Common extraction mistakes:**
- Extracting from the abstract only — findings in results sections have the actual effect sizes
- Paraphrasing instead of quoting — breaks the provenance chain at the first link
- Leaving compound claims unsplit — hides partial truth
- Missing negative results — "no significant effect found" is a finding worth extracting

## Part 2: Verify

### The Independence Requirement

This is the most important part, and the most counterintuitive. The scrutiny agent must re-read the source **without seeing the extraction first**, then compare. Reading the extraction first anchors judgment and defeats CoVE's +23% F1 improvement.

In practice, this means scrutiny:
1. Reads the source paper
2. Forms its own understanding of what the source says
3. Only then opens the extraction file
4. Compares claim by claim

### The CoVE Protocol Per Claim

For each extracted claim:

**1. Locate the quote.** Find the verbatim quote in the source. Is it exact? Sometimes extraction introduces small changes — a rounded number, a missing qualifier, a word substitution.

**2. Read surrounding context.** Read 2-3 paragraphs before and after the quote. Context can reverse meaning. A finding followed by "however, this result did not replicate in Study 2" changes everything.

**3. Generate verification questions.** 3-5 questions per claim that would confirm or refute it:

For factual claims:
- Does the source contain this exact number?
- Is the direction (positive/negative/neutral) correct?
- Is the sample size correctly reported?

For methodological claims:
- Does the source describe this method?
- Are conditions and steps correctly listed?

For scope claims:
- Does the source claim this level of generality?
- Are boundary conditions preserved?

For causal claims:
- Does the source claim causation or correlation?
- Is the causal language warranted by the study design?

**4. Answer from the source.** Answer each question by reading the source — not by checking the extraction.

**5. Compare and assign a verdict.**

| Verdict | When | Example |
|---------|------|---------|
| **VERIFIED** | Claim accurately represents the source | Number, direction, scope all match |
| **CORRECTED** | Core finding exists, but details wrong | "β=0.51" when source says "β=0.507" |
| **REFUTED** | Claim misrepresents the source | "positive effect" when source says "negative effect" |
| **INSUFFICIENT** | Can't verify | Quote not found, source ambiguous, methodology unclear |

### What the Output Looks Like

```markdown
### dhuliawala2023:c1 — VERIFIED
ORIGINAL CLAIM: Chain-of-Verification (CoVE) achieves a +23% F1 improvement over baseline verification methods.
VERIFICATION: Confirmed. Source states "Chain-of-Verification achieves a +23% improvement in F1 score" in Abstract, paragraph 1. Surrounding context in Section 4.2 confirms this is measured against same-context verification baseline.
No discrepancies found.
```

Or, when something's wrong:

```markdown
### dhuliawala2023:c3 — CORRECTED
ORIGINAL CLAIM: CoVE eliminates hallucination in long-form generation.
CORRECTION: Source says "reduces" not "eliminates." The exact quote: "significantly reduces hallucination rates." No claim of elimination is made.
CORRECTED CLAIM: CoVE significantly reduces hallucination rates in long-form generation.
EVIDENCE: Section 5.1, paragraph 2.
```

The verification file goes to `.research/verification/[source-name].md`.

### Check Your Verification

- [ ] Every claim has a verdict
- [ ] CORRECTED claims have the corrected text and evidence
- [ ] REFUTED claims explain what the source actually says
- [ ] INSUFFICIENT claims state why verification failed and what to do next
- [ ] No "looks right" verdicts — every VERIFIED has evidence

**Red flags that verification was too soft:**
- 100% VERIFIED rate with no corrections — not impossible, but suspicious
- Verification evidence restates the extraction rather than citing the source independently
- No verification questions generated — just "confirmed"

## What You Have at the End

Two files:

1. **Extraction** (`.research/extraction/source-name.md`) — Atomic claims with verbatim quotes, locations, and tiers
2. **Verification** (`.research/verification/source-name.md`) — Each claim with a verdict and evidence

Together, these form the first three links of the provenance chain:

```
Source text → verbatim quote → extracted claim → verification verdict
```

From here, verified claims (VERIFIED and CORRECTED) can flow into synthesis for cross-source integration. Or you can use them directly — cite a verified claim with confidence because you know the quote exists, the claim follows from it, and an independent check confirmed it.

## Working with Multiple Papers

When extracting and verifying multiple papers for the same project:

- **Extract in parallel.** Each extraction is per-source with no cross-source dependencies.
- **Verify after extraction.** A source must be fully extracted before verification starts (scrutiny needs the extraction file).
- **Verify in parallel.** Once extracted, multiple sources can be verified concurrently.
- **Use consistent claim IDs.** The pattern `[source-short-name]:c[N]` keeps claims traceable across the workspace.

The order matters: always extract-then-verify per source, never the reverse. Verification without extraction is just reading. Extraction without verification is unconfirmed.
