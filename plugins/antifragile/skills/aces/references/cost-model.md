# Cost Model

The quantitative treatment of the cycle. Shapes, not magnitudes.

## Notation

- $n$ — effective extension count (plugins, filters, processors). Appears in drag and opacity.
- $\tau$ — ecosystem-divergence rate.
- $K$ — platform-team capacity in extension-equivalents.
- $\rho = n/K$ — utilization.
- $u$ — undeclared-interaction count. Bounded by $\binom{n}{2} \in O(n^2)$.
- $P$ — platform-team cost.
- $I$ — cost per incident-hour.
- $f$ — incident frequency.
- $S_0$ — initial switching cost.
- $B$ — bounded one-time boundary construction cost.

## Distributed Caveat

The model assumes a logical observer with a consistent view of $n$, $\tau$, $f$, $I$. Real platforms are distributed; these quantities are eventually consistent at best. Little's Law applies per-queue, not globally. The cycle can skip iterations under partition because cost signal and investment signal propagate at network speed, not at thought speed. The framing is centralized-as-abstraction.

## Three Cost Functions

### Stasis cost

$$C_\sigma(t) = S_0 \cdot e^{\tau t}$$

Switching cost compounds exponentially with ecosystem divergence. Every capability the proprietary surface lacks relative to the ecosystem is additional migration cost accruing silently.

**Adaptability caps this**: switching becomes bounded (one adapter), and $\tau$ drops toward zero.

### Drag cost

$$C_\delta(t) = P \cdot \rho(t), \qquad \rho(t) = \frac{n(t)}{K}$$

Platform-team capacity consumed by mediation. When $\rho \to 1$, the team's mediation queue saturates. By Little's Law, wait time grows without bound as utilization approaches one. The saturation is an asymptote, not a wall — the observable consequence is a queue that goes vertical before throughput stalls.

**Extensibility caps this**: platform involvement drops toward $O(1)$ validation per extension (schema check) rather than $O(\text{extension complexity})$ review. This is rate-decoupling: the platform's service rate decouples from work volume because validation cost stops scaling with extension internals.

### Opacity cost

$$C_\omega(t) = I \cdot u(t)^2 \cdot f$$

Diagnostic complexity as a function of undeclared interactions. The $u^2$ term reflects the pairwise search space ($u \leq \binom{n}{2} \in O(n^2)$), which is an upper bound on typical cost, not a prediction of typical cost.

**Composability caps $u$**: declared interactions remain a DAG with up to $O(n^2)$ edges, but they are inspectable from configuration. What collapses is the diagnostic search space, not the interaction graph. Undeclared interactions approach zero when composition is declared in configuration rather than emergent from runtime coupling.

## Coupled Dynamics

The channels are not superposed. They feed each other:
- Stasis increases $n$ by preventing migration.
- Drag increases $u$ by forcing workarounds that accumulate as undeclared behavior.
- Opacity suppresses the investment signal and so raises $\tau$ by keeping the organization on the proprietary surface.

Formally, the system is $\dot{x} = g(x)$ where $x = (C_\sigma, C_\delta, C_\omega)$ and $g$ has positive off-diagonal entries in its Jacobian: each channel's rate of change depends positively on the others. The result is positive-feedback dynamics. Total cost compounds rather than sums.

This is a modeling commitment, not a derivation. The cycle's runaway character follows from the coupling structure, not from the per-channel shapes alone. Real systems confirm direction (signs, shapes, feedback structure); magnitude requires calibration.

## Geometric Scale: NM → N+M+B

At platform scale, the cost signature collapses to a counting argument.

- Under full coupling: $N$ capabilities against $M$ runtimes is $NM$ integration points.
- Under protocol mediation: $N + M + B$ integration points.

The gap grows multiplicatively in $(N, M)$, not linearly. For $N = M = 10$ and $B$ modest, 100 vs. 21. For $N = M = 20$, 400 vs. 41. The ratio widens without bound as $N$ or $M$ grows.

## Diverging Curves

Two cost trajectories over time:
- **Without the boundary**: superlinear in $t$. The cycle compounds.
- **With the boundary**: bounded by $B + O(t)$ under stable conditions. Capped per-channel costs.

The area between the curves grows without bound. For plausible parameter ranges, divergence by an order of magnitude within a small number of years; the exact timeline is calibration-dependent. What the equations force is direction, not magnitude.

## Payoff Shapes

Two distinct payoff shapes apply. Keeping them separate matters because they explain different parts of the observed gap.

### Network-effect payoff (Arthur, Metcalfe)

Each additional capability written against the protocol becomes available to every runtime that speaks the protocol. Value is superadditive in the count of boundary-aligned components. This is the increasing-returns argument, not Taleb's convexity. The upside compounds because the ecosystem composes with itself.

### Antifragile payoff (Taleb)

Let $\sigma$ denote environmental volatility: heterogeneity shocks, new runtimes, new teams, new protocol versions, new integration patterns. The ACES system has $\partial^2 V / \partial \sigma^2 > 0$. Payoff is convex in volatility. The boundary gains from disorder. A new runtime arrives as capability expansion rather than integration cost. A new team arrives as capability contribution rather than coordination tax. Hormesis is the observable consequence.

### Both apply

ACES gets both shapes simultaneously. Network-effect payoff explains why the boundary compounds under stable conditions. Antifragile payoff explains why the boundary absorbs shocks. This is part of why reported returns look implausible at first reading.

The non-ACES path has both shapes inverted. Marginal return on maintenance investment decreases (concave in investment). Environmental shocks fracture rather than strengthen (concave in volatility). Both shapes point down.

## Calibration

The model predicts shape. It does not predict magnitude.

Reported ratios between coupled and decoupled cost for an identical capability cluster in the range of 40 to 100 times for mature Coupled Monolith instances running the full cycle. These magnitudes are illustrative, not derived. Magnitude depends on the system's $\tau$, $K$, $f$, $I$ and on the stressor distribution the system encounters.

### Measurement Surrogates

To operationalize the model against a real system:

| Parameter | Surrogate |
|---|---|
| $\tau$ | Cosine distance between the platform's API surface and ecosystem reference protocol, sampled quarterly. Rate = slope. |
| $K$ | Extensions-merged per quarter divided by extensions-submitted. |
| $f$ | Incidents rooted in cross-component interaction (not single-component bugs) per unit $n$. |
| $I$ | Mean engineer-hours per such incident. |
| ACES adherence | Three binary probes per property, with inter-rater reliability (Cohen's κ > 0.7). |

### Falsification Conditions

The coupling claim (positive off-diagonal Jacobian) fails if:
- A fleet with high stasis and high drag shows opacity *decreasing*.
- Granger-causality tests on $(\tau, \rho, u)$ time series show no cross-channel predictive power beyond autocorrelation.
- Real systems show superposition behavior (total cost ≈ sum of channel costs) rather than multiplicative.

### Validation Experiment

Select one Coupled Monolith and one ACES platform, matched on $N$, $M$, and age. Instrument a common capability delivery (e.g., add a rate-limiting policy). Measure engineer-hours, review cycles, and incident-hours over 90 days post-launch. Pre-register the predicted ratio range. Establish a same-platform variance noise floor with three capability additions first.

## What Calibration Enables

Shape-level claims ("the gap grows multiplicatively in $(N, M)$", "payoff is convex in $\sigma$") are testable from the model without calibration. Magnitude-level claims ("the ratio will be 40x for this system") require calibration against real parameter values.

Until that calibration work is done, the framework is:
- Falsifiable in direction.
- Unfalsified in magnitude.
- Rigorously testable when the calibration apparatus is built.

A companion paper treats the apparatus in full.
