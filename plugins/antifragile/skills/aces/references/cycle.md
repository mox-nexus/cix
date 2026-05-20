# The Cycle

Three coupling channels feeding each other. The engine that converts legible costs into illegible costs.

## The Three Channels

### Stasis — System-to-terrain coupling

A platform's runtime and the surrounding ecosystem drift apart on independent clocks. A proprietary control plane accumulates behaviors the industry standardizes elsewhere. Expertise on the proprietary surface depreciates on someone else's release schedule. The switching cost rises without anyone deciding to raise it.

**Diagnostic question**: Can you change the runtime without rewriting the core?

**Observable signals**:
- Proprietary API surface that lacks equivalents in ecosystem standards
- Engineering hires require ramp on technology only you use
- Every ecosystem release is a port, not a pull
- "Migration" is perpetually six months away

### Drag — Contributor-to-platform coupling

Shared execution means every capability change routes through the platform team. The team becomes a serialization point not by choice but by architecture. The backlog looks like a velocity problem. It is a topology problem.

**Diagnostic question**: Can a team contribute capability without platform-team mediation?

**Observable signals**:
- Review queue grows faster than review capacity
- Platform team at or near 100% KTLO
- Every "small change" requires the platform team's bandwidth
- Contributors build workarounds to bypass the queue
- Shadow deployments appear

### Opacity — Behavior-to-integration coupling

Composed behavior emerges from runtime interaction rather than declaration. The system cannot predict itself from its configuration. You have to run it to know what it does. Cost information distributes across ledgers, so no single view shows the full price.

**Diagnostic question**: Can you predict composed behavior from declared description?

**Observable signals**:
- Incidents require reconstructing interactions across multiple components
- Cost appears on several budget lines, attributable to none
- Behavior at position $p$ depends on what positions 1 through $p-1$ did
- Debugging is observation, not prediction
- The architecture looks healthy because silence reads as health

## Coupling Dynamics

The channels are coupled, not superposed. Each raises the inputs of the next.

- Stasis → Drag. Proprietary surface diverges from ecosystem; maintenance consumes bandwidth that could have funded migration. The platform team's capacity erodes because the platform they maintain is less and less like anything else.
- Drag → Opacity. Blocked teams route around the bottleneck. Shadow deployments, undocumented sidecars, vendor hairpins accumulate as undeclared behavior. The architecture's actual behavior diverges from its declared behavior.
- Opacity → Stasis. The investment signal is absent. Without a legible cost attributable to the architecture, the organization funds the symptoms (more headcount, more process) rather than the cause (the boundary). Stasis deepens.

Formally, the system is $\dot{x} = g(x)$ where $x = (C_\sigma, C_\delta, C_\omega)$ — the three channel costs — and $g$ has positive off-diagonal entries in its Jacobian. Each channel's rate of change depends positively on the others. The result is positive-feedback dynamics. Total cost compounds rather than sums. This is a modeling commitment: the cycle's runaway character follows from the coupling structure, not from the per-channel shapes alone.

## The Engine: Legible → Illegible

The cycle converts legible costs into illegible costs. "Legible" means the cost is visible to the decision-maker in a form they can act on. "Illegible" means the cost exists, affects decisions, but is unavailable to the decision-making process.

Essential-versus-accidental complexity (Brooks) describes this territory but sits on an observer-dependent boundary. What is essential to the business may be accidental to the problem; what is essential to the implementation may be accidental to the architecture. The boundary moves with the observer.

Legible-versus-illegible is stable given a fixed observer. In platform contexts the observer is typically the organization that funds platform investment. For that observer, a cost on a single legible line is actionable; a cost distributed across five ledgers is not.

## Prior Art

- **Lehman's laws of software evolution (1974)** — continuing change, increasing complexity, declining quality, feedback as a system property. Lehman named the phenomenon. The cycle names the machinery, with channel specificity (coupling types, not aggregate complexity) and the self-concealment mechanism (opacity suppressing the investment signal).
- **Parnas (1972) on information hiding** — the antecedent of composability-via-declared-state.
- **Simon's Architecture of Complexity (1962)** — near-decomposability. Composability is near-decomposability enforced at runtime rather than only at structure.
- **Goldratt** — bottleneck theory. Drag alone is Goldratt; the contribution is the coupling with Stasis and Opacity.
- **Brooks and Parnas on illegibility** — Opacity alone is illegibility; the contribution is its causal coupling with Stasis and Drag.

## Entry Channels and Archetypes

Platforms enter the cycle through different channels. The entry channel no longer matters once inside.

- **Coupled Monolith** — drag-first entry. Extensions share a runtime; the platform team serializes everything. Stasis solidifies around the queue.
- **Fragmented Estate** — opacity-first entry. Multiple gateways accumulated through organic growth. No single view of routing topology. Costs distributed across teams and budgets.
- **SDK Frontier** — stasis-first entry. Framework ecosystem churns quarterly. Switching cost accumulates from day one.

Three archetypes. Three entry points. Same cycle. This is why the contribution is the cycle, not the taxonomy.

## Exogenous vs. Endogenous

Taleb models exogenous volatility: external shocks stress systems, fragile ones break. The cycle models endogenous volatility: information systems manufacture their own internal volatility through their own operation. The monolith is not degraded by a market event or a change in requirements. It degrades because its own architecture produces drag and opacity as natural byproducts.

This is the piece's core differentiation. Different physics, same substrate.
