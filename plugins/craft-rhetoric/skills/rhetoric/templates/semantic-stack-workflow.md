# Pipeline Workflow

One pipeline. Every content project. Orchestrator (main Claude) adapts per project. Orwell gates voice after prose steps. Ebert makes the ship/return call.

## Workspace Structure

```
.rhet/
├── ground-truth.md       socrates (discourse) — immutable voice reference
├── voice.md              socrates (discourse) — voice features + habits
├── map/                  magellan (MOC.md + cluster files + SOURCES.md)
├── PLAN.md               orchestrator (tracking)
├── inventio/             feynman — comprehend + draft
├── memoria/              sagan — weave (copies from inventio/)
├── arrangement/          vyasa — structure, reading paths
├── figures/              tufte — visual artifacts
├── staging/              jobs — experience specs
├── critique/             ebert — evaluation reports
```

**Boundary**: Only magellan sees outside the workspace. Feynman follows references from map/MOC.md to sources. Everyone else works within the workspace only.

## Phase 1: Foundation

Foundation steps run once per project.

### Step 1: Setup
**Script**: `./setup.sh [workspace-path]`
**Output**: `.rhet/` workspace with all subdirectories, added to `.gitignore`
**Gate**: Workspace directory exists

### Step 2: Discourse (socrates)
**Agent**: socrates | **Skills**: `rhetoric`, `discourse`
**Output**: `ground-truth.md` + `voice.md`
**Gate**:
- [ ] Communicate — purpose articulated
- [ ] Setup — audience, medium, constraints named
- [ ] Substance — content grounded in what the human knows
- [ ] State-back confirmed
- [ ] Ground truth written to file
- [ ] Voice anchor co-created

### Step 3: Cartography (magellan)
**Agent**: magellan | **Skills**: `rhetoric`, `mapping`
**Input**: ground-truth.md + source material (outside workspace)
**Output**: `map/` (MOC.md + cluster files + SOURCES.md)
**Gate**:
- [ ] Every source inventoried (type, location, scope, strength)
- [ ] Sources clustered by topic/claim
- [ ] Connections traced (reinforcement, tension, dependency)
- [ ] Gaps named with type and impact

### Step 3b: Orchestrator creates PLAN.md
**Input**: ground-truth.md + map/MOC.md
**Output**: `PLAN.md`

Group clusters into work units, sequence them, note dependencies. This is the orchestrator's job, not a separate agent.

---

## Phase 2: Per-Deliverable

The evaluator-optimizer loop. Orchestrator launches agents, orwell gates voice, ebert makes the final call.

### Step 4: Inventio (feynman)
**Agent**: feynman | **Skills**: `rhetoric`, `discovering`
**Input**: PLAN.md + ground-truth.md + map/MOC.md (follows references to sources)
**Output**: `inventio/`
**Gate**:
- [ ] Four-pass reading complete
- [ ] All three doors present in draft
- [ ] Entry door chosen deliberately
- [ ] Evidence levels labeled
- [ ] No claims without source attribution
- [ ] Numbers verified against source text (grep, not memory)

### Step 4b: Orwell (voice check)
**Agent**: orwell | **Skills**: `rhetoric`, `voicing`
**Input**: `inventio/` + `ground-truth.md` + `voice.md`
**Gate**:
- [ ] No LLM tells introduced
- [ ] Voice features preserved
- [ ] Rough edges from ground-truth.md intact

### Step 5: Memoria (sagan)
**Agent**: sagan | **Skills**: `rhetoric`
**Input**: `inventio/` (post-orwell) + ground-truth.md
**Output**: `memoria/` (copies from inventio/, weaves)
**Gate**:
- [ ] Strong doors from inventio preserved
- [ ] Missing doors threaded into existing passages
- [ ] At least one dimensional shift
- [ ] Content woven, not sequenced
- [ ] Universal thread surfaced

### Step 5b: Orwell (voice check)
**Agent**: orwell | **Skills**: `rhetoric`, `voicing`
**Input**: `memoria/` + `ground-truth.md` + `voice.md`
**Gate**:
- [ ] No LLM tells introduced
- [ ] Voice features preserved
- [ ] Specific phrasing not replaced with generic synonyms

### Step 6: Dispositio (vyasa)
**Agent**: vyasa | **Skills**: `rhetoric`, `arranging`
**Input**: `memoria/` (post-orwell) + PLAN.md
**Output**: `arrangement/`
**Skip if**: single deliverable (no collection)
**Gate**:
- [ ] Layer model applied
- [ ] Reading paths defined
- [ ] Single source of truth
- [ ] Diataxis type assigned
- [ ] No orphan documents

### Step 7: Actio (tufte / jobs)
**Agent**: tufte (visuals) | **Skills**: `rhetoric`, `figures`
**Agent**: jobs (experience) | **Skills**: `rhetoric`, `staging`
**Input**: `arrangement/` (or `memoria/` if no dispositio)
**Output**: `figures/` and/or `staging/`
**Skip if**: no visuals or staging needed
**Gate**:
- [ ] Every visual serves information structure
- [ ] Reduced-motion fallbacks
- [ ] Data-ink ratio acceptable
- [ ] If staging: beat structure + progressive disclosure
- [ ] Prose and visuals integrated

### Step 7b: Orwell (voice check after jobs)
Only if jobs ran. Did experience design sanitize the prose?
**Gate**:
- [ ] No LLM tells introduced by staging
- [ ] Voice features preserved

### Step 8: Critique (ebert)
**Agent**: ebert | **Skills**: `rhetoric`, `evaluating`
**Input**: final output + ground-truth.md
**Output**: `critique/`
**Gate**:
- [ ] Propagation test passed
- [ ] Three Doors traversal complete
- [ ] Evidence verified (numbers trace to bibliography to source)
- [ ] No "uncertain" as "solid"
- [ ] Comprehension tests pass
- [ ] Before Shipping checklist passes
- [ ] **Verdict: SHIP or RETURN**

---

## Orchestration Protocol

1. After discourse: read ground-truth.md + map/MOC.md, create PLAN.md
2. Per work unit: launch agents in pipeline order
3. Orwell gates voice after each prose-transforming step (feynman, sagan, jobs)
4. Ebert gives the final verdict
5. On return: ebert specifies which agent and what fix. Re-run from that step.
6. Max 2 returns per step → escalate to human

## Return Routing

| Failure type | Return to | Agent |
|--------------|-----------|-------|
| Evidence errors | inventio/ | feynman |
| Modal lock | memoria/ | sagan |
| Dimensional shift missing | memoria/ | sagan |
| Structural issues | arrangement/ | vyasa |
| Voice issues | current step | orwell |
| Propagation failure | memoria/ | sagan |
| Content gaps | discourse | human |
