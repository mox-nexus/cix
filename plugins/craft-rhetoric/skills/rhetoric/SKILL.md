---
name: rhetoric
description: "This skill should be used when the user asks to 'write docs', 'explain this concept', 'create a tutorial', 'make a diagram', 'review content quality', 'design a scrollytelling experience', or needs research synthesis, visual explanations, voice evaluation, or collection architecture."
version: 0.3.0
---

# Rhetoric

> Understanding that propagates.

Every layer of this craft serves comprehension transfer. The inner layers (inventio, memoria) build understanding that sticks. The outer layers (dispositio, elocutio, actio) reduce friction to receiving it. Neither substitutes for the other.

This is nishkama karma applied to communication — right effort, action in service of uplifting through understanding, not confounding. Understanding is the heavy center. Outer layers reduce friction. The stack has gravity pulling inward.

## Contents

- [The Thesis](#the-thesis)
- [The Four Failure Modes](#the-four-failure-modes)
- [The Semantic Stack](#the-semantic-stack)
- [The Three Doors](#the-three-doors)
- [Modal Lock](#modal-lock)
- [Wider, Not Louder](#wider-not-louder)
- [Dimensional Shift](#dimensional-shift)
- [The Weaving Method](#the-weaving-method)
- [Audience Calibration](#audience-calibration)
- [Voice Preservation](#voice-preservation)
- [Routing](#routing)
- [The Pipeline](#the-pipeline)
- [Anti-Patterns](#anti-patterns)
- [Before Shipping](#before-shipping)

## The Thesis

Impact shouldn't be gated behind skills that aren't the point. The person who has a breakthrough insight shouldn't need a literature degree to get that insight into the world. The insight is the spark. Writing craft is the delivery vehicle.

Writing is thinking — not documentation of thinking. When you write "this experiment tests whether..." and can't finish the sentence, the writing surfaced a thinking gap. Discourse applies this: the human is writing when they're talking to the agent. The agent won't let hand-waving happen. By the end, the human has thought clearly. That's the ground truth.

Discourse finds the spark — pushes until the thinking is sharp. The rest of the pipeline is delivery infrastructure. The human never needed to learn the delivery. They needed a collaborator who could force clarity on the thinking and then handle the craft.

Let humans save cognition for things that drive them — those are the things they'll excel at, and they have the spark. Find the sparks, amplify them, don't gate behind skills they could spend 4 years learning.

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

A compiler pipeline for meaning. Each canon transforms the semantic representation:

| Canon | Agent | What they do |
|-------|-------|-------------|
| **Discourse** (skill 0) | socrates | Draw out ground truth through dialectical questioning |
| **Inventio** (discovery) | feynman | Comprehend sources, discover what to say |
| **Memoria** (memory) | sagan | Weave Three Doors, make understanding stick across audiences |
| **Dispositio** (arrangement) | vyasa | Arrange the collection — reading paths, layers, structure |
| **Elocutio** (voice) | orwell | Voice preservation — runs after every prose-transforming step |
| **Actio** (delivery) | tufte / jobs | Deliver — visual artifacts, experience design |
| **Critique** (quality gate) | ebert | Final evaluation — does it work? Ship or return. |

Memoria — making understanding internalize, not just inform — was dropped from modern rhetoric when print made memorization unnecessary. But in the AI age, content that washes over the reader without sticking is the default failure. Sagan restores the lost canon.

Orwell is not a single step — he's the continuous voice guardian. After every prose-transforming agent (feynman, sagan, jobs), orwell runs a full voice review. Voice drift is cumulative. Catching it per-step prevents compound erosion.

```
Source (code, research, raw material)
  | setup — scaffold .rhet/ workspace, add to .gitignore
  | discourse — socrates asks, human generates ground truth + voice anchor
  | cartography — magellan surveys source landscape
  ─── per deliverable ───
  | inventio — feynman discovers and drafts → orwell (voice check)
  | memoria — sagan weaves → orwell (voice check)
  | dispositio — vyasa arranges
  | actio — tufte delivers (figures), jobs delivers (staging) → orwell (voice check after jobs)
  | critique — ebert evaluates: ship or return
  > Target (reader's understanding)
```

**Discourse covers both subject and context.** The human articulates what they're communicating, who it's for, and the presentation context. Understanding the medium, audience, and constraints early informs every downstream decision.

Understanding is the heavy center. Each outer layer exists to make understanding easier to receive, not more convincing.

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

**Expertise reversal**: What helps novices actively harms experts. High guidance for novices, low guidance for experts. Detect and adapt.

## Voice Preservation

**Voice is not style applied at the end. Voice is present in the source material and must be actively preserved at every step.**

The default posture of every agent in the pipeline is preservation. Changes require justification against the agent's specific scope. A multi-agent pipeline will destroy the original voice through cumulative drift — death by a thousand polishes — unless voice preservation is architecturally enforced.

### The Voice Anchor

A `voice.md` file in the workspace defines the author's voice characteristics. Co-created with the author during discourse. Injected into the context of **every agent**, not just orwell.

The voice anchor distinguishes:
- **Voice features** (protect): sentence rhythm, characteristic phrasing, cross-domain connections, strategic inefficiencies, humor, authority posture, rough edges that signal thinking happening live
- **Voice habits** (correct): patterns the author has explicitly flagged as unintentional

Only habits explicitly flagged by the author are correctable. Everything else is preserved by default.

### Scoped Agent Mandates

Each agent makes changes **only** within its scope. Everything outside scope passes through unchanged.

| Agent | Scope | Does NOT |
|-------|-------|----------|
| feynman | Accuracy, comprehension, evidence | Rephrase, restructure, or "improve" language |
| sagan | Three Doors weaving, dimensional shifts | Replace author's word choices or phrasing |
| vyasa | Section ordering, reading paths | Rewrite sentences within sections |
| orwell | Voice evaluation, LLM tell removal | Change meaning, restructure arguments |
| tufte/jobs | Visual artifacts, experience design | Touch prose (exception: captions) |

No agent has a general "improve the writing" mandate.

### Minimal Transformation Principle

Every agent: **make the minimum change necessary for your specific function.**

If a sentence is structurally sound but "could be better," leave it. "Better" according to whom? The agent's training distribution, which converges on generic quality. The author's voice lives in the specific choices that diverge from generic quality.

### Ground Truth as Voice Reference

`ground-truth.md` is immutable. No agent modifies it. Every agent can read it to understand not just what the author said, but *how they said it*. The phrasing, rhythm, and rough edges carry voice signal.

Discourse phrasings (author's live speech) get higher preservation priority than already-processed text.

### Diff-Against-Source

Every agent produces a structured diff showing what it changed and why, mapped to its specific mandate. If an agent changes phrasing flagged as a voice feature in the anchor, it must provide explicit justification. This creates an audit trail for voice drift.

## Routing

One hub triggers. It routes to specialized skills on demand.

| Need | Agent | Spoke skill |
|------|-------|-------------|
| Draw out ground truth | socrates | [discourse](../discourse/SKILL.md) |
| Survey source landscape | magellan | [mapping](../mapping/SKILL.md) |
| Inventio — comprehend + draft | feynman | [discovering](../discovering/SKILL.md) |
| Memoria — weave + make it stick | sagan | rhetoric is enough |
| Dispositio — arrange collection | vyasa | [arranging](../arranging/SKILL.md) |
| Elocutio — voice preservation | orwell | [voicing](../voicing/SKILL.md) |
| Actio — visual artifacts | tufte | [figures](../figures/SKILL.md) |
| Actio — experience design | jobs | [staging](../staging/SKILL.md) |
| Critique — ship or return | ebert | [evaluating](../evaluating/SKILL.md) |

## The Pipeline

One pipeline. Every content project follows it. The orchestrator (main Claude) adapts it per project. Orwell gates voice after prose steps. Ebert makes the ship/return call.

This is an **evaluator-optimizer loop**: multiple optimizers (agents that transform content), two evaluators (orwell for voice, ebert for propagation), and an orchestrator that routes between them.

```
socrates (discourse) → ground-truth.md + voice.md
  → magellan (cartography) → map/
  ─── per deliverable ───
  → feynman (inventio) → orwell (voice check)
  → sagan (memoria) → orwell (voice check)
  → vyasa (dispositio)
  → tufte (figures) — if applicable
  → jobs (staging) → orwell (voice check) — if applicable
  → ebert (critique — ship or return)
```

### Workspace

The workspace directory is the shared state. All agents read from and write to it.

**Boundary**: Only magellan sees outside the workspace (surveys source material wherever it lives). Feynman follows references from map/MOC.md back to sources. Everyone else works entirely within the workspace.

**Archive is off-limits.** Any directory named `archive/` contains superseded work. Never read, reference, or draw from archived content.

Each transformation step writes to its own folder. Orwell reviews and edits in the current step's output folder, preserving a change summary.

```
.rhet/
├── ground-truth.md       socrates (discourse) — immutable voice reference
├── voice.md              socrates (discourse) — voice features to protect, habits to correct
├── map/                  magellan (MOC.md + cluster files + SOURCES.md)
├── PLAN.md               orchestrator (tracking)
├── inventio/             feynman — comprehend + draft
├── memoria/              sagan — weave (copies from inventio/)
├── arrangement/          vyasa — structure, reading paths
├── figures/              tufte — visual artifacts
├── staging/              jobs — experience specs
├── critique/             ebert — evaluation reports
```

| Folder/File | Created by | Consumed by |
|-------------|------------|-------------|
| `ground-truth.md` | socrates (discourse) | **every agent** — immutable voice reference |
| `voice.md` | socrates (discourse) | **every agent** — voice features + habits |
| `map/` | magellan | orchestrator, feynman |
| `PLAN.md` | orchestrator | all agents (read), orchestrator (update) |
| `inventio/` | feynman | orwell (voice check), sagan |
| `memoria/` | sagan | orwell (voice check), vyasa |
| `arrangement/` | vyasa | tufte, jobs, ebert |
| `figures/` | tufte | ebert |
| `staging/` | jobs | orwell (voice check), ebert |
| `critique/` | ebert | human (ship decision) |

### Step 1: Setup (script)

Scaffold the `.rhet/` workspace and add it to `.gitignore`.

```bash
./setup.sh [workspace-path]
```

Creates workspace directory structure (all subdirectories) and ensures `.rhet/` is in `.gitignore`. Default path is `.rhet/` in the project root.

**Gate: setup → discourse**
- [ ] Workspace directory exists with all subdirectories
- [ ] `.rhet/` added to `.gitignore`

### Step 2: Discourse (socrates)

The agent asks, the human generates ground truth. Socrates runs the [discourse](../discourse/SKILL.md) protocol.

Three movements — socrates draws out each:

| Movement | What socrates draws out |
|----------|------------------------|
| **Communicate** | What are you trying to communicate? Purpose, thesis, the core thing. |
| **Setup** | Who is this for? What medium? What constraints? |
| **Substance** | What do you know about it? Adapts to project type. |

Socrates also co-creates `voice.md` — listening for voice signal in how the human talks. Voice features (protect) vs voice habits (correct).

Agents cannot provide ground truth. If you skip this step, you get failure mode #4 — the generated.

**Gate: discourse → cartography**
- [ ] Communicate — purpose articulated clearly
- [ ] Setup — audience, medium, constraints named
- [ ] Substance — content grounded in what the human actually knows
- [ ] State-back confirmed — socrates restated ground truth in own words, human confirmed
- [ ] Ground truth written to `ground-truth.md` in workspace
- [ ] Voice anchor co-created — `voice.md` written with features to protect and habits to correct

### Step 3: Cartography (magellan)

Survey the source landscape, scoped by what ground truth surfaces as subject or related materials.

**Agent**: magellan | **Skills**: `rhetoric`, `mapping`
**Input**: ground-truth.md + source material (outside workspace)
**Output**: `map/` (MOC.md + cluster files + SOURCES.md)

Method: Survey (enumerate) → Cluster (group by claim) → Connect (trace relationships) → Gap (name what's missing).

Magellan surveys breadth. Feynman comprehends depth. Magellan first.

**Gate: cartography → inventio**
- [ ] Every known source inventoried with type, location, scope, strength
- [ ] Sources clustered by topic/claim with coverage assessment
- [ ] Connections between clusters traced (reinforcement, tension, dependency)
- [ ] Gaps named with type (coverage, evidence, connection, recency) and impact
- [ ] map/ written to workspace (MOC.md + cluster files + SOURCES.md)

### Step 4: Inventio (feynman)

Comprehend sources and draft content per deliverable.

**Agent**: feynman | **Skills**: `rhetoric`, `discovering`
**Input**: PLAN.md + ground-truth.md + map/MOC.md (follows references to sources)
**Output**: `inventio/` (drafted content with comprehension traces)

Four-pass reading → gap-state tracking → explain-back → Three Doors draft → internal Socratic loop.

**Gate: inventio → orwell (voice check)**
- [ ] Four-pass reading complete
- [ ] All three doors present in draft
- [ ] Entry door chosen deliberately (not defaulting to Door 1)
- [ ] Evidence levels labeled on every cited claim
- [ ] No claims without source attribution
- [ ] No claims from parametric knowledge — every fact traces to a source document
- [ ] Numbers verified against source text (grep, not memory)
- [ ] Content written to `inventio/`

### Step 4b: Orwell (voice check after inventio)

**Agent**: orwell | **Skills**: `rhetoric`, `voicing`
**Input**: `inventio/` + `ground-truth.md` + `voice.md`

Full voice review: mechanical checks, em dash analysis, four-pass review, voice regression against ground truth. Orwell edits in `inventio/` and notes changes.

Did feynman flatten the human's phrasing? Did accuracy-seeking neutralize voice?

**Gate: inventio voice check → memoria**
- [ ] No LLM tells introduced
- [ ] Voice features from voice.md preserved
- [ ] Rough edges from ground-truth.md intact

### Step 5: Memoria (sagan)

Weave content so understanding sticks across audiences. Runs on every deliverable.

**Agent**: sagan | **Skills**: `rhetoric`
**Input**: `inventio/` (post-orwell) + ground-truth.md
**Output**: `memoria/` (copies from inventio/, weaves — preserves pre-weave versions)

Weaving method: ANCHOR → THREAD → SHIFT → VERIFY. Find the universal thread, ground in specifics, ensure the reader crosses from knowing to feeling.

**Gate: memoria → orwell (voice check)**
- [ ] Strong doors from inventio preserved — nothing weakened
- [ ] Missing doors now threaded into existing passages (not bolted-on sections)
- [ ] At least one dimensional shift — a crossing happens
- [ ] Content woven, not sequenced
- [ ] Universal thread surfaced — reader feels why this matters
- [ ] Content written to `memoria/`

### Step 5b: Orwell (voice check after memoria)

**Agent**: orwell | **Skills**: `rhetoric`, `voicing`
**Input**: `memoria/` + `ground-truth.md` + `voice.md`

Did sagan genericize while weaving? Did the universal thread replace specific voice?

**Gate: memoria voice check → dispositio**
- [ ] No LLM tells introduced
- [ ] Voice features from voice.md preserved
- [ ] Author's specific phrasing not replaced with generic synonyms

### Step 6: Dispositio (vyasa)

Collection-level organization. Skip for single-deliverable projects.

**Agent**: vyasa | **Skills**: `rhetoric`, `arranging`
**Input**: `memoria/` (post-orwell) + PLAN.md
**Output**: `arrangement/`

Layer model → Diataxis types → reading paths → single source of truth → cross-links.

**Gate: dispositio → actio**
- [ ] Layer model applied — progressive depth, clear stopping points per audience
- [ ] Reading paths defined — at least one per audience
- [ ] Single source of truth — no concept explained in multiple places
- [ ] Diataxis type assigned per document
- [ ] No orphan documents — everything reachable
- [ ] Structure written to `arrangement/`

### Step 7: Actio (tufte / jobs)

Visual artifacts and experience design. Skip if not applicable.

**Agent**: tufte | **Skills**: `rhetoric`, `figures` — AND/OR — jobs | **Skills**: `rhetoric`, `staging`
**Input**: `arrangement/` (or `memoria/` if no dispositio)
**Output**: `figures/` (tufte) and/or `staging/` (jobs)

Tufte: medium selection → type selection → design → build → verify.
Jobs: medium selection → beat structure → progressive disclosure → integration review.

Tufte's own standards gate visuals. Orwell does not review figures — only prose.

**Gate: actio → orwell (voice check after jobs) → critique**
- [ ] Every visual serves the information structure (not decoration)
- [ ] Reduced-motion fallbacks for animations
- [ ] Data-ink ratio acceptable — no chartjunk
- [ ] If staging: beat structure, pacing variation, progressive disclosure
- [ ] Prose and visuals integrated — not bolted on

### Step 7b: Orwell (voice check after jobs)

Only if jobs ran. Did experience design sanitize the prose? Did pacing changes flatten rhythm?

**Gate: staging voice check → critique**
- [ ] No LLM tells introduced by staging changes
- [ ] Voice features preserved through experience design

### Step 8: Critique (ebert)

Final quality gate. Does it work?

**Agent**: ebert | **Skills**: `rhetoric`, `evaluating`
**Input**: final output + ground-truth.md
**Output**: `critique/` (evaluation reports)

Propagation test → Three Doors traversal → evidence verification → the verdict: **ship** or **return**.

Ebert judges the piece by what it was trying to do, then whether it did it. Not "I'd do it differently" — "does this achieve what it set out to achieve?"

**Gate: critique → ship**
- [ ] Propagation test passed — reader can explain it to someone else, not just repeat it
- [ ] Three Doors traversal — all doors present, dimensional shift happens
- [ ] Evidence verified — every number traces to bibliography to source
- [ ] No "uncertain" presented as "solid"
- [ ] Comprehension tests pass on final output
- [ ] Before Shipping checklist (below) passes
- [ ] Verdict: SHIP

### The Orchestration Protocol

The orchestrator (main Claude) manages the pipeline:

1. **After discourse**: Read ground-truth.md and map/MOC.md. Group clusters into work units. Create PLAN.md with sequence and dependencies.
2. **Per work unit**: Launch agents in pipeline order. Check gate checklists between steps.
3. **Orwell gates voice**: After each prose-transforming step (feynman, sagan, jobs), launch orwell. If voice issues found, orwell fixes them directly.
4. **Ebert gates output**: After all steps, launch ebert for the ship/return verdict.
5. **On return**: Ebert specifies which agent and what fix. Orchestrator routes back. Re-run the failed step and everything after it.
6. **Max 2 returns per step**: After 2 failures, escalate to human. The agent cannot resolve this alone.

### When to Skip Steps

| Step | Skip when | Mark in PLAN.md |
|------|-----------|-----------------|
| Cartography | Single source, already well-known | `skip: single source` |
| Dispositio | Single deliverable (no collection) | `skip: single deliverable` |
| Actio (figures) | No visual artifacts needed | `skip: no visuals` |
| Actio (staging) | No experience design needed | `skip: no staging` |
| Setup | Already have workspace | `skip: workspace exists` |
| Discourse | Never skip | — |
| Inventio + memoria + orwell + critique | Never skip | — |

### Return Routing

When ebert returns content or the orchestrator detects a problem:

| Failure type | Return to | Agent |
|--------------|-----------|-------|
| Evidence errors (wrong numbers, missing sources) | Inventio | feynman re-reads source |
| Modal lock (stuck in one Door) | Memoria | sagan re-weaves |
| Dimensional shift missing | Memoria | sagan re-weaves with ebert's feedback |
| Structural issues (orphans, broken paths) | Dispositio | vyasa re-compiles |
| Voice issues (LLM tells, flat rhythm) | Current step | orwell re-reviews |
| Propagation failure (reader can't reconstruct) | Memoria | sagan re-weaves with ebert's feedback |
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
| **Cumulative voice drift** | Each agent polishes slightly, compound effect erases voice | Orwell after every prose step. Scoped mandates. Voice anchor. |

## Before Shipping

1. Does this trust the learner?
2. Will they discover something themselves?
3. Can the ground-seeker find their door at every point?
4. Can the constituency-seeker feel the contrast in the reasoning?
5. Can the principle-seeker pull their thread from any passage?
6. Is the weave woven, not sequenced?
7. Does a dimensional shift happen — does the explanation cross doors?
8. Does understanding propagate? Can the reader explain it to someone else?
9. Does this still sound like the author? Compare against ground-truth.md — are the rough edges, characteristic phrasings, and voice features intact?
10. Have I trusted what I cannot see?

## References

Spoke skills — load for domain-specific craft:
- [discourse](../discourse/SKILL.md) — Draw out ground truth, voice anchor
- [mapping](../mapping/SKILL.md) — Survey, synthesis, map of contents
- [discovering](../discovering/SKILL.md) — Comprehension transform, Diataxis production formats
- [arranging](../arranging/SKILL.md) — Collection structure, reading paths, layer model
- [voicing](../voicing/SKILL.md) — Writing craft, voice evaluation, anti-LLM-speak
- [evaluating](../evaluating/SKILL.md) — Propagation test, evidence verification, accuracy
- [figures](../figures/SKILL.md) — Diagram type selection, dataviz, animation
- [staging](../staging/SKILL.md) — Medium selection, pacing, progressive disclosure
