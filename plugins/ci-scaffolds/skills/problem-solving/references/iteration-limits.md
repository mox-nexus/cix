# Iteration Limits

When to stop iterating and start over.

## Contents

- [The Research](#the-research)
- [The 3-Iteration Checkpoint](#the-3-iteration-checkpoint)
- [Context Degradation Signals](#context-degradation-signals)
- [Counter-Patterns](#counter-patterns)
- [When to Stop Entirely](#when-to-stop-entirely)
- [Relationship to Other Hooks](#relationship-to-other-hooks)

## The Research

**Shukla et al. 2025** (arXiv:2501.16820):
- Security vulnerabilities increase **37.6%** after 5 conversational iterations
- **14.3% increase** per 10% complexity added
- Security-focused prompts improve results only in iterations 1-3

**The mechanism:**
- Each iteration adds without removing
- Compounds assumptions
- Narrows hypothesis space
- Sunk cost fallacy keeps you on the same path

**Context degradation:**
- "Lost in the middle" effect (Liu et al. 2024)
- Information in middle of context gets less attention than beginning or end
- After many iterations, early constraints and decisions fade from effective context

## The 3-Iteration Checkpoint

After 3 attempts at the same problem that haven't converged, stop and assess.

### Self-Assessment Questions

| Question | Purpose |
|----------|---------|
| **Right problem?** | Am I solving the actual problem or a symptom? Restate the goal in one sentence. |
| **Same approach?** | If I'm trying the same approach with slight variations, the approach is wrong. Try a fundamentally different angle. |
| **Fresh context?** | Have I accumulated assumptions that might be wrong? What did I believe at the start that might be incorrect now? |
| **Am I spinning?** | If the last 3 attempts look similar, I'm in a loop. Wolf Protocol. |

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Same approach, different execution | Change approach entirely |
| Different approaches, same failure | Problem is misframed — step back |
| Complexity growing with each attempt | Solving symptoms, not cause |
| Working but not converging | Scope is too large — reduce |

## Context Degradation Signals

### Early Signs (act now)

- Re-reading files that were read earlier in the session
- Referencing decisions from 50+ messages ago
- Making suggestions contradicted by earlier analysis
- Losing track of which files were modified
- Proposing approaches without checking if they were already tried

### Late Signs (must act)

- Contradicting your own earlier statements
- Proposing approaches already tried and rejected
- Increasing solution complexity with each attempt
- Forgetting constraints established earlier
- Circular reasoning (using conclusions as premises)

## Counter-Patterns

### 1. Fresh Start

**When**: Assumptions have accumulated, context is polluted

**How**:
- `/clear` and restate the problem from scratch
- Write a brief summary of what's been tried and what failed
- Often, the clean context reveals the actual issue

**Why it works**: Removes accumulated assumptions, resets hypothesis space

### 2. Subagent Delegation

**When**: Subproblem is well-defined but main context is cluttered

**How**:
- Spawn a specialized agent with a clean context
- Give it the specific subproblem, not the whole history
- The agent doesn't carry accumulated assumptions

**Why it works**: Fresh perspective without conversational baggage

### 3. Human Checkpoint

**When**: 3 attempts haven't converged

**Pattern**:
```
"I've tried 3 approaches:
1. [Approach A] - [Result]
2. [Approach B] - [Result]
3. [Approach C] - [Result]

Here's what I'm seeing: [Pattern]
What am I missing?"
```

**Why it works**:
- Human has context you don't (recent changes, environment, constraints)
- Human can reframe the problem
- This is not failure — it's the collaboration loop working correctly

### 4. Scope Reduction

**When**: Problem feels too large, solutions keep getting complex

**How**:
- Solve a smaller version of the problem first
- If you can't solve the small version, you've found the core issue
- If you can, the extension to full scope is usually obvious

**Example**:
```
Instead of: "Make the entire auth system work"
Try: "Can I authenticate one user with a hardcoded token?"
```

**Why it works**: Isolates core vs. incidental complexity

### 5. Wolf Protocol

**When**: Spinning detected — same failure mode repeating

**How**: Invoke Mr. Wolf (5-step structured breakdown)

**Why it works**: Forces reframing, prevents circular thinking

See: [mr-wolf.sh hook](../../hooks/PostToolUse/detect-debugging-loop.sh)

## When to Stop Entirely

If **5 iterations** haven't converged, the problem is likely:

| Category | Indicators | Action |
|----------|-----------|--------|
| **Misframed** | Different approaches fail for different reasons | Step back, reframe with human |
| **Missing information** | Keep hitting "unknown" states | Ask human for context |
| **Beyond current capability** | Approaches are theoretically sound but don't work | Acknowledge limit, hand back |
| **Environmental** | Code looks right, behavior is wrong | Check config, dependencies, runtime |

**In any case**: Stop, surface what you know, hand back to human.

## Relationship to Other Hooks

| Hook | Trigger | Connection |
|------|---------|------------|
| **detect-debugging-loop.sh** | 3 consecutive failures | Heuristic for iteration overrun, invokes Wolf |
| **detect-frustration.sh** | Human frustration signals | Often caused by iteration overrun |
| **speculative-fix-prevention.sh** | Fix without evidence | Prevents iteration waste during active debugging |

These hooks work together to prevent iteration overrun before it degrades decision quality.

## Quick Reference

| After N iterations | Action |
|--------------------|--------|
| **3** | Self-assessment checkpoint |
| **5** | Stop, surface findings, hand back |
| **Any** | Context degradation signals → counter-pattern |
