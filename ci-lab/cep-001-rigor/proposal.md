# CEP-001: Does Iteration Improve Code Generation?

**Status**: Draft
**Author**: Yashodeep Vyas
**Created**: 2026-02-14

## Question

Does multiple self-review iterations produce more correct code than single-shot generation?

## Hypothesis

Agents that review and revise their own output (self-review loop) will produce higher correctness scores than single-shot generation, with diminishing returns beyond 3 iterations.

## Background

Self-review is a common pattern in agent frameworks — generate, critique, revise. The assumption is that iteration improves quality. But does it? And if so, how many iterations matter?

Lab-1337 found that **task difficulty dominates prompting strategy** — easy tasks show ceiling effects (all conditions pass), hard tasks show floor effects (all conditions fail). Only "discriminating" tasks (30-70% baseline pass rate) produce signal. This experiment must use discriminating tasks or the iteration count won't matter.

## Design

**Independent variable**: Iteration count (1, 3, 5)

**Subjects** (conditions):
| Subject | Iterations | Review Prompt |
|---------|-----------|---------------|
| `single` | 1 | None — single shot |
| `ralph-3` | 3 | Self-review: edge cases, complexity, correctness |
| `ralph-5` | 5 | Same review prompt, more rounds |

**Sensor**: `function-test` — extracts code, runs against test cases, grades pass/fail per case.

**Trials**: 5 per subject per task (minimum for initial signal; increase to 10+ if noise floor is acceptable).

**Tasks**: Need 2+ discriminating tasks with clear test suites. Current cases from rep-001-rigor:
- `interval-merging` — algorithm problem with edge cases
- `text-justify` — string processing with formatting rules

## Metrics

- **Primary**: Mean score per subject (0.0-1.0 from test pass rate)
- **Secondary**: Per-category pass rates (if tasks have category structure)
- **Tertiary**: Token usage per trial (cost of iteration)
- **Observational**: Did the agent actually revise? (diff between iterations)

## Validation Criteria (Ixian)

**H0**: No difference in score between 1, 3, and 5 iterations. Observed differences are within run-to-run noise.

**Method**: Bayesian credible intervals on per-subject score distributions. Compute posterior P(ralph-3 > single) and P(ralph-5 > ralph-3).

**Noise floor**: Run `single` for 10 trials first. If std dev > 0.25, the task is too noisy. If mean > 0.90 or < 0.10, the task doesn't discriminate.

**Signal threshold**: P(condition_A > condition_B) > 0.80 to claim a difference.

**Diminishing returns**: If P(ralph-5 > ralph-3) < 0.60, iteration has diminishing returns beyond 3.

## Open Questions

1. Does the ix runner support iteration loops yet? The review_prompt config implies the agent gets multiple passes, but this requires the Probe/TrialNode to loop.
2. Should "ralph" subjects use test-feedback (feed failures back) or pure self-review (agent reviews without test results)?
3. Are interval-merging and text-justify discriminating enough? Need baseline measurement.

## References

- lab-1337 iteration strategy: `none`, `self-review`, `test-feedback`
- lab-1337 finding: task difficulty dominates prompting strategy
