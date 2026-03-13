# ci-lab

Experiment workspace for testing claims about collaborative intelligence.

## Purpose

The cix project makes design claims — WHY > HOW, skills add value, complementary beats substitutive. Claims without evidence are opinions. ci-lab turns them into falsifiable experiments.

Each experiment follows the CEP (Collaboration Enhancement Proposal) format: a question, a hypothesis, a design with controlled variables, and phased execution that retires early if there's no signal. CEPs test proposed enhancements — extension and plugin design, agent design, interaction strategy effects, documentation formats, prompt framing.

## Structure

```
ci-lab/
├── cep-001/                # Skills vs Help — does skill-format docs improve agent accuracy?
├── marketplace/            # Earlier exploratory experiments (skill-activation, skill-vs-help)
├── src/ci_lab/             # Shared experiment utilities
└── pyproject.toml          # Workspace member, depends on ix
```

### CEP Format

Each `cep-*/` directory contains:

| File | Purpose |
|------|---------|
| `proposal.md` | Question, hypothesis, design, metrics, phased execution plan |
| `experiment.yaml` | ix experiment config (subjects, sensor, trials) |
| `subjects/` | System prompts — one per experimental condition |
| `tasks/` | Probes with labeled expectations and structured metadata |
| `assets/` | Test fixtures (tools, schemas) |
| `results/` | Run outputs (JSON summaries) |

### Experiments

**CEP-001 — Skills vs Help**: Do tool-description skills add value over `--help` output? Three documentation formats compared (help-only, skill-at-tool, help-plus-agent-skill) using a controlled memex corpus. Status: draft/active, Phase 1 complete.

### Phased Execution

All CEPs use phased execution to avoid wasting API calls:

- **Phase 0** — Calibrate. Establish baselines, retire broken probes, confirm the discrimination zone.
- **Phase 1** — Signal check. Run the comparison. If no signal, report the null finding.
- **Phase 2+** — Earned only. Decompose the active ingredient if Phase 1 shows signal.

A null result is not a failed experiment. It is the experiment doing its job.

## Running Experiments

ci-lab depends on `ix` (workspace member). Experiments run through the ix CLI:

```bash
ix run cep-001 --lab ci-lab --mock    # Dry run, no API calls
ix run cep-001 --lab ci-lab           # Real run
ix results cep-001 --lab ci-lab       # View results
```

## Relationship to ix

ix is the evaluation engine. ci-lab is where experiments live. ix provides the domain types (Probe, Subject, Trial, Reading), sensors (ToolUsageSensor, FunctionTestSensor), and the experiment service. ci-lab provides the questions.
