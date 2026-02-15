# CLI Developer Experience Patterns

Best-in-class CLI DX distilled from production tools. Not syntax or framework docs — the judgment calls that separate correct CLIs from delightful ones.

Sources: [clig.dev](https://clig.dev/), [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46), Evil Martians, Thoughtworks, Atlassian, and the tools themselves.

---

## Contents

- [The Six Laws](#the-six-laws)
- [Progressive Disclosure](#1-progressive-disclosure)
- [Guided Wizards](#2-guided-wizards)
- [Rich Output](#3-rich-output)
- [Error DX](#4-error-dx)
- [Discoverability](#5-discoverability)
- [Composability](#6-composability)
- [Cross-Cutting Patterns](#cross-cutting-patterns)
- [Audit Checklist](#audit-checklist)

---

## The Six Laws

1. **Guide, don't require** -- Wizards for first use, flags for repeated use
2. **Smart defaults, explicit overrides** -- Optimize the 80% case, escape hatches for the 20%
3. **Show, don't tell** -- Color, tables, progress bars are your UI toolkit
4. **Teach at the point of failure** -- Every error is a documentation opportunity
5. **Help them discover** -- Completions, suggestions, contextual hints
6. **Play well with others** -- TTY detection, `--json`, stdin/stdout, exit codes

---

## 1. Progressive Disclosure

**Exemplar: ripgrep.** Zero-config smart defaults (respects .gitignore, skips binaries, smart-case). Each `-u` peels back one filter layer: `-u` includes gitignored, `-uu` adds hidden, `-uuu` adds binary. Users learn what the defaults *are* by disabling them incrementally.

**Exemplar: httpie.** `http POST api.example.com/users name=test` infers method, content-type, scheme. One character distinguishes types: `key=value` (JSON body), `key==value` (query param), `key:value` (header).

**Principle:** Optimize for the common case. The expert and the beginner use the same tool — they just use different depths. Smart defaults mean the tool does the right thing without flags.

**Apply when:** Your tool has settings that matter to power users but not to beginners. Default to the safe/common case, provide flags to peel back layers.

---

## 2. Guided Wizards

**Exemplar: `gh pr create`.** Detects TTY. Terminal gets a multi-step wizard (prompts for title, body, metadata). Pipe/CI gets flag-driven execution. Every prompt has a flag equivalent. Each prompt has a sensible default. Escape hatch at every step.

**Exemplar: `npm init`.** Defaults in parentheses — Enter accepts them. Writes a config file you can tweak later. `npm init -y` skips all prompts.

**Principle:** A wizard is a config file generator with training wheels. The output should always be a file or state the user can edit manually afterward. Every prompt must have a flag equivalent for scripting.

**Apply when:** First-run setup, project scaffolding, complex multi-option operations. NOT for routine commands — wizards are for onboarding, flags are for daily use.

---

## 3. Rich Output

**Progress display hierarchy** (Evil Martians):

| Duration | Pattern | Example |
|----------|---------|---------|
| < 2s | Spinner | `Loading...` with animated dots |
| 2-30s | X of Y | `Installing 3 of 7 packages...` |
| > 30s | Progress bar | Full bar with ETA and percentage |
| Parallel | Multi-bar | Docker's layered download display |

**Key rule:** Always clear spinners/bars when done. A stale spinner is worse than no spinner.

**Exemplar: `gh pr list`.** No table borders (cleaner, parseable). Color-coded status. Relative timestamps ("2h ago"). `--json` for machine consumption.

**Principle:** Output is a user interface — design it like one. Use color for semantics (red=error, yellow=warning, green=success), not decoration. Detect TTY: rich for humans, structured for pipes.

---

## 4. Error DX

**Exemplar: Rust compiler.** The industry benchmark:
1. **Error code** (E0308) — searchable, linkable
2. **Source context** — shows YOUR code, not internals
3. **Dual annotation** — expectation + actual
4. **Causal chain** — "expected due to this"
5. **Actionable suggestion** — exact code to fix it
6. **Expandable detail** — `rustc --explain E0308`

**Exemplar: Cargo typo correction.** `cargo buidl` → "Did you mean `build`?" Uses Damerau-Levenshtein distance.

**Error message anatomy:**
```
[CODE] Title
  What happened (one line)
  Why it happened (context)
  How to fix it (actionable steps)
  Reference: https://docs.example.com/errors/CODE
```

**Anti-patterns:**

| Don't | Do |
|-------|-----|
| Stack trace as message | Name the specific failure |
| Silent failure (exit 1, no output) | Always write to stderr |
| "An error occurred" | "Config file not found at ~/.config/tool.yaml" |
| "Invalid input" | "Expected a number, got 'abc'" |

**Principle:** Error messages are documentation at the point of need. They answer: What happened? Why? What do I do now? Invest in errors like you invest in features.

---

## 5. Discoverability

**Three mechanisms, in order of leverage:**

### Shell Completions

Tab becomes a discovery engine. The highest-leverage single feature you can add to a CLI — users learn commands, flags, and arguments by exploring.

All major frameworks generate them. **Expose it** — don't leave it buried in docs:

| Framework | Expose via |
|-----------|-----------|
| click/rich-click | `eval "$(_MYTOOL_COMPLETE=zsh_source mytool)"` |
| clap | `mytool completions zsh > _mytool` |
| cobra | `mytool completion zsh > _mytool` |

Consider a `mytool completions <shell>` command so users don't need to know the env var incantation.

### Typo Correction

`git comit` → "Did you mean `commit`?" Damerau-Levenshtein distance on all commands and subcommands. Most frameworks support this out of the box (clap's `suggest`, click's `max_content_width`). Cheap to add, prevents frustration.

### Contextual Next-Step Hints

The most underused pattern. After a command succeeds, tell the user what to do next — the `git status` pattern.

**Exemplar: `git status`.** Parenthetical hints are contextual tutorials: `(use "git add <file>..." to update what will be committed)`. Different users see different hints depending on their state. `git status -s` for the terse version.

**Where to add next-step hints:**

| After this | Suggest this |
|------------|-------------|
| `init` / first-run | The first real command (import, create, connect) |
| `ingest` / import | The primary query command |
| `search` / query | How to drill deeper (view, expand, follow) |
| `create` | How to use what was just created |
| `delete` / destructive | How to undo or recreate |
| Any command with @N output | How to use @N references |

**Key rule:** Hints go to stderr (so they don't pollute piped output). Or respect `--quiet`.

**Principle:** The CLI should teach you how to use it. Lead with examples. Suggest the next command. Correct typos. Every interaction is a teaching moment.

---

## 6. Composability

### TTY-Aware Default Format

The master pattern. The CLI should behave differently based on context — automatically:

| Context | Default behavior | Override |
|---------|-----------------|----------|
| **TTY** (human at terminal) | Rich: colors, tables, panels | `--plain` forces plain |
| **Piped** (stdout to another program) | Plain: line-oriented, no color | `--color=always` forces color |
| **`--json` flag** | Structured: lossless, machine-parseable | Always explicit |

**Exemplar: ripgrep.** Auto-detects TTY. Terminal gets colored, grouped-by-file output. Pipe gets one-match-per-line, no color. `--json` for full structured output. `--color=always` for `less -R`.

**The key insight:** Don't make users opt into composability. If they're piping your output, they want plain text — give it to them automatically. The `--format` flag should have a "auto" default that checks `isatty()`.

### The Three Output Modes

Best-in-class CLIs offer all three:

- **Rich** (TTY default) — colors, tables, panels, spinners
- **Plain** (pipe default) — grep-friendly, one entry per line, tab-separated
- **Structured** (`--json`) — machine-parseable, lossless, every field included

If you only have time for two: rich + `--json`. Plain can be derived from JSON with `jq`.

### Stderr Discipline

- **stdout** — data, results, content (the thing being piped)
- **stderr** — progress, status, hints, warnings, errors (the metadata)

This means spinners, progress bars, and next-step hints go to stderr. When piped, the user sees progress in their terminal while clean data flows through the pipe.

**Exemplar: `fzf`.** Reads stdin for data, opens `/dev/tty` for interactive UI, stdout stays clean for the next pipe stage. The separation is total.

**Principle:** Respect the Unix contract. Don't make users opt into composability — detect their context and do the right thing. The tool should be useful both standalone and as a pipeline stage.

---

## Cross-Cutting Patterns

### Configuration Hierarchy

```
CLI flags (highest priority)
  > Environment variables
    > Project-local config (.tool.toml)
      > User config (~/.config/tool/config.toml)
        > Built-in defaults (lowest priority)
```

Violating this hierarchy feels broken. Users expect flags to win.

### Dry-Run Pattern

| Tool | How | What it shows |
|------|-----|---------------|
| terraform | `plan` | Infrastructure diff before apply |
| rsync | `-n` | Files that would be copied |
| cargo | `publish --dry-run` | Validation without publishing |

**Principle:** Reversibility builds trust. If users can see what will happen first, they use the tool with confidence.

### Idempotent Retry

Commands should be safe to re-run after failure. Skip already-completed steps. Report what was skipped and why. This is especially important for multi-step operations (deploy, migrate, ingest).

---

## Audit Checklist

Score your CLI against the six laws (0-3 each):

| Law | 0 | 1 | 2 | 3 |
|-----|---|---|---|---|
| **Progressive disclosure** | All-or-nothing | Flags exist | Smart defaults | Layered complexity (rg `-u`) |
| **Guided wizards** | No first-run help | Static instructions | Interactive wizard | TTY-aware wizard + flag equivalents |
| **Rich output** | Plain text only | Color | Tables + progress | Duration-matched + `--json` |
| **Error DX** | Generic messages | What happened | What + Why | What + Why + Fix + Code |
| **Discoverability** | `--help` only | Examples in help | Shell completions | Completions + next-step hints |
| **Composability** | Rich-only output | `--json` flag | TTY-aware default format | 3 modes + stderr discipline |

**Target: 12+ / 18** for a production CLI. **15+** for best-in-class.

### Quick Wins (highest impact, lowest effort)

These three patterns take a CLI from 12 to 15+ with minimal code:

1. **Next-step hints** — After every command that produces results, suggest what to do with them. Costs one `console.print` per command. Goes to stderr when piping.

2. **TTY-aware format default** — Check `isatty()` and default to plain/ids when piped. One conditional at the format-selection point. Instantly makes the tool composable.

3. **Shell completions command** — Expose what the framework already generates. One subcommand or one line in the README. Users discover your entire CLI surface via Tab.
