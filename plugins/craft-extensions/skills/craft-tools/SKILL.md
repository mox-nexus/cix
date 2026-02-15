---
name: craft-tools
description: "Crafts software tools with great developer experience. Use when: creating a CLI tool, designing an API, building tools like memex/cix/radix, or when error messages are confusing, feedback is slow, output is hard to parse, or users ask 'what do I do next'."
---

# Craft Tools

The non-obvious patterns that separate correct tools from delightful ones. For syntax, frameworks, and boilerplate — ask Claude directly. This skill teaches judgment.

**Claude Code extensions:** See `craft-plugins` skill (skills, hooks, commands, MCP).

---

## CLI DX — The Six Laws

1. **Progressive disclosure** — Smart defaults for 80%, flags for 20% (ripgrep's `-u` layers)
2. **Guided wizards** — Interactive first-run, flag-equivalent for scripting (`gh pr create`)
3. **Rich output** — Spinner < 2s, X-of-Y for steps, progress bar > 30s (Evil Martians)
4. **Error DX** — What + Why + Fix + Error Code (Rust compiler benchmark)
5. **Discoverability** — Shell completions, typo correction, next-step hints (`git status`)
6. **Composability** — TTY detection: rich for humans, plain for pipes, `--json` for machines

For exemplars, anti-patterns, and the full audit checklist: see [cli-dx.md](references/cli-dx.md).

**Python hex + streaming patterns:** See [python-hex.md](references/python-hex.md) — hexagonal layout, functional streaming, itertools pipelines, ONNX resource model.

---

## Key Decision Frameworks

### Config Hierarchy (never violate this)

```
CLI flags        (highest — always wins)
  > Env vars     (CI/CD, per-session)
    > Project    (.tool.toml — travels with repo)
      > User     (~/.config/tool/ — personal defaults)
        > Built-in defaults (lowest)
```

### Error Messages (the anatomy)

```
Error: Could not read config file
  Path: ~/.config/tool/config.toml
  Reason: File not found
  Fix: Run `tool init` to create default config
```

Pattern: **What** happened + **Why** (context) + **How to fix** (actionable).

Anti-pattern: `Error: invalid input` — tells you nothing.

### Output Mode Selection

| Context | Default | Override |
|---------|---------|----------|
| TTY (human) | Rich: color, tables, panels | `--plain` |
| Piped (machine) | Plain: line-oriented, no color | `--color=always` |
| Explicit | Structured: `--json` or `--format json` | — |

The tool should detect context automatically via `isatty()`. Don't make users opt into composability.

### Destructive Operations

Always require one of:
- `--yes` / `-y` flag (scripting)
- Interactive confirmation (terminal)
- `--dry-run` preview (trust building)

Show what will be affected BEFORE asking for confirmation.

---

## API DX — Non-Obvious Decisions

### Error Responses

Always return: machine-readable `code` + human-readable `message` + field-level `details`:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid input",
    "details": [{"field": "email", "message": "Invalid format"}]
  }
}
```

The `code` is for programmatic handling (`switch`/`match`). The `message` is for logs and debugging. The `details` are for form UIs.

### Pagination

**Cursor-based** for feeds, timelines, anything that changes during traversal.
**Offset-based** only for stable, rarely-changing datasets.

Default: cursor. Offset is simpler but breaks when items are added/removed between pages.

### Versioning

URL path (`/api/v1/`) for breaking changes. Header (`Accept: application/vnd.api+json;version=2`) for content negotiation. Default to URL path — it's visible, debuggable, and cacheable.

---

## Quality Checklist (DX-focused)

### Does it teach?
- [ ] Error messages tell you how to fix the problem
- [ ] `--help` leads with examples, not option lists
- [ ] After success, hints suggest what to do next
- [ ] First-run experience guides the user

### Does it compose?
- [ ] `--json` flag for structured output
- [ ] TTY detection changes default output format
- [ ] Errors go to stderr, data to stdout
- [ ] Exit codes follow conventions (0/1/2/130)

### Does it respect the user?
- [ ] Smart defaults — works without flags
- [ ] `--dry-run` for destructive operations
- [ ] Confirmation shows impact before asking
- [ ] Shell completions available

---

## Limitations

- **Progressive disclosure adds complexity.** For one-shot scripts or single-purpose tools, simple flags may be better than layered defaults.
- **Rich output adds dependencies.** In minimal environments (Docker alpine, CI), prefer plain text with optional rich mode.
- **TTY detection has edge cases.** `tmux`, `screen`, and some IDE terminals report as non-TTY. Provide `--color=always` and `--plain` overrides.
- **Wizards slow down experts.** Always provide flag equivalents. Never force interactive mode.
- **The Six Laws target multi-command CLIs.** Single-command tools (like `jq`, `rg`) need fewer laws — composability and error DX matter most.
