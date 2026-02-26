# Collaborative Intelligence Extensions (cix)

> Liberation through Collaborative Intelligence.

Build a marketplace of cognitive extensions where AI amplifies human capability and judgment. Every extension must make humans more capable, not dependent.

---

## The Thesis

**AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable long-term human capability.**

The interaction pattern — not the technology — determines the outcome. Same AI, different design, opposite results. The research coefficients: control is the strongest lever (β=0.507), transparency second (β=0.415), paternalistic engagement backfires (b=-0.555). Mastery orientation preserves capability (OR=35.7); performance orientation destroys it.

Full evidence with effect sizes: `docs/content/library/reference/bibliography.md`

---

## Plugin Taxonomy

7 plugins organized by CI lifecycle phase:

| Plugin | Phase | Purpose |
|--------|-------|---------|
| **craft-research** | Research | Literature review, multi-paper synthesis, citation-grounded research |
| **craft-rhetoric** | Understand | Explanation craft via the Five Canons — 9 agents |
| **guild-arch** | Design | 13 orthogonal reasoning agents for architectural deliberation |
| **craft-extensions** | Craft | Build extensions (skills, agents, hooks, commands, MCP), data layers, reasoning prompts |
| **craft-evals** | Measure | Eval methodology — write evals that measure what matters |
| **ci-scaffolds** | Cross-cutting | Collaboration, problem-solving, and engineering craft scaffolds |
| **run-openclaw-seatbelt** | Security | OpenClaw setup with Seatbelt sandbox |

Lifecycle: **research → understand → design → craft → measure**. Each plugin owns one phase. Composable across a project lifecycle — use what you need.

---

## Design Principles

Five principles govern every extension. For depth, examples, research backing, and anti-patterns: load `craft-extensions:craft-plugins` reference `design-principles.md`.

| # | Principle | Rule |
|---|-----------|------|
| 1 | **Complementary, Not Substitutive** | AI amplifies, human remains central. Never substitutive. |
| 2 | **Pit of Success** | Right thing is the only obvious path. Defaults for most, escape hatches for few. |
| 3 | **Transparent Abstractions** | If you can't see through it, you can't learn from it. |
| 4 | **Compound Value** | Every change makes the next change easier. |
| 5 | **Composable, Not Comprehensive** | Small focused extensions that combine. Human synthesizes. |

### The Cardinal Test

For every extension feature:
1. Does this make users more capable or more dependent?
2. Does the user retain the generative step (doing the thinking)?
3. Would users be helpless after extended use?

---

## Extension Components

| Component | Purpose | Pattern |
|-----------|---------|---------|
| **Skill** | Decision frameworks, domain knowledge | Teaches HOW to think |
| **Agent** | Specialized perspective, multi-step reasoning | Offers viewpoint, human synthesizes |
| **Hook** | Event-triggered behavior | Enhances workflow, guardrails |
| **Command** | User-initiated procedure | Human triggers, extension executes |
| **MCP** | External service integration | Bridges systems, human orchestrates |

For component selection, file anatomy, and build guidance: load `craft-extensions:craft-plugins` skill.

### Key Design Concepts

**Dual-Content Model**: Extensions serve two audiences — Claude needs token-efficient, actionable guidance; humans need explanatory, traceable content. Claude reads `SKILL.md`, `references/`, `templates/`, `scripts/`. **Never read `docs/` directories** — they contain human-optimized prose that wastes tokens and may confuse actionable guidance with learning material.

**Orthogonality Lock**: Agents provide one perspective, not comprehensive coverage. Forces human synthesis across multiple viewpoints.

**Progressive Disclosure**: Metadata (always loaded) → SKILL.md (on activation) → References (on demand). Tokens are a public good.

---

## Design Lever Hierarchy

Research-established ordering of what works in human-AI co-production (Blaurock et al. 2025, n=654):

| Rank | Lever | Effect | Implication |
|------|-------|--------|-------------|
| 1 | **Control** | β=0.507 | User agency is the strongest lever |
| 2 | **Transparency** | β=0.415 | Show reasoning — but explanations that substitute for evaluation increase overreliance |
| 3 | **Mastery orientation** | OR=35.7 | Users focused on learning maintain capability; task-completion focus destroys it |
| 4 | **AI confidence** | r=-0.68 | Higher AI confidence predicts less critical thinking. Build human evaluative confidence instead |
| 5 | **Engagement features** | b=-0.555 | Gamification, "was this helpful?" — negative effect for experienced users |

Additional: diversity reduction g=-0.863 (28 studies, n=8,214), skill formation gap d=0.738 (Anthropic RCT), learning harm -17% without guardrails (Bastani PNAS).

---

## Anti-Patterns

| Anti-Pattern | Signal | Alternative |
|--------------|--------|-------------|
| **Auto-fix** | Human doesn't learn why | Explain issue, offer fix, human applies |
| **Black box** | Human can't evaluate | Show reasoning at every step |
| **Scope creep** | Agent does more than asked | Strict orthogonality constraints |
| **Confidence theater** | Fake certainty | Explicit uncertainty (evidence levels) |
| **Memory hoarding** | Private agent state | Shared knowledge substrate |
| **Paternalism** | "I know better" | "Here's my perspective, you decide" |

---

## Project Architecture

```
cix/
├── tools/cix/              # CLI package (hexagonal architecture)
│   └── src/cix/
│       ├── domain/         # Pure domain models
│       ├── ports/          # Interface definitions
│       ├── adapters/       # Implementations
│       └── application/    # Use case orchestration
├── plugins/                # Marketplace plugins (distributable)
└── .claude/                # Project-specific Claude extensions
```

### Hexagonal Architecture

- **Domain**: Pure business logic with no external dependencies
- **Ports**: Interfaces for what cix needs (driven) and how users interact (driving)
- **Adapters**: Implementations of ports (git, filesystem, CLI)
- **Application**: Use case orchestration through ports

This enables:
- Testing without external dependencies
- Multiple implementations (git + local, CLI + API)
- Clear separation of concerns
- Protocol independence

---

## Observability

### Where Logs Live

Claude Code logs all conversations and agent outputs to JSONL:

```
~/.claude/projects/<project-path>/
├── <session-uuid>.jsonl                    # Main conversation
└── <session-uuid>/subagents/
    └── agent-<id>.jsonl                    # Subagent outputs
```

### Log Format

```json
{
  "type": "user|assistant",
  "agentId": "a1b59b6",
  "timestamp": "2026-01-30T21:19:38.857Z",
  "message": {
    "role": "assistant",
    "content": [{"type": "text", ...}, {"type": "tool_use", ...}]
  }
}
```

### What Can Be Observed

| Observable | Source | Method |
|------------|--------|--------|
| **Agent activation** | JSONL logs | Parse `agentId`, `timestamp` |
| **Tool call sequences** | JSONL `content[type=tool_use]` | Parse tool names, args |
| **Token usage** | API response metadata | Capture in hooks |
| **Session patterns** | JSONL timestamps | Time-series analysis |

### What Requires Evaluation

**Decision quality** cannot be directly observed — it requires:
- **Human feedback** — user ratings on outputs
- **Evals** — automated checks (see `evals/` in plugins)
- **Downstream metrics** — bugs, PR rejections, rework

### Querying Logs

DuckDB can query JSONL directly:

```sql
SELECT
  json_extract_string(line, '$.agentId') as agent,
  json_extract_string(line, '$.timestamp') as ts,
  json_extract_string(line, '$.type') as msg_type
FROM read_json_auto('~/.claude/projects/.../agent-*.jsonl')
WHERE json_extract_string(line, '$.type') = 'assistant';
```

---

## Working Conventions

### Scratch Directory

When taking notes or preserving context across sessions, use `scratch/` in the project root.

### Screenshots

Save all screenshots to `.screenshots/` in the project root. This directory is gitignored.

- **Always use `.screenshots/`** — never save PNGs to the project root
- Use descriptive filenames: `catalog-mermaid-fixed.png`, `landing-hero-v2.png`

### Evidence-Based Claims

All claims in extensions should be traceable to specific sources with author, year, and finding. Never say "research shows" without a citation. When evidence is limited, say so explicitly.

---

## guild-arch Ontology (Karman-Approved)

The guild-arch plugin provides 13 orthogonal reasoning agents across 10 Core Drives, 4 Skills, and a Domain Vocabulary Mapping mechanism.

### Domain Vocabulary Mapping

The guild speaks in agent metaphors (Erlang's "Valve", Lamport's "Time", Burner's "Boundary"). When reasoning about a specific domain, agents check the project's CLAUDE.md for a `## Guild Vocabulary` section that maps these metaphors to domain-specific terms. This lets the guild reason precisely about any domain without ix-specific knowledge baked into the plugin.

### 10 Core Drives

| Drive | Agent | Focus |
|-------|-------|-------|
| Strategic | K | Forces, constraints, optionality |
| Protective | Burner | Integrity, boundaries |
| Adversarial | Vector | Attack surface, exploitation |
| Principled | Karman, Dijkstra | Truth, correctness |
| Traumatic | Lamport, Chesterton, Taleb | Past failures, experience |
| Empirical | Ixian | Falsifiability, measurement |
| Physical | Erlang | Flow dynamics, system limits |
| Mathematical | Knuth | Resource physics, complexity |
| Nuanced | Lotfi | Degrees of truth, fuzzy scoring |
| Humanistic | Ace | Developer advocacy, cognitive load |

### Key Decisions

- **Ixian** = Principal Experimentation Architect (Falsifiability drive, designs experiments, not just metrics)
- **Protocol > ABC** for Python hexagonal ports (`typing.Protocol` with `@runtime_checkable`)
- **stat-rigor.md** reference: Bayesian methods, CLT rejection, clustered SEs, pass@k, row vs aggregate scoring
- **Domain Vocabulary Mapping** (not "Overlay") as the mechanism name (Karman: precision over metaphor)

---

## References

Full bibliography with 45+ entries, effect sizes, and expandable abstracts: `docs/content/library/reference/bibliography.md`

Primary source papers collected as text: `scratch/papers/`

---

## Session Bootstrap

**CRITICAL: On session start, read `scratch/bootstrap-session-2026-02-16.md` FIRST.**

It documents a recurring issue where context overflow flattens architectural decisions into shallow renames. It contains the correct two-layer architecture (`ix.domain` + `ix.domains.eval`) that was user-approved but never implemented due to context loss.

Previous bootstrap (still relevant for Matrix status): `scratch/bootstrap-session-2026-02-14.md`

Key references:
- `scratch/kmaster-ix-reference.md` — definitive ix reference (ontology, arch, CLI, landscape)
- `scratch/matrix-v1-spec.md` — full Matrix platform spec (config, registry, container, adapters)
