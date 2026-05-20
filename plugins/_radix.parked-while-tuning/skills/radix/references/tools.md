# Tools — Locators for Mining

The skill drives mining; tools are *locators* — they help find candidate content for Claude to read, project to canonical form, and capture as rows. Claude does the interpretation; tools do the search.

## Contents

- [Tooling philosophy](#tooling-philosophy)
- [Required (universal)](#required-universal)
- [Strongly recommended](#strongly-recommended)
- [Recommended for specific modes](#recommended-for-specific-modes)
- [Optional advanced](#optional-advanced)
- [Per-mode tool fit](#per-mode-tool-fit)
- [Install notes](#install-notes)
- [Fallback when tools are missing](#fallback-when-tools-are-missing)

## Tooling philosophy

A tool earns a place in the toolkit if it surfaces candidate fragments faster or more accurately than `rg` + Claude's reading. Many tools claim to do "code analysis"; few actually save time over a careful `rg` pass plus reading. The list below is conservative — only tools that have demonstrably high signal-to-noise for one of the eight mining modes.

The skill works on the universals (git + rg + gh + jq + ast-grep). Other tools enhance specific modes; their absence reduces yield in those modes but doesn't break the workflow.

## Required (universal)

These four are non-negotiable. The skill assumes them.

| Tool | Purpose | Where it's used |
|---|---|---|
| **git** | Version control + history mining | All modes; primary for `oscillations` |
| **rg** (ripgrep) | Fast content search | All modes |
| **gh** (GitHub CLI) | PR / issue / discussion / RFC archaeology | `oscillations` (PR archaeology), `tradeoffs`, `antipatterns` |
| **jq** | JSONL processing — query, filter, aggregate the corpus | Phase 4 synthesis, post-extraction queries |

If any are missing, install before running.

## Strongly recommended

| Tool | Purpose | Where it's used |
|---|---|---|
| **ast-grep** | Structural AST search across many languages (Rust, Go, TS, JS, Python, Java, C/C++, ...) | `signatures`, `schemas`, structural-pattern recurrence; pattern-based capture is far higher-signal than text-based for typed shapes |

A single Rust-binary install. Pairs naturally with `rg` (which does text; ast-grep does structure).

## Recommended for specific modes

| Tool | Purpose | Best for | Cost |
|---|---|---|---|
| **code-maat** | Temporal coupling (which files change together), hotspots (high-churn complexity), ownership distribution, commit-clustering | `oscillations` (temporal-coupling = paired-revert candidates; hotspots = where archaeology is densest); `aesthetics` (ownership concentration is a maintainership signal) | JVM dependency |
| **language servers** (`rust-analyzer`, `gopls`, `tsserver`, `pyright`, etc.) | Type-aware queries: who calls X, what's the inferred type, find-references | `signatures`, `schemas` (when ast-grep alone is too text-shaped); `models` (resolving cross-file type relationships) | Per-language install; LSP client to drive them |
| **PyDriller** | Python library for programmatic git mining (commits, modifications, refactorings, code metrics) | `oscillations` when a script needs more structure than `git log` alone | Python install + writing a script |
| **difftastic** / **diffsitter** | Semantic diffs (AST-aware, not line-based) | `oscillations` — comparing original vs resettlement is much clearer in a semantic diff | Single-binary install |

## Optional advanced

| Tool | Purpose | Best for | Cost |
|---|---|---|---|
| **Semgrep** | Pattern-based static analysis with rule libraries for many languages | `scars` (off-the-shelf rules for SAFETY-marker variants, `unsafe` patterns); `antipatterns` (off-the-shelf rules for known anti-patterns per language) | Python install; learning rule syntax; runtime cost on large repos |
| **CodeQL** | Query language for code-as-graph; canonical for graph-extraction | `schemas` (extract labeled-property-graphs at scale); `antipatterns` (security-pattern queries) | CodeQL CLI install + database build per repo; query learning curve |
| **tree-sitter** (CLI / parsers) | Direct AST access; underlying parser for ast-grep | When ast-grep's pattern syntax can't express what you need | Per-language grammar install |
| **scc** / **tokei** / **cloc** | Code counters with complexity metrics | Phase 3b reconnaissance — quickly assess source size, language mix, complexity distribution | Single-binary install |
| **gitleaks** / **trufflehog** | Secret scanning | Phase 3b reconnaissance — flag if a repo accidentally contains secrets in history (rare but worth knowing) | Single-binary install |

## Per-mode tool fit

Recommended tools per mining mode:

| Mode | Required | Strongly helpful | Optional |
|---|---|---|---|
| **oscillations** | git, rg, gh | code-maat (hotspots), difftastic (semantic diffs), PyDriller (programmatic) | Semgrep (rules for known revert patterns) |
| **scars** | rg | ast-grep (for marker patterns in structured contexts) | Semgrep (off-the-shelf marker rules) |
| **signatures** | rg, ast-grep | language servers (type-aware) | tree-sitter (custom grammars) |
| **schemas** | ast-grep | language servers, tree-sitter | CodeQL (graph queries at scale) |
| **models** | rg, ast-grep | language servers (cross-file type resolution) | CodeQL (entity-relationship extraction) |
| **tradeoffs** | git, gh, rg | code-maat (revert clusters → tradeoff candidates) | — |
| **antipatterns** | git, gh, rg | Semgrep (off-the-shelf antipattern rules per language), code-maat (high-churn = maintenance pain) | CodeQL (security antipatterns) |
| **aesthetics** | rg, ast-grep | code-maat (ownership = maintainership signal) | — |

## Install notes

Quick install pointers (verify against official docs; versions move):

```bash
# Required (most package managers have these)
brew install git ripgrep gh jq          # macOS
apt install git ripgrep gh jq            # Debian/Ubuntu
# Strongly recommended
cargo install ast-grep                  # or: brew install ast-grep
# Recommended
brew install difftastic                  # diffsitter via cargo install diffsitter

# code-maat (JVM)
git clone https://github.com/adamtornhill/code-maat
# Then either: lein uberjar (build) or use prebuilt JAR
# Run: java -jar code-maat-standalone.jar -l <log> -c git2 -a <analysis>

# Optional
pip install semgrep                      # OR: brew install semgrep
brew install --cask codeql               # CodeQL CLI (verify availability)
pip install pydriller
```

## Fallback when tools are missing

The skill's discipline: **the universals (git + rg + gh + jq + ast-grep) are sufficient for all 8 modes at reduced yield.** No mode is gated on the recommended/optional tools. If one isn't available:

- No `code-maat` → manually identify hotspot files via `git log --name-only | sort | uniq -c | sort -rn | head` and pair-revert candidates by reading commit clusters.
- No language server → ast-grep + careful reading covers signature and schema extraction; type resolution is manual.
- No `difftastic` → `git diff --word-diff` or just `git show` and read.
- No `Semgrep` / `CodeQL` → write the patterns as ast-grep / rg queries; slower per-pattern but covers the same ground.
- No `PyDriller` → `git log --pretty=format:` with careful awk/jq pipelines; harder for complex programmatic mining.

Note in PLAN.md which tools are available and which fallbacks were used. STATUS.md tracks what was mined; the choice of tool is a methodological detail belonging in PLAN.md.
