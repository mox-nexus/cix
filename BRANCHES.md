# Branches preserved at wind-down

> Reference for branches that were intentionally **not** merged into `main` when this repo was archived in favor of [mox-labs/gnx](https://github.com/mox-labs/gnx). Each was either out of scope for the wind-down (research, not plugins/tools/architecture), partially superseded, or in-flight work parked for migration.

**Date:** 2026-05-20

---

## `wip/memex-perf-adapters`

**Created during wind-down (2026-05-20) to preserve uncommitted work found in the `cix-memex-next` worktree.**

| | |
|---|---|
| Tip | `1f11f94` (branched from `feat/memex-plaintext-daemon@1c3e683`) |
| Lines | +692 / -232 |
| Status | Working but unreviewed |

Contents:

- `tools/memex/src/memex/adapters/_out/embedding/mlx_embedder.py` — Native Metal inference via `mlx-embeddings` for Apple Silicon. Replaces the broken ONNX/fastembed path; handles dynamic input shapes natively on unified memory.
- `tools/memex/src/memex/adapters/_out/embedding/st_embedder.py` — Sentence-transformers adapter using PyTorch MPS (Apple Silicon) or CUDA (Linux/Windows). Defaults to EmbeddingGemma. Replaces fastembed/ONNX when the `gpu` extra is installed.
- `tools/memex/src/memex/adapters/_out/sources/gemini/` — Gemini conversations source adapter (`__init__.py`, `adapter.py`) alongside the existing Claude + OpenAI source adapters.

**Next step:** Migrate the work into gnx's memex equivalent (or, if memex stays here as a tool, open as a PR — but the gnx-side direction is more likely).

---

## `lance`

**Research workstream. Parked.**

| | |
|---|---|
| Tip | `99de759` |
| Unique commits | 18 |
| Last activity | 2026-04-25 |

The "lance" workstream — research consolidation, Round 3 gap-coverage inquiries, cross-model verification. Out of scope for the plugins/tools/arch-design wind-down boundary.

Top commits:

```
99de759 research(round-3): gap-coverage inquiries doc + light verification
f12fb13 docs(research): concepts.md — methodological corrections + design thesis
c2fb36a feat(research): Round 2 cross-model verification — SHIP all streams
```

**Worktree:** This branch is checked out at `~/mox/products/cix-memex-next-lance/` locally.

**Next step:** Material is research output; if anything is load-bearing for gnx, surface it back into the gnx research substrate. Otherwise: archival.

---

## `snap/lance-2026-05-04`

**Snapshot superset of `lance`.**

| | |
|---|---|
| Tip | `ebaac59` |
| Unique commits | 19 (= `lance` + 1 snapshot commit) |
| Last activity | 2026-05-04 |

`snap/lance-2026-05-04` ⊃ `lance`. Contains all 18 lance commits plus one snapshot on top:

```
ebaac59 snapshot: memex-next design + research consolidation (2026-05-04)
99de759 research(round-3): ...  (lance from here down)
```

**Next step:** Whatever decision applies to `lance` applies here. If lance gets archived, this also goes.

---

## `feat/library-ia`

**Mixed bag: ~75% experience-layer rewrites, ~25% product changes. Stale.**

| | |
|---|---|
| Tip | `b899ce4` |
| Unique commits | 8 (of 9; 1 already content-merged) |
| Last activity | 2026-02-25 |

Top commits:

```
b899ce4 fix(catalog): add missing PluginDetail.svelte
4748a35 chore(cix): prep for PyPI publishing + fix install URLs
0dcab17 feat(docs): rename library → docs, condense 6 articles → 3
6aa0945 fix(library): strip pipeline evidence brackets from articles
7ff2dbf fix(library): remove .md from file properties, fix base path check
7aa2ace fix(library): add Ashery et al. 2025 to bibliography
49f2feb fix(library): rebuild bibliography from v3 article citations
310a9c9 feat(library): rebuild evidence library as 6-article argument arc
cd13ea9 feat(library): IA restructure, content rewrites, landing polish
```

**Product changes worth salvaging:**
- `tools/cix/` PyPI publishing prep (LICENSE, README, pyproject.toml)
- `plugins/run-openclaw-srt/docs/**` and `skills/openclaw-srt-setup/**` mass deletion (deprecated plugin cleanup, ~5000 lines removed)

**Experience changes likely superseded:** library→docs rename, article condensation. The docs site has evolved since February.

**Next step:** Cherry-pick the PyPI-prep bits into gnx if `cix` CLI is being kept. Otherwise: archival.

---

## `feat/collab-scaffolds-v2`

**Plugin work, almost certainly superseded.**

| | |
|---|---|
| Tip | `61d0c16` |
| Unique commits | 2 (of 4; 2 already content-merged) |
| Last activity | 2026-02-09 |
| Behind main | 70 commits |

`collab-scaffolds` v0.5.0 work — adds `building`, `collaboration`, `problem-solving` skills; adds `detect-stuck.sh`, `incomplete-refactoring-guard.sh`, `scaffolding-cleanup-gate.sh` hooks; removes Advocate agent.

The plugin was subsequently renamed `collab-scaffolds` → `ci-scaffolds` and rewritten. Recent PR #48 (`refactor(ci-scaffolds): drop legacy hook system, add mudge agent + whitehat skill`) is the modern successor work, already on `main`.

**Next step:** Almost certainly archival. Confirm nothing in those 2 commits failed to make it forward, then close.

---

## What was merged in the wind-down

For completeness — these PRs landed on `main` as the wind-down state:

| PR | Subject |
|---|---|
| #44 | chore: add MIT LICENSE |
| #45 | feat(antifragile): plugin |
| #46 | feat(assay): tool |
| #47 | feat(guild-arch): trust-boundaries skill + docs |
| #48 | refactor(ci-scaffolds): drop legacy hook system, add mudge agent + whitehat skill |
| #49 | docs(craft-extensions): scaffolding |
| #50 | docs(craft-rhetoric): scaffolding |
| #51 | feat(craft-research): collecting spoke updates + new docs/references |
| #52 | refactor(recon): collectors and configs |
| #54 | feat(radix): park plugin while tuning in external workspace |
| #55 | fix: clean project lint (ruff check + format) for wind-down |
| #41 | feat(memex): v0.3.0 — metadata, adapter split, graph traversal, DuckPGQ, plaintext daemon |
| #42 | feat(ix): per-probe activation, config-driven repeats, confusion matrix |

19 content-merged branches (work already on `main` via different SHAs) and 2 truly-empty branches were deleted during the same wind-down pass.

---

*The successor is [mox-labs/gnx](https://github.com/mox-labs/gnx). See its README for the place in the broader stack ([slick](https://github.com/mox-labs/slick) → gnx → [geist.sh](https://github.com/mox-labs/geist.sh)).*
