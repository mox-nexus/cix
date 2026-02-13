# Memex: Methodology

Why memex exists and how it's designed.

---

## Contents

- [The Problem](#the-problem)
- [Bush's Vision](#bushs-vision)
- [Design Decisions](#design-decisions)
- [Hybrid Search Architecture](#hybrid-search-architecture)
- [The Fragment as Unit of Recovery](#the-fragment-as-unit-of-recovery)
- [Convention Over Configuration](#convention-over-configuration)
- [Hexagonal Architecture](#hexagonal-architecture)
- [What Memex Is Not](#what-memex-is-not)

---

## The Problem

Human-AI collaboration generates artifacts: conversations, decisions, reasoning traces, design explorations. These accumulate across platforms (Claude, ChatGPT, Gemini) and sessions. Within weeks, the volume makes retrieval difficult. Within months, critical context is effectively lost.

The cost is real. Teams re-derive decisions that were already made. Reasoning that led to architectural choices evaporates. The same questions get asked and re-answered because the original exchange is buried in an export file no one can search.

**This is the excavation problem.** The artifacts exist. Finding them is the bottleneck.

---

## Bush's Vision

Vannevar Bush described the memex in "As We May Think" (The Atlantic, 1945) as "an enlarged intimate supplement to memory." His insight wasn't about storage -- it was about **associative trails**: the ability to link related ideas across a personal knowledge corpus and follow those connections later.

Bush was writing about physical media (microfilm, mechanical selectors), but the core problem he identified persists: human memory is associative, not indexed. We remember that we discussed authentication *somewhere*, not the date, platform, or conversation ID. A useful retrieval system must bridge this gap.

Memex implements Bush's vision with modern tools:

| Bush's Concept | Memex Implementation |
|----------------|---------------------|
| Personal knowledge corpus | DuckDB-backed fragment store |
| Associative trails | FOLLOWS edges between fragments |
| Selection by content | Hybrid search (BM25 + semantic + reranking) |
| Intimate supplement | Local-first, convention-over-config |

---

## Design Decisions

### Excavation, Not Observation

Memex operates on **historical artifacts** -- conversations and reasoning traces that already happened. It does not stream, watch, or observe live interactions. This is a deliberate scope constraint:

- Live observation requires persistent processes, event streams, and real-time indexing
- Historical excavation requires only ingestion and search
- The two are architecturally different problems

Conflating them produces a tool that does both poorly. Memex does excavation well.

### Local-First

All data stays on the user's machine. No cloud sync, no remote API calls for search. The embedding model (nomic-embed-text-v1.5) and cross-encoder reranker (MS MARCO MiniLM) run locally via ONNX.

**Why:** Collaboration artifacts contain sensitive context -- strategic decisions, security discussions, personnel conversations. Sending these to external services for search indexing is a non-starter for many users.

### Defaults for Most, Complexity for Few

```
memex dig "where did I decide on auth?"     # 80% case: hybrid search
memex query "SELECT * FROM fragments ..."    # 20% case: SQL escape hatch
```

The `dig` command is the primary interface. It combines BM25 keyword search, semantic embedding search, and cross-encoder reranking. Users don't need to understand any of that -- they type a query, get results.

The SQL escape hatch exists for power users who need complex filtering, aggregation, or ad hoc analysis. DuckDB's analytical SQL is available directly.

---

## Hybrid Search Architecture

Single search modalities have known limitations:

| Modality | Strength | Weakness |
|----------|----------|----------|
| **Keyword (BM25)** | Exact term matching, fast | Misses synonyms, paraphrases |
| **Semantic (embeddings)** | Conceptual similarity | Misses exact terms, "dilutes" precision |
| **Cross-encoder reranking** | Pair-level relevance scoring | Too slow for full-corpus search |

Memex combines all three via Reciprocal Rank Fusion (RRF):

1. **BM25** retrieves keyword-matching fragments from DuckDB's full-text search index
2. **Semantic search** retrieves conceptually similar fragments via HNSW vector index
3. **RRF** (k=60) fuses the two ranked lists into a single ordering
4. **Cross-encoder** reranks the fused top-N for final relevance scoring

This pipeline means `memex dig "OAuth2 implementation"` finds fragments that:
- Contain the exact term "OAuth2" (BM25)
- Discuss authentication concepts without using that term (semantic)
- Are ranked by actual query-fragment relevance (cross-encoder)

### Why RRF Over Learned Fusion

Reciprocal Rank Fusion (Cormack et al., 2009) is a parameter-free fusion method. It doesn't require training data or tuning -- it works by reciprocal rank combination.

For a personal knowledge tool where the corpus varies dramatically per user, a training-free fusion method is the right choice. There's no representative training set for "all possible personal knowledge corpora."

---

## The Fragment as Unit of Recovery

The atomic entity in memex is the **Fragment** -- a self-contained unit of collaborative intelligence. Not a message (too small, lacks context), not a full conversation (too large, buries signal).

Fragments are extracted during ingestion. Each carries:
- **Content**: The actual text
- **Provenance**: Where it came from (source_kind, source_id, timestamp)
- **Embedding**: Vector representation for semantic search
- **FOLLOWS edges**: Links to chronologically adjacent fragments

The fragment granularity is a design decision with consequences:

| Granularity | Search Quality | Storage Cost | Context |
|-------------|---------------|-------------|---------|
| Message-level | Noisy (too many tiny hits) | Low | Lost (single turn) |
| Fragment-level | Balanced | Moderate | Preserved (coherent unit) |
| Conversation-level | Few results, hard to scan | High | Complete but overwhelming |

---

## Convention Over Configuration

Memex uses `.memex/` directories like `.git/` -- walk up from CWD to find the active workspace.

```
~/.memex/           # Global workspace (default)
project/.memex/     # Project-local workspace (overrides global)
```

**No flags needed.** If you're in a project with `.memex/`, memex uses that store. If not, it falls back to global. This is the same mental model as git: you don't pass `--repo` flags, you work in a directory and git finds the repo.

The precedence order:
1. `MEMEX_*` environment variables (explicit override)
2. Local `.memex/` (walk up from CWD)
3. Global `~/.memex/config.toml`
4. Defaults

---

## Hexagonal Architecture

Memex follows hexagonal architecture (ports and adapters) to separate concerns:

**Domain**: Pure business logic with no external dependencies. Fragment, Provenance, EmbeddingConfig are plain models. ExcavationService orchestrates use cases through port interfaces.

**Ports**: Protocol-based interfaces (`typing.Protocol` with `@runtime_checkable`). Four driven ports:
- `CorpusPort` -- persistence and search
- `EmbeddingPort` -- vector generation
- `RerankerPort` -- cross-encoder reranking
- `SourceAdapterPort` -- format-specific ingestion

**Adapters**: Concrete implementations. DuckDB for corpus, fastembed for embeddings, Rich+Click for CLI.

**Why this matters for users:** The architecture means memex can swap components without changing behavior. A new embedding model, a different storage engine, or an additional source format (Gemini, custom) requires one new adapter -- zero domain changes.

---

## What Memex Is Not

Precision in scope prevents scope creep:

| Memex Is | Memex Is Not |
|----------|-------------|
| Historical artifact excavation | Live session observation |
| Personal knowledge retrieval | Team knowledge management |
| Source-agnostic search | Claude-specific tooling |
| Local-first | Cloud-synced |
| CLI-first | GUI application |

The boundaries are deliberate. Each "is not" represents a different tool with different architecture. Trying to be all of them produces none of them well.
