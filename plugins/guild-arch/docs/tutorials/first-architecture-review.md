# Tutorial: Your First Architecture Review

**Time:** 15-20 minutes
**What you'll do:** Walk through a full Guild architecture review of a real decision -- whether to add Redis caching to a web application.
**What you'll learn:** How the Guild works, what the agents actually produce, and how to interpret their output.

## The Scenario

You have a web application running on 4 replicas behind a load balancer. User sessions are stored in a per-process `HashMap`. Response times are fine now, but users occasionally report being logged out unexpectedly.

You're considering adding Redis as a shared session store. Should you?

## Step 1: Ask for the Review

Start with a clear description of the decision and the context. Context matters -- the Guild can only reason about what you tell it.

```
Review this architecture decision:

We have a web app running 4 replicas behind a load balancer.
Sessions are stored in per-process HashMap (in-memory).
Users report intermittent logouts.
Proposal: migrate session storage to Redis.
```

The architecture skill activates. The Guild classifies this as a **Review task** (you're evaluating a proposal, not designing from scratch) and selects agents.

## Step 2: Watch Agent Selection

For this decision, the Guild picks Focus mode. The domain is "distributed" (multiple replicas, shared state), so the initial selection is:

- **Lamport** -- consistency and distributed systems
- **Erlang** -- capacity and flow
- **Taleb** -- resilience and failure modes
- **Burner** -- boundaries and coupling

Plus the cross-cutting agents:
- **K** -- strategic context (available on any deliberation)
- **Ixian** -- validation criteria (mandatory, closes every deliberation)

Notice who's *not* here: Dijkstra (no auth logic under review), Knuth (no algorithmic complexity concern), Ace (not a DX question). Focus mode keeps noise down.

## Step 3: Read the Independent Verdicts

Each agent evaluates independently. Nobody sees anyone else's verdict first. Here's what their reasoning looks like:

**K (Strategic):** APPROVE with conditions
> HashMap works for single-instance. But with 4 replicas, session affinity or shared state is mandatory. Redis is the commodity solution -- low risk, well-understood, widely deployed. Building a custom solution would be over-engineering. The strategic move: migrate to Redis, keep the HashMap interface so the swap is clean.

**Lamport (Distributed):** BLOCK
> Per-process HashMap with 4 replicas behind a load balancer means user hits replica A, session stored there, next request hits replica B -- session missing. This is the Local Assumption: treating distributed state as local. The intermittent logouts aren't a bug in your code. They're the inevitable result of per-process state in a multi-replica deployment. Redis or any shared store fixes the physics. HashMap cannot work here unless you pin sessions to replicas (sticky sessions), which introduces its own fragility.

**Erlang (Flow):** CONCERN
> Redis adds a network hop to every request. Current p99 session lookup: nanoseconds (in-memory). With Redis: ~1ms per lookup over the network. At 4 replicas, that's fine. At 40 replicas with 10k concurrent sessions, watch connection pool exhaustion. Size the connection pool and add a circuit breaker. Also: what's the eviction policy? If Redis memory fills, which sessions get dropped?

**Taleb (Resilience):** CONCERN
> Redis is now a single point of failure. If Redis goes down, all sessions are lost. Mitigation: Redis Sentinel or Redis Cluster for HA. But have you tested the failover? "We have Redis Sentinel" is not the same as "we killed the primary last Tuesday and sessions survived." Also: what's the recovery story? If Redis loses data, can users re-authenticate, or are they stuck?

**Burner (Boundaries):** APPROVE
> Clean swap if done correctly. Session storage is a driven port (outbound dependency). The domain shouldn't know it's talking to Redis vs HashMap. Create a `SessionStore` protocol in the domain, implement `RedisSessionStore` as an adapter, wire it in the composition root. If the domain imports Redis types directly, that's a boundary violation.

## Step 4: Follow the Tally

The tally:
- 1 BLOCK (Lamport)
- 2 CONCERN (Erlang, Taleb)
- 2 APPROVE (K, Burner)

**Any BLOCK stops everything.** Lamport's concern isn't "maybe this is a problem" -- it's "per-process HashMap physically cannot work with multiple replicas." The intermittent logouts prove it.

But Lamport is blocking the *current design*, not the *proposal*. The proposal (migrate to Redis) actually resolves Lamport's block. So the deliberation continues with the proposal accepted in principle, and the concerns from Erlang and Taleb shaping the implementation.

## Step 5: See How Concerns Shape the Decision

Erlang and Taleb raised real concerns about the Redis migration:

| Agent | Concern | Action |
|-------|---------|--------|
| Erlang | Connection pool exhaustion at scale | Size the pool, add circuit breaker |
| Erlang | Eviction policy unclear | Define max memory and eviction strategy |
| Taleb | Redis as single point of failure | Deploy Redis Sentinel for HA |
| Taleb | Untested failover | Schedule a failover test before launch |
| Burner | Domain must not import Redis types | Use a SessionStore protocol |

These aren't blockers -- they're implementation requirements that the review surfaced. Without the Guild, you might have added Redis without thinking about failover or connection pools. Those gaps would show up in production instead of in review.

## Step 6: Read the Validation Criteria

Ixian closes every deliberation. Here's what that looks like:

```
### Validation Criteria (Ixian)

Hypothesis: Redis migration eliminates intermittent logouts
  and maintains acceptable latency.
Null (H0): Logouts persist or latency degrades beyond threshold.

Metrics:
  - Intermittent logout rate: < 0.1% over 7 days (currently ~2%)
  - P99 session lookup latency: < 5ms (currently ~0.001ms in-memory)
  - Redis failover recovery time: < 30 seconds (test before launch)

Noise floor: Measure baseline logout rate for 48 hours
  before migration to establish the actual current rate.

Rollback trigger: If logout rate does not decrease within
  72 hours post-migration, the problem isn't session storage.
```

This is the feedback loop. Without it, you'd migrate to Redis, logouts might decrease, and you'd never know if it was the migration or something else. Ixian makes the decision falsifiable.

## Step 7: Check the Ratchet

After a significant decision, the Guild captures the learning:

```markdown
## 2026-04-07: Session Storage -- HashMap to Redis

### Blocking Agents
- Lamport: Per-process HashMap breaks session consistency
  with multi-replica deployment

### Principle Extracted
> "In-memory state in a multi-replica deployment requires either
>  session affinity or shared storage. Per-process state
>  is the Local Assumption."

### Future Trigger
Any per-process cache or state in a multi-replica service
```

Next time someone proposes an in-memory cache in a distributed service, the ratchet fires. The Guild already knows what happened last time.

## What You Just Learned

1. **Focus mode** selects 3-4 agents matched to the decision. You don't need all 13 for most questions.

2. **Independent verdicts** prevent conformity. Lamport's BLOCK isn't influenced by K's APPROVE. Each agent sees only the question.

3. **BLOCK stops everything.** But it stops the current state, not necessarily the proposal. Lamport blocked HashMap, not Redis.

4. **Concerns shape implementation.** Erlang and Taleb didn't block, but their concerns became requirements: connection pools, circuit breakers, HA, failover testing.

5. **Ixian makes decisions falsifiable.** "It should fix the logouts" becomes "logout rate < 0.1% over 7 days, measured against a 48-hour baseline."

6. **The ratchet compounds learning.** This decision teaches the Guild about future decisions with similar shapes.

## Next Steps

- **Try a design review** -- point the Guild at a specific module with `"Review the design of src/your-module/"`. See the [code design review guide](../how-to/review-code-design.md).
- **Try a tradeoff** -- ask "Redis vs Memcached for session storage?" and watch Lotfi produce a dimension scoring matrix.
- **Try a design exploration** -- ask "How should we structure the notification service?" and watch agents generate independent proposals instead of verdicts.
- **Read the methodology** -- [Why The Guild Works](../explanation/methodology.md) explains the research behind the deliberation protocol.
