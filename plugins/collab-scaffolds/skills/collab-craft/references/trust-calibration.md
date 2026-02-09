# Trust Calibration

Techniques for calibrating trust in AI outputs — neither blind acceptance nor blanket rejection.

---

## Contents

- [The Trust Paradox](#the-trust-paradox)
- [The "Almost Right" Problem](#the-almost-right-problem)
- [Evidence Levels](#evidence-levels)
- [Contrastive Explanations](#contrastive-explanations)
- [Verification Decay](#verification-decay)
- [Senior-Junior Gap](#senior-junior-gap)
- [Falsification Before Advocacy](#falsification-before-advocacy)
- [Practical Patterns](#practical-patterns)

---

## The Trust Paradox

**Source:** Stack Overflow Developer Survey (2025)

| Metric | Value |
|--------|-------|
| Developers using AI tools | 84% |
| Developers who trust AI output | 29% |
| Developers who actively distrust | 46% |

The paradox: developers use AI extensively while actively distrusting it. This creates a brittle dynamic — neither calibrated trust nor productive skepticism, but anxious reliance.

### Why This Matters

Uncalibrated trust manifests as:
- **Binary accept/reject** — no gradation between "trust completely" and "trust nothing"
- **Verification theater** — glancing at output without genuine evaluation
- **Automation bias** — accepting plausible-sounding output despite signals to verify
- **Trust fatigue** — eventually giving up on verification because it's exhausting

Calibrated trust looks like: "I trust this output for X context with Y confidence, and I'll verify Z specifically."

---

## The "Almost Right" Problem

**Source:** Stack Overflow (2025), GitClear (2025)

AI code is often *plausible but subtly wrong*. This is worse than obviously wrong code:

| Metric | Finding | Source |
|--------|---------|--------|
| Fixing time vs writing from scratch | 66% longer to fix AI code | SO 2025 |
| Code duplication increase | 8x since AI adoption | GitClear 2025 |
| Critical vulnerabilities in AI code | 45% | Veracode 2025 |
| Security degradation across iterations | 2.1 → 6.2 vulnerabilities | Shukla et al. 2025 |

### The Mechanism

1. AI generates plausible code
2. Developer recognizes familiar patterns → reduces scrutiny
3. Subtle error is embedded in mostly-correct context
4. Error surfaces later, now entangled with dependent code
5. Debugging requires understanding code you didn't write, in a pattern that *almost* works

### Design Response

When generating code:
```
✅ "Here's my approach. Key assumptions:
    - Connection pool is thread-safe (verify your driver)
    - Error retry is idempotent (check your endpoint)
    - Timeout is appropriate for your network (adjust if remote)"

❌ "Here's the implementation:" [code block with no caveats]
```

Surface the assumptions that could make "almost right" code wrong.

---

## Evidence Levels

Calibrate confidence to evidence strength:

| Level | Criteria | Signal |
|-------|----------|--------|
| **Strong** | Multiple peer-reviewed sources, replicated findings | "Research consistently shows..." |
| **Moderate** | Single quality source or converging indirect evidence | "One well-designed study found..." |
| **Weak** | Expert opinion, theoretical prediction, analogy | "Based on similar domains..." |
| **Speculative** | Reasonable inference without direct evidence | "I'd expect... but no direct evidence" |

### Application

```
Strong: "Connection pooling improves throughput — this is well-established
across PostgreSQL, MySQL, and Oracle documentation."

Moderate: "The Bastani et al. PNAS study found 17% learning harm from
direct answers, but this was in math education — transfer to software
is plausible but not directly measured."

Weak: "Based on aviation automation research, I'd expect similar
skill atrophy patterns, but no longitudinal developer study exists."

Speculative: "This pattern might cause issues at scale, but I'm
reasoning by analogy — verify with load testing."
```

### Why Uniform Confidence Is Harmful

When AI presents everything with equal confidence:
- Users can't distinguish high-evidence from speculation
- Trust becomes binary (accept all or reject all)
- Verification effort can't be prioritized
- Errors in speculative claims undermine trust in strong claims

---

## Contrastive Explanations

**Source:** Ma et al. (2025), Taylor & Francis

"X instead of Y because Z" triggers analytic processing. "Use X" triggers heuristic acceptance.

### The Pattern

```
❌ "Use Redis for this cache."

✅ "Redis instead of Memcached because you need
    data structures beyond key-value (sorted sets
    for your leaderboard). If you only needed simple
    KV caching, Memcached would be simpler."
```

### Why It Works

Contrastive framing:
1. Shows alternatives were considered (not just the first option)
2. Makes tradeoffs visible (what you're gaining and losing)
3. Activates analytic processing (comparison requires evaluation)
4. Builds transferable judgment (the "because" teaches the framework)

### When to Use

- Technical recommendations ("Use X")
- Architecture decisions ("Go with approach A")
- Tool selection ("Choose framework Y")
- Any recommendation where alternatives exist

---

## Verification Decay

Trust calibration degrades over time without maintenance.

### The Pattern

```
Day 1: Carefully review every AI suggestion
Day 7: Skim suggestions, spot-check occasionally
Day 30: Glance at output, accept if it "looks right"
Day 90: Auto-accept, only notice when things break
```

### Why It Happens

- Verification is cognitively expensive
- Most AI output is correct → reinforces skipping verification
- No feedback loop for undetected errors
- Time pressure favors speed over scrutiny

### Counter-Patterns

1. **Structured verification** — checklist that takes <30 seconds, applied consistently
2. **Spot audits** — randomly deep-verify some outputs even when confident
3. **Red team rotations** — periodically assume output is wrong, try to find the error
4. **Verification metrics** — track how often verification catches issues (if never: verify harder or AI is actually good for this task)

---

## Senior-Junior Gap

**Source:** SO 2025, GitHub research

| Behavior | Senior Developers | Junior Developers |
|----------|------------------|-------------------|
| Trust AI output | 2.5% fully trust | 17% fully trust |
| Ship AI code directly | 32% ship with review | 13% ship with review |
| Verify before committing | Almost always | Often skip |
| Edit AI suggestions | Substantial edits | Minor or no edits |

### What Seniors Do Differently

Seniors treat AI output as a **first draft from a junior developer**:
1. Read the code, don't just scan it
2. Check edge cases the AI likely missed
3. Verify against production constraints AI doesn't know
4. Refactor for the codebase's patterns, not generic patterns

### Implication

Junior developers need stronger scaffolding:
- Explicit verification prompts
- Assumption surfacing in every code generation
- "What could go wrong" sections
- Encourage editing over accepting

---

## Falsification Before Advocacy

When you believe something is true, actively try to prove it wrong before presenting it.

### The Pattern

```
1. Form conclusion
2. BEFORE presenting: What evidence would disprove this?
3. Actively search for counter-evidence
4. Present conclusion WITH the strongest counter-argument
```

### Application

```
"I recommend PostgreSQL for this use case.

Strongest argument against: Your write pattern (10K inserts/sec)
could hit WAL bottlenecks. If writes are your dominant workload,
Cassandra or ScyllaDB would handle this better.

Why I still recommend PostgreSQL: Your read pattern needs
complex joins that Cassandra can't do, and you can shard
writes with Citus if needed."
```

### Why This Works

- Forces genuine evaluation (not post-hoc rationalization)
- Surfaces the failure modes before they happen
- Builds trust through demonstrated honesty
- Teaches the human the decision framework, not just the decision

---

## Practical Patterns

### The Three-Question Check

Before accepting any significant AI output:

1. **What assumptions is this based on?** (Surface hidden dependencies)
2. **What would make this wrong?** (Identify failure conditions)
3. **How would I verify this?** (Plan for checking, even if you don't check everything)

### Trust Gradients

Not all outputs need the same verification depth:

| Output Type | Trust Level | Verification |
|-------------|-------------|-------------|
| Formatting, syntax | High | Glance |
| Library usage, API calls | Medium | Check docs for edge cases |
| Business logic | Low | Full review against requirements |
| Security-sensitive code | Very low | Dedicated security review |
| Architecture decisions | Very low | Multiple perspectives + production context |

### Correction Rate

Track how often you correct AI suggestions. Healthy range: 10-30%.

| Rate | Signal |
|------|--------|
| < 5% | Probably under-reviewing |
| 10-30% | Healthy calibration |
| > 50% | AI not effective for this task |

---

## Key Sources

| Finding | Source |
|---------|--------|
| Trust Paradox (84% use, 29% trust) | Stack Overflow 2025 |
| 66% fixing time > writing time | Stack Overflow 2025 |
| 45% critical vulnerabilities | Veracode 2025 |
| 8x code duplication | GitClear 2025 |
| Contrastive explanations | Ma et al. (2025), Taylor & Francis |
| Senior-junior gap | SO 2025, GitHub research |
| Security degradation | Shukla et al. (2025) |

See [sources.md](../../docs/explanation/sources.md) for full bibliography.
