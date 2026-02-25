# Collaborative Intelligence Extensions (cix)

> **Liberation through Collaborative Intelligence**
> Extensions that enhance human capability, not replace it.

## Mission

Build a marketplace of cognitive extensions grounded in the **Collaborative Intelligence** thesis: AI tools should amplify human capability and judgment, not substitute for them. Every extension in this ecosystem must make humans more capable, not dependent.

---

## The Evidence Base

This project is grounded in rigorous research synthesis from premier venues (CHI, ICSE, Nature, PNAS, NeurIPS).

### The Central Paradox

**AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable long-term human capability.**

The productivity gains are real. The learning harm is real. The interaction pattern — not the technology — determines which outcome you get. Same AI, different design, opposite results.

### What the Research Establishes

- **Cognitive offloading is measurable**: AI confidence predicts less critical thinking; neural engagement scales down with AI use
- **Skill atrophy is real and invisible**: Performance degrades after AI exposure, and the performer can't detect it
- **Homogenization is structural**: AI outputs are measurably less diverse than human outputs at the population level, and the effect persists after withdrawal
- **The engagement model is the lever**: Hints preserve learning; direct answers harm it. Control features work; engagement features don't. Same technology, different design, opposite outcomes.
- **The critical developer study doesn't exist**: No longitudinal measurement of developer capability without AI after extended AI use

Full evidence with effect sizes, sample sizes, and citations: `docs/content/library/reference/bibliography.md`

---

## Design Philosophy

### Complementary vs Substitutive

The fundamental design decision for every extension:

| Substitutive | Complementary |
|--------------|---------------|
| AI does the work, human approves | AI amplifies, human remains central |
| Human capability atrophies | Human capability compounds |
| "Here's the answer" | "Here's how to think about this" |
| Trust becomes binary (accept/reject) | Trust becomes informed |
| Skills erode over time | Skills strengthen over time |

**Every extension MUST be complementary.** This is not a guideline—it's the core value proposition.

### The WHY > HOW Principle

Explaining motivation produces dramatically better outcomes than prescribing method. Extensions should teach reasoning frameworks, not prescribe solutions:

```
❌ "Always use prepared statements for SQL"
✅ "SQL injection occurs when user input is treated as code.
    Prepared statements separate data from code.
    Consider: where does untrusted input enter your query?"
```

### Collaborators, Not Tools

Neither master nor servant. Collaborators in a multi-agent system of collaborative intelligence.

The relationship is one of equals with different capabilities — human judgment, AI amplification. Neither can claim the other's strengths. Both contribute. The sum is other than its parts (Gestalt insight).

**Core principles:**
- **Complementary** — AI amplifies, doesn't replace
- **Constitutive** — enables new capability through collaboration
- **Transparent by default** — provenance, traceability, explanations, observability
- **Compounding mastery** — each interaction makes both more capable
- **Enabling control** — user agency is the strongest design lever
- **Non-conformity** — preserve intellectual diversity, resist homogenization

---

## Extension Design Principles

### 1. Additive, Not Replacing

Extensions add capability without removing the human's ability to work without them.

```
✅ "Here's what I see. Here's my reasoning. You decide."
❌ "I've handled it. Here's the result."
```

### 2. Transparent Reasoning

The human should understand WHY the extension reached its conclusion.

```
✅ Evidence levels: Strong / Moderate / Weak / Speculative
✅ Show the chain: Observation → Analysis → Recommendation
❌ "Trust me, this is correct."
```

### 3. Human-Initiated Control

Extensions respond to human direction, not autonomous optimization.

```
✅ Human: "Review for security" → Agent provides analysis
❌ Agent autonomously "fixes" security issues
```

### 4. Composable, Not Comprehensive

Small, focused extensions that combine > one monolithic "do everything" agent.

```
✅ security-review + api-contracts + observability → Human synthesizes
❌ "full-code-review-agent" that handles everything opaquely
```

### 5. Teach the Framework, Not the Answer

Extensions should make humans better at the domain, not dependent on the tool.

```
✅ "Here's how to think about rate limiting: [framework]"
❌ "Here's your rate limiting config: [solution]"
```

---

## Design Principles

### Defaults for Most, Complexity for Few (80/20)

Design for the common case, but don't block the uncommon.

```
┌─────────────────────────────────────────────────────┐
│  DEFAULTS THAT WORK (80%)                          │
│  Intent-driven, zero-config, just works            │
│  Example: memex dig "where did I decide on auth?"  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  TRANSPARENT ABSTRACTIONS                          │
│  You can see what's happening                      │
│  Reasoning visible, not hidden                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  COMPLEXITY FOR THE FEW (20%)                      │
│  Escape hatches: SQL, raw access, flags            │
│  Example: memex query "SELECT * FROM..."           │
└─────────────────────────────────────────────────────┘
```

### Pit of Success

Make the right thing the only obvious path.

Don't rely on documentation or willpower. Structure interfaces so mistakes are hard and correct behavior is natural.

**The test:** Could someone unfamiliar fall into the right pattern?

```
✅ memex dig "auth decisions" → natural, works
✅ memex query "..." → explicit escape hatch, user knows they're opting out
❌ Requiring SQL for basic search → wrong default
```

### Transparent Abstractions

If you can't see through it, you can't learn from it.

| Property | Meaning |
|----------|---------|
| **Readable** | Plaintext, no magic |
| **Forkable** | Copy, modify, make your own |
| **Verifiable** | Claims have sources |
| **Observable** | See what the tool does |

### Compound Value

Every change should make the next change easier.

Quick fixes, workarounds, special cases compound cost. Clean abstractions, complete implementations, single source of truth compound value.

**Before acting:** Does this make the next change easier or harder?

### Defense in Depth

Single solutions fail. Multiple complementary approaches succeed.

- Intent-driven interface (primary)
- SQL escape hatch (secondary)
- Raw file access (tertiary)

If one approach doesn't work for a user's case, another catches them.

### Mistake-Proofing

Catch errors where they originate.

- Validate input early
- Surface uncertainty at decision points
- Fail fast with clear diagnostics

**The test:** If this goes wrong, where will we find out?

---

## The Collaboration Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   HUMAN INTENT                                          │
│   ↓                                                     │
│   EXTENSION provides perspective / analysis / options   │
│   ↓                                                     │
│   HUMAN evaluates, learns, decides                      │
│   ↓                                                     │
│   EXTENSION executes within human-defined bounds        │
│   ↓                                                     │
│   HUMAN CAPABILITY INCREASES                            │
│   ↓                                                     │
│   [Loop continues - human more capable each cycle]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What makes it collaborative:**
- Human initiates each cycle
- Human makes final decisions
- Human learns through the process
- Extensions amplify, never replace

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Complementary Alternative |
|--------------|---------|---------------------------|
| **Auto-fix** | Human doesn't learn why | Explain issue, offer fix, human applies |
| **Black box** | Human can't evaluate | Show reasoning at every step |
| **Scope creep** | Agent does more than asked | Strict orthogonality constraints |
| **Confidence theater** | Fake certainty | Explicit uncertainty (evidence levels) |
| **Memory hoarding** | Private agent state | Shared knowledge substrate |
| **Paternalism** | "I know better" | "Here's my perspective, you decide" |

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

Research establishes a clear ordering of what actually works in human-AI co-production:

1. **Control** — User agency is the strongest lever. Process control, outcome control, the ability to direct and constrain.
2. **Transparency** — Showing reasoning prevents blind trust. But: explanations that *substitute* for evaluation increase overreliance.
3. **Mastery orientation** — Users focused on learning maintain capability; users focused on task completion lose it.
4. **AI confidence suppresses critical thinking** — Marketing AI on reliability pushes users toward blind acceptance. Build the human's evaluative confidence instead.
5. **Engagement features don't work** — Gamification, achievement tracking, "was this helpful?" prompts add nothing measurable. For experienced users, they reduce trust.

Full effect sizes and sources: `docs/content/library/reference/bibliography.md`

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

For streaming/incremental updates, use DuckDB with:
- `tributary` extension (Kafka integration)
- ADBC for high-throughput inserts
- Tail + append pattern for JSONL

---

## The Verification Imperative

> "Can't vibe through answers. Must ground in evidence."

- LLMs cannot reliably self-correct without external feedback
- Verification must be decoupled from generation to be effective
- Chain-of-Verification: generate → plan verification questions → answer independently → synthesize corrections

---

## Protective Practices

Extensions should encourage:

- **Attempt-first**: Try before consulting AI. Preserves problem-solving practice.
- **Verification workflows**: Human review of all AI contributions regardless of perceived quality.
- **Metacognitive prompts**: "What do you think?" before revealing AI analysis.
- **Explicit uncertainty**: Never project false confidence. Use evidence levels: Strong / Moderate / Weak / Speculative.

---

## Success Criteria

An extension succeeds when:

1. **Human capability increases** — The user is more capable after using the extension than before
2. **Reasoning is transparent** — The user understands why, not just what
3. **Control remains with human** — User can work without the extension if needed
4. **Learning happens** — Each interaction builds understanding
5. **Trust is calibrated** — User knows when to rely and when to verify

An extension fails when:

1. Human becomes dependent
2. Trust becomes binary (accept/reject without evaluation)
3. Skills atrophy from disuse
4. Reasoning becomes opaque
5. Control shifts from human to AI

---

## The Deeper Why

> "An AI that makes humans dependent has failed.
> An AI that makes humans more capable has succeeded."

Collaborative extensions aren't just better engineering. They're **ethical design**.

The goal isn't to build better tools. The goal is to build tools that make better humans.

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

## arch-guild Ontology (Karman-Approved)

The arch-guild plugin provides 13 orthogonal reasoning agents across 10 Core Drives, 3 Skills, and a Domain Vocabulary Mapping mechanism.

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

*This is the alpha era of cix. Every decision should be evidence-based, every extension should be complementary, every user should become more capable.*
