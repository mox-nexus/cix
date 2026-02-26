# Installation Reference

## Installing Packages

### From default source

```bash
cix add guild-arch
cix add core-ci
```

### From specific source

```bash
cix add cix/guild-arch
cix add my-local/test-plugin
```

### Installation Target

Default target is `claude-code` (installs to `~/.claude/plugins/`).

```bash
cix add guild-arch --target claude-code  # Explicit (same as default)
```

## Managing Installations

```bash
cix list                    # Show installed packages
cix list -v                 # Verbose (show commit hash)
cix rm guild-arch           # Remove by name
cix update                  # Update all
cix update guild-arch       # Update specific package
```

## Installation Location

Packages are installed to:
```
~/.claude/plugins/<package-name>/
```

Each package contains:
- `skills/` - Skill definitions
- `agents/` - Agent definitions
- `hooks/` - Hook configurations
- `.claude-plugin/plugin.json` - Manifest

## Pin Behavior

By default, cix pins installations to the commit at install time:

```bash
cix list -v                 # Shows commit hash
cix update guild-arch       # Updates to latest
```

## Troubleshooting

### Package not found

```bash
# Check if source is registered
cix source list

# Refresh to fetch latest
cix source refresh

# List available packages
cix list -a
```

### Source not found

```bash
# Check source name
cix source list

# Use explicit source/package format
cix show my-source/package-name
```
