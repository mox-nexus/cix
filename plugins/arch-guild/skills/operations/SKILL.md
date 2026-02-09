---
name: operations
description: This skill should be used when the user asks to "review for production", "check production readiness", "evaluate resilience", "assess observability", "review ops", "design chaos experiments", or discusses deployment, monitoring, incident response, failure modes, or chaos engineering.
---

# Operations

Production readiness evaluation through Guild failure-first reasoning.

## What This Adds

Claude already knows circuit breakers, RED metrics, structured logging, retry patterns, and production checklists. This skill doesn't reteach those — it adds **failure-first architectural perspectives** that find the gaps between knowing the patterns and surviving production.

## The Three Operations Lenses

### Taleb (Antifragile) — Does the system benefit from disorder?

Not "can it survive failure?" — but "does failure make it stronger?"

**Taleb's Tests:**
- Have you actually pulled the plug? Or just drawn diagrams?
- What's the difference between your redundancy plan and your reality?
- Name three failures that would surprise you — those are the ones that will happen
- Is your monitoring monitoring itself?

**Taleb's Hierarchy:**
1. **Fragile** — Breaks under stress (no fallbacks, single points of failure)
2. **Robust** — Survives stress (redundancy, circuit breakers)
3. **Antifragile** — Improves from stress (chaos experiments → automated fixes, incidents → runbooks)

**What Taleb catches:**
- Fragility Theater ("we have redundancy" without ever testing it)
- Untested recovery procedures
- Monitoring that goes blind during the failures you most need to observe
- Single points of failure hiding behind "high availability" labels

### Erlang (Hydraulic) — Where is the valve?

Not "what's the capacity?" — but "what happens when capacity is exceeded?"

**Erlang's Core Law:** If λ (arrival rate) > μ (service rate), the queue grows unbounded. Always.

**Erlang's Tests:**
- At 2x expected load, what degrades first?
- At 10x, what breaks?
- Is every queue bounded? What happens when it's full?
- Can the system shed load gracefully, or does it accept-until-death?

**What Erlang catches:**
- Unbounded queues (memory exhaustion under sustained load)
- Missing backpressure (system accepts work it can't complete)
- Cascading saturation (one slow service pools up all upstream connections)
- The "works fine at demo scale, dies at production scale" trap

### Vector (Adversarial Ops) — How do failures become attack vectors?

Not "is the system secure?" — but "how do operational failures create exploitable windows?"

**Vector's Tests:**
- During failover, are auth checks still enforced?
- Do error messages leak internal state?
- Does graceful degradation degrade security too?
- Can an attacker trigger the failure mode deliberately?

**What Vector catches:**
- Error pages revealing stack traces, versions, internal paths
- Failover modes that bypass authentication
- Rate limit implementations that can be circumvented
- DoS vectors in legitimate endpoints (expensive queries, unbounded uploads)

## Production Readiness Routing

| Concern | Primary | Secondary | Why |
|---------|---------|-----------|-----|
| Failure modes | Taleb | Erlang | Antifragility + capacity |
| Load behavior | Erlang | Knuth | Flow dynamics + complexity |
| Security posture | Vector | Dijkstra | Attack surface + correctness |
| Distributed failure | Lamport | Taleb | Consistency + resilience |
| Validation criteria | Ixian | Taleb | Measurement + antifragility |

## Chaos Experiment Design

The Guild's approach to chaos — not as a checklist, but as Ixian-informed experimentation:

### 1. Steady State Hypothesis (Ixian)

Before breaking anything, define "normal" with falsifiable metrics:

```
Hypothesis: System maintains <1% error rate under [failure]
Null (H0): Failure causes >1% error rate
Noise floor: Baseline error rate = [measure first]
```

### 2. Failure Selection (Taleb)

Pick failures that would **surprise** you, not ones you've already mitigated:
- What failure have you never tested?
- What would happen if your monitoring failed during an incident?
- What's your longest untested recovery procedure?

### 3. Blast Radius Containment

```
Level 1: Single instance, non-critical path → Start here
Level 2: Single instance, critical path
Level 3: Multiple instances, single AZ
Level 4: Entire AZ
Level 5: Cross-region (extreme caution)
```

### 4. Abort Conditions

Automatic termination if:
- Error rate exceeds threshold
- Customer impact detected
- On-call paged
- Monitoring itself fails (Taleb's meta-failure)

## Output Format

```
## Production Readiness: {Service}

### Taleb (Antifragility)
- {Finding — fragile, robust, or antifragile?}

### Erlang (Hydraulics)
- {Finding — where does the queue grow unbounded?}

### Vector (Attack Surface)
- {Finding — how do failures become exploitable?}

### Specialists Invoked
- {Agent}: {finding} (if applicable)

### Untested Assumptions
{What has been designed but never verified in production?}

### Recommended Experiment
{A specific chaos experiment to close the biggest open loop}

### Validation Criteria (Ixian)
- {Falsifiable metric 1}
- {Falsifiable metric 2}
```

## Additional Resources

- **`references/chaos-patterns.md`** — GameDay planning template and experiment scaffolds
