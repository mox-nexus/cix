---
name: aces
description: Use when the user asks to "review this architecture", "review our platform", "evaluate this design", "is this a good boundary", "is this over-engineered", "are we building an Inner Platform", "why is our platform slow to change", "our platform team is a bottleneck", "migrations take quarters", "we have N versions of the same thing", "should we migrate off proprietary X", "hexagonal architecture review", "ports and adapters", "anti-corruption layer", "protocol adapter", "Pipeline Envelope", "is this the right abstraction", "multi-tenancy concerns", "run an antifragile review", "ACES review", "boundary test". Also triggers on mentions of Stasis / Drag / Opacity, the Coupled Monolith / Fragmented Estate / SDK Frontier archetypes, or explicit requests to apply the ACES (Adaptable, Composable, Extensible Software) framework to architecture, security, cost, data, or agent systems.
---

# ACES: Adaptable, Composable, Extensible Software

Diagnose endogenous structural fragility. Apply the inversion. The framework for platform systems that decay through their own operation rather than through external shocks.

## What This Adds

Claude already knows SOLID, hexagonal architecture, ports and adapters, the strangler fig, the adapter pattern, and general "good architecture" heuristics. This skill does not reteach those. It adds:

- A **three-channel cycle** (Stasis → Drag → Opacity → Stasis) that compounds multiplicatively and hides its own cost from the people who would fund the fix.
- A **diagnostic protocol** — three yes/no questions that map symptoms to coupling types.
- The **Boundary Test** — arithmetic discrimination between a real boundary and an Inner Platform.
- The **Pipeline Envelope** pattern, with an explicit degeneration condition.
- A **mapping from ACES properties to hexagonal architecture mechanisms** so that "ports and adapters" becomes testable, not aspirational.

This skill is **prescriptive**: it tells you which property applies to which channel through which mechanism.

## This Skill Composes, It Does Not Overwrite

This is a reasoning scaffold, not a replacement for other review skills. Use it alongside:

- **`guild-arch:architecture`** — multi-perspective deliberation (Taleb, Dijkstra, Burner, Lamport, Vector, etc.). ACES is one lens among many. When the user wants multi-lens review, route there first and invoke ACES as one of the lenses.
- **`guild-arch:operations`** — production readiness, failure modes, chaos. ACES complements (structural fragility) but does not substitute (runtime resilience).
- **`guild-arch:trust-boundaries`** — the architectural half of security review. ACES covers correctness boundaries; trust-boundaries covers trust boundaries. They compose: ACES tells you whether the structure holds; trust-boundaries tells you whether the trust model holds.
- **`guild-arch:design`** — API design, abstractions, DX. ACES is platform-topology scope; design is interface-level scope.
- **`modularity`** (external Claude Code plugin by Vladik Khononov) — class/module-level coupling analysis via the Balanced Coupling Model. ACES sits above it at platform topology. Coexist.
- **`craft-research:verifying`** — claim verification against sources. Use for calibration evidence when ACES predictions are disputed, not for the framework itself.

Do not treat an ACES review as a replacement for any of the above. An architectural review that wants breadth should also invoke `guild-arch:architecture`. A security review that wants depth should also invoke `guild-arch:trust-boundaries`. The right answer is usually **both**.

## The Cycle

Three channels, each a distinct kind of coupling.

| Channel | Coupling type | What it looks like |
|---|---|---|
| **Stasis** | System-to-terrain | Proprietary surface drifts from industry standards. Switching cost compounds silently. |
| **Drag** | Contributor-to-platform | Platform team becomes serialization point for every capability change. Backlog is topology, not velocity. |
| **Opacity** | Behavior-to-integration | Composed behavior emerges from runtime interaction, not declaration. The system cannot describe itself. |

The channels feed each other. The third channel — Opacity — structurally prevents the first two from being addressed because it hides cost from the funding decision-maker. Deep treatment: `references/cycle.md`.

## The Diagnostic Protocol

Three questions identify which channel is active.

| Channel | Diagnostic question |
|---|---|
| Stasis | Can you change the runtime without rewriting the core? |
| Drag | Can a team contribute capability without platform-team mediation? |
| Opacity | Can you predict composed behavior from declared description? |

If the answer to any question is no, you are in that channel. If two are no, the cycle is likely running. If all three are no, the cycle is compounding. These are operational thresholds on continuous variables, not ontological categories.

## The Inversion: ACES Mapped to Hexagonal Architecture

ACES is the articulation of what hex arch is solving for at platform scale. Ports-and-adapters is the concrete dependency-direction pattern the three properties rely on.

| Property | Breaks | Hex role | Mechanism | Dependency direction |
|---|---|---|---|---|
| **Adaptability** | Stasis | Primary port | Wire protocol (e.g., xDS, OpenTelemetry OTLP, gRPC schemas) | Runtimes are adapters against the port. Runtimes depend on the protocol. The protocol does not depend on any runtime. |
| **Extensibility** | Drag | Secondary port with typed config | Typed extension schema (protobuf, JSON Schema) | Extensions are adapters. Extensions depend on the schema. The platform does not depend on any individual extension. |
| **Composability** | Opacity | State contract (declared access, declared order) | State contract (not shared mutable heap) | Components are adapters against the contract. Components depend on the contract, not on each other. |

Hex arch concepts that map into ACES:

- **Ports** = the ACES boundary interfaces (protocol, schema, state contract).
- **Adapters** = runtimes, extensions, and components that plug into the ports.
- **Anti-corruption layer** = the boundary that keeps bounded contexts from leaking into each other. Passes the Boundary Test by construction if it narrows the interface.
- **Domain core has zero external imports** = the protocol-as-port doesn't know about the adapters.

Simon (1962) named the underlying design principle as near-decomposability. Composability is near-decomposability enforced at runtime rather than only at structure. Deep treatment: `references/inversion.md`.

## The Boundary Test

If the boundary reduces total integration surface, it is a boundary. If it increases total integration surface, it is an Inner Platform.

Integration surface is countable: distinct interfaces crossed per capability-runtime pairing. Under full coupling, $N$ capabilities across $M$ runtimes cost $NM$. Under protocol mediation, the cost is $N + M + B$ where $B$ is the bounded one-time boundary construction cost. The test is arithmetic.

Deep treatment: `references/boundary-test.md`.

## Running an ACES Review

When the user asks for a review (platform, design, proposal), execute this workflow:

1. **Parse the target.** What is being reviewed (platform, design document, code, proposal, archetype described in prose).
2. **Decide the lens(es).** If the target is primarily an architecture concern, invoke the `antifragile-arch` agent. If the target involves trust, auth, PII, or information flow, invoke `antifragile-sec` (in addition to `antifragile-arch` if architecture is also present). If the target wants multi-perspective deliberation beyond ACES, delegate to `guild-arch:architecture` first and invoke ACES as one of its lenses.
3. **Run the diagnostic protocol.** Map observable signals (queue depth, KTLO ratio, incident character, cost attribution, auth surface, policy-review bottleneck, emergent attack paths) to the three channels.
4. **Run the Boundary Test** if the review includes a proposed boundary or abstraction.
5. **Flag correctness-vs-trust** when security is involved. A schema conformance check is not an adversarial-input check. A state contract that permits `reads PII + writes logs` compositions leaks cleanly unless information-flow typing is added.
6. **Synthesize.** Return a structured review with per-lens verdicts, channel(s) active, recommended inversion mechanisms, boundary-test outcome, scope limits (magnitude is calibration-dependent, distributed observation is abstracted over, organizational dynamics are deferred to Conway's Ratchet), and federation pointers for lenses this skill does not cover.

The per-agent output format is documented in their agent files. The consolidated review synthesis lives in the calling Claude's response.

## Running the Boundary Test in Isolation

When the user asks specifically for a boundary test ("is this a boundary or an Inner Platform?"), skip the diagnostic protocol and execute directly:

1. Enumerate the proposal's integration surface.
2. Compute $NM$ under coupling vs $N + M + B$ under mediation.
3. Check dependency direction — does the boundary depend on its callers, or do callers depend on it?
4. Check protocol purity — does the boundary surface stay runtime-agnostic, or accrete runtime-specific semantics?
5. Check thinness — is the boundary narrower than what it replaced?
6. If the proposal resembles a Pipeline Envelope, name it as transitional and evaluate the degeneration condition.
7. Return a verdict: **BOUNDARY**, **TRANSITIONAL BOUNDARY**, or **INNER PLATFORM**, with arithmetic evidence.

## Correctness Is Not Trust

The three mechanisms validate conformance, composition, and declaration. They do not validate adversarial input resistance, information flow, or authorization. Schema conformance is $O(1)$; adversarial-input check is not. A state contract that permits "reads PII" and "writes logs" to compose cleanly will leak cleanly. Structural boundaries are necessary for trust but not sufficient. Trust boundaries live on top of correctness boundaries, built with different instruments (authentication, authorization, information-flow typing, rate limits, abuse monitoring).

For trust-architecture review specifically, invoke `antifragile-sec` (the security mirror of ACES), then compose with `guild-arch:trust-boundaries` for the full architectural security posture.

Do not conflate correctness and trust when applying ACES.

## Domain Applications

The framework generalizes across domains. The channels and inversions have the same structure; the mechanisms and their domain knowledge vary.

| Domain | Stasis example | Drag example | Opacity example | Inversion mechanisms |
|---|---|---|---|---|
| **Architecture** | Proprietary control plane | Platform-team bottleneck | Shared-process emergent behavior | xDS, typed filter config, declared composition |
| **Security** | Proprietary auth surface | Security-team review bottleneck | Emergent attack surface | Standard trust protocols (mTLS, SPIFFE, OAuth2), policy-as-code, information-flow typing |
| **Cost** | Proprietary vendor lock-in | Platform team consumed by KTLO | Cost distributed across ledgers | Open billing formats (FOCUS, OpenCost), self-service chargeback, declared cost attribution |
| **Data** | Proprietary warehouse format | Central data team as bottleneck | Emergent schema drift | Open table formats (Iceberg, Delta), data mesh with contracts, schema registry |
| **Agent systems** | SDK fragmentation | Orchestration as serialization | Emergent tool composition | Agent protocols (MCP, A2A), tool schemas, declared capability composition |

Specialized agents apply the framework per domain. `antifragile-arch` and `antifragile-sec` are shipped in this plugin; `antifragile-cost`, `antifragile-data`, `antifragile-agents` are planned extensions that will conform to the same skill interface.

## Calibration Is Open

The skill predicts *shape* (superlinear in time, multiplicative in the number of capabilities and runtimes, positive feedback across channels). It does not predict *magnitude*. Reported ratios between coupled and decoupled cost for an identical capability tend to fall in the range of 40 to 100 times for mature Coupled Monolith instances, but these magnitudes are illustrative, not derived. Magnitude depends on the system's specific parameters ($\tau$, $K$, $f$, $I$).

Quantitative mode and measurement surrogates: `references/cost-model.md`.

## Output Format

For a full review, return:

```
Target: <one sentence>
Archetype: <Coupled Monolith | Fragmented Estate | SDK Frontier | other | none>
Channels active: <Stasis | Drag | Opacity | combinations>
Coupling type(s): <system-to-terrain | contributor-to-platform | behavior-to-integration>
Recommended inversion: <Adaptability | Composability | Extensibility>
Mechanism: <wire protocol | typed schema | state contract>
Boundary Test: <pass | fail | not applicable>, <NM vs N+M+B>
Security cut: <applicable | not applicable; correctness-vs-trust notes>
Scope limits: magnitude illustrative; distributed observation abstracted; Conway's Ratchet deferred
Federation pointers: <guild-arch:architecture for multi-lens; trust-boundaries for security depth; modularity for class-level coupling>
Next actions: <concrete>
```

For a standalone Boundary Test, return:

```
Proposal: <one line>
Integration surface: NM = <count>; mediated = N + M + B = <count>
Dependency direction: <runtimes depend on boundary | boundary depends on runtimes | mixed>
Protocol purity: <runtime-agnostic | accreting runtime specifics>
Thinness: <thinner | same | thicker> than replaced
Pipeline Envelope applicable: <yes | no>
Degeneration risk: <low | medium | high | active>
Verdict: <BOUNDARY | TRANSITIONAL BOUNDARY | INNER PLATFORM>
```

## Additional Resources

- `references/cycle.md` — The three channels, coupling types, coupled dynamics, Lehman lineage
- `references/inversion.md` — ACES mechanisms, dependency directions, hex arch mapping, Taleb vocabulary, heterogeneity reframe
- `references/boundary-test.md` — Arithmetic test, Pipeline Envelope pattern, degeneration conditions, SOLID/Unix non-substitutes
- `references/cost-model.md` — Cost functions, coupled dynamics, $NM \to N + M + B$ geometry, measurement surrogates, falsification conditions

## Agents in This Plugin

- `antifragile-arch` — architecture lens. Diagnoses platforms, runs the Boundary Test, recommends inversions. Composes with `guild-arch:architecture`.
- `antifragile-sec` — security lens. Applies the security mirror of the cycle, distinguishes correctness from trust, names endogenous security fragility. Composes with `guild-arch:trust-boundaries`.
