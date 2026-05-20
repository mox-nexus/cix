# Tutorial: Your First Research Pipeline

In this tutorial, you'll run the craft-research pipeline on a real topic — from scoping to verified synthesis. You'll end with findings grounded in a provenance chain: every finding traceable to a source quote, through extraction, verification, and synthesis.

**Time:** 20-30 minutes
**What you need:** The `craft-research` plugin installed, and 2-3 papers on a topic you're interested in (PDFs on disk or accessible URLs)

## The Scenario

You want to answer a specific research question: **"Does independent verification reduce errors in AI-generated research?"**

We'll use two papers that address this directly:
- Dhuliawala et al. (2023) — *Chain-of-Verification Reduces Hallucination in Large Language Models* (Meta Research)
- Metropolitansky & Larson (2025) — *Towards Effective Extraction and Evaluation of Factual Claims* (ACL 2025)

You can substitute your own papers and topic. The pipeline works the same way.

## Step 1: Scope the Research (5 minutes)

Start by telling Claude what you want to research:

```
I want to research whether independent verification reduces errors in
AI-generated research outputs. I have two papers: the CoVE paper
(Dhuliawala et al. 2023) and the Claimify paper (Metropolitansky &
Larson 2025).
```

The elicit agent will ask you questions across three movements:

**Inquire** — What specifically are you trying to learn? Why does this matter?

Your answers might be: "I want to know if there's empirical evidence that verification done independently — where the verifier doesn't see the original output — catches more errors than same-context checking. I'm building a research pipeline and need to decide whether independent verification is worth the extra cost."

**Bound** — What's in scope? What level of depth?

"Focused review — I'm comparing two papers, not surveying the whole field. I care about error reduction rates and the mechanism (why independence matters). I don't need a four-layer gap analysis."

**Source** — What do you already know?

"I know CoVE is from Meta Research and claims a +23% F1 improvement. I've heard Claimify achieves 99% claim entailment. I haven't read either paper in detail."

When elicit has enough, it writes two files:

**`scope.md`** — Your research questions, boundaries, and success criteria. It might look like:

```markdown
## Research Questions
1. What is the measured effect of independent verification on error
   reduction in AI-generated claims?
2. What is the mechanism by which independence improves verification?

## Boundaries
- In scope: Empirical results from CoVE and Claimify papers
- Out of scope: General hallucination literature, non-verification approaches
- Depth: Focused review (2 papers)
- Intent: Inform pipeline design decision

## Success Criteria
- Effect sizes extracted and verified from both papers
- Mechanism of independence identified and grounded in evidence
```

**`sources/inventory.md`** — Your source list with metadata and tier estimates.

**Checkpoint:** Read both files. Do the research questions capture what you actually want to learn? If not, tell elicit what's missing. Once confirmed, `scope.md` is locked — no downstream agent changes it.

## Step 2: Set Up the Workspace (1 minute)

Create the `.research/` directory structure. If a setup script exists, run it:

```bash
./setup.sh
```

Or create the directories manually:

```bash
mkdir -p .research/{sources,extraction,verification,synthesis,audit}
```

Copy `scope.md` and `sources/inventory.md` into the workspace. Add `.research/` to your `.gitignore`.

## Step 3: Extract Claims from Paper 1 (5 minutes)

Ask Claude to extract claims from the first paper:

```
Extract claims from the CoVE paper (Dhuliawala et al. 2023).
Use the scope in .research/scope.md for relevance filtering.
```

The extract agent reads the full paper and runs the Claimify pipeline. Watch for these three stages:

**Selection** — It filters out background review, related work summaries, and hedged speculation. Only empirical findings, methodology, and defined constructs pass through.

**Disambiguation** — References like "the proposed method" become "Chain-of-Verification (CoVE)." Every pronoun resolved.

**Decomposition** — Compound findings split into atoms. "CoVE improves accuracy and reduces hallucination" becomes two separate claims.

The output lands in `.research/extraction/dhuliawala2023.md`. Open it and check a few claims:

```markdown
### dhuliawala2023:c1
QUOTE: "Chain-of-Verification achieves a +23% improvement in F1 score
        compared to same-context verification"
LOCATION: Section 4.2, Results
CLAIM: CoVE achieves a +23% F1 improvement over same-context
       verification baselines.
TIER: 1
```

**What to check:**
- Are quotes verbatim (not paraphrased)?
- Is each claim atomic (one fact)?
- Are locations specific enough to find the quote?

Now extract the second paper the same way. Both extractions can run in parallel since they're independent.

## Step 4: Verify Claims (5-7 minutes)

After both papers are extracted, launch verification:

```
Verify the extracted claims from dhuliawala2023 using CoVE.
```

The scrutiny agent runs a specific protocol:

1. **Reads the source paper independently** — forms its own understanding before looking at the extraction
2. **Generates verification questions** for each claim — "Does the source contain this exact number?" "Is the comparison baseline correctly identified?"
3. **Answers from the source** — not from the extraction
4. **Compares** and assigns a verdict

The output lands in `.research/verification/dhuliawala2023.md`:

```markdown
### dhuliawala2023:c1 — VERIFIED
ORIGINAL CLAIM: CoVE achieves a +23% F1 improvement over same-context
                verification baselines.
VERIFICATION: Confirmed. Section 4.2 states "+23% improvement in F1"
              comparing independent verification against same-context.
              Baseline is same-model verification without independence.
```

You might also see corrections:

```markdown
### dhuliawala2023:c4 — CORRECTED
ORIGINAL CLAIM: CoVE works across all model sizes.
CORRECTION: Source tests on 7B and 65B parameter models. No claim
            of universality. Results shown for specific model sizes only.
CORRECTED CLAIM: CoVE shows F1 improvements on both 7B and 65B
                 parameter language models.
EVIDENCE: Table 3, Section 4.3
```

Run verification on the second paper as well.

**What to check:**
- Any REFUTED claims? These are claims the extraction got wrong.
- Any INSUFFICIENT claims? These may need you to check the original PDF.
- Are the verdicts evidence-based, or just "confirmed" with no detail?

## Step 5: Synthesize (5 minutes)

With verified claims from both papers, run synthesis per research question:

```
Synthesize verified claims from both papers to answer the research
questions in scope.md.
```

The synthesis agent gathers all VERIFIED and CORRECTED claims relevant to each question, then maps convergence and divergence.

The output lands in `.research/synthesis/` — one file per research question. For the first question about measured effects:

```markdown
# Synthesis: Effect of Independent Verification on Error Reduction

## Findings

### Finding 1: Independent verification measurably reduces errors
CLAIM: Independent verification achieves statistically significant
       error reduction compared to same-context checking.
EVIDENCE:
  - [dhuliawala2023:c1] — +23% F1 improvement (CoVE) — VERIFIED
  - [metropolitansky2025:c2] — 99% claim entailment (Claimify) — VERIFIED
CONFIDENCE: MEDIUM — 2 converging Tier 1 sources

## Convergence Map
- Both papers find that structuring the verification process
  (independence in CoVE, three-stage pipeline in Claimify)
  improves accuracy over unstructured approaches.

## Divergence Map
- CoVE measures verification accuracy (F1).
  Claimify measures extraction fidelity (entailment).
  Different metrics — convergent direction, but not directly comparable.

## Gap Map
- No head-to-head comparison of CoVE vs Claimify exists
- No studies test these techniques in systematic review contexts
  (both test general Q&A / fact-checking)
```

Notice: the finding is MEDIUM confidence, not HIGH — because only two sources converge. HIGH requires 3+ sources. Confidence tracks evidence, not plausibility.

**What to check:**
- Does every finding reference specific claim IDs?
- Are the confidence levels justified by the evidence pattern?
- Are gaps named (the things no source addresses)?

## Step 6: Review the Provenance Chain

You now have a complete chain for each finding. Pick one and trace it:

```
Finding: "Independent verification achieves significant error reduction"
  ↑ supported by
[dhuliawala2023:c1] — VERIFIED (verification/dhuliawala2023.md)
  ↑ extracted from
QUOTE: "+23% improvement in F1 score" (extraction/dhuliawala2023.md)
  ↑ found in
Source: Dhuliawala et al., Section 4.2
```

Every link is checkable. You can open each file and confirm the chain holds. That's evidentiary provenance — the central design constraint of the pipeline.

For a focused review like this one, you can stop here. For a systematic review, you'd run the audit agent next, which walks these chains programmatically and makes a SHIP/RETURN decision.

## What You Built

```
.research/
├── scope.md                              # Your questions and boundaries
├── sources/inventory.md                  # Source catalog
├── extraction/
│   ├── dhuliawala2023.md                 # Atomic claims with quotes
│   └── metropolitansky2025.md
├── verification/
│   ├── dhuliawala2023.md                 # Verified claims with verdicts
│   └── metropolitansky2025.md
└── synthesis/
    ├── effect-of-verification.md         # Findings for question 1
    └── mechanism-of-independence.md      # Findings for question 2
```

Every finding in synthesis traces back through verification and extraction to a verbatim source quote. The workspace is the audit trail — open any file and follow the chain.

## Next Steps

**Add more sources.** Run extract and verify on additional papers. Re-run synthesis to incorporate the new evidence. If 3+ sources converge, findings can upgrade to HIGH confidence.

**Run the full pipeline.** For high-stakes research (publication, policy decisions), add the audit step. The audit agent walks provenance chains end-to-end and makes a binary SHIP/RETURN verdict.

**Use the claims.** Verified claims with provenance are safe to cite. You know the quote exists, the claim follows from it, and an independent check confirmed it. That's more than most AI-generated citations can say.

## Troubleshooting

**"Elicit keeps asking questions."** It's pushing for specificity. If your research questions are already answerable and bounded, tell it you're ready to proceed.

**"Extraction produced too few claims."** Check whether the extract agent read the full paper or only the abstract. Effect sizes live in results sections, limitations in discussion sections. Ask for a completeness check.

**"Everything is VERIFIED."** A 100% verification rate is possible but uncommon. Check that scrutiny re-read the source independently and generated real verification questions, not just "confirmed."

**"Synthesis confidence seems too low."** Confidence is structural. A single study — even a great one — is MEDIUM at best. That's by design. More sources with convergent findings increase confidence. Reasoning alone does not.
