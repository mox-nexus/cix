# How to Recognize and Break Debugging Loops

When working with AI coding assistants, debugging loops waste time and often introduce new bugs. This guide shows you how to spot the signs and break the cycle.

## What the Hooks Detect

The `collab-scaffolds` plugin watches for two failure patterns:

**Debugging loop detection** (`detect-debugging-loop.sh`):
- Tracks consecutive Bash command failures in `/tmp/claude-mrwolf-state-${PPID}`
- After 3 consecutive failures, triggers Mr. Wolf protocol
- Looks for error patterns: "error", "failed", "exception", "not found", "permission denied"
- Resets counter on success

**Speculative fix prevention** (`speculative-fix-prevention.sh`):
- Activates when 2+ consecutive failures have occurred
- Warns when you edit files during active debugging
- Requires evidence-gathering before code changes
- Shares state file with loop detection

## Signs You're in a Loop

Watch for these patterns:

**1. Same error keeps appearing**
```
attempt 1: "FileNotFoundError: config.json"
attempt 2: "FileNotFoundError: /app/config.json"
attempt 3: "FileNotFoundError: ./config/settings.json"
```
The error type hasn't changed, only slight variations.

**2. Solution complexity is growing**

Started with "add a check" and now you're refactoring the entire validation system. If the fix keeps expanding, you're not converging on the root cause.

**3. Trying slight variations**

"Let me try imports in a different order" or "Maybe if I rename this variable". Random perturbations without a hypothesis means you're guessing.

**4. Referencing old context**

"Earlier we tried X" or "Remember when we changed Y". If you're maintaining a mental history of attempts rather than diagnosing the current state, you're looping.

## How to Break Loops

### 1. Invoke Wolf Protocol

When the debugging loop hook fires, the protocol is:

```
1. STOP current approach
2. Tell user: "This isn't converging. Bringing in Mr. Wolf."
3. Spawn the mrwolf agent
4. Do not continue debugging yourself
```

Mr. Wolf systematically breaks down the problem:
- Restate the actual goal (not "fix this error" but "what are we trying to accomplish?")
- Classify problem type (configuration, logic, environment, interface)
- Break into verifiable components
- Test one thing at a time

### 2. Gather Evidence First

Before editing code during active debugging:

**Read the actual error output:**
```bash
# Not "it says file not found"
# Read the full stack trace
cat error.log | tail -20
```

**Check runtime state:**
```bash
# What files actually exist?
ls -la /path/to/directory
# What's the actual config?
cat config.json
# What's running?
ps aux | grep process_name
```

**Form a hypothesis:**
Write down what you think is wrong and why before changing code. "I believe the config path is incorrect because the error shows '/app/config.json' but the file is at '/config/app.json'."

### 3. Use `/clear` for Fresh Context

Long threads accumulate failed approaches. Start fresh:

```
/clear
[Restate the goal]
[Share only relevant diagnostic evidence]
```

This prevents "we already tried that" bias and resets to first principles.

### 4. Spawn a Subagent

For isolated investigation without polluting main context:

```
Task(
  subagent_type="investigation",
  prompt="Analyze why config loading fails. Do not edit code."
)
```

The subagent investigates in a clean context, returns findings, then exits.

### 5. Ask for Constraints

If you're hitting the same wall repeatedly, you may be missing information:

"What I know: X, Y, Z. What I don't know: Is there a firewall rule? Are there environment-specific configs? What's the actual deployment structure?"

Humans have context you don't. Ask.

## Why This Matters

Research shows iterative debugging without convergence degrades code quality:

**Shukla et al. (2025)**: Vulnerability density increases from 2.1 to 6.2 per 1K LOC over 5 iterations. Each refinement adds code without removing prior problems.

**Effect**: 37.6% vulnerability increase when iteration doesn't converge.

The loop itself is the problem. Breaking it early prevents compounding technical debt.

## When to Use Each Strategy

| Situation | Strategy |
|-----------|----------|
| 3+ consecutive failures | Wolf Protocol (automatic) |
| 2+ failures + about to edit code | Gather evidence first |
| Thread is long and confused | `/clear` and restate |
| Need focused investigation | Spawn subagent |
| Keep hitting unknown constraint | Ask human |

## Opt-Out

If you need to disable the hooks temporarily:

```bash
export SKIP_MRWOLF_HOOKS=1      # Disables debugging loop detection
export SKIP_EVIDENCE_HOOKS=1    # Disables speculative fix prevention
```

Use sparingly. The hooks catch real problems.
