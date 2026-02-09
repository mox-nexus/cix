---
name: deep-reasoning
description: "Use when: 'write a prompt for o1', 'optimize for reasoning models', 'engineer prompts for Deep Think', 'o3 prompting', 'reasoning model constraints', or designing prompts for models with internal RL (o1, o3, Gemini Deep Think)."
---

# Deep Reasoning

Prompting for models with internal reinforcement learning: o1, o3, Gemini Deep Think.

**Key insight:** You're building a gym, not writing instructions.

---

## Two Modes

| Mode | Input | Output | Use When |
|------|-------|--------|----------|
| **Direct** | You write the XML constraints | XML → reasoning model | You know the domain |
| **Meta (Deep Think Architect)** | You describe what you need | Meta-prompt generates XML for you | Domain is unfamiliar, want auto-scenario-injection |

The Deep Think Architect meta-prompt is in `references/deep-think.md`. Feed it to a standard model (Claude, GPT-4) with your context, and it outputs copy-pasteable XML for the reasoning model.

---

## The Difference

| Autoregressive (Claude, GPT-4) | Reasoning (o1, Deep Think) |
|-------------------------------|---------------------------|
| Tell them HOW to think | Tell them WHERE to search |
| Chain-of-thought helps | Chain-of-thought is redundant |
| More examples = better | Examples can hurt |
| Detailed prompts help | Over-detailed prompts hurt |

---

## The Constraint Philosophy

| Don't | Do |
|-------|-----|
| "Think step by step" | Define the destination |
| "Consider multiple options" | Force triangulation between named positions |
| "Be thorough" | Set electric fences (hard constraints) |
| "Check your work" | Define what failure looks like |

---

## Core Patterns

### Scenario Injection

Abstract requests → specific high-stakes simulations.

| Abstract | Injected Scenario |
|----------|-------------------|
| "Check for bugs" | "Simulate a race condition in a high-frequency trading engine" |
| "Critique this plot" | "Rewrite the climax assuming the protagonist fails" |
| "Evaluate this team" | "The team just lost their lead engineer. What breaks first?" |

### Triangulation Constraint

Force the model to hold conflicting hypotheses simultaneously.

```
Simulate a debate: X wants speed, Y wants safety, Z wants simplicity.
Synthesize a position that addresses all three.
```

### Negative Constraints

Remove easy outs.

- NO happy paths (force failure handling)
- NO hedging (force decisions)
- NO generic advice (force specificity)

### Technical Density

Demand domain jargon to anchor the search space.

```
Use terms: idempotency, CRDTs, backpressure, eventual consistency
```

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| "Think step by step" | They already do — wastes tokens |
| Provide examples | o1 performs worse with examples |
| Over-detailed prompts | Counterproductive with sophisticated models |
| Role prompting for accuracy | Little to no effect on correctness |

---

## References

- `references/deep-think.md` — Extended patterns and examples

---

## When to Use

- Prompting o1, o3, Gemini Deep Think
- When "think step by step" isn't working
- Complex multi-constraint optimization
- Forcing rigorous evaluation criteria
