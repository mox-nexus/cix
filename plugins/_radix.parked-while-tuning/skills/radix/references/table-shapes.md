# Table Shapes — Per-Mode Canonical Form

The canonical projection per mode. Every row in `extracts/<source>.<mode>.jsonl` (extraction modes) and `synthesis/<mode>.jsonl` (synthesis modes) has the universal envelope (`surface` + `canonical` + `lineage`) and a per-mode `canonical` shape defined here.

Don't invent your own shapes. Downstream tools (synthesis, query, future builders) depend on shape stability.

## Contents

- [Universal envelope](#universal-envelope)
- [Extraction modes (Phase 3c)](#extraction-modes-phase-3c)
  - [oscillations](#oscillations)
  - [scars](#scars)
  - [signatures](#signatures)
  - [schemas](#schemas)
- [Synthesis modes (Phase 4)](#synthesis-modes-phase-4)
  - [models](#models)
  - [tradeoffs](#tradeoffs)
  - [antipatterns](#antipatterns)
  - [aesthetics](#aesthetics)
- [Principles (cross-mode promotion)](#principles-cross-mode-promotion)
- [Cross-mode notes](#cross-mode-notes)

## Universal envelope

```yaml
surface:
  text: <verbatim source — the provenance anchor>
  location: <addressable: path:line | commit:sha | issue:#N | rfc:section | discussion:#N>
  kind:
    file-content: code | doc-comment | source-text          # file-resident
    forge-content: commit-msg | pr-discussion | issue       # git/forge artifact
    document-genre: rfc | adr | spec | book-chapter         # standalone document
    # use the most specific value; the three groups above just clarify the ontology
canonical:
  # per-mode shape (below)
lineage:
  source: <repo-url-or-path>
  commit: <sha>
  mode: <mode name>
  extracted_at: <YYYY-MM-DDTHH:MM:SSZ — iso-8601 utc, second precision>
  extracted_by: <agent-id — value, not constraint; e.g., "claude" or "gpt-5-2025-Q1">
```

JSONL = one row per line, no whitespace inside the JSON. Pretty-print only when reading.

For synthesis-mode rows, `surface.text` is the *most-load-bearing supporting verbatim*; the full N-of-3+ supporting list lives in `canonical.supporting_evidence_refs`.

## Extraction modes (Phase 3c)

Direct per-row capture from a single source. Each row is one finding with verbatim provenance.

### oscillations

```yaml
canonical:
  original_commit: <sha>
  revert_commit: <sha>
  resettle_commit: <sha-or-null-if-no-resettle-yet>
  file: <primary file affected>
  failure_mode: <distilled from revert_message>
  original_diff_summary: <one-line>
  resettle_diff_summary: <one-line>
  revert_message: <verbatim revert message>
```

**Exemplar**:

```json
{"surface":{"text":"revert: hyper PR #2342 — Connection pool reuse caused use-after-poll on cancelled futures","location":"hyperium/hyper@9a8b7c6d","kind":"commit-msg"},"canonical":{"original_commit":"6f3a2b1c","revert_commit":"9a8b7c6d","resettle_commit":"ee4f5d2a","file":"src/client/pool.rs","failure_mode":"use-after-poll on cancelled futures","original_diff_summary":"Added connection reuse via shared Arc<Pool>","resettle_diff_summary":"Per-connection ownership with explicit Drop guards","revert_message":"This reverts commit 6f3a2b1c. Connection pool reuse caused use-after-poll..."},"lineage":{"source":"hyperium/hyper","commit":"ee4f5d2a","mode":"oscillations","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### scars

```yaml
canonical:
  comment_text: <verbatim comment, marker stripped>
  marker_kind: SAFETY | WARNING | NOTE | XXX | HACK | "panics if" | "must not" | other
  protected_code_excerpt: <N lines of code the comment guards>
  invariant: <interpreted invariant being protected>
  language_construct: <e.g., "unsafe block" | "panic-on-condition" | "lock-required-access" | "RAII guard">
```

**Exemplar**:

```json
{"surface":{"text":"// SAFETY: caller must hold the lock before accessing self.inner\n*self.inner.get()","location":"parking_lot/src/raw_mutex.rs:142","kind":"doc-comment"},"canonical":{"comment_text":"caller must hold the lock before accessing self.inner","marker_kind":"SAFETY","protected_code_excerpt":"*self.inner.get()","invariant":"lock held by caller; access only via this method when locked","language_construct":"unsafe block"},"lineage":{"source":"Amanieu/parking_lot","commit":"<sha>","mode":"scars","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### signatures

```yaml
canonical:
  item_kind: fn | trait | struct | enum | impl | type | interface | class | module | function
  name: <item name>
  signature_text: <verbatim full signature>
  generic_params: [<param-name>, ...]
  bound_predicates: [<predicate-text>, ...]   # e.g., "T: Send + Sync + 'static"
  visibility: public | crate-private | private | other
  language: <rust | go | ts | python | java | ...>
```

**Exemplar**:

```json
{"surface":{"text":"pub trait Service<Request> {\n    type Response;\n    type Error;\n    type Future: Future<Output = Result<Self::Response, Self::Error>>;\n    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>>;\n    fn call(&mut self, req: Request) -> Self::Future;\n}","location":"tower-rs/tower-service/src/lib.rs:23","kind":"code"},"canonical":{"item_kind":"trait","name":"Service","signature_text":"pub trait Service<Request>","generic_params":["Request"],"bound_predicates":["Self::Future: Future<Output = Result<Self::Response, Self::Error>>"],"visibility":"public","language":"rust"},"lineage":{"source":"tower-rs/tower","commit":"<sha>","mode":"signatures","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### schemas

Labeled property graph: typed nodes + typed edges + invariant predicates. Captures structural **relationships across multiple types** (cross-item) at module-or-broader scope. Per-item structural extraction belongs in `signatures`; `schemas` exists when a single signature row isn't enough — when you need the *graph* of related types.

```yaml
canonical:
  scope: per-module | per-source | cross-source
  nodes:
    - {id: <node-id>, kind: type | field | param | trait | resource | endpoint, label: <name>, attrs: {...}}
  edges:
    - {from: <node-id>, to: <node-id>, kind: has-field | returns | takes | depends-on | implements | extends | composes, label: <relationship>, attrs: {...}}
  predicates:
    - {kind: invariant | constraint | precondition | bound, expr: <text>, refs: [<node-ids>], lang_specific: bool}
```

**Exemplar** (a per-module schema — a request-handling pipeline with multiple related types):

```json
{"surface":{"text":"pub trait Service<Request> { type Response; type Error; type Future: Future<Output = Result<Self::Response, Self::Error>>; ... }\n\npub trait Layer<S> { type Service; fn layer(&self, inner: S) -> Self::Service; }\n\npub struct ServiceBuilder<L> { layer: L }","location":"tower-rs/tower/src/lib.rs:1-180","kind":"code"},"canonical":{"scope":"per-module","nodes":[{"id":"n0","kind":"trait","label":"Service","attrs":{"generic_params":["Request"]}},{"id":"n1","kind":"trait","label":"Layer","attrs":{"generic_params":["S"]}},{"id":"n2","kind":"type","label":"ServiceBuilder","attrs":{"generic_params":["L"]}},{"id":"n3","kind":"type","label":"Future","attrs":{"associated":true}}],"edges":[{"from":"n1","to":"n0","kind":"produces","label":"Layer::layer wraps an inner Service"},{"from":"n2","to":"n1","kind":"composes","label":"ServiceBuilder accumulates Layers"},{"from":"n0","to":"n3","kind":"returns","label":"Service::call returns a Future"}],"predicates":[{"kind":"bound","expr":"Self::Future: Future<Output = Result<Self::Response, Self::Error>>","refs":["n0","n3"],"lang_specific":true}]},"lineage":{"source":"tower-rs/tower","commit":"<sha>","mode":"schemas","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

(For a single struct's fields, prefer a `signatures` row — the per-item structural shape captured as text. `schemas` shines when the graph of relationships across N items carries the design.)

## Synthesis modes (Phase 4)

Cross-row reasoning. Each row consumes ≥1 extraction-mode row (or other synthesis-mode rows) and projects an interpretation. The `surface.text` field carries the most-load-bearing supporting verbatim; full evidence in `canonical.supporting_evidence_refs`.

### models

Program model + domain model per Pennington 1987. Captures the conceptual entities and relationships the source uses — what the program *is* (domain model: entities, relationships, goals) and what it *does* (program model: control flow, data flow, procedural structure).

```yaml
canonical:
  model_frame: program | domain | cognitive | formal
  entities:
    - {id: <entity-id>, label: <name>, role: <core | supporting | boundary>, attrs: {...}}
  relationships:
    - {from: <entity-id>, to: <entity-id>, kind: <relationship-type>, label: <name>}
  description: <one-paragraph statement of what this model captures>
  supporting_evidence_refs:
    - {source: <repo>, mode: <extraction-mode>, location: <path:line>, summary: <one-line>}
    - ...
```

**Exemplar** (a domain-model row from mining a web framework):

```json
{"surface":{"text":"pub trait Service<Request> { ... }","location":"tower-rs/tower-service/src/lib.rs:23","kind":"code"},"canonical":{"model_frame":"domain","entities":[{"id":"e0","label":"Service","role":"core","attrs":{"protocol":"async-readiness"}},{"id":"e1","label":"Request","role":"boundary"},{"id":"e2","label":"Response","role":"boundary"},{"id":"e3","label":"Future","role":"core","attrs":{"shape":"async result"}}],"relationships":[{"from":"e0","to":"e1","kind":"consumes","label":"Service::call takes Request"},{"from":"e0","to":"e2","kind":"produces","label":"via Future yielding Result<Response>"}],"description":"The Service trait is the domain core: a stateful async function from Request to Future<Response>. Tower, Hyper, Axum, Tonic all converge on this entity-relationship structure.","supporting_evidence_refs":[{"source":"tower-rs/tower","mode":"signatures","location":"tower-service/src/lib.rs:23","summary":"Service trait definition"},{"source":"hyperium/hyper","mode":"signatures","location":"src/service/service.rs:14","summary":"Service trait re-export"},{"source":"tokio-rs/axum","mode":"signatures","location":"axum-core/src/extract/mod.rs:88","summary":"Handler-as-Service composition"}]},"lineage":{"source":"<workspace synthesis>","commit":"<workspace commit>","mode":"models","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### tradeoffs

Decisions with named alternatives + rationale. Read across RFCs, PR archaeology, oscillations, and "we chose X" comments.

```yaml
canonical:
  alternatives: [<alt_1>, <alt_2>, ...]
  decision: <the chosen alternative>
  rationale: <why this one>
  forces: [<force_1>, <force_2>, ...]   # what was being weighed
  context: <when this decision applies — scope of the choice>
  supporting_evidence_refs: [...]
```

**Exemplar**:

```json
{"surface":{"text":"We considered (a) implicit Box::pin desugar, (b) explicit Box<dyn Future>, (c) generic associated types... The committee chose (a) for ergonomics matching sync trait methods.","location":"rust-lang/rfcs/text/3185-async-fn-in-trait.md:78","kind":"rfc"},"canonical":{"alternatives":["implicit Box::pin","explicit Box<dyn Future>","GAT-based"],"decision":"implicit Box::pin (desugar)","rationale":"ergonomics matching sync trait methods","forces":["ergonomics","desugar transparency","perf"],"context":"trait method desugar in stable Rust 2024","supporting_evidence_refs":[{"source":"rust-lang/rfcs","mode":"oscillations","location":"text/3185:78","summary":"RFC alternatives section"}]},"lineage":{"source":"<workspace synthesis>","commit":"<workspace commit>","mode":"tradeoffs","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### antipatterns

Approaches that look reasonable but fail. Distinct from `tradeoffs` — a tradeoff weighs alternatives and chooses one; an antipattern is something that *appears* to be a reasonable choice but breaks in practice.

```yaml
canonical:
  pattern_text: <abstract statement of the antipattern>
  why_fails: <the failure mode>
  looks_like: <what makes it appear reasonable>
  replacement: <the right approach instead — optional but high-value>
  supporting_evidence_refs: [...]
```

**Exemplar**:

```json
{"surface":{"text":"// DON'T cache Futures here — they're stateful and a cached one will replay completed state","location":"<source>/src/cache.rs:88","kind":"doc-comment"},"canonical":{"pattern_text":"caching a Future before polling it","why_fails":"Futures are stateful; a cached Future replays its completed state instead of progressing","looks_like":"caching is a standard optimization","replacement":"cache the awaited output, not the Future","supporting_evidence_refs":[{"source":"<repo-A>","mode":"scars","location":"src/cache.rs:88"},{"source":"<repo-B>","mode":"oscillations","location":"<sha>","summary":"reverted attempt to cache Futures"},{"source":"<repo-C>","mode":"scars","location":"src/transport.rs:142"}]},"lineage":{"source":"<workspace synthesis>","commit":"<workspace commit>","mode":"antipatterns","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

### aesthetics

What "right" feels like in this domain — the aesthetic principles experts encode but rarely state. Lower-confidence by nature; multi-signal triangulation strengthens (explicit statement + exemplar density + cross-codebase consistency + model bias).

```yaml
canonical:
  aesthetic_label: <short name>
  description: <one-paragraph statement>
  exemplar_refs: [<source refs to canonical examples>]
  counter_exemplar_refs: [<source refs to violations>]   # optional
  rationale: <why this aesthetic is preferred>            # optional
  confidence: low | medium | high   # low: single-source; medium: multi-source; high: explicit-statement + multi-source-density
  supporting_evidence_refs: [...]
```

**Exemplar**:

```json
{"surface":{"text":"return Err(anyhow!(\"failed to bind on {addr}\")).context(format!(\"port {port} already in use\"));","location":"<source>/src/server.rs:54","kind":"code"},"canonical":{"aesthetic_label":"errors-carry-context","description":"Errors carry enough context to debug from the error message alone, without requiring the caller to reconstruct context. Ubiquitous via anyhow::Context and thiserror's #[error(\"...\")] templates.","exemplar_refs":[{"source":"<repo-A>","location":"src/server.rs:54"},{"source":"<repo-B>","location":"src/handler.rs:101"},{"source":"<repo-C>","location":"src/db.rs:223"}],"rationale":"reduces debugging to reading the error chain","confidence":"medium","supporting_evidence_refs":[{"source":"<repo-A>","mode":"scars","location":"src/server.rs:54"},{"source":"<repo-B>","mode":"signatures","location":"<location>"}]},"lineage":{"source":"<workspace synthesis>","commit":"<workspace commit>","mode":"aesthetics","extracted_at":"2026-05-04T12:00:00Z","extracted_by":"claude"}}
```

## Principles (cross-mode promotion)

Principles are not a separate mode — they're a *promotion criterion*. Any synthesis-mode row recurring across ≥3 independent sources can be promoted to a principle in `synthesis/principles.md`.

The principle row format (markdown, not JSONL — principles are human-readable artifacts):

```markdown
## P<N> — <statement>

- Source mode: <which synthesis mode produced this>
- Recurring in: <source>, <source>, <source>, ...
- Source count: <int>
- Cross-paradigm: <yes/no>
- Surface evidence:
  - <source> @ <location> — "<verbatim>"
  - <source> @ <location> — "<verbatim>"
  - <source> @ <location> — "<verbatim>"
- Scope: domain-wide | paradigm-specific | tooling-specific
- Confidence: floor (≥3 within paradigm) | strong (≥4 within paradigm) | cross-paradigm (≥3 across paradigms)
```

A principle's evidence is the cross-source supporting set; the canonical statement is the abstracted claim.

## Cross-mode notes

- **Surface preservation is mandatory across all modes.** No row without `surface.text` and `surface.location`. This invariant never relaxes.
- **`surface.text` must be `rg`-locatable in the source** at `surface.location`. Don't paraphrase, don't reformat, don't strip whitespace differently than the source.
- **JSONL one row per line** — no embedded newlines in the JSON. JSON-escape verbatim newlines as `\n`.
- **Don't merge canonical fields across modes.** If you find yourself wanting to put `signature_text` and `decision` in the same row, you have two rows — split them.
- **Synthesis modes consume extraction-mode rows.** They reference them via `canonical.supporting_evidence_refs`.
- **Referential integrity** (Discipline #10): every `supporting_evidence_refs` entry must point to an extraction row that *exists in the workspace* — verify before writing the synthesis row. Never invent supporting evidence.
- **Synthesis `surface.text` must be a verbatim quote from one of `supporting_evidence_refs`** — specifically the most-load-bearing one. Don't synthesize a `surface.text` that doesn't appear in any referenced extraction row.
- **Per-jsonl-file commit invariance** (Discipline #5): all rows in `extracts/<source>.<mode>.jsonl` for one extraction pass share one `lineage.commit`. If a `git pull` happens mid-pass, start a new pass (and new file or restart).
- **Confidence semantics**:
  - Code that compiles is ground truth for its own assertion (the bounds are enforced; the signature is real).
  - Doc comments are testimony from the maintainer (high-credibility but not ground truth).
  - Synthesis rows are abstractions — confidence comes from the supporting evidence count and cross-paradigm spread.
- **Cross-codebase signature aggregation** is owned by the `models` synthesis mode (entity-relationship recurrence) and by promoted principles in `synthesis/principles.md` (rule-of-three convergence). Per-item signature rows in `extracts/*.signatures.jsonl` stay per-source; aggregation happens in synthesis, not by writing cross-source signatures rows.
