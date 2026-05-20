---
name: review
description: Use when the user asks to "run an antifragile review", "ACES review", "do an antifragile review on this", "review this for structural fragility", "diagnose this platform", "check this platform for the cycle", or requests a focused structural review using the ACES (Adaptable, Composable, Extensible Software) framework. Composes with other review skills; does not replace them.
---

# Antifragile Review

A workflow skill that runs a structural-fragility review using ACES. Delegates the framework itself to the `aces` skill and dispatches domain-specific reasoning to the `antifragile-arch` and `antifragile-sec` agents.

## This Composes, It Does Not Replace

This skill runs **one kind** of review: a structural-fragility review using the ACES framework. It does not replace:

- **`guild-arch:architecture`** — multi-perspective architectural deliberation (Taleb, Dijkstra, Burner, etc.). If the user wants breadth, route there first and invoke this skill as one lens among many.
- **`guild-arch:operations`** — production-readiness and failure-mode review. Structural fragility is upstream; operations is runtime. Both apply for most real systems.
- **`guild-arch:trust-boundaries`** — the architectural security review skill. Use alongside `antifragile-sec` for a complete security posture.
- **`guild-arch:design`** — API and interface design review. Sits at interface level; ACES sits at platform topology.
- **`modularity`** (external plugin) — class/module-level coupling analysis. Coexist.
- Product-specific review flows (e.g., `code-review` for code-level diffs).

When the user says "review this," do not assume they want only an antifragile review. Offer the structural lens (this skill) and invite them to add `guild-arch:architecture` for multi-perspective deliberation or `code-review` for code-level concerns.

## When to Use This Skill

Invoke when the user's request is explicitly about structural fragility, coupling cycles, ACES properties, boundary-vs-Inner-Platform discrimination, or a named archetype (Coupled Monolith, Fragmented Estate, SDK Frontier).

Prefer this skill when the user says "antifragile review," "ACES review," or "review this for structural fragility."

Prefer `guild-arch:architecture` when the user says "review this architecture" without specifying a lens — then offer ACES as one available lens.

## Workflow

Execute in order.

### Step 1: Parse the target

Identify what is being reviewed. Accepted forms:

- A file path or directory (read it).
- A design document (read it).
- A prose description of a platform or proposal.
- An architecture snippet in the conversation already.

If the target is ambiguous or missing, ask once for clarification. Do not invent a target.

### Step 2: Decide the lens(es)

Signals that select the lens:

| Signal | Lens |
|---|---|
| Auth, trust, PII, leak, information flow, rate limits, authorization, adversarial, tenant isolation | `antifragile-sec` |
| Platform, gateway, proxy, plugin, pipeline, monolith, migration, boundary, xDS, ext_proc, SDK, orchestration, runtime coupling | `antifragile-arch` |
| Both categories present | Both agents |
| None strongly present | `antifragile-arch` by default; ask if unsure |

If the user wants multi-perspective deliberation (not ACES-specific), say so and offer to route to `guild-arch:architecture` instead.

### Step 3: Load the `aces` skill

The `aces` skill carries the framework vocabulary, the diagnostic protocol, the inversion mechanisms, the Boundary Test, and the references. Pull from its body and references as needed. Do not re-derive any of it here.

### Step 4: Dispatch the agent(s)

Use the Task tool with `subagent_type` of `antifragile:antifragile-arch` and/or `antifragile:antifragile-sec`. Pass the target and context to the agent. The agent returns a structured verdict per its own output format.

### Step 5: Synthesize

If multiple agents ran, consolidate:

- **Convergent findings** — both agents flagged Opacity, for example.
- **Divergent findings** — arch says APPROVE, sec says CONCERN. Note both.
- **Correctness-vs-trust boundary** — explicit when security is involved.

If a boundary was proposed, include the arithmetic Boundary Test result.

### Step 6: Scope limits

Always include:

- Magnitude is calibration-dependent, not derived from the model.
- The model assumes a logical observer; real platforms are distributed.
- Organizational dynamics (why 40:1 returns don't overcome incentive gradients) are deferred to Conway's Ratchet, a separate piece.

### Step 7: Federation pointers

State what this review did **not** cover and where to go:

- Multi-perspective deliberation → `guild-arch:architecture`
- Production readiness → `guild-arch:operations`
- Full architectural security review → `guild-arch:trust-boundaries`
- Class-level coupling → `modularity` (external)
- Evidence / calibration → `craft-research:verifying`

## Output

A single consolidated review. Sections:

```
# Antifragile Review: <target name>

## Archetype
<Coupled Monolith | Fragmented Estate | SDK Frontier | other | none>

## Channels Active
<per-channel findings with evidence>

## Coupling Types
<system-to-terrain | contributor-to-platform | behavior-to-integration>

## Recommended Inversions
<Adaptability / Extensibility / Composability, each with concrete mechanism>

## Boundary Test (if applicable)
<arithmetic + verdict>

## Security Cut (if applicable)
<correctness-vs-trust flags, information-flow concerns, adversary-model notes>

## Per-Lens Verdicts
- antifragile-arch: <verdict> — <one-line rationale>
- antifragile-sec: <verdict> — <one-line rationale> (if invoked)

## Convergence / Divergence (if multi-lens)
<where lenses agree, where they disagree>

## Scope Limits
<magnitude, distributed observation, Conway's Ratchet>

## What This Review Did Not Cover
<federation pointers to guild-arch, modularity, etc.>

## Next Actions
<concrete steps>
```

Do not echo the user's input. State what was reviewed, what was found, and what to do next.

## Framework Reference

See the `aces` skill for:

- The three channels and their coupling types
- The diagnostic protocol
- The inversion mechanisms and hex-arch mapping
- The Boundary Test and Pipeline Envelope pattern
- Cost model, measurement surrogates, falsification conditions

This skill is the workflow. The `aces` skill is the framework.
