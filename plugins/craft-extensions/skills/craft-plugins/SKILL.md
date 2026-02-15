---
name: craft-plugins
description: "Crafts Claude Code extensions (skills, commands, agents, hooks, MCP servers). Use when: creating any Claude Code extension component, authoring skill content, deciding between component types, or combining components into a plugin."
---

# Build Plugin

Claude Code extensions for effective human-AI collaboration.

> **Composes with official skills.** This skill adds quality methodology. For authoritative templates and schemas:
>
> | Building... | Use skill |
> |-------------|-----------|
> | Plugin structure | `plugin-dev:plugin-structure` |
> | Skill format | `plugin-dev:skill-development` |
> | Hook events | `plugin-dev:hook-development` |
> | Agent schema | `plugin-dev:agent-development` |
> | Command template | `plugin-dev:command-development` |
> | MCP server | `plugin-dev:mcp-integration` |
> | SDK app | `agent-sdk-dev:new-sdk-app` |

---

## Contents

- [Component Decision](#component-decision)
- [Skill Authoring](#skill-authoring)
- [Component Reference](#component-reference)
- [Composition Patterns](#composition-patterns)
- [Validation Checklist](#validation-checklist)
- [Quality Assurance](#quality-assurance)

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

### Intent-Driven Activation

Trigger on **user goals**, not tool names.

| Wrong | Right |
|-------|-------|
| "Use when: Midjourney prompting" | "Use when: creating artwork, images, visual assets" |
| "Use when: using pytest" | "Use when: writing tests, test-driven development" |
| "Use when: running kubectl" | "Use when: deploying to Kubernetes, managing clusters" |

**The pattern:** `[Domain/activity] + [user goals/outcomes]`, NOT `[Tool name] + [tool-specific actions]`.

Users think in goals ("I need an image"), not tools ("I need Midjourney"). Intent-driven activation catches synonyms and related tasks that tool-specific descriptions miss.

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

### Recipe vs Workflow

Skills that perform multi-step operations have two modes. Know which you need.

| Recipe | Workflow |
|--------|----------|
| Static checklist — user executes steps | Claude-driven — Claude infers, acts, verifies |
| User drives, skill is reference | Claude drives, user approves at checkpoints |
| Errors discovered at step N | Prerequisites caught at step 0 |
| Good for: simple installs, one-time setup | Good for: stateful operations, security, deployment |

**The workflow pattern:**
1. **Infer** — Check OS, existing state, prerequisites (read-only)
2. **Assess** — Report current state to user
3. **Choose** — Present numbered options (user replies with digit)
4. **Plan** — Show exact steps before any changes
5. **Execute** — Each step with explicit approval
6. **Verify** — Run checks, diagnose failures, offer fixes

**Anti-pattern:** Using a recipe when a workflow is needed. If the skill performs state-changing actions, prefers the workflow pattern — Claude can check prerequisites, detect errors early, and handle failures that a static checklist cannot.

### Core Rules (for State-Changing Skills)

Skills that modify files, configs, or system state need explicit behavioral constraints:

```markdown
## Core rules
- Require explicit approval before any state-changing action
- Infer OS, existing state, prerequisites before asking user
- Show exact command before executing
- Stop on unexpected output and ask for guidance
- Numbered choices so user can reply with a single digit
```

Without core rules, Claude may execute destructive operations without confirmation or skip prerequisite checks.

### Fail-Safe Defaults

Skills that generate configs, templates, or security settings must default to the most restrictive option.

```markdown
# Bad — permissive default, user must restrict
Default: allow all domains, user removes unsafe ones

# Good — minimal default, user expands consciously
Default: allow only required domains (2)
User adds domains as needed, each addition is a decision
```

Every permission expansion is a conscious user decision. This applies to: network allowlists, file access, API scopes, CI permissions, deployment targets.

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
| **Jargon description** | Won't activate for real users | Use intent language, test against user queries |
| **Recipe for stateful ops** | Errors caught late, no recovery | Use workflow pattern (infer → plan → execute → verify) |
| **Permissive defaults** | Security/access risks | Default to minimal, user expands |
| **Missing limitations** | Overclaiming erodes trust | Add "does NOT protect against" section |
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

### Cross-Skill References

Skills that complement each other should say so. Users who need one often need the other.

```yaml
# In skill A's description:
description: "Audits host security. Use when: security review. Works with: sandbox skill for OS-level process containment."

# In skill B's description:
description: "Restricts process access. Use when: hardening. After running: healthcheck for full posture."
```

Without cross-references, users discover complementary skills by accident or not at all.

---

## Validation Checklist

### Skills
- [ ] Description includes "Use when:" triggers
- [ ] Description uses intent language, not implementation jargon
- [ ] Description tested: "Would a user saying X activate this?"
- [ ] SKILL.md < 500 lines
- [ ] References one level deep
- [ ] Files > 100 lines have TOC
- [ ] No explaining what Claude already knows
- [ ] Multi-step operations use workflow pattern (not recipe)
- [ ] State-changing skills have Core Rules section
- [ ] Config-generating skills use fail-safe (minimal) defaults
- [ ] Security/reliability claims have Limitations section
- [ ] Complementary skills cross-referenced

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

## Quality Assurance

After building, validate through the eval → optimize cycle.

### Quick Evaluation

```
"Evaluate plugins/my-extension"
```

The evaluator agent checks all 7 quality gates and returns a verdict:
- **PASS**: ≥ 17/21, no gate below 2 → ready to ship
- **NEEDS WORK**: ≥ 12/21, fixable issues → run optimizer
- **NOT READY**: < 12/21 or fundamental problems → rethink approach

### Optimization

If evaluator returns NEEDS WORK:

```
"Optimize plugins/my-extension based on the evaluation"
```

The optimizer applies minimal, targeted fixes in priority order (critical → major → minor) and escalates domain decisions to you.

### Full Quality Loop

For iterative tuning:

```
"Run quality loop on plugins/my-extension until it passes"
```

Runs eval → optimize → re-eval cycles (max 3 iterations) until passing or escalation.

| Situation | Action |
|-----------|--------|
| Just built new extension | Run evaluator |
| Evaluator says NEEDS WORK | Run optimizer |
| After optimizer fixes | Re-run evaluator |
| Want full automated tuning | Run quality loop |
| Auditing existing plugins | Run evaluator on each |

---

## References

| Need | Load |
|------|------|
| Progressive disclosure in depth | [progressive-disclosure.md](references/progressive-disclosure.md) |
| Checklists and feedback loops | [checklists-and-loops.md](references/checklists-and-loops.md) |
| Degrees of freedom guidance | [degrees-of-freedom.md](references/degrees-of-freedom.md) |
| Anti-patterns in depth | [anti-patterns.md](references/anti-patterns.md) |
| OTel instrumentation for extensions | [observability.md](references/observability.md) |
| Evidence-based skill research | [evidence-workflow.md](references/evidence-workflow.md) |
