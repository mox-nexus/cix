# Contributing to cix

## Git Workflow

We use **GitHub Flow** - a simple, branch-based workflow.

```
main ─────●─────●─────●─────●─────
          │           ↑
          └── feature-branch ──┘
```

### The Flow

1. **Create a branch** from `main`
2. **Make commits** following conventional commit format
3. **Open a PR** when ready for review
4. **Merge to main** after approval
5. **Delete the branch**

### Branch Naming

```
feat/short-description    # New feature
fix/issue-description     # Bug fix
docs/what-changed         # Documentation
refactor/what-changed     # Code restructuring
chore/what-changed        # Maintenance tasks
```

## Commit Conventions

We use **Conventional Commits** for clear, parseable history.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, tooling |
| `perf` | Performance improvement |

### Scope

Optional, indicates the area affected:

- `cli` - CLI commands and interface
- `domain` - Domain models and logic
- `adapters` - Port implementations
- `deps` - Dependencies

### Examples

```
feat(cli): add verbose flag to list command
fix(adapters): handle missing plugin.json gracefully
docs: add contributing guidelines
refactor(domain): simplify Extension model
chore(deps): bump rich-click to 1.9
```

### Breaking Changes

Add `!` after type/scope and explain in footer:

```
feat(cli)!: change source command structure

BREAKING CHANGE: `cix source add` now requires --name flag
```

## Versioning

We use **Semantic Versioning** (semver): `MAJOR.MINOR.PATCH`

| Increment | When |
|-----------|------|
| `MAJOR` | Breaking changes |
| `MINOR` | New features (backward compatible) |
| `PATCH` | Bug fixes (backward compatible) |

### Pre-release

During alpha/beta: `0.x.y` where breaking changes bump MINOR.

Current: **0.1.0** (alpha)

## Pull Requests

### Before Opening

- [ ] Branch is up to date with `main`
- [ ] Tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check`)
- [ ] Types check (`uv run mypy`)

### PR Title

Follow conventional commit format:

```
feat(cli): add extension search command
```

### PR Description

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
How to test these changes.
```

## Development Setup

```bash
# Clone
git clone https://github.com/mox-nexus/cix
cd cix

# Install dependencies
uv sync

# Install CLI for development
uv tool install --editable ./extensions/cix

# Run tests
uv run pytest

# Lint
uv run ruff check
uv run ruff format --check

# Type check
uv run mypy extensions/cix/src
```

## Release Process

1. Update version in:
   - `extensions/cix/pyproject.toml`
   - `extensions/cix/src/cix/__init__.py`

2. Update `CHANGELOG.md`

3. Create release commit:
   ```bash
   git add -A
   git commit -m "chore: release v0.2.0"
   ```

4. Tag the release:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin main --tags
   ```

5. GitHub Release (optional): Create from tag with changelog excerpt
