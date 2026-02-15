# cix

Collaborative Intelligence Extensions for Claude Code.

## Install

```bash
git clone https://github.com/mox-nexus/cix.git
```

Then add plugins to Claude Code:

```bash
claude plugin add ./cix/plugins/arch-guild
```

## Extensions

Browse the [catalog](https://mox-nexus.github.io/cix/catalog).

## Architecture

```
cix/
├── tools/cix/       # CLI (Python + uv, hexagonal architecture)
├── plugins/         # Marketplace extensions
├── docs/
│   ├── experience/  # SvelteKit site
│   └── content/     # Markdown content
└── .claude/         # Project extensions
```

## Development

```bash
cd docs/experience
bun install
bun run dev
```

## Status

Pre-alpha. MIT licensed.
