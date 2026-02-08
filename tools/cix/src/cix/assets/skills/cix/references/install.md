# Installation Reference

## Installing Packages

### From default source

```bash
cix add arch-guild
cix add core-ci
```

### From specific source

```bash
cix add cix/arch-guild
cix add my-local/test-plugin
```

### Installation Target

Default target is `claude-code` (installs to `~/.claude/plugins/`).

```bash
cix add arch-guild --target claude-code  # Explicit (same as default)
```

## Managing Installations

```bash
cix list                    # Show installed packages
cix list -v                 # Verbose (show commit hash)
cix rm arch-guild           # Remove by name
cix update                  # Update all
cix update arch-guild       # Update specific package
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
cix update arch-guild       # Updates to latest
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
