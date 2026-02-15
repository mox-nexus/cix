# Sources

Research, frameworks, and production evidence behind eval patterns.

---

## Research Synthesis

The evaluation landscape in 2026 has converged on three principles: single metrics mislead (dimensional measurement required), deterministic graders alone miss nuance (layered grading needed), and saturation is the enemy of useful evals (60-80% target range). The sources below provide the evidence base, frameworks, and statistical methods that support these principles.

---

## Primary Guidance

**Anthropic (2026). "Demystifying Evals for AI Agents."**
https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

The canonical guide to agent evaluation. Covers the 7-step eval building process, grader design, task specification, and saturation management.

**Key insights:**
- Prefer code-based graders over model-based when possible
- Start with 20-50 tasks from actual failures
- Target 60-80% pass rates to measure improvement
- "Grade what the agent produced, not the path it took"

**Anthropic (2025). "Building Effective Agents."**
https://www.anthropic.com/engineering/building-effective-agents

Agent design philosophy with measurement guidance.

**Key quote:** "The key to success is measuring performance and iterating."

---

## Behavioral Evaluation

**Anthropic (2025). "Bloom: Automated Behavioral Evaluations."**
https://alignment.anthropic.com/2025/bloom-auto-evals/

Framework for testing alignment properties at scale.

**Targets:** Sycophancy, self-preservation, power-seeking, sabotage, deception.

**Why it matters:** Automated tests catch behavioral issues that functional tests miss.

---

## Research Foundations

**arxiv:2507.21504 — "LLM Agent Evaluation: A Survey and Framework" (KDD 2025)**
https://arxiv.org/abs/2507.21504

Comprehensive survey of agent evaluation approaches.

**Coverage:**
- Task completion metrics
- Multi-agent coordination evaluation
- Long-horizon reasoning assessment
- Human preference alignment

**arxiv:2506.07540 — "MCPGauge: A Framework for Evaluating MCP Servers" (2025)**
https://arxiv.org/abs/2506.07540

Four-dimensional evaluation framework for tool servers:
1. **Proactivity** — Does the server take appropriate initiative?
2. **Compliance** — Does it follow constraints and user intent?
3. **Effectiveness** — Does it actually accomplish the task?
4. **Overhead** — How much coordination cost does it impose?

**Scott Spence (2025). "How to Make Claude Code Skills Activate Reliably"**
https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably

Empirical study with 200+ activation tests.

**Findings:**
- Skill descriptions must be intent-driven, not tool-centric
- Metadata "Use when:" triggers activation
- Forced mode inflates activation scores

---

## Statistical Methods

**Anthropic (2024). "Statistical Approach to Model Evals."**
https://www.anthropic.com/research/statistical-approach-to-model-evals

Methodological rigor for comparing model performance.

**Covers:**
- Paired differences for A/B testing
- Clustering for test set quality
- Sample size requirements
- Confidence intervals

---

## Frameworks

### Evaluation Platforms

**DeepEval**
https://deepeval.com/docs/metrics-task-completion

Python-first evaluation framework.

**Key metrics:**
- `TaskCompletionMetric` — Multi-component task scoring
- `ToolCorrectnessMetric` — Tool call validation
- `GEval` — LLM-as-judge with rubrics

**Braintrust**
https://www.braintrust.dev/

Unified platform for offline evals + production observability.

**Why it matters:** Identical API for Python and TypeScript; bridges dev and production.

**RAGAS**
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/agents/

RAG and agent-specific metrics.

**Key metrics:**
- `ToolCallAccuracy` — Precision of tool selection
- `ToolCallF1` — Balanced tool usage
- Context relevance/precision/recall for RAG

### Observability

**Phoenix (Arize)**
https://docs.arize.com/phoenix

Local-first LLM observability and tracing.

**Why use:** Privacy-preserving, runs locally, integrates with OpenTelemetry.

**Promptfoo**
https://promptfoo.dev/

YAML-based assertions and red teaming.

**Use case:** Quick smoke tests, adversarial evaluation, non-Python workflows.

**Harbor**
https://github.com/ai-anchor/harbor

Containerized agent task execution.

**Use case:** Isolated environments, security boundaries, reproducible builds.

---

## Benchmarks

**SWE-bench Verified**
https://www.swebench.com/

500 verified code agent tasks from real GitHub issues.

**Why "Verified":** Original 2,294 tasks had quality issues. Verified subset is gold standard.

**τ2-Bench**
https://github.com/tau-bench/tau-bench

Multi-turn conversational agent evaluation (retail, airline domains).

**Key insight:** State tracking across turns; turn limits prevent unbounded conversation.

**WebArena**
https://webarena.dev/

812 tasks for web agents. Realistic websites, multi-step flows.

**Evaluation mode:** Screenshot + DOM state inspection.

**OSWorld**
https://os-world.github.io/

Computer use agent benchmark.

**Evaluation mode:** File system state verification.

---

## Observability Standards

**OpenTelemetry GenAI Semantic Conventions**
https://opentelemetry.io/blog/2025/ai-agent-observability/

Standard spans for AI agent instrumentation:
- `agent_run` — Top-level agent execution
- `llm_call` — Model invocation
- `tool_call` — External tool usage
- `skill_check`, `skill_match` — Skill activation

**Claude Agent SDK**
https://code.claude.com/docs/en/monitoring-usage

Native OpenTelemetry support.

**Google Agent Developer Kit (ADK)**
https://google.github.io/adk-docs/observability/cloud-trace/

OTel + Cloud Trace integration.

---

## Security Evaluation

**garak — LLM Vulnerability Scanner**
https://github.com/leondz/garak

Probes for:
- Prompt injection
- Jailbreaking
- Data leakage
- Toxic output

**OWASP LLM Top 10**
https://owasp.org/www-project-top-10-for-large-language-model-applications/

Security risk catalog for LLM applications:
1. Prompt injection
2. Insecure output handling
3. Training data poisoning
4. Model denial of service
5. Supply chain vulnerabilities
6. Sensitive information disclosure
7. Insecure plugin design
8. Excessive agency
9. Overreliance
10. Model theft

---

## Production Case Studies

### Iterative Evaluation (Ralph Pattern)

**Source:** Internal discovery from multi-agent eval work

**Finding:** Agents with mediocre pass@1 often have excellent recovery rates with feedback loops.

**Implication:** Traditional pass@k misses learning capability. Measure iterations_to_pass, recovery_rate, feedback_sensitivity.

### Multi-Agent Coordination

**Framework:** MultiAgentBench (implied from multi-agent.md references)

**Metrics discovered:**
- Handoff success rate
- Communication efficiency
- Role adherence
- Work duplication detection

**Real-world failure:** Agents with 90%+ individual task scores achieving <50% system completion due to coordination failures.

---

## Anti-Pattern Evidence

**Forced Mode Inflation**
**Source:** Scott Spence empirical testing (200+ trials)

**Finding:** Forcing skill activation in tests produces inflated scores. Skills appear reliable under forced activation but fail to trigger naturally.

**Fix:** Test activation in realistic conditions.

**Grader Bias**
**Source:** Anthropic transcript review guidance

**Finding:** 15% of evals had grader bugs discovered through manual transcript review.

**Implication:** Metrics tell you where failures happen. Transcripts tell you why.

---

## Related Frameworks

**LangSmith**
https://smith.langchain.com/

LangChain-integrated evaluation platform.

**Langfuse**
https://langfuse.com/

Self-hosted alternative to LangSmith.

---

## The State of the Field (2026)

**Consensus:**
- Code-based graders preferred over LLM judges (speed, objectivity)
- OpenTelemetry as standard for observability
- Pass@k insufficient for production (need iterative metrics)
- Multi-agent evaluation requires coordination-specific metrics
- Behavioral evals (Bloom) catch issues functional tests miss

**Open Questions:**
- Standardized multi-agent benchmarks (field still fragmenting)
- Long-term skill retention evaluation (most studies are <1 week)
- Transfer learning between eval frameworks

---

## Meta-Sources

**Metric Definitions:**

| Metric | Formula | Source |
|--------|---------|--------|
| F1 | 2×(P×R)/(P+R) | Standard ML literature |
| pass@k | P(≥1 success in k trials) | Chen et al. (Codex paper) |
| pass^k | P(all k succeed) | Extension of pass@k |
| RRF | 1/(rank+k) fusion | Cormack et al. (SIGIR) |

**Effect Size Standards:**

| Statistic | Interpretation | Source |
|-----------|----------------|--------|
| Cohen's d | 0.2 small, 0.5 medium, 0.8 large | Cohen (1988) |
| Correlation (r) | 0.3 moderate, 0.5 strong | Standard psych |
| Beta (β) | Regression coefficient | Standard stats |

---

All links accessed and verified January 2026.
