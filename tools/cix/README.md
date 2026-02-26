# cix - Collaborative Intelligence Extensions CLI

> Discover, install, and manage cognitive extensions that enhance rather than replace human capability.

## Installation

From PyPI (once published):

```bash
uv tool install cix
```

From git:

```bash
uvx --from "cix @ git+https://github.com/mox-nexus/cix#subdirectory=tools/cix" cix
```

## Quick Start

```bash
# Add the mox-labs marketplace
cix source add https://github.com/mox-nexus/cix

# List available extensions
cix list -a

# Install an extension
cix add guild-arch

# See what's installed
cix list
```

## Commands

### Sources (Extension Marketplaces)

```bash
cix source add <url>        # Register a source
cix source list             # Show registered sources
cix source rm <name>        # Remove a source
cix source refresh [name]   # Fetch latest from source(s)
```

### Extensions

```bash
cix list [-a] [-v]          # List installed (or -a available) extensions
cix add <extension>         # Install an extension
cix rm <extension>          # Remove an extension
cix update [extension]      # Update extension(s)
cix show <extension>        # Show extension details
```

### System

```bash
cix info                    # Show cix configuration and status
cix --skill                 # Output skill documentation for Claude
```

## Extension Types

| Type | Purpose | Example |
|------|---------|---------|
| **Skill** | Decision frameworks and methodology | reasoning-patterns |
| **Agent** | Specialized subagents for delegation | structured-problem-solver |
| **Hook** | Event-triggered behaviors | metacognitive-check |
| **MCP** | External service integrations | knowledge-base-connector |

## Design Principles

1. **Complementary, not Substitutive** - Extensions enhance your capability, they don't replace it
2. **Transparent Reasoning** - See why, not just what
3. **Human-Initiated** - You control when and how extensions engage
4. **Source-Agnostic** - No central registry; you choose which sources to trust

## License

MIT
