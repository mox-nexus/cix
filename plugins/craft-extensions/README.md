# craft-extensions

Build extensions that enable effective human-AI collaboration.

## Skills

| Skill | Purpose | Use When |
|-------|---------|----------|
| **craft-plugins** | Claude Code extensions (skills, commands, agents, hooks, MCP) | Creating any Claude Code component |
| **craft-tools** | Software tools — CLIs, APIs, libraries | Creating CLIs, APIs, packages, or improving tool DX |

## Relationship

```
craft-tools (general patterns)
       ↓
craft-plugins (Claude Code specifics)
       ↓
plugin-dev (templates & structure)
```

- **craft-tools:** Universal patterns (CLI DX, API design, progressive disclosure, packaging)
- **craft-plugins:** Claude Code specific (skills, agents, hooks, commands, MCP, composition)
- **plugin-dev:** Templates and directory structure (referenced, not duplicated)

## When to Use

| Need | Use |
|------|-----|
| Creating a Claude Code skill | craft-plugins |
| Creating a Claude Code agent | craft-plugins |
| Creating a hook or command | craft-plugins |
| Building an MCP server | craft-plugins |
| Building a CLI tool | craft-tools |
| Building an API | craft-tools |
| Improving CLI developer experience | craft-tools |
| Plugin directory structure | plugin-dev |

## Agents

| Agent | Purpose |
|-------|---------|
| evaluator | Quality validation for extensions |
| optimizer | Fix identified issues |

## Structure

```
craft-extensions/
├── .claude-plugin/plugin.json
├── docs/
│   └── explanation/              # Human-optimized (WHY)
│       ├── methodology.md        # Research base & design rationale
│       ├── sources.md            # Full bibliography
│       ├── observability.md      # Why observability matters
│       ├── eval-first-design.md  # Eval-first philosophy
│       ├── evaluator.md          # Evaluator design rationale
│       └── optimizer.md          # Optimizer design rationale
├── agents/
│   ├── evaluator.md              # Quality validation (7 gates)
│   └── optimizer.md              # Targeted fix patterns
├── skills/
│   ├── craft-plugins/            # Claude Code extensions
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── observability.md  # OTel instrumentation
│   │       └── evidence-workflow.md  # Research methodology
│   └── craft-tools/              # Software tools (CLIs, APIs, libraries)
│       ├── SKILL.md
│       └── references/
│           └── cli-dx.md         # CLI DX patterns (six laws)
└── README.md
```

## License

MIT
