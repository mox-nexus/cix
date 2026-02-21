# ix

Intelligent Experimentation — evals, benchmarks, and QoS experiments for AI agents.

## Usage

```bash
# List experiments in a lab
ix experiment list --lab ci-lab

# Run an experiment (mock mode, no API calls)
ix run skill-activation --lab ci-lab --mock --seed 42

# Show experiment details
ix experiment show skill-activation --lab ci-lab

# View past results
ix results skill-activation --lab ci-lab
```

## What ix Does

ix runs **experiments** against AI systems. You write cases, ix runs them multiple times, and gives you F1, precision, recall.

Each experiment runs multiple **trials** per case — AI behavior is stochastic, so you need the distribution, not a single result. Majority vote per case, F1 across all cases.

## Quick Example

```
$ ix run skill-activation --lab ci-lab --mock --seed 42
Running skill-activation in lab ci-lab (28 cases, 5 trials, mock)
  must-001: OK (score=100%)
  must-002: OK (score=80%)
  ...

────────────── Results ──────────────
  Precision    100.0%
  Recall        93.3%
  F1            96.6%

Status: EXCELLENT
```

## Documentation

| Document | Description |
|----------|-------------|
| [Running Experiments](docs/how-to/running-experiments.md) | Create a lab, write cases, run, interpret results |
| [What is ix?](docs/explanation/what-is-ix.md) | The problem, what ix does, what it's not |
| [Domain Models](docs/reference/domain-models.md) | All types: Subject, Interaction, Reading, EvalCase, ... |
| [Experiment Format](docs/reference/experiment-format.md) | YAML config, markdown cases, results format |
