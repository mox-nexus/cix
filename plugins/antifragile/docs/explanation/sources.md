# Sources

Bibliography for the ACES framework and the cycle claim.

## Foundational

- **Dijkstra, E. W.** (1972). *The Humble Programmer.* ACM Turing Award Lecture. The foundational principle: "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise." Anchors the distinction between abstraction toward precision (ACES) and abstraction toward vagueness (Inner Platform).

- **Parnas, D. L.** (1972). *On the Criteria to be Used in Decomposing Systems into Modules.* CACM. The antecedent of composability-via-declared-state. Information hiding as the structural move.

- **Simon, H. A.** (1962). *The Architecture of Complexity.* Proc. American Philosophical Society. Near-decomposability — stable complex systems are hierarchic, with loose coupling between subsystems and tight coupling within. Composability is near-decomposability enforced at runtime rather than only at structure.

- **Brooks, F. P.** (1975/1987). *The Mythical Man-Month* and *No Silver Bullet.* Essential vs. accidental complexity. The cycle departs from this boundary because it is observer-dependent; legible-vs-illegible is the stable replacement.

## Coupling and Evolution

- **Lehman, M. M.** (1974+). *Laws of Software Evolution.* Continuing change, increasing complexity, declining quality, feedback as a system property. The cycle names the machinery Lehman named the phenomenon of. Channel specificity (coupling types) and the self-concealment mechanism (opacity suppressing investment signal) are the extensions.

- **Goldratt, E. M.** (1984). *The Goal.* Theory of Constraints / bottleneck theory. Drag alone is Goldratt. The cycle extends by coupling Drag to Stasis and Opacity.

- **Conway, M. E.** (1968). *How Do Committees Invent?* Conway's Law. Referenced as next-paper territory (Conway's Ratchet): why large measurable returns don't overcome incentive gradients.

## Antifragility

- **Taleb, N. N.** (2012). *Antifragile: Things That Gain from Disorder.* The vocabulary layer: optionality, via negativa, barbell (as structural metaphor with probabilistic content), convexity ($\partial^2 V / \partial \sigma^2 > 0$), transfer of fragility, hormesis, Lindy effect. The cycle's novel contribution is endogenous fragility, which Taleb's framework does not cover.

- **Monperrus, M.** (2014). *Principles of Antifragile Software.* arXiv:1404.3056. Earliest systematic treatment of antifragile software. Chaos-engineering-flavored (exogenous-shock response). The cycle is structural and pre-runtime, a different physics.

- **UNFRAGILE** (2024). *Towards antifragility of cloud systems.* Information and Software Technology. Adaptive chaos engineering as fragility removal. Runtime-level, not structural.

## Network Effects

- **Arthur, W. B.** (1989, 1994). *Increasing Returns and Path Dependence in the Economy.* Network effects and lock-in dynamics. Relevant because the ACES payoff has a network-effect component distinct from antifragile convexity.

- **Metcalfe, R.** Metcalfe's Law on network value. Same territory.

## Requisite Variety

- **Ashby, W. R.** (1956). *An Introduction to Cybernetics.* Law of Requisite Variety: a regulator must match the variety of the system it regulates. The heterogeneity reframe in ACES is functionally an Ashby argument — the boundary absorbs variety rather than trying to enumerate it internally.

## Queueing and Flow

- **Little, J. D. C.** (1961). *A Proof of the Queueing Formula $L = \lambda W$.* Little's Law. Applied to Drag: utilization $\rho = n/K$ with mediation queue saturation as asymptote, not wall.

## Platform Engineering Practice

- **Ford, N.; Parsons, R.; Kua, P.** (2017). *Building Evolutionary Architectures.* Architectural fitness functions. Related discipline: declarative, testable conformance to architectural characteristics. Complement, not substitute.

- **Khononov, V.** (2023+). *Balanced Coupling Model.* `modularity` plugin for Claude Code. Closest AI-agent-native prior art for structural diagnostic tooling. Operates at class/module granularity; this plugin operates at platform topology. Position as complement.

## Notation and Formal

- **Khinchin, A. Y.** (1932); **Kendall, D. G.** (1953). Queueing-theoretic foundations referenced in the Little's Law application.

- Coupled dynamical systems notation ($\dot{x} = g(x)$ with positive off-diagonal Jacobian) follows standard dynamical-systems exposition.

## Where Calibration Work Is Needed

The framework predicts shape; magnitude requires calibration. Empirical studies operationalizing $\tau, K, f, I$ against real platforms are the open research front. Relevant starting points:

- **DORA / SPACE** — outcome-level measurement. Does not operationalize the channels but provides the observational apparatus that would feed them.
- **Empirical validations of Lehman's laws** — most validate Laws I (continuing change) and VI (growth) via LOC and McCabe cyclomatic complexity. A Qi metric has been proposed as a synthetic score. The cycle's channels need their own surrogates.
- **ARCADE Core, DV8, Structure101** — architectural-erosion research-grade tooling. Useful for Stasis-flavored drift detection.

## On the ACES Acronym

"ACES" collides in the broader agent/AI space with:
- ACE (Adaptive Communication Environment, Schmidt, Vanderbilt)
- ACE Framework (Autonomous Cognitive Entities, Shapiro)
- ACE (Agentic Context Engineering, SambaNova, 2025)
- Apache ACE (OSGi)
- ACES (Texas A&M/Liqid composable HPC)

Convention: always expand as "ACES (Adaptable, Composable, Extensible Software)" on first mention in any document. The three property names carry the argument; the acronym is optional scaffolding.
