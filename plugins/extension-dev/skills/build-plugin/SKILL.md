---
name: build-plugin
description: "Builds Claude Code extensions (skills, commands, agents, hooks, MCP servers). Use when: creating any Claude Code extension component, authoring skill content, deciding between component types, or combining components into a plugin."
---

# Build Plugin

Claude Code extensions for effective human-AI collaboration.

**Structure/templates:** See `plugin-dev` skill.

---

## Contents

- [Component Decision](#component-decision)
- [Skill Authoring](#skill-authoring)
- [Component Reference](#component-reference)
- [Composition Patterns](#composition-patterns)
- [Validation Checklist](#validation-checklist)

---

## Component Decision

| Need | Component | Why |
|------|-----------|-----|
| Teach Claude a workflow | **Skill** | Activated by description matching |
| Give Claude external access | **MCP** | Tools + resources + prompts |
| Run code on events | **Hook** | Pre/post triggers for Stop/Edit/Bash/etc. |
| User-invoked action | **Command** | Slash commands like `/review` |
| Orchestrate complex task | **Agent** | Multi-step reasoning with tool access |

### Skill vs MCP

| Use **Skill** when | Use **MCP** when |
|-------------------|------------------|
| Teaching Claude domain knowledge | Claude needs external data/actions |
| Workflow guidance and patterns | Connecting to APIs, databases, services |
| Decision frameworks | Real-time data access |
| No external dependencies | Tool invocation required |

**Combine them:** MCP provides tools, skill teaches how to use them effectively.

---

## Skill Authoring

Skills are the core extension mechanism. Get these patterns right.

### Progressive Disclosure

Context window is a public good. Every token must justify its presence.

| Level | Content | Loaded |
|-------|---------|--------|
| **Metadata** | name + description | Always (system prompt) |
| **SKILL.md body** | Core instructions | When activated |
| **references/** | Deep detail | On demand |

**Rules:**
- Metadata: 1-2 sentences with "Use when:" triggers
- Main content: < 500 lines
- References: One level deep only. TOC if > 100 lines.

### Description Writing

Write for Claude's pattern matching. Third person. Include triggers.

```yaml
# Good
description: "Analyzes CSV files for statistical patterns. Use when: user asks to 'analyze data', 'find patterns', 'run stats', or uploads .csv files."

# Bad - too vague
description: "Helps with data."

# Bad - missing triggers  
description: "Sophisticated statistical analysis system."

# Bad - wrong voice
description: "I can help you analyze your data."
```

### Naming Conventions

Use **gerund form** (verb-ing):

| Good | Bad |
|------|-----|
| building-extensions | extension-helper |
| analyzing-data | data-utils |
| processing-pdfs | pdf-tools |

**Avoid:** helper, utils, tools, manager, handler (too vague).

### Degrees of Freedom

Match constraint level to the task:

| Freedom | Use When | Pattern |
|---------|----------|---------|
| **High** | Multiple valid approaches | "Consider...", principles, guidelines |
| **Medium** | Preferred pattern, variation OK | "Default to X, adjust for Y" |
| **Low** | Fragile operations, consistency critical | "ALWAYS...", exact steps, checklists |

### Feedback Loops

For operations with observable success/failure:

```markdown
1. Make changes
2. Validate: `command --check`
3. If issues: fix and return to step 2
4. Only proceed when validation passes
```

### Checklists

For complex multi-step workflows where steps matter:

```markdown
## Before Starting
- [ ] Dependencies installed
- [ ] Config file exists
- [ ] Access tokens valid
```

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Over-explaining** | Token waste, Claude already knows | Assume Claude is smart |
| **Too many options** | Decision paralysis | Default + escape hatch |
| **Deep nesting** | Files get skipped | One level deep max |
| **Vague description** | Poor activation | Include "Use when:" |
| **No TOC** | Long files unreadable | Add TOC for > 100 lines |
| **Time-sensitive info** | Goes stale | Use "deprecated patterns" section |

---

## Component Reference

### Skills

**Activation:** Description determines when skill loads.

```yaml
description: "Analyzes Figma files and generates handoff docs. Use when: user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'."
```

**Debugging activation:** Ask Claude "When would you use the [skill name] skill?" It will quote the description.

**Gotchas:**
- Description missing "Use when:" = poor activation
- SKILL.md > 500 lines = context bloat
- No TOC on files > 100 lines = Claude skips content

### Agents

Autonomous multi-step reasoning with tool access.

```markdown
# Agent Name

One-line purpose.

## Objective
What this agent accomplishes.

## Approach
How it reasons through the task.

## Tools Available
What it can use.

## Constraints
Boundaries and limits.
```

**Patterns:** Single-shot | Loop | Pipeline | Orchestrator

**Observability:**
```
Observation: [what I see]
Conclusion: [what I infer]
Reasoning: [why]
Next: [what I'll do]
```

### Hooks

Code that runs on Claude Code events.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit",
      "command": "python /path/to/hook.py"
    }]
  }
}
```

**Events:** PreToolUse | PostToolUse | Stop

**Gotchas:**
- Suggest, don't block: `{"decision": "allow", "message": "Consider X."}`
- Always provide escape hatch
- Exit code 0 always (non-zero kills hook system)
- 60s timeout default

### Commands

User-invoked slash commands.

```markdown
---
name: review
description: Reviews code against style guide
allowed-tools: Read, Grep, Glob
---

# /review

## Instructions
1. Find files to review
2. Check against [guidelines]
3. Report issues with line numbers
```

**Patterns:**
- Stateless (no side effects without confirmation)
- Checkpoints before irreversible actions
- Support --dry-run where applicable

### MCP Servers

External tool access for Claude.

| Build MCP | Don't Build MCP |
|-----------|-----------------|
| External API integration | Static knowledge (use skill) |
| Database access | Workflow guidance (use skill) |
| Real-time data | One-off scripts (use command) |
| Reusable tool suite | Project-specific automation (use hook) |

**Bundle pattern:** Pair MCP with skill that teaches usage.

---

## Composition Patterns

### Skill + MCP

MCP provides tools. Skill teaches workflow.

```
User: "Set up a new project in Linear"
       ↓
[linear-workflows skill activated]
       ↓
Skill guides: "Create project → Add default labels → Set up views"
       ↓
[Linear MCP tools called]
```

### Agent + Hooks

Agent does work. Hooks enforce guardrails.

### Command + Agent

Command triggers. Agent executes.

---

## Validation Checklist

### Skills
- [ ] Description includes "Use when:" triggers
- [ ] SKILL.md < 500 lines
- [ ] References one level deep
- [ ] Files > 100 lines have TOC
- [ ] No explaining what Claude already knows

### Agents
- [ ] Clear objective and constraints
- [ ] Reasoning visible in output
- [ ] Tools listed and bounded

### Hooks
- [ ] Suggests, doesn't block (escape hatch exists)
- [ ] Returns exit 0 always
- [ ] Handles timeout gracefully

### Commands
- [ ] Stateless or confirms before side effects
- [ ] Checkpoints before irreversible

### MCP
- [ ] Bundled skill teaches usage
- [ ] Rich errors (what + why + fix)
- [ ] Bounded output size

---

## References

| Need | Load |
|------|------|
| Progressive disclosure in depth | [progressive-disclosure.md](references/progressive-disclosure.md) |
| Checklists and feedback loops | [checklists-and-loops.md](references/checklists-and-loops.md) |
| Degrees of freedom guidance | [degrees-of-freedom.md](references/degrees-of-freedom.md) |
| Anti-patterns in depth | [anti-patterns.md](references/anti-patterns.md) |
