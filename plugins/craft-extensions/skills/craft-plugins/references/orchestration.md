# Orchestration Patterns

Deep reference for multi-agent prompt orchestration in Claude Code.

---

## Contents

- [Task Tool Reference](#task-tool-reference)
- [Agent Definition Schema](#agent-definition-schema)
- [Execution Patterns](#execution-patterns)
- [Context Passing Templates](#context-passing-templates)
- [Background Execution](#background-execution)
- [Real-World Pipelines](#real-world-pipelines)
- [Debugging Agent Activation](#debugging-agent-activation)

---

## Task Tool Reference

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subagent_type` | string | Yes | Agent type or `plugin:agent-name` |
| `prompt` | string | Yes | Task description for the agent |
| `description` | string | Yes | Short label (3-5 words) |
| `model` | string | No | `sonnet`, `opus`, `haiku`, or `inherit` (default) |
| `run_in_background` | boolean | No | `true` for async execution (default: false) |
| `resume` | string | No | Agent ID to continue previous work |

### Built-in Agent Types

| Type | Tools | Model | Use For |
|------|-------|-------|---------|
| `Explore` | Read, Grep, Glob | haiku | Fast codebase search, read-only analysis |
| `Plan` | Read, Grep, Glob | inherit | Pre-planning research |
| `general-purpose` | All | inherit | Complex multi-step tasks |
| `Bash` | Bash only | inherit | Terminal commands |

### Custom Agent Types

Reference as `plugin-name:agent-name` (e.g., `craft-rhetoric:editor`).

Agents defined in `.claude/agents/` are referenced by filename without extension.

---

## Agent Definition Schema

### Frontmatter (Complete)

```yaml
---
name: agent-identifier          # Required. Lowercase, hyphens, 3-50 chars
description: |                  # Required. Activation trigger
  [Role]. Use when: [triggers].

  <example>
  Context: [Situation]
  user: "[Request]"
  assistant: "[Response with Task tool mention]"
  <commentary>[Why triggered]</commentary>
  </example>

model: sonnet                   # Optional. sonnet|opus|haiku|inherit
tools: Read, Grep, Glob        # Optional. Comma-separated allowlist
disallowedTools: Edit, Bash     # Optional. Comma-separated denylist
skills: writing, aesthetic      # Optional. Skills injected at startup
permissionMode: default         # Optional. default|acceptEdits|plan|bypassPermissions
maxTurns: 15                    # Optional. Max agentic turns
color: cyan                     # Optional. UI indicator
---
```

### System Prompt Body

The markdown body below frontmatter becomes the agent's system prompt.

```markdown
You are a [role].

## Objective
[What this agent accomplishes]

## Approach
[How it reasons — not step-by-step instructions, but principles]

## Constraints
[Boundaries and limits]

## Collaboration
[Who provides input, who consumes output]

## Output Format
[What the output looks like — enables structured handoffs]
```

### Tool Access Patterns

**Principle of least privilege** — give agents only what they need.

```yaml
# Read-only analysis
tools: Read, Grep, Glob

# Code modification
tools: Read, Write, Edit, Grep, Glob

# Full access (rare — use for general-purpose)
tools: "*"
```

**Denylist pattern** (everything except):
```yaml
disallowedTools: Task, Bash
```

---

## Execution Patterns

### Pattern 1: Sequential Pipeline

```
Parent Claude
    │
    ├─ Task(A) ─── wait ─── result_A
    │                           │
    ├─ Task(B, context=result_A) ── wait ── result_B
    │                                          │
    └─ Task(C, context=result_B) ── wait ── result_C
```

**Prompt template for Stage B:**

```markdown
Based on the following analysis from the previous stage:

---
{result_A}
---

Now perform [task B]. Focus on:
- [constraint 1]
- [constraint 2]

Output format:
[structured format for stage C to consume]
```

### Pattern 2: Parallel Fan-Out

```
Parent Claude
    │
    ├─ Task(A, bg=true) ──┐
    ├─ Task(B, bg=true) ──┼── all running
    └─ Task(C, bg=true) ──┘
                           │
                    TaskOutput × 3
                           │
                    Synthesize results
```

**When to parallelize:**
- Tasks read different parts of the codebase
- Tasks analyze different dimensions of the same data
- Tasks are fully independent (no shared state)

**When NOT to parallelize:**
- Task B needs Task A's output
- Tasks modify the same files (race conditions)
- Total parallel agents > 4 (diminishing returns)

### Pattern 3: Checkpoint Aggregation

```
Phase 1 (Discovery):
  Task(search_frontend, bg=true)
  Task(search_backend, bg=true)
  → CHECKPOINT 1: Merge findings, resolve conflicts

Phase 2 (Analysis):
  Task(analyze_patterns, context=checkpoint_1, bg=true)
  Task(analyze_gaps, context=checkpoint_1, bg=true)
  → CHECKPOINT 2: Synthesize analysis

Phase 3 (Action):
  Task(implement_fixes, context=checkpoint_2)
  → Final result
```

**Checkpoint prompt template:**

```markdown
## Checkpoint: Phase N Aggregation

### Agent A found:
{agent_a_output}

### Agent B found:
{agent_b_output}

### Conflicts to resolve:
[Parent Claude identifies contradictions]

### Cleaned context for Phase N+1:
[Resolved, deduplicated findings]
```

### Pattern 4: Conditional Routing

```
Task(evaluator, "Check quality of X")
  → result

IF result.verdict == "PASS":
  → done
ELIF result.verdict == "NEEDS WORK":
  → Task(optimizer, context=result.issues)
  → Task(evaluator, "Re-check") ← loop
ELSE:
  → escalate to user
```

**The evaluator output structure that enables routing:**

```markdown
## Evaluation: [subject]

### Verdict: PASS | NEEDS WORK | NOT READY

### Issues (ordered by severity)
1. CRITICAL: [issue] → [suggested fix]
2. MAJOR: [issue] → [suggested fix]
3. MINOR: [issue] → [suggested fix]
```

---

## Context Passing Templates

### Template 1: Pipeline Handoff

```markdown
# Task for [Agent B]

## Context from [Agent A]
{agent_a_structured_output}

## Your Task
[What Agent B should do with this context]

## Constraints
- [Boundary 1]
- [Boundary 2]

## Output Format
[Structure that Agent C will consume]
```

### Template 2: Parallel Analysis Prompt

```markdown
# Task: Analyze [Dimension X]

## Scope
- Files: {file_patterns}
- Focus: [specific aspect]

## What to Look For
- [Pattern 1]
- [Pattern 2]

## Output Format
### Findings
- [finding]: [evidence with file:line]

### Severity
- CRITICAL: [count]
- MAJOR: [count]
- MINOR: [count]
```

### Template 3: Synthesis After Parallel

```markdown
# Synthesis Task

## Input from Agent A (Dimension X)
{agent_a_output}

## Input from Agent B (Dimension Y)
{agent_b_output}

## Your Task
1. Identify themes across both analyses
2. Flag contradictions
3. Produce unified recommendation

## Output Format
### Unified Findings
[merged, deduplicated]

### Contradictions
[where agents disagreed, with resolution]

### Recommendation
[actionable next steps]
```

---

## Background Execution

### Foreground (Blocking)

```
Parent spawns agent → blocks → agent runs → result returns → parent continues
```

- Agent CAN prompt user (AskUserQuestion)
- Agent CAN request tool permissions interactively
- Use for: tasks needing human input mid-execution

### Background (Async)

```
Parent spawns agent (bg=true) → parent continues immediately
  └─ agent runs independently
     └─ result available via TaskOutput
```

- Agent CANNOT prompt user
- Tool permissions must be pre-approved
- Use for: independent, self-contained work

### Resume Parameter

Continue a previous agent's work with full context:

```
Initial run:
  Task(reviewer, "Review auth module") → agent_id: abc123

Later:
  Task(reviewer, "Now check the API module too",
       resume="abc123")
```

The resumed agent sees its FULL prior conversation + the new prompt. No context loss.

---

## Real-World Pipelines

### Writing Pipeline

```
1. content-strategist
   Input: topic, audience, existing materials
   Output: outline, section structure, tone guidance
   ↓
2. narrator (sequential — needs outline)
   Input: outline + voice profile (via skills)
   Output: draft narrative
   ↓
3. editor (sequential — needs draft)
   Input: draft + writing principles (via skills)
   Output: polished prose
   ↓
4. rhetorician + voice-critic (PARALLEL — both need polished draft)
   4a: rhetorician → argument quality report
   4b: voice-critic → voice fidelity report
   ↓
5. Decision gate:
   Both pass → done
   Either fails → narrator revises (loop to step 2)
```

### Quality Assurance Pipeline (from craft-extensions)

```
1. evaluator
   Input: plugin directory path
   Output: gate scores + verdict
   ↓
2. IF verdict == "NEEDS WORK":
     optimizer
     Input: evaluator output (issues list)
     Output: targeted fixes applied
     ↓
3. evaluator (re-check)
   Input: same plugin path
   Output: updated scores
   ↓
4. Repeat max 3 times or until PASS
```

### Research Pipeline (parallel discovery)

```
1. Parallel discovery:
   Task(explore_A, "Search for X patterns", bg=true)
   Task(explore_B, "Search for Y patterns", bg=true)
   → wait for both

2. Synthesis:
   Task(general-purpose, "Synthesize findings:
     Agent A found: {a_output}
     Agent B found: {b_output}
     Produce unified analysis.")

3. Action:
   Task(implementation_agent, "Implement based on:
     {synthesis_output}")
```

---

## Debugging Agent Activation

### Agent Never Fires

**Check description triggers:**
```yaml
# Ask Claude: "When would you use the [agent-name] agent?"
# Claude will quote the description. If it doesn't match
# your intent, rewrite the description.
```

**Common causes:**
- Description missing "Use when:" with specific verbs
- Description uses implementation terms (tool names) not intent terms (user goals)
- No `<example>` blocks showing trigger scenarios
- Description too vague ("Helps with code")

### Agent Fires at Wrong Time

**Common causes:**
- Description too broad ("Use when: writing anything")
- Examples overlap with another agent's domain
- Missing negative triggers ("NOT for simple typo fixes")

### Agent Produces Poor Results

**Common causes:**
- Task prompt missing critical context (isolation principle)
- Agent has wrong tool access (needs Write but only has Read)
- Model too weak for the task (haiku on architectural reasoning)
- Skills not specified (agent lacks domain knowledge)
- System prompt specifies HOW instead of WHAT

### Context Too Large

**Symptoms:** Slow responses, agent loses focus, token budget warnings.

**Fixes:**
1. Move stable knowledge to skills (loaded once, not per-prompt)
2. Summarize prior agent output before passing
3. Pass only relevant excerpts, not full output
4. Use structured output formats (parse and extract)

---

## Sources

- [Claude Code subagent documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Agent Teams (experimental)](https://docs.anthropic.com/en/docs/claude-code/agent-teams)
- Real-world orchestration patterns from CIX ecosystem plugins
