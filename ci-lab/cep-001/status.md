# CEP-001: Skills vs Help — Status

**Status**: Draft / Active
**Last Updated**: 2026-03-11

## Thesis

Mechanical interfaces (`--help`) are insufficient for LLM legibility. Skill-format documentation provides semantic glue that improves agent task completion accuracy.

## Experiment Design

Agent searches a controlled memex corpus (8 conversations, 34 fragments) and produces YAML config files. A deterministic grader checks field values against ground truth. No paraphrase variance.

Three subjects compared:
1. **help-only** — memex described via `--help` output
2. **skill-at-tool** — memex described via `--skill` output (semantic layer)
3. **help-plus-agent-skill** — both `--help` and agent-provided skill guidance

## Current State

### Completed

- [x] Experiment infrastructure (ix run, OutcomeSensor, YAML graders)
- [x] 6 task-based YAML probes (replaced vocabulary-graded prose probes)
- [x] 8-conversation corpus ingested into local `.memex/`
- [x] Construct validity (15/15 grader tests passed)
- [x] Phase 1 noise floor (help-only, N=10)

### Phase 1 Results (help-only, N=10)

| Probe | Mean | SD | Verdict |
|-------|------|----|---------|
| task-001 (auth storage) | 100% | 0.00 | CEILING — trivial for help-only |
| task-002 (rate limiting) | 67% | 0.47 | BIMODAL — turn-budget gated |
| task-003 (embedding model) | 100% | 0.00 | CEILING — trivial for help-only |
| task-004 (reranking bug) | 82.5% | 0.12 | CLEAN — partial credit works |
| task-005 (trails vs similar) | 20% | 0.42 | BIMODAL — near floor |
| task-006 (hex ports) | 90% | 0.32 | CLEAN — usable |

### Not Yet Done

- [ ] Phase 2: discrimination check (help-only vs skill-at-tool, N=5)
- [ ] Phase 3: full experiment (all 3 subjects, N=5+)
- [ ] Update proposal with results

## Key Learnings

### Infrastructure Bugs (Fixed)

1. `.memex/config.toml` pointed to wrong database — agent searched empty corpus
2. `max_turns: 5` too tight — agent exhausted turns searching, never produced YAML

### Bimodal Pattern

Probes that score 0% or 100% (nothing in between) are measuring turn-budget efficiency, not information quality. The agent either finds data quickly and aces it, or maxes out turns and produces nothing. This may actually be the right signal — skills should help agents find data more efficiently.

### Evaluation Tax

Most time was spent debugging apparatus, not running experiments. For every hour of measurement: ~10 hours of infrastructure, metric design, and calibration.

## Resume Instructions

```bash
# Phase 2: discrimination check
uv run ix run cep-001 --lab ci-lab --subject help-only --trials 5
uv run ix run cep-001 --lab ci-lab --subject skill-at-tool --trials 5

# Analyze
uv run python ci-lab/cep-001/analyze_phase1.py
```

### Key Files

| File | Purpose |
|------|---------|
| `experiment.yaml` | Experiment config (sensor: outcome, graders: graders.py) |
| `graders.py` | YAML-based graders (GRADERS registry) |
| `tasks/task-*.md` | 6 task probes |
| `subjects/*.md` | 3 subjects (help-only, skill-at-tool, help-plus-agent-skill) |
| `corpus/` | 8 conversations + seed data |
| `validate_graders.py` | Construct validity tests |
| `analyze_phase1.py` | Noise floor analysis with rollback triggers |
| `PLAN-task-based-probes.md` | Detailed plan with Phase 1a/1b notes |
| `proposal.md` | Original CEP proposal |

### Prerequisites

- Local `.memex/` must exist with corpus ingested (check: `cd ci-lab/cep-001 && memex corpus`)
- All subjects use `max_turns: 10`
