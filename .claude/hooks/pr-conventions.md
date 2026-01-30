---
name: pr-conventions
event: UserPromptSubmit
match_arg: "\\b(pull request|PR|pr create|gh pr)\\b"
---

# Pull Request Conventions

## PR Title

Use conventional commit format (this becomes the squash commit message):

```
feat(cli): add extension search command
```

## PR Description

```markdown
## Summary
[1-2 sentences: what and why]

## Changes
- [Specific change 1]
- [Specific change 2]

## Test Plan
[How to verify this works]
```

## Pre-PR Checklist

Run before creating:

```bash
uv run ruff check && uv run ruff format --check && uv run mypy extensions/cix/src && uv run pytest
```

| Check | Command | Fixes |
|-------|---------|-------|
| Lint | `uv run ruff check` | `uv run ruff check --fix` |
| Format | `uv run ruff format --check` | `uv run ruff format` |
| Types | `uv run mypy extensions/cix/src` | Fix type errors manually |
| Tests | `uv run pytest` | Fix failing tests |

## When to Update CHANGELOG

Update `CHANGELOG.md` under `[Unreleased]` for:
- New features (`feat`)
- Bug fixes (`fix`)
- Breaking changes

Skip for: `docs`, `test`, `chore`, `refactor` (internal only)
