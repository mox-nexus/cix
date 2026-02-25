---
name: rhetoric
description: "Rhetoric craft — explanation, visual design, voice, and collection architecture. Use when: writing docs, explaining concepts, research synthesis, creating tutorials, making diagrams (Mermaid, D2, C4), building dataviz or cinematic animation, organizing documentation sites, designing scrollytelling or staged reveals, reviewing content for accuracy or voice quality, stripping LLM tells, verifying citations."
version: 0.2.0
---

# Rhetoric

> Understanding that propagates.

Every layer of this craft serves comprehension transfer. The inner layers (inventio, memoria) build understanding that sticks. The outer layers (dispositio, elocutio, actio) reduce friction to receiving it. Neither substitutes for the other.

This is nishkama karma applied to communication — right effort, action in service of uplifting through understanding, not confounding. Understanding is the heavy center. Outer layers reduce friction. The stack has gravity pulling inward.

## Contents

- [The Four Failure Modes](#the-four-failure-modes)
- [The Semantic Stack](#the-semantic-stack)
- [The Three Doors](#the-three-doors)
- [Modal Lock](#modal-lock)
- [Wider, Not Louder](#wider-not-louder)
- [Dimensional Shift](#dimensional-shift)
- [The Weaving Method](#the-weaving-method)
- [Audience Calibration](#audience-calibration)
- [Routing](#routing)
- [The Pipeline](#the-pipeline)
- [Anti-Patterns](#anti-patterns)
- [Before Shipping](#before-shipping)

## The Four Failure Modes

Every workflow and evaluation criterion in this plugin prevents these:

| # | Mode | What fails |
|---|------|------------|
| 1 | **The academic** | Understanding dies in the document. Rigorous content, terrible presentation. No one reads it. |
| 2 | **Marketing** | Beautiful presentation, hollow core. Doesn't just fail to propagate — actively drowns out genuine understanding. At AI scale, floods the information environment. |
| 3 | **The spectacle** | Substance exists but presentation buries it. The reader leaves impressed but can't explain what they learned. |
| 4 | **The generated** | Understanding never existed anywhere in the pipeline. The LLM pattern-matched, the human approved without generating ground truth, the reader consumed without reconstructing. No one can explain the reasoning because no one ever had it. |

**The generated** is the only failure mode that compounds — generated content persists in docs, codebases, training data, degrading everything downstream. This is the default when you do nothing.

## The Semantic Stack

A compiler pipeline for meaning. Each layer transforms the semantic representation:

The five canons of rhetoric map to five agents:

| Canon | Agent | What they do |
|-------|-------|-------------|
| **Inventio** (discovery) | feynman | Comprehend sources, discover what to say |
| **Memoria** (memory) | sagan | Weave Three Doors, make understanding stick across audiences |
| **Dispositio** (arrangement) | vyasa | Arrange the collection — reading paths, layers, structure |
| **Elocutio** (style) | orwell | Voice — precision, rhythm, authenticity |
| **Actio** (delivery) | tufte / jobs | Deliver — visual artifacts, experience design |

Memoria — making understanding internalize, not just inform — was dropped from modern rhetoric when print made memorization unnecessary. But in the AI age, content that washes over the reader without sticking is the default failure. Sagan restores the lost canon.

```
Source (code, research, raw material)
  | setup — scaffold .rhet/ workspace, add to .gitignore
  | discourse — agent asks, human generates ground truth
  | cartography — magellan surveys source landscape (inventory, clusters, connections, gaps)
  | planning — planner breaks project into deliverables (types, agents, dependencies, sequence)
  ─── per deliverable ───
  | inventio — feynman discovers and drafts (four-pass, gap-state, Three Doors)
  | memoria — sagan weaves (cross-audience threading, dimensional shifts)
  | dispositio — vyasa arranges (reading paths, layers, structure)
  | elocutio — orwell voices (precision, rhythm, authenticity)
  | actio — tufte, jobs deliver (visual artifacts, experience design)
  | evaluating — socrates verifies (completeness, evidence, propagation)
  > Target (reader's understanding)
```

**Discourse covers both subject and context.** The human articulates what they're communicating, who it's for, and the presentation context. Understanding the medium, audience, and constraints early informs every downstream decision.

Understanding is the heavy center. Each outer layer exists to make understanding easier to receive, not more convincing.

**Metacognition must be architecturally designed, not prompted for** (Huang et al. ICLR 2024). You cannot ask a model "are you sure?" and expect calibrated output. The techniques that work introduce structural independence between generation and verification. This principle informs every workflow below.

## The Three Doors

Explanations aren't layers to traverse top-down. They're fabric with three simultaneous dimensions — coordinate axes, not a ladder.

| Door | Explanation | Engineering | Philosophy | The receiver asks |
|------|-------------|-------------|------------|-------------------|
| **1** | Principle | Abstraction | Universal | "Why does this hold together?" |
| **2** | Concretions | Planning | Constituency | "Who is this for, and why this, not that?" |
| **3** | Ground | Execution | Self | "What do I carry away?" |

All three are present in every good explanation. The difference is which door the receiver enters through.

The doors narrow: **Universal > Constituency > Self.** Door 1 is true everywhere. Door 2 is true for these people, in this situation. Door 3 is true for me, right now, in my hands. Constituency is the bridge — the universal becomes concrete *for someone*. Skip it and Door 3 is just generic steps anyone could follow and no one does.

## Modal Lock

Your default failure mode. You default to Door 1 — Abstraction | Universal. Clean taxonomies, complete frameworks, universal truths beautifully organized. When it doesn't land, you amplify: more structure, more categories, more abstraction. The explanation gets taller without getting wider.

What's missing isn't "practice" generically. It's **Constituency** — Door 2. The question you almost never ask: *who is standing at this door right now, and what do they specifically need?*

### Directional Diagnosis

Modal lock shifts through the next door, not a skip. 1>2>3. The bridge isn't optional.

| Lock | Symptom | What's missing | Shift to |
|------|---------|----------------|----------|
| Stuck in Door 1 | Beautiful framework, nobody moves | Who is this *for*? | Door 2: concretize for a constituency |
| Stuck in Door 2 | Endless options, trade-offs, analysis | What do *I* do right now? | Door 3: enable self-execution |
| Stuck in Door 3 | Shipped but nobody knows why | Why does this *matter*? | Door 1: connect to the universal |

### Signal Table

| Signal | Missing door | Shift to |
|--------|-------------|----------|
| "I don't get why this matters" | Door 1 | Connect to something they care about |
| "Who is this for?" | Door 2 | Concretize for a specific audience |
| "How does this fit with X?" | Door 2 | Show the relationship to what they know |
| "What do I actually do?" | Door 3 | Ground in what they carry away |
| "This is too abstract" | Door 3 | Start with the specific, derive the general |
| "This is just steps, I don't understand" | Door 1 | Explain WHY these steps, not others |

## Wider, Not Louder

When explanation fails, the instinct is more of the same — more docs, more slides, more energy. This deepens the lock.

The fix: **encode all three doors simultaneously** so the signal survives lossy compression. Each receiver — each organizational layer — compresses through whatever dimensions it can perceive. If you encode wide, enough survives in whatever door the receiver can pass.

**Weave, don't sequence.** "A why section, then a how section, then a what section" is three one-dimensional presentations in a trench coat. Every passage should carry all three threads. The reader pulls theirs.

## Dimensional Shift

The most powerful explanation moments happen at intersections between doors — not within one.

| Shift | Experience | Design move |
|-------|-----------|-------------|
| Door 1 > Door 3 | "I understood it, then suddenly I *felt* it" | Principle becomes embodied |
| Door 2 > Door 3 | "I iterated, then it settled into my hands" | Contrast becomes ground |
| Door 3 > Door 2 | "It was automatic, then I had to choose again" | Ground becomes deliberate |

Design for dimensional shift, not dimensional purity. The moment an idea crosses from one door to another is when it stops being information and starts being knowledge.

## The Weaving Method

Sagan's protocol (Memoria). When content is modal-locked — strong in one or two doors, weak in others — the fix is weaving, not adding sections.

### ANCHOR

Mark what already works. Identify passages with genuine weight, the entry door, existing dimensional shifts. **Never weaken a strong door to strengthen a weak one.** Weaving is additive threading, not redistribution.

### THREAD

For each passage locked in one door, thread the missing door INTO that passage:

| Thread this door | Into existing content by | Watch out for |
|------------------|------------------------|---------------|
| **Door 3** | Drop one specific, undeniable thing (number, name, sensation) | Generic examples (Door 1 in costume) |
| **Door 2** | Name the constituency, show what was chosen against | Listing options without choosing |
| **Door 1** | Surface the reason beneath the step — why this, not that | Interrupting the flow with theory |

### SHIFT

Ensure at least one dimensional crossing happens:

| Desired shift | Technique |
|---------------|-----------|
| Door 1 > Door 3 | Follow a principle with an undeniable example that makes the reader *feel* it |
| Door 3 > Door 1 | After concrete steps, surface why those steps matter |
| Door 2 > Door 3 | After naming alternatives, show what the chosen path looks like in practice |
| Door 3 > Door 2 | After showing the thing working, zoom out to who it serves |

### VERIFY

- [ ] Strong doors preserved — nothing that worked was weakened
- [ ] Missing doors now present — as threads in existing passages, not bolted-on sections
- [ ] At least one dimensional shift — a crossing happens
- [ ] Still woven, not sequenced
- [ ] Weight present — at least one thing that doesn't argue for itself

If verification fails, return to THREAD.

## Audience Calibration

Don't guess — detect:

| Signal | Expertise | Adjust |
|--------|-----------|--------|
| Uses jargon correctly | Competent+ | Skip scaffolding |
| Asks foundational questions | Novice | More Door 3, less Door 2 |
| Points out edge cases | Expert | Engage Door 1, skip basics |
| "Just tell me what to do" | Any (task-focused) | Lead with Door 3 |
| "Why?" | Any (understanding-focused) | Lead with Door 1 |

**Expertise reversal** (Tetzlaff 2025, n=5,924): What helps novices actively harms experts. High guidance for novices (d=0.505). Low guidance for experts (d=-0.428). Detect and adapt.

## Routing

One hub triggers. It routes to specialized skills on demand.

| Need | Agent | Spoke skill |
|------|-------|-------------|
| Survey source landscape | magellan | [mapping](../mapping/SKILL.md) |
| Plan deliverables + sequence | planner | rhetoric is enough |
| Inventio — comprehend + draft | feynman | [discovering](../discovering/SKILL.md) |
| Memoria — weave + make it stick | sagan | rhetoric is enough |
| Dispositio — arrange collection | vyasa | [arranging](../arranging/SKILL.md) |
| Elocutio — voice + authenticity | orwell | [voicing](../voicing/SKILL.md) |
| Actio — visual artifacts | tufte | [figures](../figures/SKILL.md) |
| Actio — experience design | jobs | [staging](../staging/SKILL.md) |
| Evaluate propagation | socrates | [evaluating](../evaluating/SKILL.md) |

## The Pipeline

One pipeline. Every content project follows it. The planner adapts it per project. Socrates gates between steps. PLAN.md is the shared state.

```
setup (script) → discourse (human) → magellan (cartography) → planner (tasks)
  ─── per deliverable ───
  → feynman (inventio — discover + draft)
  → sagan (memoria — weave + stick)
  → vyasa (dispositio — arrange)
  → orwell (elocutio — voice)
  → tufte (actio — figures) — if applicable
  → jobs (actio — staging) — if applicable
  → socrates (evaluate)
```

### Workspace

The workspace directory is the shared state. All agents read from and write to it.

**Boundary**: Only magellan sees outside the workspace (surveys source material wherever it lives). Feynman follows references from map/MOC.md back to sources. Everyone else works entirely within the workspace.

**Archive is off-limits.** Any directory named `archive/` contains superseded work. Never read, reference, or draw from archived content.

Each transformation step writes to its own folder. Every intermediate state is preserved.

```
.rhet/
├── ground-truth.md       discourse (human)
├── map/                  magellan (MOC.md + cluster files + SOURCES.md)
├── PLAN.md               planner (all agents update)
├── discovering/          feynman — comprehension state per topic
├── inventio/             feynman — drafted content
├── memoria/              sagan — woven content (copies from inventio/, weaves)
├── arrangement/          vyasa — structure, reading paths
├── voicing/              orwell — voiced content (copies from memoria/, applies voice)
├── figures/              tufte — visual artifacts
├── staging/              jobs — experience specs
├── evaluation/           socrates — reports per deliverable
```

| Folder/File | Created by | Consumed by |
|-------------|------------|-------------|
| `ground-truth.md` | discourse (human) | magellan, planner, feynman, sagan |
| `map/` | magellan | planner, feynman |
| `PLAN.md` | planner | all agents (read + update on completion) |
| `discovering/` | feynman | feynman (drafting step) |
| `inventio/` | feynman | sagan |
| `memoria/` | sagan | vyasa, orwell |
| `arrangement/` | vyasa | orwell, socrates |
| `voicing/` | orwell | tufte, jobs, socrates |
| `figures/` | tufte | jobs, socrates |
| `staging/` | jobs | socrates |
| `evaluation/` | socrates | human (ship decision) |

### Step 1: Setup (script)

Scaffold the `.rhet/` workspace and add it to `.gitignore`.

```bash
./setup.sh [workspace-path]
```

Creates workspace directory structure (all subdirectories) and ensures `.rhet/` is in `.gitignore`. Default path is `.rhet/` in the project root. Override with a custom path if needed.

**Gate: setup → discourse**
- [ ] Workspace directory exists with all subdirectories
- [ ] `.rhet/` added to `.gitignore`

### Step 2: Discourse (human)

The agent asks, the human generates ground truth. The discourse protocol lives in [discovering](../discovering/SKILL.md#discourse).

Three movements — the agent draws out each:

| Movement | What the agent draws out | Examples |
|----------|-------------------------|----------|
| **Communicate** | What are you trying to communicate? Purpose, thesis, the core thing. | "What is this about? Why does it exist?" |
| **Setup** | Who is this for? What medium? What constraints? | "Who reads this? Where does it live? What are the limits?" |
| **Substance** | What do you know about it? The content itself. | Varies by project type (see below) |

The substance movement adapts to the project:

| Project type | Substance looks like |
|-------------|---------------------|
| Research synthesis | Claims with evidence levels, what studies establish, where evidence conflicts |
| Experience page | Story arc, emotional journey, what the reader should feel |
| Project docs | Architecture, entry points, what the audience needs to do |
| Presentation | Key takeaways, narrative structure, what lands |

Agents cannot provide ground truth. If you skip this step, you get failure mode #4 — the generated.

**Gate: discourse → cartography**
- [ ] Communicate — purpose articulated clearly
- [ ] Setup — audience, medium, constraints named
- [ ] Substance — content grounded in what the human actually knows
- [ ] State-back confirmed — agent restated ground truth in own words, human confirmed
- [ ] Ground truth written to `ground-truth.md` in workspace

### Step 3: Cartography (magellan)

Survey the source landscape with direction from discourse.

**Agent**: magellan | **Skills**: `rhetoric`, `mapping`
**Input**: ground-truth.md + source material (outside workspace)
**Output**: `map/` (MOC.md + cluster files + SOURCES.md)

Method: Survey (enumerate) → Cluster (group by claim) → Connect (trace relationships) → Gap (name what's missing).

Magellan surveys breadth. Feynman comprehends depth. Magellan first.

**Gate: cartography → planning**
- [ ] Every known source inventoried with type, location, scope, strength
- [ ] Sources clustered by topic/claim with coverage assessment
- [ ] Connections between clusters traced (reinforcement, tension, dependency)
- [ ] Gaps named with type (coverage, evidence, connection, recency) and impact
- [ ] map/ written to workspace (MOC.md + cluster files + SOURCES.md)

### Step 4: Planning (planner)

Group evidence clusters into work units, sequence them, and seed each agent directory with its plan and gate checklist.

**Agent**: planner | **Skills**: `rhetoric`
**Input**: ground-truth.md + map/MOC.md
**Output**: `PLAN.md` (root tracker) + `*/PLAN.md` (per-directory plans)

Planner does NOT name articles or content — it groups clusters, sequences work, and enables each agent with structure and discourse context. What the work units become is discovered by feynman and arranged by vyasa.

PLAN.md is the tracking mechanism — every agent updates it upon completion.

**Gate: planning → per-work-unit pipeline**
- [ ] Clusters grouped into coherent work units
- [ ] Dependencies between work units are explicit
- [ ] Sequence justified (dependencies first, dense evidence first)
- [ ] Each agent directory has a PLAN.md with gate checklist and relevant discourse context
- [ ] Root PLAN.md written to workspace

### Step 5: Inventio (feynman)

Comprehend sources and draft content per deliverable.

**Agent**: feynman | **Skills**: `rhetoric`, `discovering`
**Input**: PLAN.md + ground-truth.md + map/MOC.md (follows references to sources)
**Output**: `discovering/` (comprehension state) + `inventio/` (drafted content)

Four-pass reading → gap-state tracking → explain-back → Three Doors draft → internal Socratic loop.

**Gate: inventio → memoria**
- [ ] Four-pass reading complete
- [ ] All three doors present in draft
- [ ] Entry door chosen deliberately (not defaulting to Door 1)
- [ ] Evidence levels labeled on every cited claim
- [ ] No claims without source attribution
- [ ] No claims from parametric knowledge — every fact traces to a source document
- [ ] Numbers verified against source text (grep, not memory)
- [ ] Content written to `inventio/`

### Step 6: Memoria (sagan)

Weave content so understanding sticks across audiences. Runs on every deliverable.

**Agent**: sagan | **Skills**: `rhetoric`
**Input**: `inventio/` + ground-truth.md
**Output**: `memoria/` (copies from inventio/, weaves — preserves pre-weave versions)

Weaving method: ANCHOR (mark what works) → THREAD (missing doors into existing passages) → SHIFT (ensure dimensional crossing) → VERIFY. Also: find the universal thread, ground in specifics, ensure the reader crosses from knowing to feeling.

**Gate: memoria → dispositio**
- [ ] Strong doors from inventio preserved — nothing weakened
- [ ] Missing doors now threaded into existing passages (not bolted-on sections)
- [ ] At least one dimensional shift — a crossing happens
- [ ] Content woven, not sequenced
- [ ] Universal thread surfaced — reader feels why this matters
- [ ] Content written to `memoria/`

Collection-level organization. Skip for single-deliverable projects.

**Agent**: vyasa | **Skills**: `rhetoric`, `arranging`
**Input**: `memoria/` + PLAN.md
**Output**: `arrangement/`

Layer model → Diataxis types → reading paths → single source of truth → cross-links.

**Gate: dispositio → elocutio**
- [ ] Layer model applied — progressive depth, clear stopping points per audience
- [ ] Reading paths defined — at least one per audience
- [ ] Single source of truth — no concept explained in multiple places
- [ ] Diataxis type assigned per document
- [ ] Cross-links use defined reading paths
- [ ] No orphan documents — everything reachable
- [ ] Structure written to `arrangement/`

### Step 8: Elocutio (orwell)

Strip LLM tells, restore specificity, check rhythm.

**Agent**: orwell | **Skills**: `rhetoric`, `voicing`, `evaluating`
**Input**: `memoria/` + `arrangement/`
**Output**: `voicing/` (copies from memoria/, applies voice — preserves pre-voice versions)

Four-pass voice review. Non-negotiable — feynman and sagan optimize for content, not voice.

**Gate: elocutio → actio**
- [ ] Four-pass voice review complete
- [ ] Zero LLM tells — no symmetric headings, no "delve/tapestry/landscape", no colon-split titles
- [ ] Specificity restored — no "various", "numerous", "a number of"
- [ ] Rhythm varies — not every paragraph the same length, not every sentence the same structure
- [ ] Borrowed phrases identified and replaced
- [ ] Content reads as if a specific human wrote it

### Step 9: Actio (tufte / jobs)

Visual artifacts and experience design. Skip if not applicable — check PLAN.md.

**Agent**: tufte | **Skills**: `rhetoric`, `figures` — AND/OR — jobs | **Skills**: `rhetoric`, `staging`
**Input**: `voicing/`
**Output**: `figures/` (tufte) and/or `staging/` (jobs)

Tufte: medium selection → type selection → design → build → verify (render test, reduced-motion fallback, data-ink audit).
Jobs: medium selection → beat structure → progressive disclosure → integration review.

Tufte's own standards gate visuals. Socrates and orwell do not review visual artifacts (exception: prose captions — orwell reviews text elements).

**Gate: actio → evaluating**
- [ ] Every visual serves the information structure (not decoration)
- [ ] Reduced-motion fallbacks for animations
- [ ] Data-ink ratio acceptable — no chartjunk
- [ ] If staging: beat structure, pacing variation, progressive disclosure
- [ ] Prose and visuals integrated — not bolted on

### Step 10: Evaluate (socrates)

Final quality gate. Does understanding propagate?

**Agent**: socrates | **Skills**: `rhetoric`, `evaluating`
**Input**: `voicing/` (or `figures/`/`staging/` if applicable) + ground-truth.md
**Output**: `evaluation/`

Propagation test → Three Doors traversal → evidence verification → accuracy check → comprehension tests.

**Gate: evaluating → ship**
- [ ] Propagation test passed — reader can explain it to someone else, not just repeat it
- [ ] Three Doors traversal — all doors present, dimensional shift happens
- [ ] Evidence verified — every number traces to bibliography to source
- [ ] No "uncertain" presented as "solid"
- [ ] Comprehension tests pass on final output
- [ ] Before Shipping checklist (below) passes

### The Orchestration Protocol

Between every agent step, the orchestrator (you) follows this loop:

1. **Read** PLAN.md — identify next step for this deliverable
2. **Launch** the assigned agent
3. **Agent completes** — updates PLAN.md (checks off step, notes issues)
4. **Socrates gates** — launch socrates to verify the gate checklist for the completed step
5. **Pass** → advance to next step
6. **Fail** → return to the agent with socrates' feedback. Max 2 returns per step.
7. **2 failures** → escalate to human. The agent cannot resolve this alone.

This protocol is structural — it cannot be shortened by "seeming fine." Every step gets gated.

### When to Skip Steps

| Step | Skip when | Mark in PLAN.md |
|------|-----------|-----------------|
| Cartography | Single source, already well-known | `skip: single source` |
| Planning | Single deliverable, obvious scope | `skip: single deliverable` |
| Dispositio | Single deliverable (no collection) | `skip: single deliverable` |
| Actio (figures) | No visual artifacts needed | `skip: no visuals` |
| Actio (staging) | No experience design needed | `skip: no staging` |
| Setup | Already have workspace | `skip: workspace exists` |
| Discourse | Never skip | — |
| Inventio + memoria + elocutio + evaluating | Never skip | — |

### Return Routing

When socrates fails a gate or the orchestrator detects a problem:

| Failure type | Return to | Agent |
|--------------|-----------|-------|
| Evidence errors (wrong numbers, missing sources) | Inventio | feynman re-reads source |
| Modal lock (stuck in one Door) | Memoria | sagan re-weaves |
| Dimensional shift missing | Memoria | sagan re-weaves with socrates' feedback |
| Structural issues (orphans, broken paths) | Dispositio | vyasa re-compiles |
| Voice issues (LLM tells, flat rhythm) | Elocutio | orwell re-reviews |
| Propagation failure (reader can't reconstruct) | Memoria | sagan re-weaves with socrates' feedback |
| Content gaps (claims missing from ground truth) | Discourse | escalate to human |

Each return re-runs only the failed step and everything after it.

---

## Anti-Patterns

| Anti-pattern | What's happening | Fix |
|--------------|------------------|-----|
| **Modal lock** | Amplifying same door when it doesn't land | Shift to next door (1>2>3) |
| **Skipping Door 2** | Jumping from universal to execution | Concretize for a constituency first |
| **Sequential traversal** | "First principle, then pattern, then steps" | Weave simultaneously |
| **Adding instead of shifting** | Bolting on "practical examples" after theory | Re-encode the theory through Door 3 |
| **Door 1 in costume** | Generic example pretending to be Door 3 | Real constituency, real context, real weight |
| **Confidence theater** | Projecting certainty without evidence | State evidence level explicitly |
| **Explanation inflation** | More words when fewer would serve | Cut. Then cut more. |
| **The generated** | No understanding exists anywhere in pipeline | Human provides ground truth. Agent comprehends before producing. |

## Before Shipping

1. Does this trust the learner?
2. Will they discover something themselves?
3. Can the ground-seeker find their door at every point?
4. Can the constituency-seeker feel the contrast in the reasoning?
5. Can the principle-seeker pull their thread from any passage?
6. Is the weave woven, not sequenced?
7. Does a dimensional shift happen — does the explanation cross doors?
8. Does understanding propagate? Can the reader explain it to someone else?
9. Have I trusted what I cannot see?

## References

Spoke skills — load for domain-specific craft:
- [mapping](../mapping/SKILL.md) — Survey, synthesis, map of contents
- [discovering](../discovering/SKILL.md) — Comprehension transform, Diataxis production formats
- [arranging](../arranging/SKILL.md) — Collection structure, reading paths, layer model
- [voicing](../voicing/SKILL.md) — Writing craft, voice evaluation, anti-LLM-speak
- [evaluating](../evaluating/SKILL.md) — Propagation test, evidence verification, accuracy
- [figures](../figures/SKILL.md) — Diagram type selection, dataviz, animation
- [staging](../staging/SKILL.md) — Medium selection, pacing, progressive disclosure
