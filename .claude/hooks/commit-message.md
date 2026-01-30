---
name: commit-message
event: UserPromptSubmit
match_arg: "\\b(commit|git commit)\\b"
---

# Commit Message Convention

This project uses **Conventional Commits** for automated changelog generation and clear history.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Maintenance, deps, tooling |
| `perf` | Performance improvement |

## Scopes (cix-specific)

| Scope | Area |
|-------|------|
| `cli` | CLI commands, output formatting |
| `domain` | Domain models in `domain/models.py` |
| `adapters` | Port implementations |
| `deps` | Dependency changes |

## Examples

```
feat(cli): add search command for extensions
fix(adapters): handle missing plugin.json gracefully
docs: update installation instructions
chore(deps): bump rich-click to 1.9
```

## Breaking Changes

Append `!` and add footer:

```
feat(cli)!: rename source command to registry

BREAKING CHANGE: `cix source` is now `cix registry`
```

## Why This Matters

- **Automated changelogs**: `feat` → Added, `fix` → Fixed
- **Semantic versioning**: `feat` bumps minor, `fix` bumps patch, `!` bumps major
- **Scannable history**: grep for `feat(cli)` to find all CLI features
