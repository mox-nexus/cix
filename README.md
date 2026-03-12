> experimental, pre release status
> 
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

| Extension | Phase | Purpose |
|-----------|-------|---------|
| **craft-research** | Research | Paper synthesis, deep research methodology |
| **craft-rhetoric** | Understand | Explanation craft via the Five Canons — 9 agents |
| **guild-arch** | Design | 13 orthogonal architecture reasoning agents |
| **craft-extensions** | Craft | Build extensions, data layers, reasoning prompts |
| **craft-evals** | Measure | Eval methodology for AI systems |
| **ci-scaffolds** | Cross-cutting | Collaboration patterns, problem-solving, engineering craft |
| **run-openclaw-seatbelt** | Security | OpenClaw with Seatbelt sandbox for secure AI assistants |

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
