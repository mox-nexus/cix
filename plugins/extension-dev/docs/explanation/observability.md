# Observability for Extensions

Why observability matters and how it connects to extension design.

---

## Contents

- [The Broken Feedback Loop](#the-broken-feedback-loop)
- [The Glass Box Pattern](#the-glass-box-pattern)
- [Hook Design Philosophy](#hook-design-philosophy)
- [Connection to Effect Sizes](#connection-to-effect-sizes)
- [What Observable Means](#what-observable-means)

---

## The Broken Feedback Loop

Sharma et al. (Anthropic, Jan 2026) analyzed ~1.5M Claude.ai conversations and found users rate harmful interactions MORE favorably in the moment. Satisfaction dropped below baseline only when users acted on outputs and saw consequences.

The implication: **users can't reliably self-correct.** Short-term satisfaction is not a reliable signal.

Without observability, extensions operate as black boxes. Nobody — not the user, not the team, not the extension author — can tell whether the extension is helping or harming. The feedback loop that should catch problems (use → observe → adjust) never fires.

Observability restores that loop by making extension behavior visible and measurable.

---

## The Glass Box Pattern

Opaque systems prevent learning. The Glass Box pattern makes the process inspectable:

| Property | What It Means |
|----------|---------------|
| **Readable** | Plaintext reasoning, no hidden state |
| **Verifiable** | Claims trace to sources |
| **Observable** | See what the tool does, not just what it produces |
| **Forkable** | Copy, modify, make your own |

For extensions, this means:

- **Agents** emit observations, conclusions, and uncertainty as they work ("work aloud")
- **Hooks** log what they detected and what they suggested (structured, not silent)
- **Skills** produce traceable reasoning chains, not just outputs
- **MCP servers** expose call traces and error context

Silent agents break team situational awareness. When humans can't see what's happening, they lose context and can't intervene at the right moment.

---

## Hook Design Philosophy

Hooks have two distinct patterns, and the distinction matters:

### Validation Hooks (suggest, don't block)

Most hooks should preserve agency:

```json
{"decision": "allow", "message": "Consider X instead of Y. Proceeding with Y."}
```

**Why:** Blocking removes agency, which hurts the control lever (the strongest design factor at beta = 0.507). Paternalistic engagement features show negative effects for frequent users (b = -0.555, Blaurock meta-analysis). Suggestions provide value without removing choice.

### Action-Triggering Hooks (directive by design)

Some hooks exist specifically to interrupt patterns:

```json
{"decision": "allow", "message": "PATTERN DETECTED. You MUST now: 1) [action] 2) [action]"}
```

**Why:** The pattern itself is the problem being solved. When a developer is going in circles or about to retry a failed approach, the whole point of the hook is to interrupt and redirect. Gentle suggestion would be ignored — the user is already in a cognitive loop.

**The key distinction:** Validation hooks protect agency over individual actions. Action-triggering hooks protect the user from metacognitive blind spots. Both serve the user, but through different mechanisms.

---

## Connection to Effect Sizes

Observability connects directly to the two strongest design levers from Blaurock's meta-analysis (106 studies):

| Lever | Effect Size | How Observability Helps |
|-------|------------|------------------------|
| **Control** | beta = 0.507 | Users can observe, steer, and override when they can see what's happening |
| **Transparency** | beta = 0.415 | Visible reasoning enables genuine evaluation, not rubber-stamping |

Without observability, both levers are disabled. The user approves outputs they can't evaluate, trust becomes binary (accept/reject), and the collaboration degrades to substitution.

Observable extensions support **calibrated trust** — users know when to rely on the extension and when to verify, because they can see the reasoning that produced the output.

---

## What Observable Means

For extension authors building new extensions:

| Extension Type | Observable When |
|----------------|----------------|
| **Agent** | Emits reasoning traces, logs tool calls, reports token usage |
| **MCP Server** | Traces calls with context, exposes errors with fix guidance |
| **Hook** | Logs trigger conditions, records suggestions made |
| **Skill** | Produces verifiable reasoning chains (not just answers) |

The technical implementation uses OpenTelemetry (see `references/observability.md` for the Claude-optimized how-to). But the philosophy matters more than the tooling: **make the process inspectable so humans can learn, verify, and improve.**

---

See [sources.md](sources.md) for full bibliography.
