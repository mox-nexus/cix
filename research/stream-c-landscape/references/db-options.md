# Memex-Next Database Options: Synthesis

**Sources:** three parallel research agents (vector family, graph family, multi-model + event-log family)
**Date:** 2026-04-14

---

## The three real options

After evaluating 20+ databases across vector, graph, multi-model, and event-log families, the field collapses to three architectures worth considering:

### Option A — Polyglot (Cognee pattern)

```
LanceDB   ← frames, artifacts, embeddings, hybrid search, versioning
  +
Kuzu      ← trails, entity graph, version chains, multi-hop queries
  +
SQLite    ← metadata, provenance, trail event log
```

- Three embedded file-based stores
- Each tool excels at its role
- Proven at scale (Cognee's production deployment)
- LanceDB confirmed pre-disaster pick
- **Cost:** three schemas, three write paths, app-layer coordination
- **Risk:** transaction boundaries span stores (no single ACID)

### Option B — DuckDB single-store

```
DuckDB    ← everything (FTS + VSS + DuckPGQ + JSON + relational)
```

- Single file, single lock, single query language (SQL)
- What current memex v1 already uses
- VSS is experimental; FTS rebuild is manual
- Graph queries via DuckPGQ or SQL self-joins (O(n) not O(degree))
- **Cost:** slower graph traversal, manual index maintenance
- **Risk:** VSS persistence fragility; experimental status

### Option C — SurrealDB unified

```
SurrealDB ← document + graph + vector + temporal in one
```

- SurrealDB 3.0 (Feb 2026) added native vector + hybrid search
- One ACID transaction across document/graph/vector
- SurrealQL (not Cypher, not SQL)
- **Cost:** team retrain on SurrealQL, smaller ecosystem
- **Risk:** vector optimization newer than LanceDB; maturity TBD

---

## How each handles the five gaps

| Requirement | Option A (Polyglot) | Option B (DuckDB) | Option C (SurrealDB) |
|---|---|---|---|
| **Ecphoric retrieval** (hybrid + context signals) | LanceDB hybrid native; context signals = app layer | FTS+VSS manual fusion; context signals = app layer | Native hybrid (RRF); context signals = app layer |
| **Conversation as native unit** (rich records) | LanceDB columnar (nested, Pydantic) | DuckDB columnar (JSON + struct) | SurrealDB document model |
| **Solidification tracking** (counters, version chains) | LanceDB versioning native + Kuzu graph for SUPERSEDES | Manual via tables and indexes | Native links with metadata; record versioning TBD |
| **Trails as first-class** (named, ordered, temporal) | Kuzu graph path + SQLite event log | DuckPGQ or SQL self-join | Record link arrays with metadata (most natural) |
| **Post-hoc annotation** (capture → annotate later) | All three handle cleanly | Native SQL INSERT/UPDATE | SurrealQL INSERT/UPDATE |

**All three options implement bi-temporal at the app layer.** No DB (except XTDB/Datomic, eliminated below) gives it for free. You're modeling `t_created`, `t_expired`, `t_valid`, `t_invalid` as edge properties regardless.

---

## What was eliminated and why

**XTDB / Datomic** — Semantically the right model (append-only, bitemporal native, time-travel queries). Eliminated on Python ergonomics (JVM-required, thin Python drivers) and operational cost. You'd layer vector + FTS on top anyway, returning to polyglot with stronger temporal guarantees at the core but weaker developer experience.

**Neo4j embedded / Memgraph / Apache AGE** — All server-based. Violates local-first embedded preference.

**FalkorDBLite** — In-memory with snapshot persistence. Reconsolidation events are irreversible writes; losing them is catastrophic. Can't accept the volatility.

**TypeDB** — Fascinating logical memory model. No vector support in 3.x. Wrong tool for this job.

**ArangoDB** — Mature document + graph, but no native vector search. Back to polyglot.

**Qdrant Edge / Chroma** — Vector-search-only. No conversation structure, no trails, no hybrid. Would need companion store.

**Turso/libSQL** — No native BM25 for hybrid. No versioning. Needs too much glue.

**TerminusDB** — Git-like versioning semantics are tempting, but WOQL + server-based + no native vectors.

**CR-SQLite / Bedrock** — Too early. Watch for 2027.

---

## The honest tradeoff

**Option A (Polyglot) is the safest choice.** Proven by Cognee, pre-disaster memex-next was heading this way, each store has a clear role. Cost is operational: 3 tools to update, 3 schemas to evolve.

**Option B (DuckDB) is the simplest choice.** One file, one tool, one query language. Current memex v1 works on this. The real question: will graph queries hurt at 1M+ records? For personal scale, probably not. VSS experimental status is the biggest concern — and it's been experimental for a while now.

**Option C (SurrealDB) is the speculative choice.** If vector + graph + document in one ACID transaction is worth betting on, SurrealDB 3.0 is the most serious attempt. But it's the least battle-tested.

---

## What the research actually recommends

Three independent analyses converged on roughly the same shape:

1. **LanceDB for vectors/storage** — no serious competitor at the embedded + hybrid + versioning + columnar intersection. Pre-disaster design was right.
2. **Separate graph DB if trails/bi-temporal need graph primitives** — Kuzu wins among embedded options. Proven by Cognee.
3. **Accept bi-temporal as app-layer work** — no DB gives it for free except XTDB/Datomic, which lose on DX.

The three agents disagreed on Option B vs Option A:
- Vector-family agent recommended A (LanceDB + Kuzu + SQLite)
- Graph-family agent recommended A (Kuzu + LanceDB + SQLite) or C (SurrealDB if unification matters)
- Multi-model-family agent recommended B (DuckDB only) for operational simplicity, with A as fallback

---

## Questions that unblock the decision

Before picking, these need to be answered:

1. **What's the write frequency?** If capture is mostly conversation ingestion (bursty, batched), all three handle it. If reconsolidation events fire every time you `memex dig`, that's heavier write volume — favors DuckDB's simplicity or LanceDB's append-only story.

2. **What's the expected graph query shape?** Trails are mostly linear traversals (follow the path). If that's 95% of graph queries, DuckDB self-joins are fine. If you need "show me all concepts that co-occur in trails crossing X" — that's where Kuzu's O(degree) traversal wins.

3. **Do you want version chains as graph edges or as records?** Squire/Wilson solidification trajectory says SUPERSEDES is a chain: v1 → v2 → v3. Graph DB makes this natural. LanceDB versioning makes the time-travel natural. Either works.

4. **Is multi-writer a concern?** DuckDB's single-writer lock is the issue that drove memexd (the daemon). LanceDB is also single-writer at the table level. If you need concurrent writes from capture + annotation + background reconsolidation, the daemon pattern returns regardless.

5. **How much bi-temporal complexity is real?** Zep's 4-timestamp model is powerful but expensive. Do you need "what did I know at time T AND what was true at time T" as separate axes, or is "when was this recorded + when was it superseded" (2 timestamps) enough?

---

## Recommended path

Given:
- The pre-disaster design chose Lance
- Cognee's pattern is proven
- Current memex v1 is on DuckDB and has hit lock issues that drove memexd
- The five gaps are mostly about retrieval architecture and data model, not storage technology

**Proposed: Option A (Polyglot) for memex-next, anchored on LanceDB.**

- **LanceDB** as primary: frames, artifacts, embeddings, hybrid search, versioning. The Lance format handles append-only well. Time-travel via version restore. Multimodal ready (future conversations may include code/images).
- **Kuzu** for trails and version chains: named trails as Path nodes, SUPERSEDES edges, bi-temporal edge properties (4 timestamps). O(degree) traversal for "show me the trail."
- **SQLite** for the trail event log + config: every reconsolidation event as an append-only row, ACID writes, standard tool.

**Why not Option B (DuckDB only):** Current memex v1 hit the VSS/lock issues. Starting the rebuild on the same stack risks re-hitting them. The graph query shape for trails benefits from Kuzu specifically.

**Why not Option C (SurrealDB):** Worth watching, but betting the rebuild on a 2026 maturity play when Cognee's pattern is already proven seems premature. Revisit if SurrealDB 3.x gets Rust-backed vector parity with LanceDB.

**Fallback:** If polyglot operational overhead becomes real (transaction boundaries leak, sync bugs, schema drift), collapse to Option B (DuckDB only) as explicit migration. The abstractions should keep this as a week's work, not a rewrite.

---

## Open questions for architecture work

- Schema: what lives in LanceDB (Frame, Artifact, Embedding, Blob?) vs Kuzu (Trail, SUPERSEDES, FOLLOWS, SIMILAR_TO, entity relationships?) vs SQLite (TrailEvent log, Settings, @N register)?
- Write coordination: ingestion writes to all three — do we use an event bus (reactor pipeline) or a single transaction coordinator that wraps all three? The former fits better with "append-only, nothing lost" but is harder to reason about.
- Identity: the pre-disaster `archive_id(platform, account, upstream_id) = blake2b(...)` pattern. Which store owns identity resolution?
- Embedding regeneration: when the embedding model changes, all LanceDB vectors become stale. Version the embedding config and support side-by-side old + new until migration completes.
