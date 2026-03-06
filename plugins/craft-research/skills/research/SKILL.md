---
name: research
description: "This skill should be used when the user asks to 'research this topic', 'analyze these papers', 'do a literature review', 'synthesize research', 'extract claims', 'verify citations', 'scope a research project', or needs systematic research with evidentiary provenance."
version: 0.3.0
---

# Research

> Every claim traceable to a source quote, through discourse, extraction, verification, and synthesis. No exceptions.

This is the hub skill for systematic research. It defines the pipeline, workspace, and orchestration protocol. Spoke skills contain the methodology for each phase. Agents execute the methodology.

## Contents

- [The Thesis](#the-thesis)
- [The Provenance Chain](#the-provenance-chain)
- [Routing](#routing)
- [The Pipeline](#the-pipeline)
- [The Workspace](#the-workspace)
- [The Orchestration Protocol](#the-orchestration-protocol)
- [Anti-Patterns](#anti-patterns)

## The Thesis

Research integrity lives or dies on **evidentiary provenance** — the unbroken chain from finding to source quote. Every claim traces to a quote. Every quote has a location. Confidence can only decrease through the pipeline, never increase without new evidence.

The interaction pattern determines the outcome. Elicit draws out the inquiry — the human's generative step. Agents extract, verify, and synthesize. Human reviews and decides. The human retains the generative step throughout: defining what questions matter, evaluating whether answers are sufficient, and deciding what to do with findings.

## The Provenance Chain

The atomic unit of research is a claim with provenance:

```
Source text (original paper)
  → Source quote (verbatim, with location)       [extract]
  → Extracted claim [source:cN]                  [extract]
  → Verification verdict                         [scrutiny]
  → Synthesized finding with claim references     [synthesis]
  → Audit trace                                  [audit]
```

Each layer transforms the representation. Each transformation is verifiable. The audit walks the chain in reverse — from finding to source — confirming every link holds.

### What Breaks Provenance

| Break | Where | Result |
|-------|-------|--------|
| Paraphrasing instead of quoting | Extraction | Can't verify claim against source |
| Rubber-stamp verification | Verification | False confidence propagates |
| Citing unverified claims | Synthesis | Provenance gap |
| Scope inflation | Synthesis | Misleading conclusions |
| Missing chain links | Any stage | Finding ungrounded |

## Routing

One hub triggers. It routes to specialized skills on demand.

| Need | Agent | Spoke Skill |
|------|-------|-------------|
| Scope research inquiry | elicit | [eliciting](../eliciting/SKILL.md) |
| Extract claims from sources | extract | [extracting](../extracting/SKILL.md) |
| Verify claims against sources | scrutiny | [verifying](../verifying/SKILL.md) |
| Integrate across sources | synthesis | [synthesizing](../synthesizing/SKILL.md) |
| Trace provenance, ship/return | audit | [auditing](../auditing/SKILL.md) |

## The Pipeline

One pipeline. Every research project follows it. The orchestrator (main Claude) adapts it per project. Human checkpoints between phases.

```
elicit — draws out research questions, boundaries, sources
  | produces scope.md + sources/inventory.md
  |
  | setup — scaffold .research/ workspace
  |
  | ─── per source ─── (parallelizable)
  | extract — reads source, extracts atomic claims with quotes
  |
  | ─── per source ─── (parallelizable, after extraction)
  | scrutiny — CoVE: independently verifies claims against source
  |
  | ─── per research question ─── (after all verification)
  | synthesis — integrates verified claims, maps convergence/divergence/gaps
  |
  | audit — traces provenance chain end-to-end, ship/return verdict
  > Human reviews, decides next steps
```

### Step 0: Discourse (elicit)

Elicit draws out the research inquiry through dialogue. The human has the domain knowledge. Elicit asks and sharpens until the research questions are specific, answerable, and bounded.

Three movements: **Inquire** (what are you trying to learn?) → **Bound** (what's in scope, what's out?) → **Source** (what do you already know, where might you look?).

**Agent**: elicit | **Skills**: `research`, `eliciting`
**Output**: `scope.md` + `sources/inventory.md`

`scope.md` is co-created but human-owned. No downstream agent modifies it. This is the research equivalent of rhetoric's `ground-truth.md`.

Use the scope template: `templates/scope-template.md`

**Gate: discourse → setup**
- [ ] Research questions are specific and answerable
- [ ] Boundaries defined (what's in, what's out)
- [ ] Source hierarchy specified (where to look)
- [ ] Sources identified and inventoried
- [ ] Success criteria stated (when is the research "done enough"?)
- [ ] Null hypotheses articulated

### Step 1: Setup (script)

Scaffold the `.research/` workspace and add it to `.gitignore`.

```bash
./setup.sh [workspace-path]
```

Creates workspace directory structure and ensures `.research/` is in `.gitignore`. Default path is `.research/` in the project root.

**Gate: setup → extraction**
- [ ] Workspace directory exists with all subdirectories
- [ ] `.research/` added to `.gitignore`
- [ ] `scope.md` written to workspace root

### Step 2: Extraction (extract)

Extract atomic claims from each source using the Claimify pipeline.

**Agent**: extract | **Skills**: `research`, `extracting`
**Input**: source material + scope.md (for relevance filtering)
**Output**: `.research/extraction/[source-name].md`

Per source: Selection → Disambiguation → Decomposition → QUOTE + CLAIM + TIER for each atomic claim.

**Parallelizable**: multiple sources can be extracted concurrently.

**Gate: extraction → verification**
- [ ] Every claim has a verbatim QUOTE with LOCATION
- [ ] Every claim is atomic (one fact per claim)
- [ ] Source tier assigned to every claim
- [ ] Claim IDs assigned ([source:cN])
- [ ] Extraction files written to `.research/extraction/`

### Step 3: Verification (scrutiny)

Independently verify each extracted claim using CoVE.

**Agent**: scrutiny | **Skills**: `research`, `verifying`
**Input**: `.research/extraction/` files + original sources
**Output**: `.research/verification/[source-name].md`

Per claim: re-read source independently → generate verification questions → answer from source → compare → verdict (VERIFIED / CORRECTED / REFUTED / INSUFFICIENT).

**Parallelizable**: multiple sources can be verified concurrently (after their extraction is complete).

**Gate: verification → synthesis**
- [ ] Every claim has a verdict
- [ ] CORRECTED claims have corrected text
- [ ] REFUTED claims have refutation with source evidence
- [ ] INSUFFICIENT claims flagged for human review
- [ ] Verification files written to `.research/verification/`

### Step 4: Synthesis (synthesis)

Integrate verified claims to answer research questions.

**Agent**: synthesis | **Skills**: `research`, `synthesizing`
**Input**: `.research/verification/` files + `scope.md`
**Output**: `.research/synthesis/[question-slug].md`

Per research question: gather relevant verified claims → cluster → map convergence/divergence/gaps → write findings → assign confidence.

**Gate: synthesis → audit**
- [ ] Every finding references specific verified claim IDs
- [ ] Convergence, divergence, and gap maps complete
- [ ] Confidence levels based on evidence patterns
- [ ] Four-layer gap analysis (theoretical, methodological, empirical, practical)
- [ ] Synthesis files written to `.research/synthesis/`

### Step 5: Audit (audit)

Trace provenance chain end-to-end. Ship or return.

**Agent**: audit | **Skills**: `research`, `auditing`
**Input**: all `.research/` files + original sources
**Output**: `.research/audit/report.md`

Chain integrity check → scope check → causation check → confidence calibration → completeness check → verdict.

**Gate: audit → ship**
- [ ] HIGH confidence findings have complete chains (100% sampled)
- [ ] Key numbers verified against sources
- [ ] No scope inflation or causal overreach
- [ ] Confidence levels calibrated
- [ ] All research questions addressed or gaps named
- [ ] Verdict: SHIP

## The Workspace

```
.research/
├── scope.md              # Co-created (elicit + human): questions, boundaries, source hierarchy
├── PLAN.md               # Orchestrator tracking
├── sources/
│   └── inventory.md      # Co-created (elicit + human): source list with metadata
├── extraction/           # extract: per-source claim files
├── verification/         # scrutiny: per-source verified claims
├── synthesis/            # synthesis: per-question findings
└── audit/                # audit: evaluation report
    └── report.md
```

### Ownership

| Folder/File | Created By | Consumed By |
|-------------|------------|-------------|
| `scope.md` | elicit + human | all agents |
| `PLAN.md` | orchestrator | all agents (read), orchestrator (update) |
| `sources/inventory.md` | elicit + human | extract |
| `extraction/` | extract | scrutiny, synthesis, audit |
| `verification/` | scrutiny | synthesis, audit |
| `synthesis/` | synthesis | audit, human |
| `audit/report.md` | audit | human (ship decision) |

### Boundary

`scope.md` is the discourse output, co-created by elicit and the human. No agent modifies it after discourse. Every agent reads it for scope and boundaries. This is the research equivalent of rhetoric's `ground-truth.md`.

## The Orchestration Protocol

The orchestrator (main Claude) manages the pipeline:

1. **Discourse**: Launch elicit. Draw out research questions, boundaries, sources. Produce `scope.md` + `sources/inventory.md`.
2. **After discourse**: Read scope.md. Confirm sources from inventory. Create PLAN.md with sequence.
3. **Extraction**: Launch extract per source (parallelizable). Check gate checklists.
4. **Verification**: Launch scrutiny per source after its extraction is complete (parallelizable). Check gates.
5. **Synthesis**: Launch synthesis per research question after all verification is complete. Check gates.
6. **Audit**: Launch audit after all synthesis. Receive verdict.
7. **On RETURN**: Audit specifies which agent and what fix. Orchestrator routes back. Re-run the failed step.
8. **Max 2 returns per step**: After 2 failures, escalate to human.

### Human Checkpoints

| After | Checkpoint |
|-------|-----------|
| Discourse | Confirm scope.md and sources/inventory.md |
| Extraction | Review claim quality — are claims atomic, quotes verbatim? |
| Verification | Review REFUTED and INSUFFICIENT — any surprises? |
| Synthesis | Review findings — do convergences and gaps make sense? |
| Audit SHIP | Accept findings or request deeper investigation |
| Audit RETURN | Review remediation plan |

Human checkpoints are recommended, not mandatory. For low-stakes research, the orchestrator can proceed through the pipeline. For high-stakes research (publication, policy decisions), checkpoint at every phase.

### When to Skip Steps

| Step | Skip When | Mark in PLAN.md |
|------|-----------|-----------------|
| Verification | Trusted extraction, low stakes | `skip: trusted extraction` |
| Four-layer gap analysis | Quick survey, not systematic review | `skip: not systematic` |
| Audit | Informal research, no publication intent | `skip: informal` |
| Discourse | Never skip | — |
| Extraction | Never skip | — |

### Return Routing

| Failure | Return To | Remediation |
|---------|-----------|-------------|
| Research question unclear | elicit | Re-scope with human |
| Sources insufficient | elicit | Re-identify sources |
| Quote not found in source | extract | Re-extract from source |
| Claim doesn't follow from quote | extract | Re-extract with correct interpretation |
| Verification rubber-stamped | scrutiny | Full CoVE with independence |
| Finding cites unverified claim | scrutiny | Verify missing claims |
| Scope inflation | synthesis | Narrow finding scope |
| Causal overreach | synthesis | Adjust causal language |
| Confidence inflation | synthesis | Recalibrate levels |
| Research question unanswered | synthesis | Address or name gap |

## Anti-Patterns

| Anti-Pattern | What's Happening | Fix |
|--------------|------------------|-----|
| **Skipping discourse** | Scope written from one-line request | Run elicit to draw out real questions |
| **Skipping extraction** | Synthesizing from raw papers | Extract per-source first — always |
| **Rubber-stamp verification** | "Looks right" is not CoVE | Independent re-reading required |
| **Filling gaps with inference** | Adding what sources don't say | Name gaps explicitly |
| **Confidence inflation** | "Makes sense" upgrades confidence | Evidence pattern determines confidence |
| **Scope creep** | Answering questions not in scope.md | Return to scope, don't expand silently |
| **Single-source synthesis** | No cross-source integration | Synthesis requires multiple verified sources |
| **Trusting the pipeline** | Each stage can err | Audit traces end-to-end independently |

## References

Spoke skills — load for domain-specific methodology:
- [eliciting](../eliciting/SKILL.md) — Research discourse, question sharpening, source identification
- [extracting](../extracting/SKILL.md) — Claimify pipeline, source tiers, extraction protocol
- [verifying](../verifying/SKILL.md) — CoVE protocol, verification verdicts, independence
- [synthesizing](../synthesizing/SKILL.md) — Evidence weighting, convergence/divergence, gap analysis
- [auditing](../auditing/SKILL.md) — Provenance chain, chain integrity, ship/return verdict
