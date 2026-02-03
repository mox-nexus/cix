# ci-dev

Collaborative Intelligence development methodology for building plugins and capabilities.

## What This Is

A skill plugin that provides CI principles and patterns for building:
- **Plugins**: Skills, agents, hooks, commands, MCPs
- **Capabilities**: Tools (CLIs), APIs

## Core Principles

| Principle | What It Means |
|-----------|---------------|
| **Transparency** | Show reasoning, cite sources |
| **Control** | User can observe, steer, override |
| **Mastery** | Build understanding, not dependency |
| **Provenance** | Claims traceable, uncertainty stated |

## When to Use

Invoke when:
- Building a new skill, agent, hook, or command
- Creating a CLI tool or API
- Need patterns for transparency, observability, error handling

## Structure

```
ci-dev/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── building-extensions/
│       ├── SKILL.md           # Claude-optimized (< 500 lines)
│       ├── references/        # Claude-optimized (load on demand)
│       │   ├── skill-authoring.md
│       │   ├── plugin-patterns.md
│       │   ├── capability-patterns.md
│       │   ├── observability.md
│       │   └── provenance-cove.md
│       └── explanations/      # Human-optimized
│           ├── methodology.md
│           └── sources.md
└── README.md
```

## License

MIT
