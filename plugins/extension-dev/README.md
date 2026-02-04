# extension-dev

Build extensions that enable effective human-AI collaboration.

## What This Is

Implementation patterns for applying transparency, control, observability, and diversity preservation to each extension type.

**For templates/structure**: use `plugin-dev`
**For implementation patterns**: use this

## Scope

| Principle | What This Plugin Provides |
|-----------|---------------------------|
| **Transparency** | How to make each extension type show reasoning |
| **Control** | How to give users agency in each extension type |
| **Observability** | How to make each extension type traceable |
| **Non-conformity** | How to preserve diversity, resist homogenization |

Plus: CLI/API patterns for LLM clients (bundle skill with capability).

## When to Use

- Building a skill, agent, hook, command, or MCP
- Creating a CLI tool or API that Claude will use
- Need patterns for transparency, control, observability
- Want to evaluate/optimize extension quality

## Structure

```
extension-dev/
├── .claude-plugin/plugin.json
├── docs/
│   └── explanation/           # Human-optimized (Diátaxis)
│       ├── methodology.md     # Why these principles
│       ├── sources.md         # Research bibliography
│       ├── evaluator.md       # Why evaluator gates
│       └── optimizer.md       # Why optimizer patterns
├── agents/
│   ├── evaluator.md           # Quality validator
│   └── optimizer.md           # Fix identified issues
├── skills/
│   └── building-extensions/
│       ├── SKILL.md           # Implementation patterns
│       └── references/        # Detailed patterns
└── README.md
```

## License

MIT
