# Worked Example — Elite Rust starter list

This is a worked example of a curated mining corpus for one domain (elite Rust). It demonstrates *what a curated starter list looks like* — the methodology applies to any language or domain. For your own domain, build the analogous list using the heuristics in `references/dataset-selection.md` and the sources listed there.

Use this list in Phase 2 (dataset selection — domain mode for Rust). Pick 3–5 to begin with, expand by goal, vet additions with the user.

The list is grouped by what each repo is good for *as a mining target*, not what it does as software. A repo lands on the list because its design choices are widely-cited, its archaeology is rich (PRs, RFCs, reverts), or its conventions exemplify "elite" practice — i.e., it scores well on the [strong signals from `dataset-selection.md`](../dataset-selection.md#heuristics-for-elite-repo-identification).

## Contents

- [Foundation — async runtimes, IO, primitives](#foundation--async-runtimes-io-primitives)
- [Application — large user-facing programs](#application--large-user-facing-programs)
- [Domain — specialized exemplars](#domain--specialized-exemplars)
- [Concurrency / data structures](#concurrency--data-structures)
- [Ecosystem-shaping](#ecosystem-shaping)
- [Picking from this list](#picking-from-this-list)
- [Adding to the list](#adding-to-the-list)
- [Beyond Rust](#beyond-rust)

## Foundation — async runtimes, IO, primitives

These are the load-bearing crates the rest of the ecosystem depends on. High archaeological value (decade of design oscillations) and high pattern density.

| Repo | Why mine it |
|---|---|
| `tokio-rs/tokio` | The dominant async runtime — `Pin`/`!Send` archaeology, executor design tradeoffs, fairness oscillations |
| `hyperium/hyper` | HTTP — protocol-correctness vs ergonomics tradeoffs; has been rewritten enough that the diffs are gold |
| `tokio-rs/axum` | Web framework — extractor pattern, type-driven middleware composition |
| `tower-rs/tower` | The `Service` trait — a pattern adopted ecosystem-wide; canonical for composition |
| `Amanieu/parking_lot` | Lock-free / fast-path locking — performance vs correctness tradeoff exemplar |
| `crossbeam-rs/crossbeam` | Concurrency primitives — channel design space, epoch-based GC |
| `tokio-rs/bytes` | Zero-copy buffer abstractions — `Bytes`/`BytesMut` design is widely imitated |
| `serde-rs/serde` | The serialization ecosystem — derive macro patterns, custom Serializer/Deserializer protocols |

## Application — large user-facing programs

Mature applications written in idiomatic Rust. Useful for end-to-end pattern extraction (how the foundation crates compose at scale).

| Repo | Why mine it |
|---|---|
| `BurntSushi/ripgrep` | Performance-focused CLI; canonical for "Rust as fast tool" idioms |
| `rust-lang/rust-analyzer` | LSP server — incremental computation, salsa pattern, large-codebase navigation |
| `rust-lang/cargo` | The build tool — config layering, manifest design, dependency resolution |
| `clap-rs/clap` | CLI parsing — derive vs builder API debates, breaking-change archaeology |

## Domain — specialized exemplars

Each represents an idiom-defining solution in a specific domain.

| Repo | Why mine it |
|---|---|
| `tauri-apps/tauri` | Desktop app framework — IPC design, Rust↔frontend boundary patterns |
| `bytecodealliance/wasmtime` | WASM runtime — VM-design patterns, sandboxing tradeoffs |
| `bytecodealliance/cranelift` | Code generator — IR design, optimization-pass patterns |
| `launchbadge/sqlx` | DB driver with compile-time-checked queries — macro-as-type-system pattern |
| `aya-rs/aya` | eBPF in Rust — unsafe-Rust at scale, kernel-boundary patterns |
| `WebAssembly/component-model` | Component model spec/impl — RFC archaeology rich |
| `hyperium/tonic` | gRPC — codegen patterns, async stream protocols |
| `tokio-rs/tracing` | Structured logging — span design, subscriber/layer composition |

## Concurrency / data structures

Specialized libraries where the design decisions are the whole product.

| Repo | Why mine it |
|---|---|
| `jonhoo/flurry` | Concurrent hash map — port of Java ConcurrentHashMap — instructive divergences |
| `jonhoo/left-right` | Eventually-consistent concurrency — pattern with strong commentary in commits |
| `Amanieu/hashbrown` | The hash map under `std::HashMap` — performance-vs-API tradeoffs |
| `dtolnay/anyhow` | Application error type — context-attaching pattern, ergonomics target |
| `dtolnay/thiserror` | Library error type — derive-driven enum errors — paired with anyhow as the canonical pair |

## Ecosystem-shaping

Crates whose API choices propagated outward.

| Repo | Why mine it |
|---|---|
| `diesel-rs/diesel` | Compile-time-checked ORM — type-system-as-design exemplar |
| `SeaQL/sea-orm` | Async ORM — divergent design choices vs diesel |
| `rust-lang/rust` | The compiler — for reading RFC implementations against the spec; archaeology is unmatched |

---

## Picking from this list

When in Phase 2, don't pick "the top 5." Pick by goal:

| Goal | Start with |
|---|---|
| Async runtime tradeoffs | tokio, hyper, async-std (compare) |
| Error handling discipline | anyhow + thiserror + 3 application repos that use them |
| Concurrent data structures | crossbeam, parking_lot, flurry, left-right |
| Macro-driven API design | serde, sqlx, diesel |
| Performance-critical code | ripgrep, hashbrown, parking_lot |
| Large-codebase navigation patterns | rust-analyzer, cargo, rust |
| RFC archaeology | rust-lang/rust, WebAssembly/component-model |

Once you've mined 3+ from a category, the rule of three becomes possible — Phase 4 synthesis can promote findings to principles.

## Adding to the list

If a candidate repo isn't here, ask:

- Is it widely cited in the elite-Rust community?
- Does it have rich archaeology (PRs with substantive discussion, RFCs, reverts with explanations)?
- Are its conventions imitated elsewhere?

Yes to two of three = worth adding. Yes to none = probably not elite enough for mining; the noise will outweigh the signal.

## Beyond Rust

For other languages, ask the user for the analog list. Heuristics that translate:
- Foundation crates → standard library + the top-N most-depended-on packages
- Application exemplars → the canonical 1–3 large user-facing programs in the language
- Domain exemplars → 5–10 idiom-defining libraries across distinct domains
