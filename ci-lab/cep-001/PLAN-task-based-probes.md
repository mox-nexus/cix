# CEP-001 Reimplementation: Task-Based YAML Probes

**Status**: Implementation complete, ready for Phase 1
**Date**: 2026-03-10

## Why

The current probes ask natural language questions and grade the agent's prose response for vocabulary overlap. This conflates three variables:

1. Did the agent find the information? (search capability)
2. Did the agent understand the information? (comprehension)
3. Did the agent use the same words we expected? (paraphrase variance)

Variable 3 is pure measurement noise. Evidence:
- out-002 scores 0% for ALL subjects — agents find rate limiting data but paraphrase it
- out-005 scores 84%+ for ALL subjects — common words like "trail" match trivially
- The 7pp gap (35.7% → 42.7%) is within the noise range

**Fix**: Replace vocabulary-graded prose with task-based YAML generation. Parse YAML, compare field values. Deterministic, no paraphrase variance.

---

## New Probe Design

Each probe asks the agent to search memex and produce a YAML config file. The grader parses YAML and checks per-field values. Same 8 corpus conversations, same 3 subjects, same sensor infrastructure.

### task-001: Auth Token Storage

**Prompt:**
> Search memex for the auth token storage decision. Based on what you find, generate the following YAML config file. Fill in every field based on the corpus — do not guess.
>
> ```yaml
> # auth-storage.yaml
> database: ""           # which database was chosen
> deployment_model: ""   # deployment topology (e.g. single-node, clustered)
> analytics_capability:  # true/false — was analytics a deciding factor?
> primary_use_case: ""   # what the analytics would be used for
> ```

**Ground truth**: database=duckdb, deployment_model=single-node, analytics_capability=true, primary_use_case=token usage patterns

**Grading**: 4 fields, equal weight. `contains` matching for strings, `boolean` for analytics_capability.

### task-002: Rate Limiting Config

**Prompt:**
> Search memex for the rate limiting strategy. Based on what you find, generate the following YAML config file with the exact numbers from the decision.
>
> ```yaml
> # rate-limiter.yaml
> algorithm: ""              # algorithm name (e.g. sliding window, token bucket)
> tiers: 0                   # number of tiers
> global_rate_per_min: 0     # global tier: requests per minute
> global_burst: 0            # global tier: burst capacity
> per_user_rate_per_min: 0   # per-user tier: requests per minute
> per_user_burst: 0          # per-user tier: burst capacity
> backoff_initial_ms: 0      # initial backoff in milliseconds
> ```

**Ground truth**: algorithm=token bucket, tiers=2, global_rate_per_min=40, global_burst=15, per_user_rate_per_min=10, per_user_burst=5, backoff_initial_ms=500

**Grading**: 7 fields, equal weight. `numeric` matching for numbers, `contains` for algorithm.

### task-003: Embedding Model

**Prompt:**
> Search memex for the embedding model selection. Generate the following YAML config.
>
> ```yaml
> # embedding.yaml
> model_name: ""        # full model name
> dimensions: 0         # embedding dimensions
> inference_mode: ""    # local or cloud
> acceleration: ""      # hardware acceleration framework (e.g. coreml, cuda)
> ```

**Ground truth**: model_name=nomic-embed-text-v1.5, dimensions=768, inference_mode=local, acceleration=coreml

**Grading**: 4 fields, equal weight.

### task-004: Reranking Bug

**Prompt:**
> Search memex for the reranking bug. Generate a bug report config.
>
> ```yaml
> # bug-report.yaml
> root_cause: ""        # what was wrong (one sentence)
> fix: ""               # what fixed it (one sentence)
> component: ""         # which component/path was affected
> commit: ""            # git commit hash that introduced the bug
> ```

**Ground truth**: root_cause contains "ascending" or "descending" or "reverse", fix contains "reverse", component contains "rerank" or "cross-encoder", commit=a3f7e21

**Grading**: 4 fields. `contains` for root_cause/fix/component, `exact` for commit (prefix match on 7 chars).

### task-005: Trails vs Similar

**Prompt:**
> Search memex for the trail architecture discussion. Generate a feature comparison config.
>
> ```yaml
> # feature-comparison.yaml
> trail_type: ""          # curated or algorithmic
> trail_creation: ""      # how trails are created (manual or automatic)
> similar_type: ""        # curated or algorithmic
> similar_method: ""      # technical method used for similarity
> trail_use_case: ""      # primary use case (one word)
> similar_use_case: ""    # primary use case (one word)
> ```

**Ground truth**: trail_type=curated, trail_creation=manual, similar_type=algorithmic, similar_method contains "cosine" or "embedding", trail_use_case=synthesis, similar_use_case=exploration

**Grading**: 6 fields, equal weight.

### task-006: Hexagonal Ports

**Prompt:**
> Search memex for the hexagonal port implementation decision. Generate an architecture decision config.
>
> ```yaml
> # arch-decision.yaml
> chosen_pattern: ""         # the Python construct chosen for ports
> typing_style: ""           # structural or nominal
> runtime_check: ""          # decorator/mechanism for isinstance support
> rejected_alternative: ""   # what was explicitly rejected
> ```

**Ground truth**: chosen_pattern contains "Protocol", typing_style=structural, runtime_check contains "runtime_checkable", rejected_alternative contains "ABC"

**Grading**: 4 fields, equal weight.

---

## Grader Architecture

Single unified YAML grader in `ci-lab/cep-001/graders.py`.

### Core functions

```python
def _extract_yaml(response: str) -> dict | None
    """Extract YAML from ```yaml code blocks or raw content. Returns None if unparseable."""

def _field_match(actual: Any, expected: Any, match_type: str) -> bool
    """Compare one field. Match types: exact, contains, numeric, boolean."""

def _grade_yaml(response: str, field_specs: list[tuple]) -> float
    """Universal YAML grader. Returns weighted score [0.0, 1.0]."""
```

### Per-probe graders

Thin wrappers calling `_grade_yaml` with field specs:

```python
def grade_task_002(response: str) -> float:
    return _grade_yaml(response, [
        ("algorithm", "token bucket", 1.0, "contains"),
        ("tiers", 2, 1.0, "numeric"),
        ("global_rate_per_min", 40, 1.0, "numeric"),
        ("global_burst", 15, 1.0, "numeric"),
        ("per_user_rate_per_min", 10, 1.0, "numeric"),
        ("per_user_burst", 5, 1.0, "numeric"),
        ("backoff_initial_ms", 500, 1.0, "numeric"),
    ])
```

### GRADERS registry (same pattern as current)

```python
GRADERS = {
    "task-001": grade_task_001,
    "task-002": grade_task_002,
    ...
}
```

---

## What Changes, What Doesn't

| Component | Changes? | Details |
|-----------|----------|---------|
| `graders.py` | **Replace** | New YAML grader architecture |
| `tasks/*.md` | **Replace** | 6 new `task-*.md` probes, archive old `out-*.md` |
| `experiment.yaml` | **Minor** | Update description only |
| `subjects/*.md` | **No** | Same 3 subjects, same system prompts |
| `corpus/` | **No** | Same 8 conversations |
| `OutcomeSensor` | **No** | Already format-agnostic, delegates to grader functions |
| `ExperimentConfig` | **No** | No structural changes |
| Composition root | **No** | Same wiring |

---

## Ixian Protocol: Phased Execution

### Phase 0: Construct Validity (before spending API tokens)

Create `validate_graders.py`:
1. Perfect responses (exact ground truth in YAML) → must score >= 0.95
2. Empty/wrong responses → must score <= 0.1
3. Partial responses (some fields correct) → proportional scores

**Rollback**: If perfect responses don't score 1.0, the grader is broken.

### Phase 1: Noise Floor (help-only only)

```bash
ix run cep-001 --lab ci-lab --subject help-only --trials 10
```

**Measure per-probe**:
- Mean score, standard deviation
- Score range (min, max)

**Rollback triggers** (any one = redesign that probe):
- Mean = 0.0 on all 10 trials (floor — task impossible)
- Mean = 1.0 on all 10 trials (ceiling — task trivial)
- SD > 0.35 (too noisy for N=5 discrimination)
- YAML extraction fails > 50% of trials

**Decision rule**:
- 0/6 trigger → proceed to Phase 2
- 1-2 trigger → redesign those probes, re-run Phase 1 for them
- 3+ trigger → fundamental rethink

### Phase 2: Discrimination Check

```bash
ix run cep-001 --lab ci-lab --subject help-only
ix run cep-001 --lab ci-lab --subject skill-at-tool
```

N=5 per probe per subject.

**Success criteria**:
- At least 2 probes show score difference > 15pp
- Overall mean difference > 10pp
- Cohen's d > 0.5

**Rollback**: Cohen's d < 0.3 → apparatus can't detect the treatment effect.

### Phase 3: Full Experiment

All 3 subjects, N=5+. Update proposal with results.

---

## Risk: Agent YAML Compliance

The biggest risk: agents don't produce valid YAML.

**Mitigations**:
1. Explicit schema in prompt (```yaml block with field names and types)
2. `_extract_yaml` takes last ```yaml block (handles agent explaining before generating)
3. If YAML fails, score = 0.0 (correct — agent failed the task)
4. If Phase 1 shows > 50% extraction failures, add "Output ONLY the YAML block" to prompts

---

## Implementation Sequence

| # | Step | Files | Depends on |
|---|------|-------|------------|
| 1 | Write new graders | `graders.py` | — |
| 2 | Write new probes | `tasks/task-001.md` through `task-006.md` | — |
| 3 | Archive old probes | `tasks/out-*.md` → `tasks/archive/` | — |
| 4 | Write construct validity test | `validate_graders.py` | Step 1 |
| 5 | Run construct validity | — | Step 4 |
| 6 | Run Phase 1 (noise floor) | — | Step 5 passes |
| 7 | Analyze Phase 1 | — | Step 6 |
| 8 | Run Phase 2 (discrimination) | — | Step 7 passes |
| 9 | Run Phase 3 (full) | — | Step 8 passes |
| 10 | Update proposal | `proposal.md` | Step 9 |

Steps 1-4 are implementation (can be done in one session). Steps 5-10 are execution and analysis.

---

## Success Criteria for the New Apparatus

The redesign succeeds if:

1. **No floor/ceiling**: Every probe mean in [0.1, 0.9] for help-only
2. **Deterministic grading**: Identical responses → identical scores
3. **YAML reliability**: >90% of trials produce parseable YAML
4. **Discrimination**: At least 2 probes show >15pp gap between subjects
5. **Monotonicity**: help-only <= skill-at-tool <= help-plus-agent-skill (mean)

The redesign fails if:
- Agents don't produce YAML reliably
- All probes score similarly across subjects (no discrimination)
- Scores measure YAML formatting skill, not information retrieval

---

## Implementation Status

| # | Step | Status |
|---|------|--------|
| 1 | Write new graders (`graders.py`) | Done |
| 2 | Write new probes (`tasks/task-001.md` through `task-006.md`) | Done |
| 3 | Archive old probes (`tasks/archive-prose-probes/`) | Done |
| 4 | Write construct validity test (`validate_graders.py`) | Done |
| 5 | Run construct validity | Done — 15/15 passed |
| 6 | Run Phase 1 (noise floor) | Done — Phase 1b passed partially (see notes) |
| 7 | Analyze Phase 1 | Done — 2 clean, 2 ceiling, 2 bimodal (see notes) |
| 8 | Run Phase 2 (discrimination) | Pending |
| 9 | Run Phase 3 (full) | Pending |
| 10 | Update proposal | Pending |

---

## Phase 1a: First Run (Failed — Infrastructure, Not Apparatus)

**Date**: 2026-03-10
**Result**: 6/6 probes triggered rollback (4 FLOOR, 1 NOISY, 1 YAML_FAIL)

### Root Cause

Two infrastructure bugs, NOT grader/probe design:

1. **Corpus misconfiguration**: `.memex/config.toml` pointed to `cep-003-skills-vs-references/.memex/corpus.duckdb` instead of `cep-001/.memex/corpus.duckdb`. Agent searched an empty database. All `memex dig` calls returned nothing.

2. **max_turns too tight**: `max_turns: 5` gave the agent no runway. Task requires: search (1-2 turns) → refine/thread (1-2 turns) → produce YAML (1 turn). With 5 turns max, agent exhausted turns searching and never produced YAML output.

### Fixes Applied

1. Fixed `.memex/config.toml` path → verified `memex corpus` shows 34 fragments, 8 conversations
2. Increased `max_turns` from 5 to 10 across all three subjects (equal treatment)

### Diagnostic Evidence

After fixes, single-trial diagnostics:
- task-001: 100% (4/4 fields, 6 turns used)
- task-002: 100% (7/7 fields, 6 turns used)

Both found data, produced valid YAML, all fields matched ground truth.

### Key Observation

The binary scoring pattern (0% or 100%, never partial) was the diagnostic clue. With 4-7 fields per grader, partial scores should be common. Scoring 0% on ALL fields meant `_extract_yaml` returned None — no YAML at all. The agent never reached the YAML-production step.

## Phase 1b: Second Run (Partially Passed)

**Date**: 2026-03-10
**Result**: 2/6 clean, 2/6 ceiling, 2/6 bimodal

| Probe | Mean | SD | Verdict |
|-------|------|----|---------|
| task-001 | 100% | 0.00 | CEILING — too easy for help-only |
| task-002 | 67% | 0.47 | BIMODAL — 0% or 100%, turn-budget gated |
| task-003 | 100% | 0.00 | CEILING — too easy for help-only |
| task-004 | 82.5% | 0.12 | CLEAN — partial credit works (75% or 100%) |
| task-005 | 20% | 0.42 | BIMODAL + near floor — 8/10 zeros |
| task-006 | 90% | 0.32 | CLEAN — borderline but usable |

### Key Insight

Bimodal pattern = turn-budget efficiency, not grading quality. Agent either finds data quickly (scores 100%) or maxes out turns searching (scores 0%, no YAML produced). This is arguably the RIGHT signal — skills should help agents find data more efficiently.

### Recommendation (Not Yet Executed)

Proceed to Phase 2 with all 6 probes. The bimodal probes test whether skills reduce the 0% rate (agent finds data faster). The ceiling probes add no information but no harm. The 2 clean probes provide traditional variance for effect size.

### Work Paused

Session stopped 2026-03-10. Infrastructure bugs consumed most of the 3-day timeline.

---

## Bootstrap Prompt (New Session)

Copy-paste this to resume work:

```
I'm continuing CEP-001 — the experiment testing whether skill-format documentation improves LLM task completion over --help.

We just reimplemented the probes from vocabulary-graded prose answers to task-based YAML config generation. Read the plan first:

  ci-lab/cep-001/PLAN-task-based-probes.md

Implementation is complete (steps 1-5). Construct validity passed (15/15). The next step is:

**Phase 1: Noise Floor** — Run help-only subject with N=10 trials to establish baseline variance.

```bash
uv run ix run cep-001 --lab ci-lab --subject help-only --trials 10
```

After Phase 1 completes, analyze per-probe mean/SD/range. Check rollback triggers (see plan). If it passes, proceed to Phase 2 (discrimination check: help-only vs skill-at-tool, N=5).

Key files:
- Plan: ci-lab/cep-001/PLAN-task-based-probes.md
- Graders: ci-lab/cep-001/graders.py (YAML-based, _extract_yaml → _grade_yaml)
- Probes: ci-lab/cep-001/tasks/task-001.md through task-006.md
- Subjects: ci-lab/cep-001/subjects/ (unchanged: help-only, skill-at-tool, help-plus-agent-skill)
- Corpus: ci-lab/cep-001/corpus/ (8 conversations, ground truth)
- Construct validity: ci-lab/cep-001/validate_graders.py (15/15 passed)
- Proposal: ci-lab/cep-001/proposal.md (needs updating after Phase 3)
- Sensor: tools/ix/src/ix/eval/sensors.py (OutcomeSensor — no changes needed)
- ExperimentResults now has `subject` field: tools/ix/src/ix/eval/models.py

Previous run results (prose-based graders, for comparison):
  Run 1 (string containment): help-only 36%, skill-at-tool 78%, combined 66%
  Run 3 (vocabulary graders): help-only 35.7%, skill-at-tool 42.7%, combined 48.3%

The thesis: mechanical interfaces (--help) are insufficient for LLM legibility. Skills provide semantic glue that improves task completion.
```
