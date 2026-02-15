# Productivity Reality

What the evidence actually shows about AI-assisted development productivity and code quality.

---

## Contents

- [The Productivity Illusion](#the-productivity-illusion)
- [Code Quality Signals](#code-quality-signals)
- [Security Degradation](#security-degradation)
- [The Explainability Gap](#the-explainability-gap)
- [Collaboration Health Metrics](#collaboration-health-metrics)
- [What Actually Improves](#what-actually-improves)
- [Practical Patterns](#practical-patterns)

---

## The Productivity Illusion

**Source:** METR / Becker et al. (2025), arXiv — Randomized Controlled Trial

| Metric | Measured | Perceived |
|--------|----------|-----------|
| Task completion time | **19% slower** with AI | 24% faster (believed) |
| Confidence in speed | — | "AI made me faster" |
| Miscalibration gap | — | **43 percentage points** |

### The Mechanism

1. AI reduces *perceived* effort (code appears faster)
2. Time spent on prompting, reviewing, fixing, integrating is uncounted
3. Context-switching between AI suggestions and own code adds overhead
4. The feeling of productivity substitutes for actual throughput measurement

### Why This Matters

If developers (and managers) believe AI makes them faster when it actually makes them slower, decisions about tooling, staffing, and timelines will be systematically wrong.

### The Nuance

METR studied experienced open-source developers on their own repos. The effect may differ for:
- Unfamiliar codebases (AI might genuinely help)
- Simple/boilerplate tasks (less integration overhead)
- Greenfield projects (less existing context to manage)

The finding isn't "AI never helps with speed" — it's "don't assume it does without measuring."

---

## Code Quality Signals

### Duplication

**Source:** GitClear (2025) — 211 million lines of code analyzed

| Metric | Before AI | After AI |
|--------|-----------|----------|
| Code duplication rate | Baseline | **8x increase** |
| Refactoring activity | Baseline | **Significant decline** |
| Copy-paste patterns | Baseline | **Sharp increase** |

### Why Duplication Increases

AI generates code without awareness of the broader codebase. Each generation produces a fresh solution, often duplicating existing patterns rather than reusing them.

The human who would have searched for existing solutions instead gets a plausible new one — faster to accept than to find and reuse.

### DORA Metrics

**Source:** DORA State of DevOps (2024)

| Metric | Change |
|--------|--------|
| Deployment stability | -7.2% |
| Throughput | -1.5% |

The most rigorous industry measurement of engineering effectiveness shows AI adoption correlating with slight degradation, not improvement.

---

## Security Degradation

### Baseline

**Source:** Veracode (2025)

| Finding | Detail |
|---------|--------|
| AI code with critical vulnerabilities | **45%** |
| Larger models more secure? | **No** — model size doesn't correlate with security |
| More iterations more secure? | **No** — see below |

### The Iteration Problem

**Source:** Shukla et al. (2025), arXiv

| Iteration | Vulnerabilities per 1000 LOC |
|-----------|------------------------------|
| 1st generation | 2.1 |
| After refinement | **6.2** |

Security *degrades* with iteration. Each refinement adds code without removing vulnerabilities from previous iterations.

### The Source Problem

**Source:** Perry et al. (2025), arXiv — 7,703 files analyzed

AI-generated code inherits vulnerabilities from training data. Common patterns:
- Hardcoded credentials
- SQL injection via string concatenation
- Missing input validation
- Insecure deserialization patterns

### Design Response

1. Never trust AI-generated code for security-sensitive operations
2. Treat every AI suggestion as potentially insecure by default
3. Security review must be independent of code generation
4. More iterations ≠ more secure (counter-intuitive but measured)

---

## The Explainability Gap

As AI generates more code, a gap opens between code complexity and developer understanding.

### The Pattern

```
Sprint 1: Developer writes 500 LOC, understands all of it
Sprint 2: AI generates 2000 LOC, developer understands ~60%
Sprint 3: AI generates on top of Sprint 2, developer understands ~30%
Sprint N: "Cathedral to Prefabs" — codebase is assembled, not designed
```

### Why It Matters

- **Debugging**: Can't debug what you don't understand
- **Maintenance**: Can't maintain what you can't reason about
- **Evolution**: Can't evolve architecture you didn't design
- **Security**: Can't secure code you haven't comprehended

### The "Cathedral to Prefabs" Shift

Traditional development: architect designs, builders construct with understanding.
AI-assisted development: assembler connects generated components without full comprehension.

This is the abstraction skill being outsourced — not just implementation, but the *understanding* of implementation.

### Counter-Pattern

Maintain understanding proportional to risk:

| Code Category | Understanding Required |
|---------------|----------------------|
| Infrastructure/boilerplate | Low (AI-generated is fine) |
| Business logic | High (human must comprehend) |
| Security boundaries | Very high (human must design) |
| Architecture decisions | Complete (human must own) |

---

## Collaboration Health Metrics

How to measure whether AI collaboration is healthy or degrading.

### Correction Rate

How often you modify AI suggestions before accepting.

| Rate | Signal |
|------|--------|
| < 5% | Under-reviewing — automation bias risk |
| 10-30% | Healthy calibration |
| 30-50% | AI struggling with this domain |
| > 50% | AI not effective here — work manually |

### Verification Latency

Time between receiving AI output and meaningful review.

| Latency | Signal |
|---------|--------|
| Immediate accept | Rubber-stamping |
| 10-30 seconds | Scanning, not reviewing |
| 1-5 minutes | Genuine review |
| > 5 minutes | Deep analysis (appropriate for complex output) |

### Understanding Depth

Can you explain the AI's output to someone else?

```
"Why does this code use a semaphore here?"

If you can't explain it, you don't understand it.
If you don't understand it, you can't maintain it.
If you can't maintain it, it's technical debt.
```

### Independence Check

Periodically assess: "Could I have done this without AI?"

| Answer | Implication |
|--------|-------------|
| "Yes, but slower" | Healthy — AI is amplifying |
| "Yes, differently" | Healthy — AI is broadening |
| "No" | Warning — dependency forming |
| "I don't know" | Red flag — capability uncertain |

---

## What Actually Improves

Despite the concerns, AI genuinely helps in measurable ways:

| Area | Evidence | Magnitude |
|------|----------|-----------|
| Task completion (with AI present) | Cui/Demirer RCTs | +26% tasks |
| Boilerplate generation | Multiple studies | Significant time savings |
| Code translation | GitHub Copilot research | Meaningful improvement |
| Learning unfamiliar APIs | Microsoft research | Faster onboarding |
| Exploration / prototyping | Anecdotal + surveys | Widely reported |

The key: these gains are real but exist alongside the quality/skill/security concerns above. The question isn't "does AI help?" — it's "how do we capture the gains without the harms?"

**Answer:** Complementary design. AI amplifies; human remains central. Not substitutive (AI replaces; human atrophies).

---

## Practical Patterns

### Measure Before Believing

Don't assume productivity gains. Measure:
- Actual time to completion (including prompting, reviewing, fixing)
- Defect rate in AI-assisted vs unassisted work
- Time spent debugging AI code vs own code

### Review Budget

Allocate explicit time for reviewing AI output:
- 20% of the time AI "saved" should go to verification
- Budget more for security-sensitive and business logic code
- Don't count review time as "overhead" — it's the quality investment

### Codebase Hygiene

Counter the duplication tendency:
- Before accepting AI code, search for existing implementations
- Refactor AI-generated code to match codebase patterns
- Treat AI output as a draft, not a final product
- Regular deduplication sweeps

---

## Key Sources

| Finding | Source |
|---------|--------|
| 19% slower, perceived 24% faster | METR/Becker et al. (2025) |
| 8x code duplication | GitClear (2025) |
| 45% critical vulnerabilities | Veracode (2025) |
| 2.1 → 6.2 security degradation | Shukla et al. (2025) |
| -7.2% stability, -1.5% throughput | DORA (2024) |
| 7,703 file vulnerability analysis | Perry et al. (2025) |
| 26% more tasks with AI | Cui/Demirer RCTs (2024) |

See [sources.md](../../docs/explanation/sources.md) for full bibliography.
