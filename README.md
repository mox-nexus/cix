# cix - Collaborative Intelligence Extensions

> **Liberation through Collaborative Intelligence**
> A marketplace of cognitive extensions that enhance human capability, not replace it.

## Philosophy

Most AI tooling is **substitutive** — it replaces human capability rather than enhancing it. This project takes a different approach based on rigorous research:

| Substitutive | Complementary |
|--------------|---------------|
| AI does the work, human approves | AI amplifies, human remains central |
| Human capability atrophies | Human capability compounds |
| Skills erode over time | Skills strengthen over time |

**Every extension in this ecosystem must make humans more capable, not dependent.**

## Evidence Base

This isn't opinion — it's grounded in peer-reviewed research:

- **26% productivity gains** with AI (Cui/Demirer RCTs, n=4,867)
- **17% worse learning outcomes** with unrestricted AI (Bastani et al. PNAS, n=1,000)
- **20% skill reduction** after 3 months AI exposure (Lancet colonoscopy study)
- **2.5x improvement** from teaching WHY vs prescribing HOW (claude-1337 research)

The conclusion: **how** you use AI matters more than **whether** you use it.

## Getting Started

```bash
# Install cix
uv tool install cix

# Add a source
cix source add https://github.com/mox-labs/cix-extensions

# List available extensions
cix list -a

# Install an extension
cix add reasoning-frameworks

# See what's installed
cix list
```

## Extension Types

| Type | Purpose | Pattern |
|------|---------|---------|
| **Skill** | Decision frameworks | Teaches HOW to think |
| **Agent** | Specialized perspective | Offers viewpoint, human synthesizes |
| **Hook** | Event-triggered behavior | Enhances existing workflow |
| **MCP** | External integration | Bridges systems, human orchestrates |

## Design Principles

1. **Complementary, not Substitutive** — Enhance capability, don't replace it
2. **WHY > HOW** — Teach reasoning frameworks, not prescribe solutions
3. **Transparent Reasoning** — Show evidence levels, not just conclusions
4. **Human-Initiated** — Respond to direction, don't assume
5. **Composable** — Small focused extensions that combine well

## Project Structure

```
cix/
├── tools/cix/          # CLI package (hexagonal architecture)
├── extensions/         # Extension packages (future)
└── research/          # Evidence base
```

## Development

```bash
# Clone and setup
git clone https://github.com/mox-labs/cix
cd cix
uv sync

# Run CLI in development
uv run cix --help

# Run tests
uv run pytest
```

## The Saarthi Principle

AI as **Saarthi** (Sanskrit: charioteer) — not a tool to be used or master to obey, but a collaborative partner that guides while humans act.

> An AI that makes humans dependent has failed.
> An AI that makes humans more capable has succeeded.

## License

MIT

---

*Part of the [Mox Labs](https://mox.nexus) research program on collaborative intelligence.*
