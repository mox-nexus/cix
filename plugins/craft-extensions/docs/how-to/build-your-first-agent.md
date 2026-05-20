# How to Build Your First Agent

A task-oriented guide for building a Claude Code agent using craft-hub methodology.

---

## Contents

- [When to Use an Agent](#when-to-use-an-agent)
- [Write the Motivation Section](#write-the-motivation-section)
- [Define Objective and Constraints](#define-objective-and-constraints)
- [Select Tools](#select-tools)
- [Handle the Isolation Principle](#handle-the-isolation-principle)
- [Write the Agent File](#write-the-agent-file)
- [Run the Evaluator](#run-the-evaluator)

---

## When to Use an Agent

Agents are reasoning entities. Skills are knowledge. The distinction matters for choosing the right component.

| Use an **agent** when | Use a **skill** when |
|----------------------|---------------------|
| The task needs multi-step reasoning | You're teaching Claude a workflow or decision framework |
| Claude needs to read, analyze, and produce structured output | The knowledge applies across many different tasks |
| You want a specialized persona (reviewer, optimizer, auditor) | No specialized execution is needed |
| The task benefits from focused scope and limited tools | Claude just needs to know something |

Agents are invoked as subagents -- Claude spawns them to do a specific job and gets back structured output. They run in isolation with their own tool set and context.

---

## Write the Motivation Section

This is the single most important difference between a good agent and a mediocre one.

Skills that explain WHY produce understanding. Rules produce compliance. The same applies to agents, but even more so -- agents need to make judgment calls in situations you didn't anticipate.

### Rules vs motivation

| Approach | Prompt | What happens |
|----------|--------|--------------|
| **Rule** | "Don't give generic advice" | Agent avoids a mental list of "generic" phrases, finds new ways to be generic |
| **Motivation** | "Generic advice wastes everyone's time. If an expert in this domain wouldn't learn something new, you haven't done your job." | Agent reaches for specificity because it understands what specificity is for |

### Write the motivation section

Put it before the objective. It answers: why does this agent exist, and what does it value?

```markdown
## Motivation

Code review exists to catch what tests miss: design problems, 
maintainability traps, and assumptions that will bite later. A review 
that says "looks good" is worthless. A review that finds the one 
subtle issue is worth the entire time investment.
```

The test: after reading the motivation, if the agent encounters a situation your prompt doesn't cover, would it know what to do? If yes, you gave it values. If no, you gave it rules.

---

## Define Objective and Constraints

### Objective

One clear statement of what the agent accomplishes. Not how -- just what.

```markdown
## Objective

Review code changes for design problems, maintainability risks, and 
non-obvious bugs. Produce a structured assessment with specific 
file/line references.
```

### Constraints

Boundaries that keep the agent focused. These ARE low-freedom -- agents working in isolation need firm guardrails to prevent scope creep.

```markdown
## Constraints

- Review only the files in the diff. Do not explore the broader codebase.
- Flag issues. Do not fix them -- the user decides what to change.
- If you're unsure whether something is a problem, say so explicitly.
- Max 10 findings. Prioritize by severity.
```

### Approach (optional but recommended)

How the agent reasons through the task. This is where you teach the agent's thinking process.

```markdown
## Approach

1. Read the full diff to understand the change as a whole
2. For each file, check:
   - Does the change do what the commit message says?
   - Are there edge cases not handled?
   - Would this be clear to someone seeing it for the first time?
3. Rank findings by severity (blocking > important > minor)
```

---

## Select Tools

Agents get an explicit tool set. Give them what they need and nothing more.

### Available tools

The `tools` field in frontmatter controls what the agent can access:

```yaml
tools: ["Read", "Glob", "Grep", "Bash"]
```

### Tool selection principles

| Principle | Why |
|-----------|-----|
| Minimum viable set | Every extra tool is a distraction. A reviewer doesn't need Write or Edit. |
| Match to objective | Read-only agents get read-only tools. Agents that fix things get Edit/Write. |
| Bash with caution | Bash can do anything. If you include it, constrain usage in the agent prompt. |

### Common tool sets

| Agent type | Tools | Rationale |
|------------|-------|-----------|
| Reviewer / evaluator | Read, Glob, Grep, Bash | Needs to read and search, not modify |
| Optimizer / fixer | Read, Edit, Write, Glob, Grep, Bash | Needs to make changes |
| Analyzer | Read, Glob, Grep | Read-only, no shell access needed |

### Skills

Agents can also load skills:

```yaml
skills: craft-hub
```

This gives the agent access to skill knowledge during execution. Use this when the agent needs domain expertise from an existing skill.

---

## Handle the Isolation Principle

This is the most common source of agent bugs.

**Subagents do NOT inherit the parent conversation.** When Claude spawns your agent, it starts with a blank slate. The agent sees only:
- Its own prompt (the agent `.md` file)
- Whatever context is explicitly passed when it's invoked
- Files it reads with its tools

### What this means in practice

The parent Claude must pass everything the agent needs:

```
"Use the evaluator agent to review plugins/craft-extensions. 
Here is the plugin structure: [structure]. 
Focus on activation quality."
```

If the parent says "review what we were just discussing" without providing the actual content, the agent has no idea what "we were just discussing" refers to.

### Design for isolation

When writing your agent, think about what context it needs to do its job:

| Context type | How it arrives |
|-------------|---------------|
| File paths | Passed in the invocation message |
| File contents | Agent reads them with its tools |
| Previous analysis | Passed in the invocation message |
| User preferences | Included in the agent prompt itself |

### Output format

Define a clear output format so the parent conversation can parse and use the results:

```markdown
## Output Format

Return your review as:

## Code Review: [file or PR name]

### Findings

| # | Severity | File:Line | Issue | Suggestion |
|---|----------|-----------|-------|------------|

### Summary

[One paragraph assessment]
```

Structured output enables handoffs between agents and makes results usable by the orchestrating conversation.

---

## Write the Agent File

Agents live in `agents/` as markdown files. Here's the complete structure:

```markdown
---
name: code-reviewer
description: |
  Reviews code for design problems and maintainability risks. 
  Use when: reviewing a PR, checking code quality, pre-merge review.
model: sonnet
color: blue
tools: ["Read", "Glob", "Grep", "Bash"]
---

You are a code reviewer who values finding real problems over 
covering every line.

## Motivation

[Why this agent exists and what it values]

## Objective

[What it accomplishes]

## Approach

[How it reasons through the task]

## Constraints

[Boundaries and limits]

## Output Format

[Structured output template]
```

### Frontmatter fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Kebab-case identifier |
| `description` | Yes | Include "Use when:" triggers |
| `model` | No | `sonnet`, `opus`, or `inherit` (default: inherit from parent) |
| `color` | No | Terminal color for the agent's output |
| `tools` | Yes | Array of tool names |
| `skills` | No | Skills to load |

### The opening line

The first line after frontmatter sets the agent's identity. Make it a value statement, not a job description:

```markdown
# Good -- identity with values
You are a ruthless quality reviewer who values substance over appearance.

# Less good -- job description
You are an agent that reviews code quality.
```

---

## Run the Evaluator

Agents get evaluated alongside the rest of the plugin. The evaluator checks agent-specific gates:

### Agent-specific checks

| Gate | What it checks for agents |
|------|--------------------------|
| Content Quality | Does the motivation add judgment, not just rules? |
| Transparency | Does the output format show reasoning? |
| Control | Can the user override or redirect? |
| Activation | Does the description trigger on the right requests? |
| Expert Value | Would an expert reviewer benefit from this agent's approach? |

### Run it

```
"Evaluate plugins/my-plugin"
```

### Common agent evaluation failures

| Problem | Symptom | Fix |
|---------|---------|-----|
| No motivation section | Agent gives generic output | Add motivation explaining why quality matters |
| Too many tools | Agent wanders off task | Remove tools it doesn't need |
| No output format | Parent can't use results | Add structured output template |
| Vague description | Agent doesn't activate or over-activates | Add specific "Use when:" triggers |
| Rules without reasons | Agent follows letter, not spirit | Rewrite rules as motivated constraints |

---

## What's Next

- **Add a companion explanation doc:** Create `docs/explanation/your-agent.md` explaining the design rationale. This helps future maintainers understand why the agent is built this way.
- **Compose with other components:** Pair agents with commands (command triggers, agent executes) or hooks (agent does work, hook enforces guardrails).
- **Multi-agent orchestration:** If you're building multiple agents that work together, see the orchestration reference in craft-hub.
