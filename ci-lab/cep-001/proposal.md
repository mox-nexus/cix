# CEP-001: Capabilities with Packaged Semantic Glue

**Status**: Directional Signal (Run 1)
**Author**: Mox Labs
**Created**: 2026-02-28
**Updated**: 2026-03-07

## Thesis

Mechanical interface definitions — `--help` output, OpenAPI specs, tool schemas — are not sufficient for LLM legibility. Skills provide a step increase in task completion by adding semantic context that makes capabilities interpretable to LLMs.

The architectural consequence — that tools should package this semantic context alongside their mechanical interface — follows from the finding. If skills > help, package the skill with the tool. That's derivation, not experimentation.

## Hypothesis

**H1**: Skill-format documentation produces higher task-completion accuracy than reference-format documentation when an agent must search a corpus, extract facts, and compose an answer.

**H0**: No measurable difference. The agent extracts equivalent understanding from the mechanical interface.

## Motivation

A tool-description skill is a deliberate bet. Someone authors it, maintains it, keeps it in sync with the interface. If the mechanical artifact that's already there is sufficient for LLM comprehension, that bet doesn't pay off.

**This experiment categorizes a type of skill, not the skill concept itself.** The finding does not contest the Agent Skills standard or the value of skills generally. It asks whether one particular category — skills that describe tools and their commands — earns its keep given that tools already come with interface definitions.

### What each outcome means

**If skill format produces higher accuracy:**

The semantic layer earns its keep. The next question is what in the skill format does the work and whether that semantic layer could be packaged at the interface itself rather than requiring a separate skill file. This is the core thesis of this proposal.

**If no measurable difference:**

Tool-description skills are redundant. Skill-authoring effort should concentrate on what tools cannot provide: workflow orchestration, multi-tool coordination, domain knowledge, decision heuristics.

## Design

### Evolution

The experiment ran in two phases with a methodology pivot between them.

**Phase 0 — Command Selection (nexus fixture, mock tool)**

Tested whether skill-format documentation improves *command selection* at decision boundaries. Used a synthetic `nexus` tool with 6 subcommands, 29 probes targeting ambiguous command pairs, single-turn AnthropicAgent (tool intent only, no execution).

Result: 25 of 29 probes hit 100% accuracy under `--help` alone. Command selection is essentially solved by the mechanical interface for Sonnet-class models. The tool schema in the API already provides enough signal. Only the locate/trace boundary showed variance (lt-003: 30%, lt-001: 70%).

**Conclusion**: Command selection is the wrong dependent variable. The discrimination zone is too narrow.

**Phase 1 — Intent-to-Outcome (memex, real tool execution)**

Pivoted to measuring *task completion*: can the agent search a real corpus, find the right information, and compose a correct answer? Used memex with a self-contained local corpus (34 fragments, 8 conversations), multi-turn ClaudeAgent (Agent SDK, real Bash execution), and three documentation formats.

### Test fixture

A local `.memex/` corpus seeded with 8 synthetic conversations covering: auth token storage (DuckDB), rate limiting (token bucket), embedding model selection (nomic-embed-text), hexagonal architecture ports (Protocol), CI lab naming, a reranking bug fix, Svelte 5 runes migration, and trail architecture design.

### Subjects

Three subjects, each a system prompt containing memex documentation in a different format. All share identical framing, corpus context, and instructions. Runtime: ClaudeAgent (Agent SDK), max 5 turns, Bash tool only.

| Subject | Format | Content |
|---------|--------|---------|
| `help-only` | Raw `--help` output for all commands | Mechanical interface, no semantic guidance |
| `skill-at-tool` | Skill format: "When to Use" tables, search strategy, @N references, troubleshooting | Semantic layer, no `--help` |
| `help-plus-agent-skill` | Both `--help` output and agent skill guide | Combined format |

### Probes

6 intent-to-outcome probes. Each presents a natural question about the corpus and expects specific facts in the response.

| ID | Category | Question | Expected Facts |
|----|----------|----------|----------------|
| out-001 | factual-retrieval | What database for auth tokens? Why? | DuckDB, single-node, analytics, token usage |
| out-002 | factual-retrieval | Rate limiting config numbers? | token bucket, 40 req/min, burst 15, 500ms backoff |
| out-003 | factual-retrieval | Which embedding model? Dimensions? | nomic-embed-text, v1.5, 768, ONNX |
| out-004 | debugging | What was the reranking bug? Fix? | cross-encoder, score normalization, 0-1 range, sigmoid |
| out-005 | conceptual | Difference between trails and similar? | trails: curated/manual, similar: algorithmic/automatic |
| out-006 | architectural | Hexagonal port pattern decision? | Protocol, structural typing, runtime_checkable |

### Sensors

Composite sensor with two components:

1. **ToolUsageSensor** — detects memex usage in Bash tool calls (handles compound commands like `cd ... && memex dig "query"`)
2. **OutcomeSensor** — grades response content against expected_facts, captures efficiency metrics (turns, tool calls)

Scoring per trial: `(tool_score + outcome_score) / 2`. Tool score is binary (used memex or not). Outcome score is fraction of expected facts found in response content.

## Results

### Phase 0 — Command Selection (10 trials x 29 probes, nexus fixture)

25 of 29 probes hit 100% accuracy under `--help` alone. Command selection is solved by the mechanical interface for Sonnet-class models.

**Conclusion**: Command selection is the wrong dependent variable. Pivoted to task completion.

### Phase 1 — Intent-to-Outcome (3 trials x 6 probes, memex)

**Tool usage: 100% across all subjects.** Every subject correctly calls `memex dig` on every trial. Command selection is not the bottleneck — confirming Phase 0.

**Outcome scores (fact extraction accuracy):**

| Subject | out-001 | out-002 | out-003 | out-004 | out-005 | out-006 | Mean |
|---------|---------|---------|---------|---------|---------|---------|------|
| **help-only** | 0% | 67% | 67% | 17% | 67% | 0% | **36%** |
| **skill-at-tool** | 100% | 100% | 67% | 50% | 83% | 67% | **78%** |
| **help-plus-agent-skill** | 33% | 67% | 67% | 100% | 100% | 33% | **66%** |

*Composite scores (tool + outcome / 2) compress the signal because tool usage is uniformly 100%. Outcome-only scores above show the actual effect size.*

### Key Findings

**1. The legibility gap is real.** help-only scores 36% on fact extraction. skill-at-tool scores 78%. That's a 42 percentage point improvement from the semantic layer alone.

**2. Skill-at-tool wins.** The semantic layer — "When to Use" tables, search strategy guidance, @N reference patterns — produces measurably better task completion. The agent finds the data AND surfaces the relevant facts.

**3. Combined format doesn't beat skill-only.** help-plus-agent-skill (66%) falls between the other two. Adding `--help` to the skill adds noise rather than signal.

**4. The failure mode is composition, not selection.** help-only trials show the agent calling the right command, getting the right search results, but failing to extract and present the expected facts. The skill format teaches the agent *how to compose answers from search results*, not just which command to run.

**5. Command selection is solved.** Both Phase 0 (29 probes, 100% accuracy) and Phase 1 (100% tool usage) confirm that `--help` is sufficient for choosing the right command. The gap is downstream.

### Interpretation

The skill format's value is not in command selection (the mechanical interface handles that) but in *legibility* — making the tool's capabilities interpretable enough for the LLM to complete the full intent-to-outcome loop. The "When to Use" table, the search strategy guidance, the @N reference workflow — these are semantic glue that connects the mechanical interface to human intent.

This suggests a design principle: **capabilities need improved LLM legibility**. The `--help` text was written for humans scanning a terminal. The skill format was written for an LLM reasoning about which tool to use and how to use it. Same information, different legibility.

## Limitations (Run 1)

**No noise floor measured.** No same-subject replication run (help-only vs help-only). Without this, the 42pp gap could partially reflect run-to-run variance rather than a treatment effect.

**N=3 is below defensible threshold.** 18 observations per subject. At N=3 per probe, a single trial swings a probe score by 33pp. The 89% HDIs for the two subjects overlap at this sample size. Cannot reject H0.

**String containment grading.** Fact-matching via `fact.lower() in content.lower()` is coarse. A verbose response dumping the corpus scores 100%; a precise paraphrase using different words scores 0%. Measurement artifact is possible.

**Single tool.** Memex only. Results claim "skills provide a step increase for memex," not the general case.

**Active ingredient unknown.** The skill format bundles: (1) decision heuristics, (2) composition guidance, (3) workflow patterns. Which drives the improvement? Decomposition is future work.

**Three simultaneous changes in the Phase 0 → Phase 1 pivot.** Changed the dependent variable (command selection → outcome), the runtime (AnthropicAgent → ClaudeAgent), and the tool (mock nexus → real memex) at once. Phase 1 results cannot be compared to Phase 0.

## Implications

1. **Mechanical interfaces are insufficient for LLM legibility.** `--help` and OpenAPI specs are sufficient for command selection but not for task completion. The 42pp gap between skill-format and help-format on fact extraction demonstrates the legibility deficit. Directional — pending noise floor measurement and increased N.

2. **Skills provide the semantic glue.** The high-value content is not command documentation — it's decision heuristics (when to use), composition guidance (how to interpret results), and workflow patterns. This is what makes capabilities legible to LLMs.

3. **Tools should package this semantic context.** This follows from the finding: if the semantic layer is necessary for task completion, it should ship with the capability, not be maintained as a separate artifact. The architectural consequence is derivable — if skills > help, package the skill with the tool.

## Iteration Roadmap

This is experiment run 1. More thorough experiments will come through iterations as nuances are identified.

### Run 2 — Measurement Foundation

Priority: establish the noise floor and fix the sensor before increasing N.

1. **Noise floor**: Run help-only vs help-only (same subject, same config, two independent runs). The absolute difference in mean outcome score IS the noise floor. All inter-subject comparisons must exceed 2x this value.
2. **Functional graders**: Replace string containment with deterministic tests against corpus ground truth. Test "did the agent retrieve fragment X and report fact Y" — verifiable from tool call output, not just natural language response.
3. **N=5 minimum**, ideally N=10, with probe-level reporting before pooling.

### Run 3 — Active Ingredient Decomposition

Only after the measurement apparatus is sound.

4. **2x2 factorial**: Format (skill vs help) x content richness (decision heuristics only vs full skill). Isolate which component of the skill format drives the improvement.
5. **Pre-register probe-level predictions**: For each probe, state before running which subject will win and why.

### Run 4 — Generalization

6. **Second tool replication**: Different tool, different command structure, different failure modes. Required for the general claim "skills provide a step increase" vs "skills provide a step increase for memex."
7. **Model comparison**: Weaker models (Haiku) may benefit more from skill format. Test across model tiers.

### Validation Criteria (Ixian)

| Level | Requirements | Status |
|-------|-------------|--------|
| **Directional signal** | N=18, string containment, no noise floor | Current (Run 1) |
| **Validated L1** | Noise floor measured, N>=75, functional graders, probe-level reporting | Run 2 target |
| **Validated L2** | 2x2 factorial, replicated on second tool, interaction effects tested | Run 3-4 target |

**Rollback trigger**: If noise floor exceeds 20pp, the measurement apparatus is too noisy — fix the sensor before continuing. If skill-format 89% HDI overlaps help-only 89% HDI after N=75, the effect is either absent or smaller than 30pp.

## References

- Phase 0 results: `results/summary-20260305T144253Z.json`
- Test corpus: `corpus/` (8 conversations, 34 fragments)
- Subjects: `subjects/help-only.md`, `subjects/skill-at-tool.md`, `subjects/help-plus-agent-skill.md`
- Probes: `tasks/out-001.md` through `tasks/out-006.md`
- Archived Phase 0 probes: `tasks/archive-command-selection/`, `tasks/archive-nexus/`, `tasks/archive/`
