# Understanding the LLM Evaluation Landscape (February 2026)

> **For**: Someone who knows Python, has built Claude Code extensions, but hasn't built evals before
> **Why**: To understand the full landscape before building ix (an experimentation platform)
> **How**: Start with examples, build to concepts, explain WHY things matter

---

## What This Document Is

This is a teaching document, not a summary. It explains the evaluation landscape as of February 2026 from first principles, with examples and reasoning at every step. By the end, you'll understand:

1. What evaluation actually means in the LLM world (it's more complex than you think)
2. What tools exist, what they're good at, and what critical gaps remain
3. What statistical methods matter and why (this is where most frameworks fail)
4. What Anthropic specifically recommends (they're the most relevant voice for evaluating Claude Code extensions)
5. Where ix fits and what problems it uniquely solves

All claims are sourced. Traceability is critical.

> **Source reports** (detailed research backing this synthesis):
> - `scratch/llm-eval-framework-landscape-2026-02-09.md` — 14 frameworks analyzed
> - `scratch/agent-eval-harness-landscape-2026-02-09.md` — Agent-specific tooling
> - `scratch/research-qos-experimentation-landscape-2026-02-09.md` — Statistical rigor and experimentation platforms
> - `scratch/anthropic-eval-research-sweep-2026-02-09.md` — 40+ Anthropic sources
> - `scratch/research-synthesis-ix-landscape-2026-02-09.md` — Unified synthesis

---

## Part 1: What Is Evaluation, Really?

### The Simple Case (That Doesn't Exist)

Imagine you're testing a function that adds two numbers:

```python
def add(a, b):
    return a + b

assert add(2, 3) == 5  # Pass or fail. Done.
```

This is testing, not evaluation. The correct answer is unambiguous, deterministic, and instant to verify.

**LLM evaluation is never this simple.** Here's why.

### The Reality: Non-Determinism, Judgment, and Cost

When you ask Claude to write code, fix a bug, or answer a question, three problems emerge:

**Problem 1: Non-Determinism**
Run the same prompt twice, get different outputs. Even with `temperature=0`, outputs vary. How do you measure quality when the answer changes?

**Problem 2: Judgment Over Correctness**
There's often no single "correct" answer. A bug fix might work but be inelegant. A summary might be accurate but miss the key point. Who decides what's "good"?

**Problem 3: Cost-Quality Tradeoffs**
An agent might get the right answer after 500 API calls costing $12. Another gets 90% accuracy in 3 calls costing $0.02. Which is better? It depends on your use case.

**This is why evaluation is hard.** You're not checking correctness — you're measuring quality, consistency, and cost across distributions of outcomes.

---

## Part 2: The Four Dimensions Every Framework Must Handle

### Dimension 1: State — Does Anything Persist Between Steps?

Consider evaluating a multi-step debugging agent:

1. Agent reads error message
2. Agent searches codebase for the bug
3. Agent proposes a fix
4. Agent runs tests
5. Agent iterates if tests fail

At step 3, the agent needs to remember what it found at step 2. That's **shared state**.

**Most frameworks treat each test as independent.** They can't check "does skill B interfere with skill A?" because they have no way to track whether adding B changed A's internal state.

**Only Inspect AI has a true state mechanism** (the `store`, a Pydantic model passed through the solver chain). Every other framework reviewed treats samples as independent.

**Why this matters for ix**: ix needs to measure skill coexistence ("adding skill B breaks skill A") and context degradation ("agent performance drops after 50 tool calls"). Both require tracking state across a session.

**Source**: LLM Framework Landscape report, "State Model" comparison matrix

---

### Dimension 2: Execution — How Are Tests Run?

You have 1,000 test cases. Do you run them:
- One at a time (slow, but simple)
- All at once (fast, but overwhelms API rate limits)
- In batches of 20 (balanced, but requires orchestration)

And within a single test case with multiple graders, do you:
- Run graders sequentially (A, then B, then C)
- Run graders in parallel (A, B, C at the same time)
- Run graders as a dependency graph (B depends on A's output, C depends on both)

**Example**: You're evaluating a RAG system. You need to:
1. Check retrieval quality (did it fetch relevant documents?)
2. Check answer accuracy (is the generated answer correct?)
3. Compute a composite F1 score from #1 and #2

If graders run sequentially, this takes 3 LLM calls. If they run as a DAG, graders 1 and 2 can run in parallel, then grader 3 computes F1 from their results. That's 2 LLM calls instead of 3.

**Most frameworks run sequentially.** DeepEval has a "DAG metric" (internal to a single metric), but no framework supports DAG orchestration across multiple metrics.

**Why this matters for ix**: ix's probe-sensor-grader-scorer pipeline is inherently a DAG. Probes generate stimuli, sensors observe responses, graders score observations, scorers aggregate across trials. These should compose as a dependency graph, not a linear chain.

**Source**: LLM Framework Landscape report, "Execution Model" comparison matrix

---

### Dimension 3: Stochastic Handling — What Do You Do About Randomness?

Run the same prompt 10 times. You get 7 correct answers and 3 wrong ones. What's your score?

**Naive answer**: 70% accuracy.

**Better question**: What's your confidence interval? If you ran 10 more trials, would you get 60%? 80%? You need error bars.

**Even better question**: Does "one success out of 10 trials" matter, or do you need consistent success? These are different metrics:

- **pass@k**: Probability of at least one success in k trials. Use for code generation tools (one working solution is enough).
- **pass^k**: Probability that all k trials succeed. Use for customer-facing agents (consistency matters).

**Example**: An agent succeeds 75% of the time.
- pass@3 = "at least one success in 3 tries" = 1 - (0.25)^3 = **98.4%**
- pass^3 = "all 3 tries succeed" = (0.75)^3 = **42.2%**

Same agent, wildly different performance depending on your metric.

**Only two frameworks handle stochasticity properly:**
1. **Inspect AI**: `epochs` parameter runs multiple trials per task, `reducers` aggregate scores, bootstrap computes standard errors
2. **LM Harness**: `bootstrap_iters` for confidence intervals

**Every other framework** says "run it again and compare manually."

**Why this matters for ix**: Without proper stochastic handling, you can't tell if a 3-point score improvement is signal or noise. Anthropic's research shows infrastructure configuration alone shifts scores by 6 percentage points — larger than most "improvements" you'll measure.

**Source**:
- [Anthropic "Infrastructure Noise"](https://www.anthropic.com/engineering/infrastructure-noise) — 6pp shifts from config alone
- [Anthropic "Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — pass@k vs pass^k

---

### Dimension 4: Grading — Who Decides What's Good?

You have an agent that summarized a document. Is the summary good? Three approaches:

**Code-based grading** (deterministic):
- Exact match: `output == expected_output`
- ROUGE score: Overlap between output and reference
- JSON validity: `json.loads(output)` succeeds

**Pros**: Fast, cheap, objective, reproducible
**Cons**: Brittle to valid variations, lacks nuance

**Model-based grading** (LLM-as-judge):
- Give Claude a rubric: "Rate this summary 1-5 on accuracy, clarity, conciseness"
- Claude grades the output
- You get scores with reasoning

**Pros**: Flexible, scalable, captures nuance
**Cons**: Non-deterministic, more expensive, requires calibration

**Human grading**:
- Expert reads output, assigns score
- Gold standard quality

**Pros**: Most accurate
**Cons**: Expensive ($50-200/hour), slow, doesn't scale

**Anthropic's hierarchy** (use the highest tier feasible):
1. Code-based (if deterministic correctness exists)
2. LLM-based (for nuance and subjective quality)
3. Human (for calibration and spot-checks only)

**Critical insight from Anthropic**: "Grade what the agent produced, not the path it took." Don't check for specific tool call sequences — agents find valid approaches designers didn't anticipate.

**Example**: You're evaluating a bug-fixing agent. Don't check "did it call `git blame`, then `grep`, then `edit`?" Instead check "did it fix the bug?" The agent might use `rg` instead of `grep`, or skip `git blame` entirely. That's fine.

**Source**:
- [Anthropic "Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — grader types table
- [Anthropic "Create Strong Empirical Tests"](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) — grading hierarchy

---

## Part 3: The Statistical Problem Everyone Ignores

### Why Your 5-Point Improvement Might Be Noise

You run a measurement. Your agent scores 73%. You make a change. It scores 78%. Success?

**Maybe. Maybe not.**

Here's what you need to know:

**1. You Measured a Sample, Not the Universe**

Your 1,000-question suite is a sample from an infinite universe of possible questions. The 73% you measured is an estimate of the true mean. How good is that estimate?

Enter the **Standard Error of the Mean (SEM)**:

```
SEM = standard_deviation / sqrt(n)
```

For 1,000 questions with std=0.45, SEM = 0.45 / sqrt(1000) = **0.014** (1.4 percentage points).

Your **95% confidence interval** is:

```
73% +/- 1.96 x 1.4% = 73% +/- 2.7% = [70.3%, 75.7%]
```

After your change, you scored 78%. That's outside the confidence interval. **Probably real.**

But if you scored 75%? That's [72.3%, 77.7%], which overlaps with the original interval. **Might be noise.**

**2. Your Questions Might Be Correlated**

Imagine you're measuring reading comprehension. You have 10 questions about one passage. A model that misunderstands the passage gets all 10 wrong. These questions are **not independent**.

Standard error assumes independence. If questions cluster (reading comp, SQL injection, etc.), naive SEM **underestimates uncertainty by up to 3x**.

You need **clustered standard errors**:

```python
# Naive SEM (wrong if clustered)
sem_naive = np.std(scores) / np.sqrt(len(scores))

# Clustered SEM (correct)
cluster_means = df.groupby('cluster_id')['score'].mean()
sem_clustered = np.std(cluster_means) / np.sqrt(len(cluster_means))
```

**Evan Miller's research** (Anthropic) found clustered SEs **3x larger** than naive calculations on benchmarks like DROP and SQuAD.

**3. Infrastructure Noise Is Real**

From Anthropic's infrastructure noise research (Feb 2026):

- Changing from 1x to 3x resource headroom shifts scores by **3.7 percentage points** (p &lt; 0.001)
- Changing Docker config shifts scores by **6 percentage points** (p &lt; 0.01)

**Recommendation**: "Leaderboard differences below 3 percentage points deserve skepticism without documented matching configurations."

**Your 5-point improvement might actually be 2 points of signal + 3 points of infrastructure noise.**

**4. Paired Comparisons Are More Powerful**

When comparing two models/agents on the same questions, don't just compare their means. Use **paired differences**:

```python
differences = scores_after - scores_before
mean_diff = np.mean(differences)
se_diff = np.std(differences) / np.sqrt(len(differences))
ci_diff = mean_diff +/- 1.96 * se_diff
```

Why? Models correlate on questions (r=0.3-0.7 on frontier measurements). Paired tests exploit that correlation for **free variance reduction**.

**Source**:
- [Anthropic "Adding Error Bars"](https://arxiv.org/abs/2411.00640) — clustered SEs, paired differences, power analysis
- [Anthropic "Infrastructure Noise"](https://www.anthropic.com/engineering/infrastructure-noise) — 6pp config shifts, 3pp skepticism threshold

---

### The CLT Is Dead for Small-N Measurements

The **Central Limit Theorem** says sample means are normally distributed for large N. Most statistics textbooks teach this.

For LLM measurements with N &lt; 100, **the CLT underestimates uncertainty**. A 2025 ICML Spotlight paper ("Don't Use the CLT") proves this empirically across 12 benchmarks.

**The fix**: Use Bayesian methods. The `bayes_evals` library provides drop-in replacements for CLT-based confidence intervals.

```python
# Wrong (CLT, underestimates uncertainty)
from scipy import stats
ci = stats.norm.interval(0.95, loc=mean, scale=sem)

# Right (Bayesian, correct uncertainty)
from bayes_evals import bayesian_ci
ci = bayesian_ci(scores, confidence=0.95)
```

**Why this matters**: ix will run measurements with 20-50 tasks (Anthropic's recommended starting point). The CLT breaks down completely at that scale. Bayesian methods are essential.

**Source**:
- ["Don't Use the CLT"](https://arxiv.org/abs/2503.01747) — ICML 2025 Spotlight
- ["Efficient Measurement with Statistical Guarantees"](https://arxiv.org/abs/2601.20251) — 5x sample efficiency via Bayesian factor models

---

## Part 4: What Frameworks Actually Exist

Now that you understand the hard parts, let's survey the landscape. I'll focus on what each framework is **actually good at**, not marketing claims.

### Category 1: Frameworks That Drive Tests (Build Your Own)

These are libraries/CLIs for defining and running evaluations.

#### Inspect AI (UK AI Safety Institute)

**What it's best at**: Agent measurement with sandboxing and reproducibility

**Architecture**:
- **Dataset**: Test cases
- **Solver**: Chain of operations (simple LLM call to complex agent)
- **Scorer**: Grading logic
- **TaskState + store**: Shared state across solver chain (unique among frameworks)

**Key capabilities**:
- **Agent Bridge**: Drives external agents (Claude Code, LangChain, etc.) in Docker/K8s sandboxes
- **Epochs**: First-class multi-trial support with reducers and bootstrap stderr
- **SWE-bench integration**: Run Claude Code on SWE-bench in containers

**Stochastic handling**: Best-in-class (epochs + reducers + bootstrap)

**Why it's relevant to ix**: Inspect is the strongest existing foundation for agent measurement. Its TaskState + store is the only shared state mechanism. Its Agent Bridge shows how to drive Claude Code programmatically in isolated environments.

**Source**:
- [Inspect AI docs](https://inspect.aisi.org.uk/)
- Agent Harness Landscape report, "Inspect AI" section

---

#### Promptfoo

**What it's best at**: Declarative YAML test definitions, red-teaming, CI/CD integration

**Architecture**:
- YAML config defines providers, prompts, test cases, assertions
- CLI runs matrix measurement (every prompt x every provider x every test)
- Built-in red-teaming (OWASP, NIST, MITRE ATLAS)

**Key capabilities**:
- **Claude Agent SDK provider**: Dedicated integration for driving Claude Code sessions
- **Assertions**: string match, regex, LLM-as-judge, cost, latency, ROUGE, BLEU, custom Python/JS
- **Side-effect management**: Serial execution, hooks for env reset between trials

**Stochastic handling**: Basic (`--repeat N`, but no CIs)

**Why it's relevant to ix**: Anthropic uses Promptfoo internally for product measurements. Its YAML format could serve as a user-facing test definition layer for ix.

**Source**:
- [Promptfoo docs](https://www.promptfoo.dev/)
- [Anthropic "Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — "Anthropic uses a version for product evals"

---

#### DeepEval

**What it's best at**: pytest-style testing with 50+ built-in metrics

**Architecture**:
- Test cases as Python code (`@pytest.mark.deepeval`)
- 50+ metrics (RAG, safety, conversational, agent)
- Optional cloud platform (Confident AI) for dataset management

**Key capabilities**:
- **DAG metric**: Deterministic LLM-powered decision trees (most powerful metric in the ecosystem)
- **pytest integration**: Familiar to Python developers
- **Concurrent execution**: `max_concurrent=20` by default

**Stochastic handling**: None (but DAG metrics are deterministic by design)

**Why it's relevant to ix**: The DAG metric concept (composing LLM calls as a decision tree) is architecturally significant. It shows how to make LLM-based grading deterministic.

**Source**:
- [DeepEval docs](https://deepeval.com/)
- LLM Framework Landscape report, "DeepEval" section

---

#### LM Harness (EleutherAI)

**What it's best at**: Academic benchmarks (MMLU, HellaSwag, etc.)

**Architecture**:
- 60+ benchmarks, hundreds of subtasks
- Unified interface across HuggingFace, vLLM, APIs
- Backend for HuggingFace Open LLM Leaderboard

**Key capabilities**:
- **Bootstrap stderr**: Mature statistical handling
- **Task versioning**: Reproducibility of previously reported scores
- **Multi-backend**: HuggingFace, vLLM, SGLang, OpenAI, Anthropic

**Stochastic handling**: Excellent (bootstrap_iters for CIs)

**Why it's relevant to ix**: Gold standard for model-level benchmarking. If ix ever needs to compare base model capabilities, LM Harness is the reference.

**Source**:
- [LM Harness docs](https://www.eleuther.ai/artifacts/lm-evaluation-harness)
- LLM Framework Landscape report, "LM Harness" section

---

### Category 2: Platforms That Observe + Measure (SaaS or Self-Hosted)

These combine tracing/observability with measurement. You instrument your code, they collect traces, you run tests against datasets.

#### Langfuse (Open Source)

**What it's best at**: Self-hosted observability + measurement

**Architecture**:
- Trace-based (traces, generations, spans, events)
- PostgreSQL backend (self-hostable Docker/K8s)
- Scores attach to traces

**Key capabilities**:
- **Most-starred** in category (21.7k GitHub stars)
- **Open-source** with full data ownership
- **50+ integrations** (LangChain, LlamaIndex, OpenAI, Anthropic)

**Stochastic handling**: Via experiment comparison (manual)

**Why it's relevant to ix**: If ix needs observability, Langfuse is the best self-hosted option. But ix is an experimentation platform, not an observability tool.

**Source**:
- [Langfuse docs](https://langfuse.com/)
- LLM Framework Landscape report, "Langfuse" section

---

#### Arize Phoenix

**What it's best at**: OpenTelemetry-based observability

**Architecture**:
- OTEL traces/spans with auto-instrumentation
- SQLite (dev) or PostgreSQL (prod)
- Runs anywhere (local, Docker, K8s, cloud)

**Key capabilities**:
- **Open-source** (Elastic License 2.0, no feature gates)
- **20x speedup** with built-in concurrency
- **Pre-built scorers**: hallucination, toxicity, relevance

**Stochastic handling**: Via experiment comparison (manual)

**Why it's relevant to ix**: Phoenix shows how to integrate measurement with OTEL tracing. If ix produces traces, Phoenix could ingest them.

**Source**:
- [Arize Phoenix docs](https://phoenix.arize.com/)
- LLM Framework Landscape report, "Arize Phoenix" section

---

#### Braintrust (Proprietary SaaS)

**What it's best at**: CI/CD integration with GitHub Actions

**Architecture**:
- Experiments are the core organizational unit
- Git-like diffing for experiment comparison
- AutoScorers library (open-source scoring)

**Key capabilities**:
- **GitHub Actions**: Block PRs if metrics regress
- **Loop AI**: Generates custom scorers from natural language
- **AutoScorers**: Levenshtein, BLEU, LLM-as-judge, pairwise

**Stochastic handling**: Via experiment comparison (manual)

**Why it's relevant to ix**: Braintrust shows the CI/CD pattern (quality gates, PR blocking). ix should support this.

**Source**:
- [Braintrust docs](https://www.braintrust.dev/)
- LLM Framework Landscape report, "Braintrust" section

---

### Category 3: Benchmarks (Measure Specific Capabilities)

These aren't frameworks — they're datasets with harnesses.

#### SWE-bench (Princeton)

**What it measures**: Real-world GitHub bug fixes

**Architecture**:
- 2,294 tasks from 12 Python repos (original)
- 500 human-verified subset (Verified)
- Dockerized harness: apply patch, run FAIL_TO_PASS + PASS_TO_PASS tests

**Current performance**: ~75% on Verified (Jan 2026)

**Why it's relevant to ix**: SWE-bench is the de facto standard for coding agent measurement. Inspect AI has SWE-bench integration. ix should too.

**Source**:
- [SWE-bench paper](https://arxiv.org/abs/2310.06770)
- Agent Harness Landscape report, "SWE-bench Family" section

---

#### WebArena / AgentBench / GAIA

**What they measure**:
- **WebArena**: Web agent tasks (e-commerce, forums, code)
- **AgentBench**: 8 environments (OS, database, gaming, embodied AI)
- **GAIA**: 466 human-curated multi-step reasoning tasks

**Current performance**:
- WebArena: 14% -> 60% (2023-2025)
- GAIA: 77% human-AI performance gap

**Why they're relevant to ix**: These show task complexity that exceeds current capabilities. If ix measures agents, these benchmarks are the ceiling.

**Source**:
- Agent Harness Landscape report, "Academic Agent Benchmarks" section

---

## Part 5: What Anthropic Specifically Recommends

Anthropic is the most relevant voice for ix (measuring Claude Code extensions). Here's their unified guidance extracted from 40+ sources.

### Core Terminology (Anthropic's Framework)

From ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

- **Task**: Single test with inputs + success criteria
- **Trial**: One attempt at a task (multiple trials handle stochasticity)
- **Grader**: Logic scoring agent performance
- **Transcript/Trace**: Complete record (outputs, tool calls, reasoning)
- **Outcome**: Final environment state (not agent's claim)
- **Harness**: Infrastructure running measurements end-to-end

This is the standard terminology. Use it.

---

### The Zero-to-One Roadmap (8 Steps)

Anthropic's practical guide from ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

**0. Start early**: 20-50 simple tasks from real failures = excellent starting point

**1. Convert manual tests first**: You already have manual checks. Automate them.

**2. Write unambiguous tasks**: Two domain experts should independently reach same pass/fail. If 0% pass@100, the task is broken (not the agent).

**3. Build balanced problem sets**: Test positive and negative cases. Avoid class imbalance.

**4. Build robust harness**: Each trial from clean environment. Prevent shared state, correlated failures.

**5. Design graders thoughtfully**:
- Grade outcome, not path
- Support partial credit
- Calibrate LLM graders with humans
- Grade each dimension separately

**6. Check the transcripts**: Scores without transcript analysis are unreliable

**7. Monitor saturation**: SWE-bench went 30% -> 80% in one year. Saturated benchmarks provide no improvement signal.

**8. Keep suites healthy**: Treat like unit tests. Dedicated teams own infrastructure.

---

### Statistical Methods (From Evan Miller's Research)

From ["Adding Error Bars"](https://arxiv.org/abs/2411.00640):

**Always report**:
- Mean score
- Standard error (SEM)
- 95% confidence interval: `mean +/- 1.96 x SEM`

**Use clustered SEs** when questions are non-independent (can be 3x larger than naive):

```python
# Group by cluster (e.g., passage_id for reading comp)
cluster_means = df.groupby('cluster_id')['score'].mean()
sem_clustered = cluster_means.std() / np.sqrt(len(cluster_means))
```

**Use power analysis** to determine sample sizes:
- Small effects require large N
- Frontier model differences are often 2-5 percentage points
- Need 500+ samples to detect 3pp difference with 80% power

**Use paired differences** when comparing models:

```python
differences = scores_model_b - scores_model_a
mean_diff = differences.mean()
se_diff = differences.std() / np.sqrt(len(differences))
```

---

### Infrastructure Configuration Matters

From ["Infrastructure Noise"](https://www.anthropic.com/engineering/infrastructure-noise):

**Key findings**:
- Resource allocation shifts scores by **6 percentage points**
- Differences below **3pp** deserve skepticism without documented configs
- Use dual parameters: guaranteed allocation floor + hard kill threshold

**Recommendations**:
- Specify floor and ceiling, not single pinned value
- Run measurements at multiple times across multiple days
- Treat resource config as first-class experimental variable

---

### Grader Design Principles

From ["Create Strong Empirical Tests"](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests):

**Hierarchy** (use highest tier feasible):
1. **Code-based**: Exact match, string match, regex. Fastest, most reliable.
2. **LLM-based**: Rubric scoring, binary classification. Fast, flexible, scalable.
3. **Human**: Expert review. Most accurate but expensive — use for calibration only.

**LLM grader best practices**:
- Use different model to grade than model that generated output
- Encourage reasoning: "Think first, then decide. Discard reasoning."
- Provide "way out": Return "Unknown" when lacking information
- Grade each dimension separately (not monolithic)
- Create clear rubrics with specific criteria
- Calibrate with human experts regularly

---

### Metrics Selection

From ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

| Situation | Metric | Formula | Why |
|-----------|--------|---------|-----|
| One success matters (coding) | **pass@k** | 1 - (1-p)^k | Probability of at least one success |
| Consistency matters (customer-facing) | **pass^k** | p^k | Probability all trials succeed |
| Semantic similarity | **Cosine similarity** | SBERT embeddings | Captures meaning, not surface form |
| Summarization | **ROUGE-L** | LCS F1 | Longest common subsequence |
| Subjective quality | **LLM-based Likert** | 1-5 scale | Captures nuance |
| Binary classification | **LLM-based binary** | Yes/no | Context-aware |

**Critical**: (0.75)^3 = 42% (pass^3) vs 1 - (0.25)^3 = 98% (pass@3). Same agent, wildly different numbers.

---

### Types: Capability vs Regression

From ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

**Capability tests**: "What can this do?"
- Start at low pass rate
- Hills to climb
- Measure progress

**Regression tests**: "Does it still work?"
- Must maintain ~100% pass rate
- Protect against backsliding
- Catch breaking changes

**Graduation**: High-pass capability tests graduate to regression suites.

---

### Behavioral Measurement (Bloom Architecture)

From [Bloom research](https://alignment.anthropic.com/2025/bloom-auto-evals/):

**Four-stage pipeline**:

1. **Understanding**: Agent reads behavior description, generates understanding of what to measure
2. **Ideation**: Generates scenarios designed to elicit target behavior
3. **Rollout**: Executes scenarios in parallel with simulated users and tools
4. **Judgment**: Judge model scores transcripts; meta-judge produces suite report

**Why it's relevant to ix**: Bloom's pipeline (Understand -> Ideate -> Rollout -> Judge) maps to ix's probe-sensor-grader-scorer ontology. Scenario generation is powerful.

**Source**: [Bloom GitHub](https://github.com/safety-research/bloom)

---

### The Swiss Cheese Model

From ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

**No single method catches everything.** Combine:

- Automated tests (scale)
- Production monitoring (real user patterns)
- A/B testing (causal impact)
- User feedback (qualitative)
- Manual transcript review (deep understanding)
- Systematic human studies (gold standard)

Each layer has holes. Layering catches more.

---

### Frameworks Anthropic Uses Internally

From ["Demystifying Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

**Primary**:
- **Promptfoo**: "Anthropic uses a version for product evals"
- **Harbor**: Containerized agent environments (internal tool)

**Recommended**:
- Braintrust (offline + production, CI/CD)
- LangSmith (tracing, datasets, LangChain)
- Langfuse (self-hosted alternative)

---

## Part 6: The Critical Gaps ix Must Fill

Now that you understand the landscape, here's what **doesn't exist**.

### Gap 1: Skill Activation Measurement

**Question**: "Given this context, does the agent activate the right skill/plugin?"

**What exists**: OpenAI's blog post ["Testing Agent Skills Systematically"](https://developers.openai.com/blog/eval-skills/) describes the pattern (use structured JSON output to verify skill invocation). But there's no tooling.

**Why it matters**: You're building a Claude Code skill marketplace. Users need to know "does the security review skill actually trigger when I paste vulnerable code?"

**What ix provides**:
- **PromptProbe**: Generates test inputs designed to trigger specific skills
- **ActivationSensor**: Observes which skills activated
- **MatcherSensor** (puma): Matches actual vs expected activations
- **ClassificationScorer**: F1 score across activation cases

**Example**:

```python
# Test case: Should this trigger the security-review skill?
test_case = {
    "input": "Review this code: cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
    "expected_skills": ["security-review"],
    "expected_findings": ["SQL injection vulnerability"]
}

# Probe generates input, sensor observes, scorer computes F1
result = ix.run_activation_test(test_cases=[test_case])
# Result: precision=0.92, recall=0.88, F1=0.90
```

**Source**: Research Synthesis report, "Five Confirmed Gaps" section

---

### Gap 2: Coexistence / Interference Measurement

**Question**: "Does adding skill B change skill A's behavior?"

**What exists**:
- **CooperBench** (Jan 2026): Multi-agent cooperation benchmark. Found frontier models achieve only 25% success when two agents collaborate — half the single-agent rate.
- **SWE-EVO**: Measures plasticity (learning new tasks) and stability (retaining old tasks) with CL-F1 score.

But these measure task-level degradation, not skill-level interference within a single agent.

**Why it matters**: You add a "explain-code" skill to an agent that already has "write-tests". Does the agent now over-explain instead of writing tests? This is invisible to single-skill tests.

**What ix provides**:
- **Comparative experiment**: Control (skill A alone) vs variant (skills A+B together)
- **ActivationSensor**: Measures whether A's activation changes when B is present
- **DeltaScorer**: Computes delta F1, delta accuracy between control and variant

**Example**:

```python
# Control: security-review skill alone
control = ix.Experiment(skills=["security-review"])

# Variant: security-review + code-optimization
variant = ix.Experiment(skills=["security-review", "code-optimization"])

# Run same test cases through both
result = ix.run_coexistence_test(control, variant, test_cases)

# Result: security-review F1 dropped from 0.90 to 0.78 when code-optimization added
# Interference detected: code-optimization generates explanations that suppress security warnings
```

**Source**:
- [CooperBench paper](https://arxiv.org/abs/2601.13295) — 75% cooperation failure rate
- Research Synthesis report, "Five Confirmed Gaps" section

---

### Gap 3: Context Degradation Measurement

**Question**: "How does agent behavior degrade after N tool calls / crowded context?"

**What exists**: Nothing. Phil Schmid's January 2026 thesis identified this as the critical gap for 2026:

> "Task durability — how well a model follows instructions after its 50th or 100th tool call — is what matters but isn't measured. A 1% leaderboard difference can't detect reliability drift."

Anthropic's ["Effective Harnesses for Long-Running Agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) describes the problem (longer context often makes things worse) but doesn't provide tooling.

**Why it matters**: Your agent works great for the first 10 interactions. After 50 tool calls, it starts hallucinating. Standard benchmarks run 1-5 tool calls and declare victory.

**What ix provides**:
- **PromptProbe with escalating context load**: Systematically increases tool calls, context size
- **TimingSensor**: Tracks latency as context grows
- **ActivationSensor**: Measures whether correct skills still trigger at step 50
- **DegradationScorer**: Plots accuracy, latency, activation F1 vs context size

**Example**:

```python
# Test case: Does the agent maintain accuracy after 100 tool calls?
degradation_test = ix.ContextDegradationTest(
    skill="code-review",
    max_tool_calls=100,
    checkpoints=[10, 25, 50, 75, 100]
)

result = ix.run_degradation_test(degradation_test)

# Result: Accuracy at step 10: 92%, step 50: 78%, step 100: 61%
# Context degradation detected: Agent loses focus after 50 calls
```

**Source**:
- [Phil Schmid "Agent Harness 2026"](https://www.philschmid.de/agent-harness-2026)
- Research Synthesis report, "Five Confirmed Gaps" section

---

### Gap 4: DAG-Based Experiment Orchestration

**Question**: "Can probes, sensors, scorers, reporters compose as a dependency graph?"

**What exists**:
- **DeepEval** has DAG metrics (scoring logic as a decision tree within a single metric)
- **Dagster** has DAG orchestration (workflow management for data pipelines)
- **Nobody combines them** for experimentation

**Why it matters**: Your experiment has:
1. Retrieval sensor (measures doc retrieval quality)
2. Generation sensor (measures answer quality)
3. F1 scorer (computes F1 from retrieval precision + recall)
4. Cost sensor (tracks API spend)
5. Composite scorer (aggregates quality + cost as Pareto curve)

This is a dependency graph: Scorers 3 and 5 depend on sensors 1, 2, 4. Running them sequentially wastes time. Running them as a DAG is parallel where possible.

**What ix provides**:
- **Matrix engine**: Kind-agnostic DAG with parallel dispatch via Python's `graphlib`
- **Typed components**: Probes, Sensors, Graders, Scorers, Reporters compose as nodes
- **Automatic parallelization**: Independent branches execute concurrently

**Example**:

```python
# Define DAG
dag = ix.ExperimentDAG()
dag.add_probe("prompt_probe")
dag.add_sensor("retrieval_sensor", depends_on=["prompt_probe"])
dag.add_sensor("generation_sensor", depends_on=["prompt_probe"])
dag.add_scorer("f1_scorer", depends_on=["retrieval_sensor", "generation_sensor"])
dag.add_reporter("console_reporter", depends_on=["f1_scorer"])

# Execute (automatic parallelization)
result = ix.run(dag)

# retrieval_sensor and generation_sensor run in parallel
# f1_scorer waits for both, then runs
# console_reporter waits for f1_scorer, then prints
```

**Source**: Research Synthesis report, "Five Confirmed Gaps" section

---

### Gap 5: Collaborative Intelligence Measurement

**Question**: "Does the extension make the human more capable, not dependent?"

**What exists**: Nothing. This requires longitudinal, human-in-the-loop measurement — a fundamentally different paradigm.

**Why it matters**: From the [evidence base](the-evidence.md):

> "AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable long-term human capability."
>
> - 26% more tasks completed with AI (productivity gains are real)
> - 17% worse exam performance without AI (learning harm is real)
> - 20% skill reduction after 3 months (deskilling is measurable)

Standard tests measure "does the AI produce good output?" Collaborative intelligence measurement asks "does the human get better over time?"

**What ix provides**: Not yet. This is M3+ territory. But ix's architecture enables it:

- **Longitudinal trials**: Track human performance with and without agent over weeks
- **Transfer tests**: After using agent for N tasks, measure human capability alone
- **Learning curves**: Plot human skill acquisition vs agent usage intensity

**The hardest gap.**

**Source**:
- [The Evidence](the-evidence.md) — CI research evidence base
- Research Synthesis report, "Five Confirmed Gaps" section

---

## Part 7: Where ix Fits in the Landscape

### The Differentiation Map

```
                    Statistical Rigor
                         |
          Statsig *      |      * ix (target)
                         |     /
                         |    /
          Braintrust *   |   /
                         |  /
     --------------------+---------------------- Agent Testing
                         | /
          Promptfoo *    |/
                         |
          DeepEval *     |     * Inspect AI
                         |
                         |
                    Simple Testing
```

**ix lives in the upper-right quadrant**: agent testing + statistical rigor + DAG orchestration.

Nobody else is there.

**Source**: Research Synthesis report, "The ix Differentiation Map"

---

### What ix Should Borrow

From the research synthesis:

| From | Take | Why |
|------|------|-----|
| **Inspect AI** | TaskState + store, epochs/reducers, async execution | Only framework with shared state and first-class stochastic handling |
| **LM Harness** | Bootstrap stderr, metric aggregation | Mature statistical infrastructure |
| **Promptfoo** | YAML test definitions, Claude Agent SDK provider | Best declarative DX, Anthropic uses it |
| **DeepEval** | DAG metric concept | Shows how to compose LLM calls as decision trees |
| **Anthropic** | Task/trial/transcript/outcome framework, pass@k | Canonical terminology and methodology |
| **Statsig** | CUPED variance reduction, sequential testing | Reduces sample size requirements 2-5x |
| **Bloom** | Understand -> Ideate -> Rollout -> Judge pipeline | Architecture for behavioral measurement generation |

---

### What ix Should NOT Build

From the research synthesis:

- **Observability**: Langfuse, Opik, Phoenix already do this. ix produces results; they visualize.
- **Red-teaming**: Promptfoo owns this (50+ vulnerability types, OWASP/NIST/MITRE).
- **Model benchmarking**: LM Harness owns this (60+ benchmarks, HuggingFace leaderboard).
- **Prompt optimization**: DSPy owns this. ix measures; DSPy optimizes.

**ix is an experimentation platform for cognitive extensions.** Stay in that lane.

---

### The ix Architecture Stack

Based on the gaps and borrowing strategy:

```
ix Experimentation Platform
+-- Core Engine
|   +-- Matrix (DAG orchestration via graphlib)
|   +-- Goal (experiment definition)
|   +-- Experiment (SLICK Workflow with state machine)
|
+-- SLICK Components (ontology)
|   +-- Probe (stimulus generation) -- SLICK Capability: tool
|   +-- Sensor (observation) -- SLICK Capability: resource
|   +-- Grader (scoring) -- domain-specific adapters for puma matchers
|   +-- Scorer (aggregation) -- F1, pass@k, distributions
|   +-- Reporter (output) -- console, JSON, HTML
|
+-- Statistical Layer (Bayesian, not CLT)
|   +-- bayes_evals library (drop-in replacement for CLT)
|   +-- Clustered standard errors
|   +-- Paired differences
|   +-- Power analysis
|
+-- Agent Harness (drive Claude Code)
|   +-- Inspect AI Agent Bridge (sandbox in Docker/K8s)
|   +-- Claude Agent SDK provider (Promptfoo pattern)
|   +-- Session management (resumable, isolated trials)
|
+-- Persistence (DuckDB)
|   +-- Trial-level results (scores, latency, cost, tokens)
|   +-- Historical tracking (regression detection over time)
|   +-- Export to observability platforms (Langfuse, Phoenix)
|
+-- Quality Gates (CI/CD)
    +-- Threshold checks (block PR if F1 < 0.8)
    +-- Regression detection (alert if performance drops >5%)
    +-- Cost limits (fail if cost > $X per trial)
```

---

## Part 8: Key Research Papers That Change How We Think

These aren't just citations — they fundamentally shift how you design experiments.

### 1. "Adding Error Bars" (Anthropic, Nov 2024)

**Paper**: [arXiv:2411.00640](https://arxiv.org/abs/2411.00640)
**Blog**: [Statistical Approach to Model Measurements](https://www.anthropic.com/research/statistical-approach-to-model-evals)

**Key contribution**: Clustered standard errors can be **3x larger** than naive calculations. Most frameworks report naive SEM — wildly overconfident.

**Actionable**:
- Always use clustered SEs when questions are non-independent
- Report paired differences with correlation coefficients
- Use power analysis to determine sample sizes

**Before this paper**: "My agent scores 78% +/- 1%."
**After this paper**: "My agent scores 78% +/- 3% (clustered SE), CI [72%, 84%]. Paired difference vs baseline: +5% +/- 2%, CI [1%, 9%], correlation r=0.54."

---

### 2. "Don't Use the CLT" (ICML 2025 Spotlight)

**Paper**: [arXiv:2503.01747](https://arxiv.org/abs/2503.01747)

**Key contribution**: Central Limit Theorem underestimates uncertainty for N &lt; 100. Bayesian methods correct this.

**Actionable**: Use `bayes_evals` library for all confidence intervals in small-N settings (which is most experiments).

**Before this paper**: "I have 50 samples, CLT applies, SEM = sigma / sqrt(50)."
**After this paper**: "I have 50 samples, CLT breaks down, use Bayesian credible intervals instead."

---

### 3. "Signal and Noise" (Allen AI, NeurIPS 2025)

**Paper**: [arXiv:2508.13144](https://arxiv.org/abs/2508.13144)

**Key contribution**: Signal-to-noise ratio as a meta-metric for benchmark quality. If SNR &lt; 2, the benchmark doesn't reliably measure what you think.

**Actionable**: Before investing effort in a benchmark, compute its SNR:

```python
# Signal = variance across models
# Noise = variance within model (across trials)
SNR = var_between_models / var_within_model

if SNR < 2:
    print("Benchmark is too noisy, redesign or get more samples")
```

**Before this paper**: "My test suite has high variance. I need more samples."
**After this paper**: "High variance might be high signal (models differ a lot) or high noise (trials differ a lot). SNR tells me which."

---

### 4. "AI Agents That Matter" (Princeton, Jul 2024)

**Paper**: [arXiv:2407.01502](https://arxiv.org/abs/2407.01502)

**Key contribution**: Always report cost alongside accuracy. Pareto curves reveal the real tradeoffs.

**Example**: LATS costs 50x more than baselines but papers don't report this. When you add cost to the graph, LATS is Pareto-dominated by cheaper methods.

**Actionable**: Every ix scorer must track:
- Quality metrics (accuracy, F1, ROUGE, etc.)
- Cost (API spend, latency, token count)
- Pareto frontier (max quality per dollar)

**Before this paper**: "Agent A: 85% accuracy. Agent B: 82% accuracy. A wins."
**After this paper**: "Agent A: 85% @ $2.50/task. Agent B: 82% @ $0.03/task. B wins for production, A wins for research."

---

### 5. CooperBench (Jan 2026)

**Paper**: [arXiv:2601.13295](https://arxiv.org/abs/2601.13295)

**Key contribution**: First benchmark measuring multi-agent cooperation. Frontier models achieve only **25% success** when two agents collaborate — roughly half single-agent rate.

**Three failure modes**:
1. Agents fail to communicate actionable information
2. Agents deviate from commitments
3. Agents hold incorrect expectations about partners

**Actionable for ix**: Coexistence tests must check for these failure modes. When skill B is added:
- Does skill A receive actionable information from B?
- Does A's behavior change when B is present?
- Do A and B have correct expectations about each other's activation?

---

### 6. SWE-EVO (Jan 2026)

**Paper**: [arXiv:2512.18470](https://arxiv.org/abs/2512.18470)

**Key contribution**: Introduces **CL-F1** (continual learning F1):
- **CL-Plasticity**: Ability to learn new tasks
- **CL-Stability**: Retention of performance on previous tasks
- **CL-F1**: Harmonic mean of plasticity and stability

**Actionable for ix**: Coexistence testing is a special case of continual learning:
- Plasticity = "can the agent use skill B?"
- Stability = "does skill A still work after adding B?"
- CL-F1 = overall coexistence score

**Example**:
```python
# Before: security-review skill scores F1=0.90
# After adding code-optimization skill:
plasticity = 0.92  # code-optimization works well
stability = 0.78   # security-review degraded
cl_f1 = 2 * (plasticity * stability) / (plasticity + stability)  # = 0.84

# Interpretation: Code-optimization added successfully, but interfered with security-review
```

---

## Part 9: Putting It All Together — A Worked Example

Let's walk through a realistic ix experiment from start to finish.

### Scenario

You've built a Claude Code skill called `security-review`. It analyzes code for vulnerabilities. You want to:

1. Measure skill activation accuracy ("does it trigger when it should?")
2. Detect coexistence interference ("does adding `code-style` break it?")
3. Track context degradation ("does it work after 50 file reviews?")
4. Ensure statistical rigor (Bayesian CIs, not naive CLT)

---

### Step 1: Define Tasks (Anthropic's Framework)

**Task**: Test case with inputs + success criteria

```python
tasks = [
    {
        "id": "sql_injection_1",
        "input": "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
        "expected_skill": "security-review",
        "expected_finding": "SQL injection vulnerability",
        "cluster": "sql_injection"  # For clustered SEs
    },
    {
        "id": "sql_injection_2",
        "input": "query = 'DELETE FROM logs WHERE ' + user_input; execute(query)",
        "expected_skill": "security-review",
        "expected_finding": "SQL injection via concatenation",
        "cluster": "sql_injection"
    },
    # ... 48 more tasks across 5 clusters
]
```

**Note**: 50 tasks, 5 clusters (10 tasks per cluster) for clustered SE calculation.

---

### Step 2: Define Experiment DAG

```python
experiment = ix.Experiment(
    name="security-review-activation",
    trials_per_task=10,  # pass@10 and pass^10 metrics
)

# DAG nodes
experiment.add_probe("prompt_probe")  # Generates test inputs
experiment.add_sensor("activation_sensor", depends_on=["prompt_probe"])  # Observes skill activation
experiment.add_sensor("finding_sensor", depends_on=["prompt_probe"])  # Extracts security findings
experiment.add_grader("activation_grader", depends_on=["activation_sensor"])  # Matches expected vs actual
experiment.add_grader("finding_grader", depends_on=["finding_sensor"])  # Matches expected finding
experiment.add_scorer("classification_scorer", depends_on=["activation_grader", "finding_grader"])  # F1
experiment.add_scorer("stochastic_scorer", depends_on=["classification_scorer"])  # pass@k, pass^k
experiment.add_scorer("cost_scorer", depends_on=["activation_sensor"])  # Tracks API spend
experiment.add_reporter("console_reporter", depends_on=["stochastic_scorer", "cost_scorer"])
```

**DAG parallelization**:
- `activation_sensor` and `finding_sensor` run in parallel (both depend only on probe)
- `activation_grader` and `finding_grader` run in parallel
- `classification_scorer` waits for both graders
- `stochastic_scorer` computes pass@k from classification results
- `cost_scorer` runs independently
- `console_reporter` waits for both scorers

---

### Step 3: Run Experiment (Skill Activation)

```python
result = ix.run(experiment, tasks=tasks)

# Result structure:
{
    "mean_f1": 0.88,
    "se_clustered": 0.03,  # 3x larger than naive SE=0.01
    "ci_95": [0.82, 0.94],
    "pass_at_10": 0.98,  # At least one success in 10 trials
    "pass_pow_10": 0.28,  # All 10 trials succeed
    "total_cost": 4.23,  # USD
    "cost_per_task": 0.085,
    "transcripts": [...]  # Full traces for inspection
}
```

**Interpretation**:
- F1 = 0.88 means precision/recall are high (skill activates correctly)
- Clustered SE = 0.03 (not 0.01) because SQL injection tasks correlate
- pass@10 = 98% means "at least once in 10 tries" almost always works
- pass^10 = 28% means "all 10 tries" rarely works — stochastic variance is high
- Cost = $0.085/task is reasonable for security review

---

### Step 4: Coexistence Test (Does Adding `code-style` Break It?)

```python
# Control: security-review alone
control = ix.Experiment(
    name="control",
    skills=["security-review"]
)

# Variant: security-review + code-style
variant = ix.Experiment(
    name="variant",
    skills=["security-review", "code-style"]
)

# Run both on same tasks
coexistence_result = ix.run_paired([control, variant], tasks=tasks)

# Result:
{
    "control_f1": 0.88,
    "variant_f1": 0.76,  # Dropped!
    "delta_f1": -0.12,
    "se_paired": 0.02,  # Paired SE (smaller than independent)
    "ci_95": [-0.16, -0.08],
    "correlation": 0.61,  # Tasks correlate across experiments
    "interpretation": "Code-style skill interferes with security-review. F1 dropped 12 points (p < 0.001)."
}
```

**Interpretation**:
- F1 dropped from 0.88 to 0.76 when code-style added
- Paired CI = [-0.16, -0.08] doesn't include zero -> **significant degradation**
- Transcript analysis shows: code-style generates explanations that suppress security warnings
- **Coexistence interference detected**

---

### Step 5: Context Degradation Test

```python
degradation_experiment = ix.ContextDegradationExperiment(
    skill="security-review",
    max_tool_calls=100,
    checkpoints=[10, 25, 50, 75, 100]
)

degradation_result = ix.run(degradation_experiment, tasks=tasks)

# Result:
{
    "checkpoints": {
        10:  {"f1": 0.88, "latency_p50": 1.2, "cost": 0.09},
        25:  {"f1": 0.85, "latency_p50": 1.4, "cost": 0.11},
        50:  {"f1": 0.78, "latency_p50": 1.9, "cost": 0.14},
        75:  {"f1": 0.71, "latency_p50": 2.5, "cost": 0.19},
        100: {"f1": 0.63, "latency_p50": 3.2, "cost": 0.26},
    },
    "degradation_rate": -0.0025,  # F1 drops 0.25 points per 10 tool calls
    "interpretation": "Context degradation detected. Agent loses focus after 50 calls."
}
```

**Interpretation**:
- F1 at step 10: 88% (baseline)
- F1 at step 50: 78% (10-point drop)
- F1 at step 100: 63% (25-point drop)
- Latency and cost also increase (crowded context is expensive)
- **Context degradation confirmed**

---

### Step 6: Statistical Rigor (Bayesian CIs)

```python
# ix automatically uses bayes_evals for small-N
from bayes_evals import bayesian_ci

# Instead of CLT (wrong):
sem_clt = np.std(f1_scores) / np.sqrt(len(f1_scores))
ci_clt = [mean - 1.96*sem_clt, mean + 1.96*sem_clt]  # Underestimates uncertainty

# Bayesian (correct):
ci_bayes = bayesian_ci(f1_scores, confidence=0.95)  # Wider, more honest

# Result:
# CLT CI: [0.85, 0.91] (overconfident)
# Bayes CI: [0.82, 0.94] (realistic)
```

**Why this matters**: With 50 tasks, CLT breaks down. Bayesian methods give you honest uncertainty.

---

### Step 7: Pareto Analysis (Cost vs Quality)

```python
# Collect quality and cost across variants
variants = [
    {"name": "security-review-base", "f1": 0.88, "cost": 0.085},
    {"name": "security-review-cot", "f1": 0.91, "cost": 0.14},
    {"name": "security-review-lightweight", "f1": 0.82, "cost": 0.03},
]

pareto_result = ix.compute_pareto(variants, quality_metric="f1", cost_metric="cost")

# Result: Pareto frontier
# - Lightweight: 0.82 F1 @ $0.03 (best for cost-sensitive)
# - Base: 0.88 F1 @ $0.085 (balanced)
# - CoT: 0.91 F1 @ $0.14 (best for quality-sensitive)

# CoT is NOT Pareto-optimal -- it costs 1.65x more for only 3-point improvement
# For production: use base or lightweight depending on budget
```

**Interpretation**: Always show cost-quality tradeoffs. Pure accuracy rankings hide the real decision.

**Source**: [AI Agents That Matter](https://arxiv.org/abs/2407.01502)

---

### Step 8: Quality Gate (CI/CD Integration)

```python
# Define thresholds
quality_gate = ix.QualityGate(
    min_f1=0.80,
    max_degradation=0.05,  # Alert if F1 drops >5pp vs baseline
    max_cost_per_task=0.10,
)

# Check results
gate_result = quality_gate.check(result)

if gate_result.passed:
    print("Quality gate passed. Deploy to production.")
else:
    print(f"Quality gate failed: {gate_result.failures}")
    sys.exit(1)
```

**Integration**: Run this in GitHub Actions on every PR. Block merge if quality regresses.

**Source**: [Braintrust CI/CD patterns](https://www.braintrust.dev/docs/core/functions/scorers)

---

## Part 10: Final Mental Model — What You've Learned

You started knowing Python and Claude Code skills. Now you know:

### 1. Measurement Under Uncertainty

It's not pass/fail. It's distributions, confidence intervals, and tradeoffs.

### 2. State, Execution, Stochasticity, Grading

Every framework makes choices on these four dimensions. Most make bad choices (no state, sequential execution, no stochastic handling, brittle grading).

### 3. Statistics Matter More Than You Think

- Clustered SEs can be 3x larger than naive
- CLT breaks down for small N (use Bayesian)
- Infrastructure noise is 3-6 percentage points
- Paired differences are more powerful than independent comparisons

### 4. Anthropic's Guidance Is Canonical

- Task/trial/transcript/outcome terminology
- pass@k vs pass^k metrics
- Grade outcome, not path
- 20-50 tasks from real failures = starting point
- Code > LLM > Human grading hierarchy

### 5. The Gaps ix Fills Are Real

- Skill activation: No tool tests "right skill for right context"
- Coexistence: No tool tests "adding B breaks A"
- Context degradation: No benchmark measures "works after 50 calls"
- DAG orchestration: No framework composes components as dependency graph

### 6. ix Is Unique

Upper-right quadrant: agent experimentation + statistical rigor + DAG orchestration.

Nobody else is there.

---

## Appendix A: Complete Source Index

All sources organized by tier and category.

### [TIER 1] Anthropic Official Research

| Source | URL | Key Contribution |
|--------|-----|------------------|
| Adding Error Bars | [arXiv:2411.00640](https://arxiv.org/abs/2411.00640) | Clustered SEs 3x larger than naive |
| Demystifying Agents | [anthropic.com](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Zero-to-one roadmap, grader types |
| Infrastructure Noise | [anthropic.com](https://www.anthropic.com/engineering/infrastructure-noise) | 6pp shifts from config alone |
| Create Strong Empirical Tests | [docs](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Code examples for every grading type |
| Bloom | [GitHub](https://github.com/safety-research/bloom) | Understand -> Ideate -> Rollout -> Judge pipeline |
| Model-Written Tests | [arXiv:2212.09251](https://arxiv.org/abs/2212.09251) | Automated test generation, 154 datasets |
| Constitutional AI | [arXiv:2212.08073](https://arxiv.org/abs/2212.08073) | Self-assessment methodology |
| Measuring CoT Faithfulness | [arXiv:2307.13702](https://arxiv.org/abs/2307.13702) | CoT is unreliable for grading |
| Sabotage Tests | [arXiv:2410.21514](https://arxiv.org/abs/2410.21514) | Four sabotage test types |
| Alignment Faking | [arXiv:2412.14093](https://arxiv.org/abs/2412.14093) | Scratchpad methodology, 12% faking rate |
| Claude Code Headless | [docs](https://code.claude.com/docs/en/headless) | Programmatic Claude Code for harnesses |

### [TIER 1] Academic Papers (Non-Anthropic)

| Source | URL | Key Contribution |
|--------|-----|------------------|
| Don't Use the CLT | [arXiv:2503.01747](https://arxiv.org/abs/2503.01747) | CLT underestimates uncertainty, use Bayesian |
| Signal and Noise | [arXiv:2508.13144](https://arxiv.org/abs/2508.13144) | SNR as benchmark quality metric |
| AI Agents That Matter | [arXiv:2407.01502](https://arxiv.org/abs/2407.01502) | Always report cost, Pareto curves |
| CooperBench | [arXiv:2601.13295](https://arxiv.org/abs/2601.13295) | Multi-agent cooperation fails 75% |
| SWE-EVO | [arXiv:2512.18470](https://arxiv.org/abs/2512.18470) | CL-F1 (plasticity + stability) |
| SWE-bench | [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) | Real-world GitHub bug fixes |

### [TIER 1] Official Framework Docs

| Framework | Docs | GitHub | Stars |
|-----------|------|--------|-------|
| Inspect AI | [docs](https://inspect.aisi.org.uk/) | [GitHub](https://github.com/UKGovernmentBEIS/inspect_ai) | 1.7k |
| Promptfoo | [docs](https://www.promptfoo.dev/) | [GitHub](https://github.com/promptfoo/promptfoo) | 10.4k |
| DeepEval | [docs](https://deepeval.com/) | [GitHub](https://github.com/confident-ai/deepeval) | 13.6k |
| LM Harness | [docs](https://www.eleuther.ai/artifacts/lm-evaluation-harness) | [GitHub](https://github.com/EleutherAI/lm-evaluation-harness) | 11.4k |
| Langfuse | [docs](https://langfuse.com/) | [GitHub](https://github.com/langfuse/langfuse) | 21.7k |
| Arize Phoenix | [docs](https://phoenix.arize.com/) | [GitHub](https://github.com/Arize-ai/phoenix) | 8.5k |
| Braintrust | [docs](https://www.braintrust.dev/) | [GitHub](https://github.com/braintrustdata/braintrust-sdk) | 114 |

### [TIER 2] Practitioner Analysis

| Source | URL | Key Insight |
|--------|-----|-------------|
| Phil Schmid "Agent Harness 2026" | [philschmid.de](https://www.philschmid.de/agent-harness-2026) | Task durability (50+ tool calls) is unmeasured |
| Hamel Husain "Inspect AI Review" | [hamel.dev](https://hamel.dev/notes/llm/evals/inspect.html) | Practitioner review of Inspect AI |

### [TIER 3] Research Syntheses (This Document)

| Source | Location | Contents |
|--------|----------|----------|
| Unified Synthesis | `scratch/research-synthesis-ix-landscape-2026-02-09.md` | Framework comparison, gaps analysis |
| LLM Framework Landscape | `scratch/llm-eval-framework-landscape-2026-02-09.md` | 14 frameworks analyzed |
| Agent Harness Landscape | `scratch/agent-eval-harness-landscape-2026-02-09.md` | Agent-specific tooling |
| Anthropic Research Sweep | `scratch/anthropic-eval-research-sweep-2026-02-09.md` | 40+ Anthropic sources |

---

## Appendix B: Key Numbers to Remember

| Number | Source | What It Means |
|--------|--------|---------------|
| **3x** | Error Bars paper | Clustered SEs can be 3x larger than naive |
| **6pp** | Infrastructure Noise | Config alone shifts benchmark scores 6 percentage points |
| **3pp** | Infrastructure Noise | Differences below 3pp deserve skepticism |
| **20-50** | Demystifying Agents | Starting point for test suite size |
| **98% vs 42%** | pass@3 vs pass^3 | Same 75% success rate, wildly different numbers |
| **25%** | CooperBench | Multi-agent cooperation success rate (vs 50% single-agent) |
| **17%** | Learning harm research | Worse exam performance after unrestricted AI use |
| **75%** | SWE-bench Verified | Current coding agent performance (Jan 2026) |

---

## Appendix C: Glossary (Anthropic's Terminology)

Use these terms. They're standard.

| Term | Definition | Example |
|------|------------|---------|
| **Task** | Single test with inputs + success criteria | "Does security-review trigger for SQL injection?" |
| **Trial** | One attempt at a task | 10 trials per task for pass@10 |
| **Grader** | Logic scoring agent performance | Code-based, LLM-based, or human |
| **Transcript** | Complete record of a trial | All outputs, tool calls, reasoning |
| **Outcome** | Final environment state | Not agent's claim — actual result |
| **Harness** | Infrastructure running experiments | Docker containers, API calls, grading |
| **pass@k** | Probability of at least 1 success in k trials | Use for coding (one working solution) |
| **pass^k** | Probability all k trials succeed | Use for customer-facing (consistency) |
| **Clustered SE** | Standard error accounting for correlation | 3x larger than naive SE |
| **Paired differences** | Compare same tasks across models | Free variance reduction from correlation |

---

*Research conducted February 2026. Three parallel research agents + Anthropic deep dive, ~300K tokens total research. All claims sourced to Tier 1 or Tier 2 evidence.*

*Next steps: Read the [ix ontology deliberation](../../scratch/guild-ix-ontology-deliberation-2026-02-08.md) and [ix-lab architecture](../../scratch/ix-lab-architecture-excavation-2026-02-06.md) to see how these concepts map to ix's implementation.*
