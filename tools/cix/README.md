# cix - Collaborative Intelligence Extensions CLI

> Discover, install, and manage cognitive extensions that enhance rather than replace human capability.

## Philosophy

cix is built on the **Collaborative Intelligence** thesis: AI tools should amplify human capability, not substitute for it. Every extension in this ecosystem is designed to make you more capable, not dependent.

## Installation

```bash
uv tool install cix
```

## Quick Start

```bash
# Add a source (marketplace of extensions)
cix source add https://github.com/mox-nexus/cix-extensions

# List available extensions
cix list -a

# Install an extension
cix add reasoning-frameworks

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
4. **Evidence-Based** - Claims are grounded in research and experience

## License

MIT
