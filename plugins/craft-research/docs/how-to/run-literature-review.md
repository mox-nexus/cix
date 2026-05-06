# How to Run a Literature Review

A step-by-step guide for running a full literature review using the craft-research pipeline. By the end, you'll have verified findings with confidence levels, a convergence/divergence map, gap analysis, and an audited provenance chain — every finding traceable to a source quote.

## Prerequisites

- The `craft-research` plugin installed
- Source material accessible (PDFs on disk, URLs, or database search terms)
- A topic you want to investigate

## Choose Your Workflow

Not every research task needs the full pipeline. Match the workflow to the job:

| Task | Workflow | What You Skip |
|------|----------|---------------|
| Check a specific claim | Quick lookup: elicit → extract → scrutiny | synthesis, audit |
| Compare 3-5 papers on a question | Focused review: elicit → extract → scrutiny → synthesis | audit, four-layer gaps |
| Build a complete evidence base | Systematic review: full pipeline | Nothing |

When in doubt, start with a focused review. You can upgrade to systematic if the initial findings surface complexity.

This guide covers the **systematic review** — the full pipeline. Skip sections marked "systematic only" if you're running a focused review.

## Step 0: Scope with Elicit

Tell Claude you want to research a topic. The elicit agent draws out your research questions through dialogue — it asks, you generate. This is the generative step: you define what questions matter.

```
"I want to research how user control affects outcomes in human-AI collaboration"
```

Elicit runs three movements:

1. **Inquire** — What are you trying to learn? Why does it matter? What will you do with the findings?
2. **Bound** — What's in scope? What's out? How deep? (Systematic review vs quick check?)
3. **Source** — What papers have you already read? What databases should we search? What should we never cite?

Expect elicit to push back on vague questions. "How does AI affect learning?" is too broad. "Does providing hints vs direct answers affect learning retention in tutoring contexts?" is specific and answerable.

**What comes out:**
- `scope.md` — Your research questions, boundaries, source hierarchy, success criteria. This file is immutable after discourse — no downstream agent modifies it.
- `sources/inventory.md` — Every source identified, with metadata and tier estimates.

**Checkpoint:** Read both files. Are the research questions specific and answerable? Are the boundaries clear? Are sources identified? If not, keep talking to elicit.

## Step 1: Set Up the Workspace

Scaffold the `.research/` directory:

```bash
./setup.sh
```

This creates the workspace structure and adds `.research/` to `.gitignore`:

```
.research/
├── scope.md
├── PLAN.md
├── sources/
│   └── inventory.md
├── extraction/
├── verification/
├── synthesis/
└── audit/
```

Copy `scope.md` and `sources/inventory.md` into the workspace if they're not already there.

## Step 2: Collect Sources

If you have more than 1-2 sources, use recon to collect them mechanically. The orchestrator (main Claude) handles this step — no subagent.

The bridge pattern:

1. Read `sources/inventory.md` to see what needs fetching
2. Translate inventory entries into a recon config
3. Probe first — run with `limit: "1"`, inspect the raw JSONL
4. Write the normalize spec from the actual response shape
5. Run the full survey
6. Check `meta.yaml` for failures
7. Stage results for extraction

**For academic papers:** Use Semantic Scholar, arXiv, or OpenAlex API collectors.

**For PDFs on disk:** Use local sources with `$pdf2text` transform.

**For code repositories:** Use local sources with CLI collectors (`rg`, `git log`).

**Checkpoint:** Are there any failed collectors in `meta.yaml`? Are the normalized records populated (titles, abstracts, authors — not empty or truncated)? Fix failures before proceeding.

**Skip this step** when you have 1-2 files Claude can read directly.

## Step 3: Extract Claims

Launch the extract agent per source. Extraction runs the Claimify pipeline:

1. **Selection** — Filter out opinions, hedges, meta-commentary. Keep empirical findings, methodology, frameworks, measured outcomes.
2. **Disambiguation** — Resolve every "it", "this approach", "their study" to the specific entity.
3. **Decomposition** — Split "X and Y" into two atomic claims. Each claim is independently true or false.

For each atomic claim, extract produces a provenance unit:

```
### blaurock2025:c1
QUOTE: "user control had the strongest effect on co-production quality (β=0.507, p<0.001)"
LOCATION: Results, Section 4.2, paragraph 3
CLAIM: User control had the strongest effect on co-production quality among all tested factors (β=0.507, p<0.001) in the Blaurock et al. (2025) RCT with n=654 participants.
TIER: 1
```

The claim ID (`blaurock2025:c1`) persists through the entire pipeline. Verification, synthesis, and audit all reference it.

**Multiple sources can be extracted in parallel** — extraction is per-source with no cross-source dependencies.

**Output:** One file per source in `.research/extraction/`.

**Checkpoint:** Is every claim atomic (one fact)? Does every claim have a verbatim quote with a location? Are source tiers assigned? If extraction quality is low, re-extract before moving to verification.

## Step 4: Verify with CoVE

Launch the scrutiny agent per source after its extraction is complete. Verification uses Chain-of-Verification (CoVE) — the most validated hallucination reduction technique (+23% F1).

The protocol for each claim:

1. **Re-read the source independently** — scrutiny forms its own understanding before looking at the extraction
2. **Generate verification questions** — "Does the source contain this exact number?" "Is the direction correct?" "Is the scope correctly represented?"
3. **Answer questions from the source** — not from the extraction
4. **Compare** independent answers against the extracted claim
5. **Assign a verdict:**
   - **VERIFIED** — claim accurately represents the source
   - **CORRECTED** — core finding exists but numbers or details wrong (correction provided)
   - **REFUTED** — claim misrepresents the source
   - **INSUFFICIENT** — can't verify (source ambiguous, quote not found)

The independence is non-negotiable. If the verifier reads the extraction before the source, it degrades to confirmation bias.

**Output:** One file per source in `.research/verification/`.

**Checkpoint:** Review any REFUTED and INSUFFICIENT claims. Are the refutations justified? Do INSUFFICIENT claims need human review of the original paper? CORRECTED claims continue into synthesis with the corrected text.

## Step 5: Synthesize Across Sources

Launch the synthesis agent per research question, after all relevant verifications are complete. Synthesis uses only VERIFIED and CORRECTED claims — never unverified extractions.

For each research question, synthesis:

1. **Gathers** all verified claims relevant to the question
2. **Clusters** claims by sub-topic
3. **Maps convergence** — where multiple sources agree (the high-confidence findings)
4. **Maps divergence** — where sources disagree, with evidence weighting by study design, sample size, and tier
5. **Maps gaps** — what the question asks that no source addresses
6. **Writes findings** — each referencing specific claim IDs and assigned a confidence level

Confidence levels are structural, based on evidence patterns:

| Level | Evidence Pattern |
|-------|-----------------|
| HIGH | 3+ converging sources, Tier 1 included |
| MEDIUM | 2 converging sources, or single Tier 1 |
| LOW | Single source, or conflicting evidence |
| INSUFFICIENT | No verified claims address this |

Confidence can only decrease through the pipeline, never increase without new evidence. "This makes sense" is not evidence.

### Gap Analysis (systematic only)

For systematic reviews, synthesis also produces a four-layer gap analysis:

- **Theoretical** — Missing formal models, undefined constructs
- **Methodological** — Missing study designs (no longitudinal data, no RCT)
- **Empirical** — Missing populations, contexts, datasets
- **Practical** — Missing implementations, deployments

Gaps are as important as findings. They point to the most important future work.

**Output:** One file per research question in `.research/synthesis/`.

**Checkpoint:** Do the convergences make sense? Are divergences preserved (not silently resolved)? Are gaps named (not silently skipped)? Does every finding reference specific claim IDs?

## Step 6: Audit (Systematic Only)

Launch the audit agent after all synthesis is complete. The audit traces the provenance chain end-to-end — from findings back to source quotes.

Four phases:

1. **Chain completeness** — every finding references verified claims, every claim has an extraction record
2. **Chain accuracy** — sampled chains walked link by link (100% of HIGH findings, 50% of MEDIUM, 25% of LOW)
3. **Scope check** — no finding overstates the evidence, causal language matches study design
4. **Completeness** — all research questions addressed or gaps named

The verdict is binary: **SHIP** or **RETURN**.

**SHIP** means all checks pass. The provenance chain is intact.

**RETURN** specifies exactly what broke and which agent needs to fix it. The orchestrator routes the fix to the right agent and re-runs from that point.

**Output:** `.research/audit/report.md`

## What You Have at the End

A complete research workspace:

```
.research/
├── scope.md              # Your research questions and boundaries
├── PLAN.md               # Pipeline execution record
├── sources/inventory.md  # Source catalog with metadata
├── extraction/           # Per-source atomic claims with quotes
├── verification/         # Per-source verified claims with verdicts
├── synthesis/            # Per-question findings with provenance
└── audit/report.md       # Provenance audit with SHIP/RETURN
```

Every finding in `synthesis/` traces through the provenance chain:

```
Finding → verified claim IDs → verification verdicts → extracted quotes → source text
```

A reader can walk this chain backwards from any finding and verify every step. That's the point.

## Common Problems

**Elicit won't stop asking questions.** It's pushing for specificity. If you've answered enough to produce answerable research questions with clear boundaries, tell it you're ready to proceed.

**Extraction misses findings.** The extract agent reads the full source, but position bias means findings in late sections can be underweight. After extraction, scan the results and discussion sections for missed claims.

**Verification rubber-stamps everything.** Check that scrutiny is re-reading the source independently, not just pattern-matching against the extraction. If all verdicts are VERIFIED with no corrections, that's a signal to look more carefully.

**Synthesis fills gaps with inference.** Every finding must reference specific claim IDs. If a finding lacks claim references, it's speculation — not synthesis. Push back.

**Audit returns to the wrong agent.** The return routing table in the hub skill maps each failure type to the right agent. Scope inflation goes back to synthesis. Broken quotes go back to extract.
