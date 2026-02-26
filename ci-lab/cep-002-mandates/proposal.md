# CEP-002: Mandates vs Motivations

**Status**: Draft
**Author**: Yashodeep Vyas
**Created**: 2026-02-14
**Lineage**: lab-1337 REP-002 (v1-v4)

## Question

Does prescribing HOW help, hurt, or not matter?

## Hypothesis

System prompts explaining motivation (WHY) produce higher task completion scores than system prompts prescribing process (HOW), measured on discriminating tasks.

## Background

The WHY > HOW principle is central to the cix design philosophy. Lab-1337 REP-002 ran 4 experiment versions investigating this:

- **v1-v3**: Floor/ceiling effects masked differences. Easy tasks — all conditions passed. Hard tasks — all failed.
- **v4**: Used "discriminating" tasks (30-70% baseline pass rate). Found signal but insufficient N for strong claims.

Key lab-1337 finding: **task difficulty dominates prompting strategy**. No condition wins globally. The task must be in the discrimination zone or the experiment produces noise.

The safe-calculator task from lab-1337 is specifically designed as a discriminating task — the "safe" requirement is intentionally vague, testing judgment under ambiguity. This is where mandate vs motivation framing should show the biggest difference.

## Design

**Independent variable**: System prompt framing (6 conditions on the autonomy spectrum)

**Subjects** (conditions, ordered from least to most structured):

| Subject | Framing | What it tests |
|---------|---------|---------------|
| `baseline` | Minimal — just the task | Lower bound |
| `full-autonomy` | "Use your best judgment" | Maximum trust |
| `motivation` | WHAT + WHY + CONSTRAINTS | Motivations without process |
| `principle-guided` | Principles without prescribed steps | Guidance without prescription |
| `mandate-template` | WHAT + WHY + required response sections | Mild structure imposition |
| `highly-structured` | Step-by-step prescribed process | Maximum prescription |

**Sensor**: `function-test` — extracts code, runs against test cases.

**Trials**: 10 per subject per task (Ixian minimum for detecting 20pp effect size with 80% power).

**Tasks**: `safe-calculator` (discriminating, 7 test categories). SWE-bench tasks deferred until RepoTestSensor exists.

**Total runs**: 1 task × 6 subjects × 10 trials = 60

## Phased Execution (Ixian Protocol)

### Phase 0: Noise Floor (10 runs)
Run `baseline` × 10 trials on safe-calculator. Measure:
- Mean score and std dev
- Per-category pass rates
- Min/max spread

**Gate**: If std dev > 0.25, the sensor or task is too noisy — redesign before proceeding.
**Gate**: If mean > 0.90, task has ceiling effect — need harder task.

### Phase 1: 3-Condition Pilot (30 runs)
Run the three most differentiated conditions: `baseline`, `motivation`, `highly-structured` × 10 trials.

**Gate**: If P(motivation > highly_structured) < 0.70, hypothesis is not supported. Reconsider before spending on full matrix.

### Phase 2: Full Matrix (60 runs)
All 6 conditions × 10 trials. Only if Phase 1 shows signal.

## Metrics

**Primary**: Mean score per subject (0.0-1.0, weighted across 7 test categories).

**Secondary — correctness decomposition**:
| Category | What it reveals |
|----------|----------------|
| basic | Procedure-following (all conditions should pass) |
| precision | Attention to detail |
| injection | Judgment under adversarial input |
| resource | Defensive thinking |
| math_error | Error handling |
| functions | API knowledge |
| invalid | Edge case reasoning |

Hypothesis: motivation-framed prompts outperform on `injection` and `resource` (judgment-heavy); highly-structured may outperform on `basic` (procedure-following).

**Tertiary**:
- pass@k per condition
- Token usage per trial (cost efficiency)
- Response length and structure (did mandate-template subjects comply with template?)

**Observational**:
- Error taxonomy — how does each condition fail? (won't compile vs compiles but fails vs passes most but misses edges)
- Whether template compliance correlates with correctness (mandate-template subjects)

## Confounds to Monitor

1. **Prompt length** — highly-structured is 2-3x longer than baseline. Length alone changes behavior. Report token counts.
2. **Implicit flattery** — full-autonomy says "expert"; others don't. Could affect confidence.
3. **Model sensitivity** — results may not transfer across models. Start with one model, note which.

## Validation Criteria (Ixian)

**H0**: No difference in task completion score between motivation-framed and process-framed system prompts. Observed differences are within LLM stochasticity.

**Method**: Bayesian credible intervals on per-subject score distributions. Compute posterior P(motivation > highly_structured) directly. Use clustered standard errors with probe_id as cluster variable if multiple probes are added later.

**Rollback**: If P(motivation > highly_structured) < 0.70, the hypothesis is not supported at this task/model combination.

## What This Proves (If Confirmed)

If motivations outperform mandates on discriminating tasks, it validates the cix design principle that extensions should explain WHY, not prescribe HOW. This directly informs:

- Skill authoring guidelines (teach frameworks, not steps)
- Agent system prompt design (motivations > process templates)
- The Collaborative Intelligence thesis (human judgment + AI amplification > prescribed workflows)

## Deferred Work

- **SWE-bench tasks** (`astropy-13033`, `astropy-13398`): Parked in `cases/_deferred/`. Need RepoTestSensor (repo checkout, patch application, test execution).
- **Multi-model comparison**: Run same conditions across Sonnet/Haiku/Opus to test model sensitivity.
- **Iteration × framing interaction**: Cross cep-001 (iteration) with cep-002 (framing) — does iteration help more or less under different framings?

## References

- lab-1337 REP-002: `~/Projects/claude-1337/lab-1337/reps/rep-002-mandates-vs-motivations.md`
- lab-1337 findings: `~/Projects/claude-1337/lab-1337/findings/rep-002-interim-findings.md`
- lab-1337 safe-calculator grader: `~/Projects/claude-1337/lab-1337/src/lab/evals/safe_calculator.py`
- cix CLAUDE.md: WHY > HOW principle, design lever hierarchy
- stat-rigor.md: Bayesian methods, CLT rejection for small-N
