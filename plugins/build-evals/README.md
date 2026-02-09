# build-evals

Eval methodology for AI systems. Write evals that measure what matters, not vanity metrics.

## What This Is

A decision framework for evaluating AI agents, skills, MCP servers, prompts, and multi-agent systems. One skill with 14 deep-dive references, a self-evaluation harness with 31 test cases, and human-optimized documentation. Grounded in Anthropic's 2026 agent evaluation guidance and peer-reviewed research (KDD 2025, MCPGauge, SWE-bench).

## When It Activates

- Writing evals for agents, skills, MCP servers, or prompts
- Measuring agent effectiveness or reliability
- Evaluating multi-agent coordination
- Choosing eval frameworks (DeepEval, Braintrust, RAGAS, Promptfoo)
- Designing graders (code-based, model-based, human)
- Handling non-determinism (pass@k, pass^k, iterative metrics)

## What You Get

### Skills

**build-eval** -- Eval methodology covering:
- Three grader types (code, model, human) with selection guidance
- Agent type matching (coding, conversational, research, computer use, multi-agent, pipeline)
- Non-determinism handling (pass@k, pass^k, iterative/Ralph pattern)
- Classification metrics (precision, recall, F1) with confusion matrix
- Framework selection (DeepEval, Braintrust, RAGAS, Promptfoo, Phoenix)
- Domain routing to 14 reference files for on-demand depth
- Cost awareness for model-based grading

### Self-Eval Harness

The plugin evaluates itself using the methodology it teaches:

| Level | What It Tests | Suite | Cases |
|-------|--------------|-------|-------|
| **Activation (F1)** | Does the skill trigger on the right prompts? | `activation-suite.json` | 27 |
| **Methodology (Rubric)** | Does Claude follow eval methodology when activated? | `methodology-rubric.json` | 4 |

```bash
python evals/run_eval.py activation    # Level 1: F1
python evals/run_eval.py methodology   # Level 2: rubric adherence
python evals/run_eval.py all           # Both
python evals/run_eval.py all --dry-run # Mock results (no API calls)
```

## Structure

```
build-evals/
├── skills/
│   └── build-eval/
│       ├── SKILL.md                   # Decision framework (< 260 lines)
│       └── references/                # On-demand depth (14 files)
│           ├── agents.md              # Agent eval patterns + OTel
│           ├── benchmarks.md          # SWE-bench, WebArena, etc.
│           ├── cost.md                # Token tracking + budget
│           ├── datasets.md            # Test case design + labeling
│           ├── frameworks.md          # DeepEval, Braintrust, RAGAS
│           ├── iterative.md           # Ralph pattern, recovery_rate
│           ├── mcp.md                 # MCPGauge + tool call metrics
│           ├── methodology.md         # Design rationale
│           ├── multi-agent.md         # Coordination + pipeline eval
│           ├── observability.md       # OTel spans + Phoenix
│           ├── prompts.md             # LLM-as-judge + rubrics
│           ├── security.md            # Red teaming + attack categories
│           ├── skills.md              # Activation F1 + testing modes
│           └── sources.md             # Citation index
├── evals/                             # Self-evaluation harness
│   ├── README.md                      # Harness documentation
│   ├── activation-suite.json          # 27 labeled test cases
│   ├── methodology-rubric.json        # 6-criterion rubric
│   └── run_eval.py                    # Eval runner (Claude SDK + Anthropic API)
├── docs/
│   ├── explanation/                   # Human-optimized (WHY)
│   │   ├── methodology.md            # Design philosophy
│   │   └── sources.md                # Full citations
│   ├── how-to/                        # Human-optimized (HOW)
│   │   ├── write-agent-evals.md       # End-to-end agent eval
│   │   ├── tune-skill-activation.md   # Precision/recall diagnosis
│   │   ├── set-up-eval-harness.md     # Harness setup + run
│   │   └── design-eval-graders.md     # Grader type selection
│   └── tutorials/                     # Human-optimized (LEARN)
│       ├── first-eval-suite.md        # Build a skill eval from scratch
│       └── evaluating-a-coding-agent.md # Full coding agent eval
└── .claude-plugin/
    └── plugin.json
```

## Key Concepts

**Three grader types:** Code-based (deterministic, preferred), Model-based (LLM rubric, flexible), Human (gold standard, expensive).

**Non-determinism:** LLMs are stochastic. Use pass@k (at least 1 success in k trials) for exploration and pass^k (all k succeed) for production reliability. Run 5+ trials per task.

**Iterative metrics (Ralph pattern):** pass@1 is not the ceiling. Feed failures back. recovery_rate tells you whether to deploy with retry loops or improve prompts.

**Two-sided testing:** Every metric has two failure modes. 100% recall with 50% precision means your eval triggers on everything (useless). Measure both.

**Defense in depth:** No single eval catches everything. Layer: automated evals + production monitoring + A/B testing + transcript review + human studies.

## Philosophy

This plugin teaches eval frameworks, not eval answers. It makes humans better at measuring AI systems rather than prescribing a single measurement approach. Every recommendation is grounded in research and traceable to sources.
