# antifragile

Diagnose endogenous fragility in platform systems and apply the ACES (Adaptable, Composable, Extensible Software) inversion.

## What This Plugin Does

Platforms decay through a self-reinforcing cycle (Stasis → Drag → Opacity → Stasis) that hides its own cost from the people who would fund the fix. ACES is the structural inversion — three properties, each breaking one channel through a specific architectural mechanism with a specific dependency direction.

This plugin operationalizes the framework. It is prescriptive: it tells you which property applies to which channel through which mechanism.

## When to Use

```
"Diagnose this platform's fragility"                 → antifragile-arch
"Is this abstraction a boundary or an Inner Platform?" → antifragile-arch
"Review our auth architecture for the cycle"         → antifragile-sec
"Apply ACES to this security decision"               → antifragile-sec
"Which channel is active here?"                      → aces skill
"Run the Boundary Test on this proposal"             → aces skill
```

## Components

### Skills

| Skill | Use When |
|-------|----------|
| `aces` | Any time the framework applies — the cycle, the inversion, the Boundary Test, the cost model |

### Agents

| Agent | Domain |
|-------|--------|
| `antifragile-arch` | System architecture — diagnose platforms against the three-channel cycle, apply ACES mechanisms |
| `antifragile-sec` | Security / trust architecture — the security mirror of the cycle, policy-as-code, information-flow typing |

### Commands

| Command | Purpose |
|---------|---------|
| `/antifragile` | Route to the right lens (arch, sec) based on the user's context |

## The Framework in One Page

### The three channels

| Channel | Coupling type | Diagnostic question |
|---|---|---|
| **Stasis** | System-to-terrain | Can you change the runtime without rewriting the core? |
| **Drag** | Contributor-to-platform | Can a team contribute capability without platform-team mediation? |
| **Opacity** | Behavior-to-integration | Can you predict composed behavior from declared description? |

### The inversion

| Property | Breaks | Mechanism | Dependency direction |
|---|---|---|---|
| **Adaptability** | Stasis | Wire protocol (e.g., xDS) | Runtimes depend on the protocol |
| **Extensibility** | Drag | Typed schema | Extensions depend on the schema |
| **Composability** | Opacity | State contract | Components depend on the contract, not on each other |

### The Boundary Test

If the boundary reduces total integration surface ($NM \to N + M + B$), it is a boundary. If it increases, it is an Inner Platform. The test is arithmetic.

### Correctness is not trust

The three mechanisms validate conformance, composition, and declaration. They do not validate adversarial input resistance, information flow, or authorization. Trust boundaries live on top of correctness boundaries, built with different instruments. `antifragile-sec` owns this distinction.

## Federation with Other Plugins

| When you want | Use instead / alongside |
|---|---|
| Multi-perspective architectural deliberation | `guild-arch:architecture` |
| Production-readiness review | `guild-arch:operations` |
| Class-level coupling metrics | `modularity` (external) or similar |
| Claim verification | `craft-research:verifying` |
| Visualization of the cycle or inversion | `craft-rhetoric:figures` |

ACES is prescriptive. guild-arch is deliberative. They compose; they do not overlap.

## Scope

**In scope (v0.1):**
- The `aces` skill with the cycle, inversion, Boundary Test, and cost-model references
- `antifragile-arch` for architecture
- `antifragile-sec` for security
- Router command

**Planned (v0.2+):**
- `antifragile-cost` — platform economics lens
- `antifragile-data` — data architecture lens
- `antifragile-agents` — agent-systems lens (SDK fragmentation, orchestration, tool composition)

**Out of scope:**
- Magnitude prediction (the framework predicts shape; calibration is a separate apparatus)
- Multi-perspective deliberation (see `guild-arch`)
- Class-level coupling analysis (see `modularity` or static-analysis tools)
- Organizational dynamics (see Conway's Ratchet, a separate piece)
- Adversarial security review (see threat-modeling tools; `antifragile-sec` covers endogenous security fragility, not exogenous threats)

## Documentation

- `skills/aces/SKILL.md` — the framework, triggers, federation, output format
- `skills/aces/references/cycle.md` — the three channels, coupling types, coupled dynamics
- `skills/aces/references/inversion.md` — ACES mechanisms, dependency directions, Taleb mapping
- `skills/aces/references/boundary-test.md` — arithmetic test, Pipeline Envelope, degeneration conditions
- `skills/aces/references/cost-model.md` — cost functions, coupled dynamics, $NM \to N + M + B$
- `docs/explanation/methodology.md` — what's novel, what the plugin does not do, federation pattern
- `docs/explanation/sources.md` — bibliography (Dijkstra, Parnas, Simon, Brooks, Lehman, Goldratt, Conway, Taleb, Arthur, Metcalfe, Ashby, Little)

## License

MIT
