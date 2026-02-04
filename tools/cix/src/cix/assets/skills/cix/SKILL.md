# cix Skill

Manage cognitive extensions for Claude Code.

## When to Use

| User Intent | Command |
|-------------|---------|
| "What extensions are available?" | `cix list -a` |
| "Install arch-guild" | `cix add arch-guild` |
| "What's installed?" | `cix list` |
| "Add a marketplace" | `cix source add <url>` |
| "Install from local source" | `cix add source-name/package` |
| "Remove an extension" | `cix rm <package>` |
| "Update extensions" | `cix update` |

## Commands

### Sources (Marketplaces)

```bash
cix source add <url>           # Register a marketplace
cix source add file:///path    # Local source (for testing)
cix source list                # Show registered sources
cix source rm <name>           # Remove a source
cix source refresh [name]      # Fetch latest from source(s)
```

### Packages (Extensions)

```bash
cix list                       # Show installed extensions
cix list -a                    # Show available from default source
cix list -av                   # Verbose with descriptions
cix add <package>              # Install from default source
cix add source/package         # Install from specific source
cix rm <package>               # Remove installed extension
cix update [package]           # Update extension(s)
cix show <package>             # Show extension details
```

### Info

```bash
cix info                       # Configuration and status
cix --skill                    # Output this skill for Claude
cix --skill -r sources         # Output specific reference
```

## Package References

| Format | Meaning |
|--------|---------|
| `arch-guild` | Package from default source |
| `cix-local/arch-guild` | Package from specific source |

## Common Patterns

### Add a new marketplace

```bash
cix source add https://github.com/org/marketplace-repo
# OR
cix source add https://github.com/org/repo --name custom-name
```

### Test local plugins

```bash
# Add local directory as source (must be git repo)
cix source add file:///path/to/local/repo --name local

# Install from it
cix add local/my-plugin
```

### List all packages from a specific source

```bash
# Use source/package syntax with show
cix show source-name/package-name
```

## Extension Structure

cix recognizes packages with:
- `.claude-plugin/plugin.json` manifest
- Or `skills/`, `agents/`, `hooks/` directories

## References

For detailed patterns, use `cix --skill -r <name>`:

| Reference | Command | Content |
|-----------|---------|---------|
| sources | `cix --skill -r sources` | Source management patterns |
| install | `cix --skill -r install` | Installation patterns |
