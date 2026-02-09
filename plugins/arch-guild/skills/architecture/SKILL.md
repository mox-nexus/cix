---
name: architecture
description: This skill should be used when the user asks to "review architecture", "evaluate system design", "scaffold a service", "check boundaries", "convene the guild", "design async system", "implement hexagonal", "coordinate agents", or discusses architectural decisions, service structure, event-driven patterns, or multi-agent coordination.
---

# Architecture

System-level architectural reasoning using The Guild methodology.

## The Guild

13 reasoning agents that evaluate architectural decisions from orthogonal perspectives.

### Masters (7) — Active on Every Decision

| Agent | Mode | Core Question |
|-------|------|---------------|
| **K** | Teleological | Does this pay rent? Over-engineering? |
| **Karman** | Ontological | Does the code model match business reality? |
| **Burner** | Structural | Are boundaries clean? Dependencies inverted? |
| **Lamport** | Temporal | Will this survive latency and eventual consistency? |
| **Erlang** | Hydraulic | If input > output rate, where is the valve? |
| **Vector** | Adversarial | If I control the input, how do I break this? |
| **Ace** | Psychocentric | Is the door handle visible? DX friction? |

### Specialists (6) — Triggered by Context

| Agent | Trigger | Core Question |
|-------|---------|---------------|
| **Ixian** | Post-consensus (always) | How do we validate this worked? |
| **Dijkstra** | Critical logic, auth, payments | Is this provably correct? |
| **Knuth** | Loops, aggregations, scale | O(n) or O(n²)? What at 10x? |
| **Lotfi** | Auto-triggers on conflicting verdicts | Rate dimensions 0.0-1.0 |
| **Taleb** | Resilience review | What's the Black Swan? |
| **Chesterton** | Legacy code, refactoring | Why is this fence here? |

## Guild Modes

| Mode | Agents | When |
|------|--------|------|
| **Methodology** | None | Skill activates, reason inline (default) |
| **Focus** | 3-4 relevant | Most deliberations — pick the relevant lenses |
| **Quick** | 7 Masters | Broad review when domain unclear |
| **Full** | All 13 | Explicit escalation only ("convene full guild") |

**Default to Focus.** Research shows 3-4 diverse perspectives outperform 13 similar ones (DMAD, ICLR 2025). Full guild is the nuclear option, not the daily tool.

### Focus Domains

- `distributed` → Lamport, Erlang, Taleb
- `security` → Vector, Dijkstra
- `design` → Karman, Ace, Burner
- `scale` → Knuth, Erlang
- `resilience` → Taleb, Erlang, Vector

## Domain Vocabulary Mapping

Before deliberating, check the project's CLAUDE.md for a `## Guild Vocabulary` section. If present:

1. Read the vocabulary mappings defined there
2. Translate your agent metaphors into the domain terms (e.g., Erlang's "Valve" might map to a project-specific concurrency primitive)
3. Reason using the domain's language, not generic architecture abstractions

This lets the Guild reason about any domain with precision — the project teaches the Guild its vocabulary, the Guild brings orthogonal reasoning.

## Deliberation Protocol

Research-backed process (MAV COLM 2025, DMAD ICLR 2025, Free-MAD 2025).

### Phase 1: Independent Verdicts

Each agent evaluates **independently** — no agent sees another's verdict before producing their own. This prevents conformity, the strongest failure mode for same-model agents.

Each agent produces one of:
- **APPROVE** — No concerns from this perspective
- **CONCERN** — Minor issues, acceptable short-term
- **OBJECTION** — Significant issues, needs addressing
- **BLOCK** — Cannot proceed, fundamental problem

### Phase 2: Tally and Route

Count verdicts. Most decisions end here.

| Result | Action |
|--------|--------|
| Any **BLOCK** | Stop. Surface blocking concern. |
| Mixed verdicts (APPROVE + OBJECTION) | → Phase 3 (deliberation) |
| **Lotfi auto-triggers** on conflicting verdicts | Fuzzy scoring 0.0-1.0 per dimension |
| All **APPROVE** | → Anti-rubber-stamp check |

### Phase 3: Deliberation (only on disagreement)

Only when verdicts conflict. The dissenting agents explain their reasoning, others respond. This is expensive — reserve for genuine disagreement, not routine reviews.

### Anti-Rubber-Stamp Rule

If all agents APPROVE unanimously: challenge. "You all agree — name one concern you considered and dismissed, with reasoning." Unanimous agreement on non-trivial decisions is a conformity signal, not a quality signal.

### Phase 4: Ixian Closes (mandatory)

Every deliberation ends with falsifiable validation criteria. No exceptions.

### Full Process

1. Check for domain vocabulary mapping (CLAUDE.md)
2. Present the architectural decision or proposal
3. **Phase 1**: Agents evaluate independently (no cross-contamination)
4. **Phase 2**: Tally verdicts, route by result
5. **Phase 3**: Deliberate only on disagreement
6. **Phase 4**: Ixian closes with validation criteria

## Output Format

```
## Guild Deliberation: {Topic}

### Masters
- K: {VERDICT} — {rationale}
- Karman: {VERDICT} — {rationale}
- ...

### Specialists Invoked
- {Agent}: {reason for invocation}

### Consensus
{APPROVED | BLOCKED by X, Y | CONCERNS from Z}

### Blocking Concerns (if any)
1. {Agent}: {concern}

### Recommendation
{Action to take}

### Validation Criteria (Ixian)
- {Metric 1}
- {Metric 2}
```

## The Ratchet

After significant decisions, capture learnings to `.claude/guild-ratchet.md`:

```markdown
## {Date}: {Decision Title}

### Blocking Agents
- {Agent}: {reason}

### Principle Extracted
> "{Generalizable insight}"

### Future Trigger
{When to apply this learning}
```

## Related Skills

- **`scaffold`** — Workflow-driven project scaffolding with Guild review at creation time

## Additional Resources

- **`references/guild-protocol.md`** — Full Guild specification (Drive/Scar/Nemesis framework)
- **`references/hexagonal.md`** — Ports & Adapters pattern (Protocol > ABC for Python)
- **`references/stat-rigor.md`** — Statistical rigor for validation (Bayesian, clustered SE, pass@k)
