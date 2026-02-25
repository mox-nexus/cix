# Unified Pipeline Workflow

One pipeline. Every content project. Planner adapts per project. Socrates gates between steps.

## Workspace Structure

```
.rhet/
├── ground-truth.md       discourse (human)
├── map/                  magellan (MOC.md + cluster files + SOURCES.md)
├── PLAN.md               planner (all agents update)
├── discovering/          feynman — comprehension state
├── inventio/             feynman — drafted content
├── memoria/              sagan — woven content (copies from inventio/, weaves)
├── arrangement/          vyasa — structure, reading paths
├── voicing/              orwell — voiced content (copies from memoria/)
├── figures/              tufte — visual artifacts
├── staging/              jobs — experience specs
├── evaluation/           socrates — reports
```

**Boundary**: Only magellan sees outside the workspace. Feynman follows references from map/MOC.md to sources. Everyone else works within the workspace only.

## Phase 1: Foundation

Foundation steps run once per project.

### Step 1: Setup
**Script**: `./setup.sh [workspace-path]`
**Output**: `.rhet/` workspace with all subdirectories, added to `.gitignore`
**Gate**: Workspace directory exists

### Step 2: Discourse
**Agent**: human (agent-facilitated)
**Output**: `ground-truth.md`
**Gate**:
- [ ] Communicate — purpose articulated
- [ ] Setup — audience, medium, constraints named
- [ ] Substance — content grounded in what the human knows
- [ ] State-back confirmed
- [ ] Ground truth written to file

### Step 3: Cartography
**Agent**: magellan | **Skills**: `rhetoric`, `mapping`
**Input**: ground-truth.md + source material (outside workspace)
**Output**: `map/` (MOC.md + cluster files + SOURCES.md)
**Gate**:
- [ ] Every source inventoried (type, location, scope, strength)
- [ ] Sources clustered by topic/claim
- [ ] Connections traced (reinforcement, tension, dependency)
- [ ] Gaps named with type and impact

### Step 4: Planning
**Agent**: planner | **Skills**: `rhetoric`
**Input**: ground-truth.md + map/MOC.md
**Output**: `PLAN.md` (root) + `*/PLAN.md` (per-directory)
**Gate**:
- [ ] Clusters grouped into work units (not named as articles)
- [ ] Dependencies explicit
- [ ] Sequence justified
- [ ] Per-directory plans with gate checklists and discourse context

---

## Phase 2: Per-Deliverable

The orchestrator reads PLAN.md, launches agents, gates with socrates.

### Step 5: Inventio (feynman)
**Agent**: feynman | **Skills**: `rhetoric`, `discovering`
**Input**: PLAN.md + ground-truth.md + map/MOC.md (follows references to sources)
**Output**: `discovering/` + `inventio/`
**Gate**:
- [ ] Four-pass reading complete
- [ ] All three doors present in draft
- [ ] Entry door chosen deliberately
- [ ] Evidence levels labeled
- [ ] No claims without source attribution
- [ ] Numbers verified against source text (grep, not memory)

### Step 6: Memoria (sagan)
**Agent**: sagan | **Skills**: `rhetoric`
**Input**: `inventio/` + ground-truth.md
**Output**: `memoria/` (copies from inventio/, weaves)
**Gate**:
- [ ] Strong doors from inventio preserved
- [ ] Missing doors threaded into existing passages
- [ ] At least one dimensional shift
- [ ] Content woven, not sequenced
- [ ] Universal thread surfaced

### Step 7: Dispositio (vyasa)
**Agent**: vyasa | **Skills**: `rhetoric`, `arranging`
**Input**: `memoria/` + PLAN.md
**Output**: `arrangement/`
**Skip if**: single deliverable (no collection)
**Gate**:
- [ ] Layer model applied
- [ ] Reading paths defined
- [ ] Single source of truth
- [ ] Diataxis type assigned
- [ ] No orphan documents

### Step 8: Elocutio (orwell)
**Agent**: orwell | **Skills**: `rhetoric`, `voicing`, `evaluating`
**Input**: `memoria/` + `arrangement/`
**Output**: `voicing/` (copies from memoria/, applies voice)
**Gate**:
- [ ] Four-pass voice review complete
- [ ] Zero LLM tells
- [ ] Specificity restored
- [ ] Rhythm varies
- [ ] Reads as human-authored

### Step 9: Actio (tufte / jobs)
**Agent**: tufte (visuals) | **Skills**: `rhetoric`, `figures`
**Agent**: jobs (experience) | **Skills**: `rhetoric`, `staging`
**Input**: `voicing/`
**Output**: `figures/` and/or `staging/`
**Skip if**: no visuals or staging needed
**Gate**:
- [ ] Every visual serves information structure
- [ ] Reduced-motion fallbacks
- [ ] Data-ink ratio acceptable
- [ ] If staging: beat structure + progressive disclosure
- [ ] Prose and visuals integrated

### Step 10: Evaluate (socrates)
**Agent**: socrates | **Skills**: `rhetoric`, `evaluating`
**Input**: `voicing/` (or `figures/`/`staging/`) + ground-truth.md
**Output**: `evaluation/`
**Gate**:
- [ ] Propagation test passed
- [ ] Three Doors traversal complete
- [ ] Evidence verified (numbers trace to bibliography to source)
- [ ] No "uncertain" as "solid"
- [ ] Comprehension tests pass
- [ ] Before Shipping checklist passes

---

## Orchestration Protocol

Between every agent step:

1. Read PLAN.md — identify next step
2. Launch assigned agent
3. Agent completes — updates PLAN.md
4. Socrates gates — verifies checklist
5. Pass → advance
6. Fail → return to agent with feedback (max 2 returns)
7. 2 failures → escalate to human

## Return Routing

| Failure type | Return to | Agent |
|--------------|-----------|-------|
| Evidence errors | inventio/ | feynman |
| Modal lock | memoria/ | sagan |
| Dimensional shift missing | memoria/ | sagan |
| Structural issues | arrangement/ | vyasa |
| Voice issues | voicing/ | orwell |
| Propagation failure | memoria/ | sagan |
| Content gaps | discourse | human |
