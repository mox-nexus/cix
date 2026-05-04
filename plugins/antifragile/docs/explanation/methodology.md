# Methodology

Why this plugin exists and what it encodes.

## The Thesis

Platforms decay through an endogenous cycle that hides its own cost from the people who would fund the fix. The cycle has three channels (Stasis, Drag, Opacity) and a specific self-reinforcing structure. ACES — Adaptable, Composable, Extensible Software — is the structural inversion, with each property breaking one channel through a specific architectural mechanism.

This plugin operationalizes that claim. It is prescriptive: it tells you which property to apply to which channel through which mechanism with which dependency direction.

## What's Novel

The cycle's novel contribution is **positive-feedback structural coupling with self-concealment**. Each of the three channels is recognizable individually under existing vocabulary:

- **Stasis** is related to vendor lock-in (recognized since the 1970s) and Lehman's laws of software evolution (1974+).
- **Drag** is related to Goldratt's bottleneck theory.
- **Opacity** is related to Brooks-Parnas illegibility and Simon's near-decomposability violations.

The contribution is not these names. It is the claim that they form a directed cycle with compounding dynamics, and that Opacity specifically hides the cost of the other two from the people who would fund the fix. This is different from prior frameworks in two specific ways:

1. **Endogenous, not exogenous.** Taleb modeled fragility as a system's response to external shocks. The cycle models systems that manufacture their own internal volatility through their own operation.
2. **Coupled dynamics, not taxonomy.** The channels feed each other multiplicatively. The Jacobian has positive off-diagonal entries. That is a specific dynamical claim, not a categorization.

The inversion is also not new as a set of principles. What is new is the claim that the three ACES properties map to the three channels with mechanical specificity (not generic aspiration), and that the inversion produces two distinct payoff shapes: network-effect (Arthur, Metcalfe) under stable conditions and antifragile (Taleb's $\partial^2 V / \partial \sigma^2 > 0$) under volatility.

## Why a Plugin

The framework is useful as prose. It is more useful as an instrument. A plugin makes the diagnostic protocol runnable, the Boundary Test mechanical, and the inversion mechanism recommendations specific to domain.

The plugin is ACES-shaped by construction:

- The `aces` skill is the **protocol** (Adaptability): any agent that speaks it participates. Runtimes (domain agents) depend on the skill, not the other way around.
- Domain agents (`antifragile-arch`, `antifragile-sec`) are **extensions** against the skill's schema (Extensibility): adding `antifragile-cost`, `antifragile-data`, `antifragile-agents` is $O(1)$ — conform to the skill's interface, bring domain knowledge, compose.
- The command surface declares **composition** (Composability): users can compose domain lenses without the plugin knowing they will.

The plugin passes its own Boundary Test. Integration surface is the skill. Extensions are the domain agents. The platform (plugin author) does not review each domain agent's domain knowledge; it validates that each agent conforms to the skill.

## What the Plugin Does Not Do

Several things are deliberately out of scope.

**Magnitude prediction.** The framework predicts shape — signs, feedback structure, multiplicative gap in $(N, M)$. It does not predict magnitude. Reported ratios cluster in the 40-100× range for mature Coupled Monolith instances, but these magnitudes are illustrative, not derived. A companion paper treats the calibration apparatus.

**Multi-perspective deliberation.** The `guild-arch` plugin does that. This plugin is prescriptive. Call guild-arch when you want orthogonal lenses; call antifragile when you want ACES specifically.

**Class-level coupling analysis.** Tools like `modularity` (Vladik Khononov's Balanced Coupling plugin), SonarQube, Structure101, NDepend, Designite do that. This plugin operates at platform topology, not class topology. Coexist with those tools; do not duplicate.

**Organizational dynamics.** Why does a 40:1 return not overcome incentive gradients? That is Conway's Ratchet, a separate piece with different physics. Physics first, economics second.

**Adversarial security.** The `antifragile-sec` agent diagnoses *endogenous security fragility* — the cycle's security mirror. It does not replace threat modeling, compliance frameworks, or cryptography-specialist review. Correctness boundaries are necessary for trust but not sufficient.

## Federation Pattern

| Need | Plugin |
|---|---|
| Multi-perspective architectural deliberation | `guild-arch:architecture`, `guild-arch:operations` |
| Research scope, claim verification, source auditing | `craft-research:eliciting`, `craft-research:verifying`, `craft-research:auditing` |
| Visualization of the cycle or a proposed inversion | `craft-rhetoric:figures` |
| Plugin quality evaluation (ACES-compliance checks on plugins) | `craft-extensions:evaluator` |
| Class-level coupling analysis | `modularity` (external) |

## Versioning and Stability

This plugin is at 0.1.0. Scope for 0.1.x: `aces` skill + `antifragile-arch` + `antifragile-sec` + router command. Scope for 0.2.x and beyond: additional domain agents (cost, data, agent systems), hooks (optional session-start context), calibration utilities.

The `aces` skill's interface is the stability contract. Domain agents will be added or refined without breaking the skill. Breaking changes to the skill trigger a minor version bump.

## What "Polished" Means Here

Polished means:
- Every agent and skill is triggerable by specific user phrasings, not by marketing.
- Every claim that would be caught by a rigorous reader is already qualified (magnitude vs. shape, correctness vs. trust, coupled vs. superposed).
- Every domain agent has an orthogonality lock naming what it cannot discuss.
- Every inversion recommendation carries its dependency direction explicitly.
- The plugin federates with existing CIX plugins rather than duplicating them.
- The thesis does not drift across files.
