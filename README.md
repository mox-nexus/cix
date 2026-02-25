# cix

Collaborative Intelligence Extensions for Claude Code.

AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable future performance. The interaction design — not the technology — determines which outcome you get. cix is a marketplace of cognitive extensions designed around the research: tools that amplify human capability rather than replace it.

## Install

```bash
uv tool install cix --from git+https://github.com/mox-nexus/cix#subdirectory=tools/cix
cix source add https://github.com/mox-nexus/cix
cix list -a
```

## Extensions

Browse the [catalog](https://mox-nexus.github.io/cix/catalog). Read the [research](https://mox-nexus.github.io/cix/library).

| Extension | Purpose |
|-----------|---------|
| **arch-guild** | 13 orthogonal architecture reasoning agents |
| **collab-scaffolds** | Human-AI collaboration patterns, problem-solving, engineering craft |
| **craft-rhetoric** | Explanation craft via the Five Canons — 7 agents, Semantic Stack workflow |
| **craft-extensions** | Build extensions: skills, agents, hooks, commands, MCPs |
| **craft-evals** | Eval methodology for AI systems |
| **craft-prompts** | Prompt engineering for reasoning models and deep research |
| **data-store** | Database selection, search, hybrid retrieval, RAG |
| **run-openclaw-srt** | OpenClaw with SRT sandbox for secure AI assistants |

## Architecture

```
cix/
├── tools/cix/       # CLI (Python + uv, hexagonal architecture)
├── plugins/         # Marketplace extensions
├── docs/
│   ├── experience/  # SvelteKit documentation site
│   └── content/     # Library articles + bibliography
└── .claude/         # Project extensions
```

## Development

```bash
cd docs/experience
bun install
bun run dev
```

## License

MIT
