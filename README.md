# cix

Collaborative Intelligence Extensions for Claude Code.

> [!IMPORTANT]
> **Archived — superseded by [mox-labs/gnx](https://github.com/mox-labs/gnx).**
>
> The work continues under a new name and home. `gnx` (generative noetic extensions for agents) is the active successor — same lineage, sharpened framing, hosted under `mox-labs`. See the [gnx README](https://github.com/mox-labs/gnx) for current direction and the place in the broader stack ([slick](https://github.com/mox-labs/slick) → gnx → [geist.sh](https://github.com/mox-labs/geist.sh)).
>
> All in-flight plugins, tools, and architecture work has been merged to `main` here as the wind-down state. Branches preserved for reference (not merged) are documented in [BRANCHES.md](./BRANCHES.md).
>
> This repo is left read-only for historical reference. Issues and PRs are no longer accepted.

AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable future performance. The interaction design — not the technology — determines which outcome you get. cix is a marketplace of cognitive extensions designed around the research: tools that amplify human capability rather than replace it.

Read about the [ethos and research](https://mox-nexus.github.io/cix/docs) behind the project.

## Install

```bash
uv tool install cix --from git+https://github.com/mox-nexus/cix#subdirectory=tools/cix
cix source add https://github.com/mox-nexus/cix
cix list -a
```

## Extensions

Browse the [catalog](https://mox-nexus.github.io/cix/catalog). Read the [research](https://mox-nexus.github.io/cix/docs).

| Extension | Phase | Purpose |
|-----------|-------|---------|
| **craft-research** | Research | Paper synthesis, deep research methodology |
| **craft-rhetoric** | Understand | Explanation craft via the Five Canons — 9 agents |
| **guild-arch** | Design | 13 orthogonal architecture reasoning agents |
| **craft-extensions** | Craft | Build extensions, data layers, reasoning prompts |
| **craft-evals** | Measure | Eval methodology for AI systems |
| **ci-scaffolds** | Cross-cutting | Collaboration patterns, problem-solving, engineering craft |

## Tools

| Tool | Purpose |
|------|---------|
| **recon** | Mechanical collection — config-driven data collection from APIs, CLI tools, and web pages into queryable JSONL |

## Architecture

```
cix/
├── tools/
│   ├── cix/         # CLI package manager (Python + uv, hexagonal)
│   └── recon/       # Mechanical collection system (Python + uv)
├── plugins/         # Marketplace extensions
├── docs/
│   ├── experience/  # SvelteKit documentation site
│   └── content/     # Library articles + bibliography
└── ci-lab/          # Experiment workspace (CEPs)
```

## Development

```bash
cd docs/experience
bun install
bun run dev
```

## License

MIT
