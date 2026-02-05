# extension-dev

Build extensions that enable effective human-AI collaboration.

## Skills

| Skill | Purpose | Use When |
|-------|---------|----------|
| **build-plugin** | Claude Code extensions (skills, commands, agents, hooks, MCP) | Creating any Claude Code component |
| **build-capability** | General capability authoring patterns | Creating skills, CLIs, APIs, any tool |

## Relationship

```
build-capability (general patterns)
       ↓
build-plugin (Claude Code specifics)
       ↓
plugin-dev (templates & structure)
```

- **build-capability:** Universal patterns (progressive disclosure, degrees of freedom, feedback loops)
- **build-plugin:** Claude Code specific (skills, agents, hooks, commands, MCP, composition)
- **plugin-dev:** Templates and directory structure (referenced, not duplicated)

## When to Use

| Need | Use |
|------|-----|
| Creating a Claude Code skill | build-plugin |
| Creating a Claude Code agent | build-plugin |
| Creating a hook or command | build-plugin |
| Building an MCP server | build-plugin |
| Authoring any capability (skill, CLI, API) | build-capability |
| Understanding progressive disclosure | build-capability |
| Plugin directory structure | plugin-dev |

## Agents

| Agent | Purpose |
|-------|---------|
| evaluator | Quality validation for extensions |
| optimizer | Fix identified issues |

## Structure

```
extension-dev/
├── .claude-plugin/plugin.json
├── docs/
│   └── explanation/           # Human-optimized (Diataxis)
│       ├── methodology.md
│       ├── sources.md
│       ├── evaluator.md
│       └── optimizer.md
├── agents/
│   ├── evaluator.md
│   └── optimizer.md
├── skills/
│   ├── build-plugin/          # Claude Code extensions
│   │   └── SKILL.md
│   └── build-capability/      # General capability authoring
│       ├── SKILL.md
│       └── references/
└── README.md
```

## License

MIT
