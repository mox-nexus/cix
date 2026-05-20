# Mining Recipes

Concrete commands per mining mode, organized by the artifact source type they read. Phase 3c (extraction modes) and Phase 4 (synthesis modes). Pick the recipes that fit the current mode and the artifact sources rich in the source you're mining.

**Run one mode per pass.** Close this file between modes — the per-mode discipline is undermined if you fan across mining modes in a single pass.

For tooling install + per-mode tool-fit, see `references/tools.md`.

## Contents

- [Universal — locate-by-quote](#universal--locate-by-quote)
- [What doesn't work as a filter](#what-doesnt-work-as-a-filter)
- [Artifact source types](#artifact-source-types)
- **Phase 3c — Extraction modes**
  - [oscillations — git history archaeology](#oscillations--git-history-archaeology)
  - [scars — battle-scar comments + protected code](#scars--battle-scar-comments--protected-code)
  - [signatures — typed-shape capture (or AST-pattern capture)](#signatures--typed-shape-recurrence-or-ast-pattern-recurrence)
  - [schemas — labeled property graph](#schemas--labeled-property-graph)
- **Phase 4 — Synthesis modes**
  - [models — program-model + domain-model](#models--program-model--domain-model)
  - [tradeoffs — alternatives and rationale](#tradeoffs--alternatives-and-rationale)
  - [antipatterns — looks-reasonable-fails](#antipatterns--looks-reasonable-fails)
  - [aesthetics — what "right" feels like](#aesthetics--what-right-feels-like)
- [Cross-mode: dispatch sketch](#cross-mode-dispatch-sketch)
- [Per-language adaptations](#per-language-adaptations)

## Universal — locate-by-quote

When you find something interesting, get its addressable location:

```bash
rg --line-number -F "<verbatim phrase>" .
```

Use the `path:line` in the row's `surface.location`.

## What doesn't work as a filter

Filename-and-title matching is unreliable for finding canonical content. Phrase-relevance queries (and their filename equivalents) **systematically miss canonical material** when titles and filenames don't carry the search phrase.

- A core architectural decision lives in `helpers/util.rs`, not `core/architecture.rs`.
- A canonical pattern is in `tests/` (encoding the spec) while `docs/` is stale.
- A revert message uses unconventional vocabulary your phrase-query missed.

**Do this instead:**
- Phrase-match over **content**, not paths or titles.
- For known canonical works (specific RFCs, named PRs, named commits), do direct lookup.
- After Phase 3b reconnaissance, mine the paths *the codebase actually uses* for the kind of content you want, not the paths their names suggest.

Phrase-relevance is for *unknown* work. Direct lookup (`git log --grep` on a known phrase, exact title, PR number, DOI) is for *known* work.

## Artifact source types

The 10 primary sources that hold WHY-layer signal, ranked by typical signal density.

**Per-repo variation**: not all repos use the same conventions. Some examples:
- `rust-lang/rust-analyzer` puts its design-doc archaeology in `docs/dev/` (architecture.md, lsp-extensions.md, syntax.md) plus a dev-blog-style `docs/dev/style.md`. No `rfcs/` directory; the dev docs ARE the deliberation artifact.
- `tokio-rs/tokio` does deliberation primarily in PRs + `RELEASES.md` + occasional design docs in `tokio/CONTRIBUTING.md`. No top-level `rfcs/`.
- `hyperium/hyper` keeps RFC-equivalent material in its CHANGELOG.md (substantial entries explain breakage rationale) plus PR threads.
- `bytecodealliance/wasmtime` and `WebAssembly/component-model` use `docs/` heavily.
- `rust-lang/rfcs` IS the RFC repo for the language itself; its `text/` directory is the gold standard.
- `tower-rs/tower` and `axum` use repo-internal `docs/` plus extensive PR discussions.

**Don't filter by filename or directory name.** If `rfcs/` doesn't exist, look for `docs/dev/`, `docs/architecture/`, `docs/design/`, `RELEASES.md`, substantial CHANGELOG entries, or `CONTRIBUTING.md`. Phase 3b reconnaissance (read README + ARCHITECTURE + ls docs/) tells you where deliberation lives in this specific repo.

| Source | Where it lives | Primary mode it feeds | Typical density |
|---|---|---|---|
| **git history** | `.git/` | oscillations | Highest WHY-density (per-change deliberation) |
| **doc comments** | within code files | scars | High (battle scars, SAFETY notes) |
| **commit messages** | `git log` | oscillations, tradeoffs | High in mature repos |
| **RFCs / design docs** | `rfcs/` directories, repo wikis, design-doc dirs | tradeoffs, oscillations | Variable; rich when present |
| **PRs** | `gh pr list` / `gh pr view` | oscillations, antipatterns | Variable |
| **issues** | `gh issue list` | antipatterns | Variable |
| **discussions** | `gh api repos/.../discussions` | tradeoffs | Newer; variable |
| **code structure** | source files | signatures, schemas, models | Always present |
| **tests** | `tests/` | scars (test-name-as-invariant) | Variable |
| **changelogs** | `CHANGELOG.md`, `NEWS.md` | tradeoffs, antipatterns | Variable |

For v0.1 (3 modes): git history + doc comments + code structure are the primary sources.

## oscillations — git history archaeology

The signal: try → revert → settle. The revert is where the failure mode is encoded; the resettlement encodes what the maintainer learned.

### Find reverts

```bash
# All reverts with messages
git log --all --grep="^revert\|^Revert" --pretty=format:'%h%n%s%n%b%n---' | head -200

# Recent reverts
git log --since="2 years ago" --grep="revert" --oneline

# Counter — how rich is this signal in this repo?
git log --all --grep="^revert\|^Revert" --oneline | wc -l
```

If the count is low (< 5 across the repo's history), oscillations may not be the highest-yield mode for this source — switch to scars or signatures.

### Find oscillation hotspots via code-maat (when available)

`code-maat` finds files that change together (temporal coupling) and high-churn complexity hotspots. For oscillations specifically: paired temporal-coupling between a file and itself across reverts is a candidate-oscillation signal.

```bash
# Generate the git log code-maat consumes
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > /tmp/git.log

# Hotspots — files with most revisions (where archaeology is densest)
java -jar /path/to/code-maat-standalone.jar -l /tmp/git.log -c git2 -a revisions | head -20

# Temporal coupling — files that change together
java -jar /path/to/code-maat-standalone.jar -l /tmp/git.log -c git2 -a coupling | head -30

# Code age (lines) — old, high-churn lines are oscillation candidates
java -jar /path/to/code-maat-standalone.jar -l /tmp/git.log -c git2 -a age | head -20

# Author ownership — single-owner files often hide tacit decisions
java -jar /path/to/code-maat-standalone.jar -l /tmp/git.log -c git2 -a entity-ownership | head -20
```

Use the hotspot list to prioritize WHICH files to walk for revert + fix-rationale archaeology. A file with 200 revisions and high temporal coupling to a sibling is a far better oscillation-mining target than a file changed twice.

### Walk the oscillation triple

For each revert commit, find the original (what was reverted) and the resettlement (what came after):

```bash
# Original — referenced in revert message or via git revert metadata
git show <revert-sha> | head -20    # often has "This reverts commit <sha>"
git log <original-sha>~1..<original-sha>  # the change being reverted

# Resettlement — commits in the same area after the revert
git log <revert-sha>..HEAD --oneline -- path/that/was/reverted
```

Capture the triple as one row: `{original_commit, revert_commit, resettle_commit, file, original_diff_summary, resettle_diff_summary, revert_message}`.

### Doc-bearing commits

Reverts aren't the only oscillation signal. "fix: X breaks Y" commits encode similar archaeology:

```bash
# Commit messages explaining a fix's rationale
git log --all --pretty=format:'%h%n%s%n%b%n---' | rg -B1 -A6 -i "(why|rationale|chose|alternative|considered|breaks|broken)"

# Fix-commits that reference their predecessor
git log --all --grep="fix" --pretty=format:'%h %s' | rg -i "(fix.*\(was|fix.*\(reverts|fix.*\(replaces)"
```

### From PRs, issues, and discussions

The forge layer (GitHub) carries deliberation artifacts that aren't in git history. **All `gh` calls must be read-only** — see the Threat model in SKILL.md (`gh pr view`, `gh pr list`, `gh issue view`, `gh issue list`, `gh api` GET, `gh repo view` only).

**PRs — closed-without-merge = rejected approaches:**

```bash
# Closed-without-merge PRs (rejected approaches feeding antipatterns)
gh pr list --state closed --limit 200 --json number,title,body,mergedAt --jq '.[] | select(.mergedAt == null) | "PR #\(.number): \(.title)"' | head

# Substantive PR with discussion (read for tradeoff archaeology)
gh pr view <N> --comments
gh pr view <N> --json title,body,comments,reviews

# PRs that took multiple iterations (signal of deliberation density)
gh pr list --state merged --json number,title,reviewDecision,reviews \
  --jq '.[] | select(.reviews | length > 5) | "#\(.number) \(.title) — \(.reviews | length) reviews"' | head
```

**Issues — failure-mode reports + abandoned approaches:**

```bash
# Closed issues with "wontfix" / "by design" labels = often hide deliberation
gh issue list --state closed --label "wontfix" --limit 50 --json number,title,body
gh issue list --state closed --label "by design" --limit 50 --json number,title,body

# Long issue threads (substantial discussion)
gh issue list --state all --limit 300 --json number,title,comments \
  --jq '.[] | select(.comments > 20) | "#\(.number) (\(.comments) comments): \(.title)"' | head

# View specific issue with full comment thread
gh issue view <N> --comments

# Issues mentioning specific patterns (e.g., "soundness", "deadlock", "leak")
gh issue list --state all --search "soundness" --limit 50
gh issue list --state all --search "deadlock OR data-race" --limit 50
```

**Discussions — debate, consensus formation (newer feature; not all repos use them):**

```bash
# List discussions (uses GraphQL via gh api)
gh api graphql -f query='query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 50) {
      nodes { number title category { name } answer { body } comments(first: 1) { totalCount } }
    }
  }
}' -F owner=<owner> -F repo=<repo>

# View a specific discussion
gh api repos/<owner>/<repo>/discussions/<N>
```

**Triage signal density before deep mining**:

```bash
echo "PRs (closed-without-merge):"
gh pr list --state closed --limit 200 --json mergedAt --jq 'map(select(.mergedAt == null)) | length'
echo "Issues (closed):"
gh issue list --state closed --limit 1000 --json number | jq 'length'
echo "Discussions enabled?"
gh api repos/<owner>/<repo> --jq '.has_discussions'
```

If any are zero or low, that surface is sparse for this repo — don't sink time there.

## scars — battle-scar comments + protected code

The signal: a doc comment encoding an invariant the maintainer knows, often unstated in the docs.

### Find scars

```bash
# Marker-based (Rust + many languages)
rg -B1 -A5 "// (SAFETY|WARNING|NOTE|XXX|panics if|must not|note:|note that|important)" --type rust
rg -B1 -A5 "(/\*|//|#)\s*(SAFETY|WARNING|NOTE|XXX|TODO|FIXME|HACK):" .

# Phrase-based (language-agnostic)
rg -B2 -A4 -i "(must not|panics if|undefined behavior|unsafe to|do not|never call|footgun|gotcha)"

# Rust-specific safety doc
rg "// SAFETY:" --type rust -A3
rg "/// # Safety" --type rust -A5

# Python-specific (dynamic; less compile-time signal)
rg "# NOTE:|# WARNING:|# TODO:|# FIXME:|# HACK:" --type py -A3

# Go-specific
rg "// NOTE:|// TODO:|// HACK:" --type go -A3

# Density count per file (sort to find scar-rich modules)
rg -c "// (SAFETY|WARNING|NOTE)" --type rust | sort -t: -k2 -nr | head -20
```

### Capture the cross-reference

Don't just record the comment — record the *protected code*. The row's value is the link:

```yaml
canonical:
  comment_text: "// SAFETY: caller must hold the lock"
  marker_kind: "SAFETY"
  protected_code_excerpt: "*self.inner.get()"  # the line(s) the SAFETY note guards
  invariant: "lock must be held when accessing self.inner"  # interpreted invariant
```

Use `rg -A5` (or `-A10` if the unsafe block is larger) to capture sufficient context.

### Test names as scars

Test names often encode invariants experts worry about:

```bash
rg "fn test_handles_concurrent_drop|test_overflow_at_isize_max|test_cancel_during_poll" --type rust
rg "#\[test\]" -A2 --type rust | rg "fn test_" | head -50
```

## signatures — typed-shape recurrence (or AST-pattern recurrence)

The signal: a structural shape that appears across multiple elite codebases, encoded in types (typed languages) or AST patterns (dynamic languages).

### Typed languages — extract signatures

```bash
# Rust
rg "^pub (struct|enum|trait|type) " --type rust
rg "where\s+" --type rust -A2 | rg ":\s*(Send|Sync|'static|Sized|\?Sized|Fn|FnMut|FnOnce)"

# TypeScript
rg "^export (interface|type|class) " --type ts
ast-grep --lang ts --pattern '
interface $NAME<$$T extends $BOUNDS> {
  $$$
}'

# Go (interfaces + generic constraints)
rg "^type \w+ interface" --type go -A10
rg "\[T \w+\]" --type go  # Go 1.18+ generics

# Java
rg "^(public )?(interface|class|enum) \w+(<[^>]+>)?" --type java

# Haskell / OCaml
rg "^class \w+|^instance \w+|^data \w+|^type \w+" --type haskell
rg "^module |^type |^val " --type ocaml

# Python (gradual typing)
rg "^class \w+\[" --type py  # generic classes
rg "Protocol\[|TypeVar\(|Generic\[" --type py
```

### Dynamic languages — extract structural patterns via AST

```bash
# ast-grep pattern matching (universal — supports many languages)
ast-grep --lang python --pattern '
@$DECORATOR
def $NAME($$$):
    $$$'

ast-grep --lang js --pattern '
const $NAME = ($$$) => { $$$ }'

# Recurring shape: builder pattern across languages
ast-grep --lang rust --pattern '
impl $T { pub fn $METHOD(mut self, $$$) -> Self { self.$F = $$$; self } }'

ast-grep --lang ts --pattern '
class $T { $METHOD($$$): this { this.$F = $$$; return this; } }'

ast-grep --lang java --pattern '
public $T $METHOD($$$) { this.$F = $$$; return this; }'
```

### Cross-codebase aggregation

The signature itself is in public datasets. The *recurrence across elite codebases* is not. The aggregation step:

1. Extract signatures per source into `extracts/<source>.signatures.jsonl`.
2. After ≥3 sources, query for shape-equivalence across them:

```bash
# Naive: extract just the bound clauses, sort, count
jq -r '.canonical.bound_predicates | join(",")' extracts/*.signatures.jsonl | sort | uniq -c | sort -rn | head -20

# Semantic: shape-comparison via Claude reading clustered signatures and producing canonical patterns
```

Cross-codebase rows go into `synthesis/principles.md`, not into the per-source signatures file.

## schemas — labeled property graph

The signal: the typed-relationship structure across an item or module — nodes (types/fields/params), typed edges (has-field, returns, takes, depends-on, implements), invariant predicates (bounds, constraints).

Schemas extend signatures: a signature row captures the textual form per item; a schema row captures the *graph* — relationships between items.

### Per-item schemas (often derivable from signatures)

If you've already extracted `signatures` for a source, schemas can often be projected from them: each `signature` row's nodes/edges are mechanical to extract.

```bash
# Build per-item schema rows from extracted signatures (sketch)
jq -c 'select(.canonical.item_kind == "struct" or .canonical.item_kind == "trait") | {
  surface: .surface,
  canonical: {
    scope: "per-item",
    nodes: [...],   # constructed from signature_text + generic_params + bound_predicates
    edges: [...],
    predicates: (.canonical.bound_predicates | map({kind: "bound", expr: .}))
  },
  lineage: (.lineage | .mode = "schemas")
}' extracts/<source>.signatures.jsonl > extracts/<source>.schemas.jsonl
```

### Per-module schemas (use a language server or tree-sitter)

For richer cross-item relationships within a module, drive a language server:

```bash
# Rust — rust-analyzer CLI subset (LSP-based extraction is fiddly to script — use sparingly)
rust-analyzer analysis-stats .                 # workspace stats: types, traits, impls, items
rust-analyzer diagnostics . 2>/dev/null | head # surface compile-time concerns
rust-analyzer symbols < <(echo '{"uri":"file://'$(pwd)'/src/lib.rs"}')  # symbol enumeration

# When rust-analyzer earns its keep over ast-grep: cross-file type resolution. If a signature
# row's bound depends on a type defined elsewhere ("where T: SomeTraitFromAnotherCrate"),
# rust-analyzer can resolve the trait path; ast-grep cannot.
# When it doesn't earn its keep: per-file structural patterns. Use ast-grep — faster, scriptable.

# Tree-sitter direct
tree-sitter parse src/lib.rs --quiet | head -100   # raw AST
```

### Cross-source schemas and cross-source signature aggregation

Cross-source aggregation (one schema or signature pattern recurring across N sources) belongs in synthesis, not extraction. Two synthesis owners:

- **`models` mode** owns *entity-relationship* aggregation across sources — when 5 elite repos all expose the same domain entity (Service, Connection, Stream) with the same relationships, that goes into a `models` row.
- **Promoted principles** (in `synthesis/principles.md`) own *convergent shape* recurrence — when 5 elite repos all use the same generic-bound shape (`where T: Send + Sync + 'static` for handler types), that's a principle promoted via rule-of-three.

Per-source `extracts/*.signatures.jsonl` and `extracts/*.schemas.jsonl` stay per-source. Aggregation never goes back into extraction files.

### CodeQL for graph-extraction at scale

If `CodeQL` is available, its database-and-query model is the canonical way to extract labeled property graphs from real codebases. Setup is heavier (database build per repo, query learning) but the queries are precise.

```bash
codeql database create --language=rust --source-root=. mydb
codeql query run --database=mydb my-query.ql > schema.json
```

## models — program-model + domain-model

**Synthesis mode.** Reads `signatures` + `schemas` + naming + module organization across sources; projects program-model artifacts (control flow, data flow as text) and domain-model artifacts (entities, relationships, what the program *is*) per Pennington 1987.

### Process

1. Read `extracts/<source>.signatures.jsonl` and `extracts/<source>.schemas.jsonl` across sources.
2. Cluster signatures by domain-meaningful name (e.g., `Service`, `Connection`, `Stream`, `Buffer`, `Pool` recur across sources — that's the domain-model entity).
3. Identify cross-codebase entity-relationship structures (the same `Service<Request> → Future<Response>` shape across Tower, Hyper, Axum).
4. Project as one `models` row per coherent entity-relationship cluster.

### Locating naming clusters

```bash
# Pull all public type names across sources
jq -r 'select(.canonical.item_kind | IN("struct","trait","interface","class","enum")) | .canonical.name' extracts/*.signatures.jsonl | sort | uniq -c | sort -rn | head -30

# Pull all generic parameter names (often domain-meaningful: Request, Response, Item, ...)
jq -r '.canonical.generic_params[]?' extracts/*.signatures.jsonl | sort | uniq -c | sort -rn | head -20
```

### Distinguishing program-model vs domain-model

- **Program model**: what the code *does* — function signatures expressing control flow, data flow as text, procedural decomposition. Surfaces in signatures + schemas as the *operational* shape (verbs, methods, transitions).
- **Domain model**: what the code *is* — entities, relationships, goals. Surfaces in signatures + schemas as the *noun-shaped* core (types, traits, the conceptual things).

Per Burkhardt 1997, expert advantage is concentrated in the *static* situation model (the domain-model in Pennington's terms). Higher mining yield in the domain-model layer than the program-model layer.

## tradeoffs — alternatives and rationale

**Synthesis mode.** Reads RFCs + PR archaeology + `oscillations` rows + "we chose X" comments; distills named alternatives + rationale per decision.

### Process

1. Read `extracts/<source>.oscillations.jsonl` — each is a rejected-then-resettled tradeoff.
2. Read RFC archaeology — explicit alternatives + rationale sections.
3. Read PR archaeology — closed-without-merge PRs are rejected alternatives.
4. Project as one `tradeoffs` row per decision.

### Find decision archaeology

```bash
# RFCs — typically in rfcs/ directory (Rust language, WebAssembly/component-model, etc.)
ls rfcs/ rfc/ docs/rfcs/ 2>/dev/null
rg "(rejected|alternatives considered|drawbacks|unresolved questions)" rfcs/ rfc/ 2>/dev/null

# Project-internal design docs (rust-analyzer's docs/dev, tower's docs, etc.)
ls docs/dev/ docs/design/ docs/architecture/ 2>/dev/null
cat docs/dev/architecture.md docs/dev/style.md 2>/dev/null  # rust-analyzer pattern
rg "(why|rationale|chose|alternative|considered)" docs/dev/ docs/design/ 2>/dev/null

# RELEASES.md / CHANGELOG.md with substantive entries (tokio, hyper)
cat RELEASES.md CHANGELOG.md NEWS.md 2>/dev/null | head -300
rg -B1 -A5 "(breaking|removed|deprecated|behavior change|design change)" RELEASES.md CHANGELOG.md 2>/dev/null | head -100

# PR threads with substantive review
gh pr list --state merged --limit 100 --json number,title,body --jq '.[] | select(.body | length > 500)'
gh pr view <N> --comments

# ADRs — architecture decision records (less common in Rust ecosystem, more common in Go/Java)
ls docs/adr/ docs/architecture/ adr/ 2>/dev/null
rg "^## (Decision|Alternatives|Rationale|Consequences)" docs/

# "we chose X over Y" comments
rg -B2 -A4 -i "(we chose|we picked|chose this over|alternative|considered.*but|instead of)" --type rust --type go --type ts
```

### Compose with oscillations

Each oscillation row is a *partial* tradeoff — the alternative was tried and reverted. Pair with RFC/PR archaeology to recover the full alternatives-considered set.

## antipatterns — looks-reasonable-fails

**Synthesis mode.** Reads `oscillations` (reverts) + closed-without-merge PRs + scars-with-replacement; distills the abstract pattern across multiple specific failures.

### Process

1. Read `extracts/<source>.oscillations.jsonl` — each revert names a failure mode.
2. Cluster failure modes across sources (the same revert pattern repeated across N codebases is a candidate antipattern).
3. Read closed-without-merge PRs — rejected approaches are antipattern data.
4. Read `scars` with `replacement:` annotations.
5. Project as one `antipatterns` row per cluster.

### Find antipattern data

```bash
# Closed-without-merge PRs (rejected approaches)
gh pr list --state closed --limit 200 --json number,title,body,mergedAt --jq '.[] | select(.mergedAt == null) | "PR #\(.number): \(.title)"'

# DON'T / NEVER comments in code
rg -B2 -A4 -i "(DON'T|don't|NEVER|never|avoid this|do not|footgun|gotcha)" --type rust --type go --type ts

# Reverts that share a failure mode
jq -r '.canonical.failure_mode' extracts/*.oscillations.jsonl | sort | uniq -c | sort -rn | head -20

# Off-the-shelf antipattern rules (if Semgrep is available)
semgrep --config=auto .
```

### What makes it *not* a tradeoff

A tradeoff weighs alternatives and chooses one consciously. An antipattern is something that *appears* reasonable until you discover the failure mode. The marker: "looks like" — what makes the antipattern attractive in the first place.

## aesthetics — what "right" feels like

**Synthesis mode.** Reads `scars` + `signatures` + style guides + cross-codebase consistency signals (naming, comment voice, error-message density, derive/decorator patterns).

### Process

1. Read style guides if present (CONTRIBUTING.md, STYLE.md, docs/style*).
2. Read `scars` — explicit normative statements ("must", "should", "prefer X").
3. Sample cross-codebase consistency: same naming convention across N sources = aesthetic.
4. Triangulate: explicit statement + exemplar density + cross-codebase consistency = high confidence; single-source aesthetic = low confidence.
5. Project as one `aesthetics` row per pattern.

### Find aesthetic signals

```bash
# Style guides
ls STYLE.md CONTRIBUTING.md docs/style* 2>/dev/null
rg -l "(api guideline|style guide|convention|preferred|idiom)" docs/ 2>/dev/null

# Naming consistency — pick a domain noun
rg "fn (\w*_handler|handle_\w*|process_\w*|on_\w*)" --type rust | head -30   # adjust per language

# Error message density
rg "(\.context|format_err!|anyhow!|return Err|fmt\.Errorf)" -A1 | head -40

# Public API ergonomics (Rust derive density)
rg "^#\[derive\(" --type rust | rg -o "derive\([^)]+\)" | sort | uniq -c | sort -rn | head -20

# Decorator chain patterns (Python/TS)
rg "^@\w+" --type py | sort | uniq -c | sort -rn | head -20

# Comment voice (sample reads, not greppable — calibrate manually)
```

### Confidence calibration

- Single-source aesthetic = low confidence (might be local quirk)
- Multi-source consistency without explicit statement = medium confidence
- Multi-source consistency + explicit normative statement (style guide / RFC) = high confidence

## Cross-mode: dispatch sketch

If the user's goal could fit multiple modes, run a triage pass first:

```bash
echo "oscillations density (reverts):"
git log --all --grep="revert\|why\|chose" --oneline | wc -l
echo "scars density (markers):"
rg -i "(SAFETY|WARNING|NOTE|panics if|must not)" -c | wc -l
echo "signatures density (public types — adjust per language):"
rg "^pub (struct|enum|trait|type) " | wc -l
```

Whichever is richest is probably where to start — but match the user's goal, not the volume.

## Per-language adaptations

The recipes above are partly Rust-flavored (because Rust has the densest type-system encoded invariants of any popular language). Adaptations:

| Language | Signature mode | Scar markers | Oscillation richness |
|---|---|---|---|
| Rust | High (generic bounds, lifetimes, `'static`, `Send`/`Sync`) | `// SAFETY:`, `// NOTE:`, `panics if`, `must not` | High in foundation crates |
| Go | Medium (interfaces, generic constraints since 1.18) | `// NOTE:`, `// TODO:`, less marker convention | High in stdlib + popular packages |
| TypeScript | Medium-high (structural types, conditional types) | `// NOTE:`, `// FIXME:`, JSDoc `@deprecated` | Variable |
| Python | Lower (gradual typing reduces signature density); but decorator chains and Protocol structures rich | `# NOTE:`, `# TODO:`, less marker convention | Variable |
| Java | Medium (generics + bounded type parameters) | `// NOTE:`, `// FIXME:`, Javadoc `@apiNote` | High in mature libraries |
| Haskell / OCaml | Very high (the type is the spec) | Comments less marker-conventional; types do the work | Variable |
| C / C++ | Medium (`const`, `volatile`, `noexcept`, `restrict`) | `// SAFETY:`, `// WARNING:`, `// TODO:` | High in long-lived projects |

For dynamic languages where signature mode is weak, lean harder on:
- Test names (encoding invariants the maintainer worries about)
- Decorator chains (encoding cross-cutting concerns as patterns)
- Protocol / ABC structures (the "duck typing made explicit")
- Convention-by-name (e.g., Python's `__dunder__` methods)

## When recipes don't apply

A repo with non-standard layout (no `src/`, no `Cargo.toml`/`package.json`/`go.mod`, custom build) — Phase 3b recon should have surfaced the layout. Adapt the recipes to what you found, or accept lower yield from this source and move on.
