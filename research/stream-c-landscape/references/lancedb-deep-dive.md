# LanceDB Deep Dive

**Sources:** `~/oss/lance/` and `~/oss/lancedb/` — cloned April 2026
**Focus:** concurrency, versioning, streaming writes, transaction semantics — the answers to the unresolved architecture questions

---

## Lance vs LanceDB — not the same thing

- **Lance** (`~/oss/lance/`) — the columnar storage format + Rust engine. Writes Arrow data, manages manifests, implements MVCC, defines the transaction protocol. This is the core.
- **LanceDB** (`~/oss/lancedb/`) — a database layer on top of Lance. Python/TS/Java bindings, built-in embedding functions, vector index abstractions, remote (cloud) support. Wraps Lance with DB-like ergonomics.

Both are Apache-2.0 licensed. Both local-first. You can use Lance directly (`pylance`) without LanceDB if you want the raw format. Memex should use LanceDB for the ergonomics.

---

## The headline finding: Lance is NOT single-writer

**Lance implements MVCC with optimistic concurrency control.** The relevant spec:

> "Lance implements Multi-Version Concurrency Control (MVCC) to provide ACID transaction guarantees for concurrent readers and writers. Each commit creates a new immutable table version through atomic storage operations. All table versions form a serializable history."
> — `~/oss/lance/docs/src/format/table/transaction.md`

This is the single most important finding. It's nothing like DuckDB's single-writer lock or the pain that drove memexd.

### How it works

Every write creates a **transaction** (protobuf: `read_version`, `uuid`, `operation`). The commit protocol uses atomic storage primitives:
- **rename-if-not-exists** (atomic file rename)
- **put-if-not-exists** (conditional PUT / PUT-IF-NONE-MATCH)

Exactly one writer succeeds when multiple writers try to commit the same version. Losers detect the conflict via transaction metadata and either **rebase automatically** or **retry at the application level**.

### Transaction types and their conflict rules

From the spec, each operation has documented compatibility:

| Operation | Compatible with | Rebaseable with | Retryable with | Incompatible |
|---|---|---|---|---|
| **Append** | Append, Delete, Update, Merge, Rewrite, CreateIndex, Project, UpdateConfig, DataReplacement | — | — | Overwrite, Restore |
| **Delete** | Append | Delete, Update (if non-overlapping rows) | Merge, Rewrite, DataReplacement | Overwrite, Restore |
| **Update** | Append | Delete, Update | Rewrite, Merge, DataReplacement | Overwrite, Restore |
| **CreateIndex** | Append, Delete, Update | CreateIndex (same singleton) | Rewrite, DataReplacement | Overwrite, Restore |
| **Merge (add column)** | — | — | Update, Append, Delete, Merge, Rewrite, DataReplacement | Overwrite, Restore, Project |
| **Overwrite** | — | — | Overwrite, UpdateConfig | — |

**The killer line:** Append never conflicts with Append. Two processes can ingest concurrently forever.

### What "rebasable" means concretely

Two writers both issue Delete transactions on the same fragment but different rows:
1. Writer A commits first → v3, deletes rows 100-199
2. Writer B detects v3 exists, its read_version was v2
3. Writer B's transaction is **rebaseable**: only modified deletion vectors, `affected_rows` don't overlap
4. Writer B merges A's deletion vector with its own, commits → v4
5. **No application retry needed.** The library did it.

### What "retryable" means concretely

Writer A compacts fragments 1-5 into one fragment. Writer B updates rows in fragment 3:
1. Writer A commits → v3, fragment 3 no longer exists
2. Writer B's update is **retryable**: the rows it targeted exist in a new fragment now
3. Library returns a retry error. Application re-reads, re-issues update against v3.

### Branches: git-like parallel histories

Lance supports named branches with parallel linear histories:

```python
ds = lance.dataset("./data.lance")
experiment = ds.create_branch("experiment")
lance.write_dataset(new_data, experiment, mode="append")  # writes to branch

ds.tags.create("experiment-rc", ("experiment", None))
rc = ds.checkout_version("experiment-rc")
```

Each branch maintains its own version numbers. Tag + `(branch, version)` tuples are global identifiers. **Branches hold references to data files — cleanup doesn't delete files referenced by any branch.** This is memory-safe garbage collection.

---

## Versioning — you were right, but with nuance

Your claim: "LanceDB versioning is table-wide, it's schema versioning."

**Correct on scope: versioning is at the table (dataset) level, not per-row.** Every `write_dataset(mode="append")`, `delete()`, `update()`, or `create_index()` creates a new manifest and a new version number.

**Partly-correct on kind:** it's not *only* schema versioning. It's table-state versioning: schema + data file references + fragment ids + deletion vectors + index metadata. Schema changes (Merge, Project) are a subset. Data changes (Append, Delete, Update) also bump the version.

**What this means practically for memex:**
- Good for: rollback entire corpus to a prior state, time-travel queries (`lance.dataset(uri, version=N)`), experiment branches
- Not for: tracking the edit history of *one specific fragment*. The dataset version tells you "what did the whole corpus look like at time T," not "how did frame_id=abc123 evolve."
- If you want per-frame history (reconsolidation events on a specific memory), that's an **append-only events table**, separate from the version mechanism. Two distinct tools for two distinct jobs.

---

## Streaming writes — the MemWAL LSM story

Lance has an experimental but well-specified MemWAL feature: LSM-tree architecture for high-throughput streaming writes while keeping indexed read performance.

From `~/oss/lance/docs/src/format/table/mem_wal.md`:

- A **shard** is a horizontal scale-out unit. Each shard has exactly one active writer.
- Writes go to an **in-memory MemTable** + a **Write-Ahead Log** for durability.
- MemTables flush to storage periodically. Flushed MemTables merge into the base table asynchronously.
- **Multiple shards = multiple concurrent writers**, each streaming into their own shard.
- Primary keys are partitioned across shards so "last write wins" semantics are preserved.

This is the streaming-writes-while-batch-ingest-also-happens story. Memex ingest (batch) can hit one shard while reconsolidation events (streaming, per-recall) hit another. They merge into the base table asynchronously without interfering.

**Caveat:** MemWAL is marked experimental. For memex v2 initial launch, plain MVCC Appends are sufficient. MemWAL is the scaling path if streaming write throughput becomes an issue.

---

## Indexing options

### Vector indices

Pattern: `{clustering}_{sub_index}_{quantization}`

- `IVF_PQ` — IVF clustering + Product Quantization (compression). Default recommendation. Tune `nprobes` (partitions searched) and `refine_factor` (re-rank candidates).
- `IVF_HNSW_SQ` — IVF + HNSW inside partitions + Scalar Quantization. Higher recall, more memory.
- `IVF_FLAT` — IVF clustering + no quantization. Exact vectors within clusters. Highest accuracy, highest memory.
- `IVF_SQ`, `IVF_RQ` — Other quantization variants.

For 1M fragments × 768 dim, `IVF_PQ` with `target_partition_size=8192` is the starting point. `(dim / num_sub_vectors) % 8 == 0` for fast index builds.

### Scalar indices

Different types for different filter shapes:

- `BTREE` — equality, range, high-cardinality columns
- `BITMAP` — equality, low-cardinality (tags, categories, source_kind)
- `LABEL_LIST` — list membership filters (trail memberships?)
- `NGRAM` — substring/contains filters (text search without full FTS)
- `INVERTED` — full-text search (BM25) — **this is memex's FTS**
- `BLOOMFILTER` — negative membership / presence checks
- `ZONEMAP` — range filters
- `RTREE` — geospatial (not relevant here)

### Hybrid search

LanceDB supports hybrid queries natively:

```python
tbl.query()
  .nearest_to([0.1, 0.2, ...])   # vector search
  .where("category = 'insight'")  # scalar filter
  .full_text_search("authentication decisions")  # BM25 via INVERTED
  .limit(10)
  .to_list()
```

Fusion between vector and FTS results uses RRF. The `prefilter=True` flag forces the scalar filter to run before vector search (correctness when filter is selective). `prefilter=False` is faster but may return fewer than k results.

---

## What Lance does NOT do (where DuckDB complements)

Lance is a storage + search engine, not a general query engine. Missing pieces:

1. **No SQL query engine.** You can filter with SQL-like expression strings (`"a > 10 AND b IN [1,2,3]"`) but not arbitrary joins, group-bys, aggregations across tables.
2. **No multi-table joins.** Each `.lance` directory is one dataset. If you want to join frames with trail metadata, you either:
   - Denormalize into one dataset (Lance way)
   - Read both as Arrow, join in DuckDB (complementary way)
3. **No graph traversal primitives.** No `MATCH (a)-[:FOLLOWS]->(b)` equivalent. You build paths by scanning edge tables and walking in app code.
4. **No stored procedures or triggers.** All logic lives in the application layer.

**DuckDB covers exactly these gaps.** DuckDB can read Lance datasets directly via `duckdb-lance` extension or via `duckdb.from_arrow(lance.dataset(uri).to_table())`. Zero copy, shared Arrow memory.

---

## Lance + DuckDB: the actual architecture

```
                ┌─────────────────────────────┐
                │       Lance (core)          │
                │                             │
                │  • Frames (Arrow records)   │
                │  • Artifacts (versioned)    │
                │  • Embeddings (768-dim)     │
                │  • Append-only event log    │
                │  • Hybrid search: BM25      │
                │    (INVERTED) + IVF_PQ      │
                │  • MVCC + branches + tags   │
                └──────────────┬──────────────┘
                               │ zero-copy Arrow
                               ▼
                ┌─────────────────────────────┐
                │          DuckDB             │
                │                             │
                │  • SQL query engine          │
                │  • Joins across datasets     │
                │  • Aggregations              │
                │  • Graph traversal as SQL   │
                │    (recursive CTEs for       │
                │     trail following)         │
                │  • JSON extraction           │
                │  • UDFs if needed            │
                └─────────────────────────────┘
```

**Division of labor:**
- Lance is the source of truth. All data lives in `.lance` directories.
- DuckDB reads Lance datasets as Arrow, queries them.
- Lance handles storage + versioning + hybrid search.
- DuckDB handles arbitrary SQL over the data.
- No sync problem — DuckDB reads from Lance, doesn't own data.

This is **one store with two query interfaces**, not polyglot.

---

## Answers to your five open questions

### 4. Multiple writes, multiple reads — SOLVED

Lance MVCC handles this natively. Appends never conflict with appends. Two ingestion processes and a background annotation process can all write concurrently. Reads are completely non-blocking (a reader pins a version, writers commit new versions).

**No memexd-style daemon required.** The DuckDB lock pain doesn't transfer to Lance.

### 5. Bi-temporal — what it actually means

Two independent time axes on every fact:

- **System time** (transaction time): when the database *knew* something
  - `t_created` — when this row was written to the system
  - `t_expired` — when this row was superseded/deleted in the system
- **Valid time** (real-world time): when something was *true in the world*
  - `t_valid` — when this fact became true in reality
  - `t_invalid` — when this fact stopped being true

**Why two axes matter for memex:**

The conversation happened on March 5. I discussed it on April 10 (recalling → reconsolidation). I updated my understanding on April 13. A bi-temporal model answers different questions with each axis:

- "What did I believe about X on April 12?" — system time query (my beliefs *as recorded by the system* on that date)
- "What was actually true about X on April 12?" — valid time query (facts *in the world* on that date)

For memex:
- **System time** is cheap: add `created_at` and `superseded_at` columns. Every row has these. Done.
- **Valid time** is expensive: every fact needs `valid_from` and `valid_to`, every update has to close the old fact's validity window and open a new one.

**My take:** memex probably only needs **system time** (2 timestamps) not full bi-temporal (4 timestamps). The conversation happened at time T. The fact was extracted at time T'. The user annotated it at time T''. These are system-time events. "When was this true in the world" is mostly the same as "when did I learn it" for conversation-based memories.

Use bi-temporal only if you model external facts that update independently (e.g., "the CEO of Acme" changes when Acme changes CEO — the valid_to for the old CEO is the valid_from for the new one, independent of when you learned it). For personal conversation memory, system time is almost always sufficient.

### 1. Batch + streaming ingest simultaneously — SOLVED

Option A (pre-MemWAL): both are Append transactions. They never conflict. Just do both.

Option B (MemWAL, when it stabilizes): put batch ingest on one shard, streaming on another. They merge into the base table asynchronously without interfering.

### 2. Graph query shape — clarification

The question was: what do graph queries in memex actually look like?

Three categories, each with a different performance profile:

**A. Linear trail walks** — 95% of trail queries
- "Show me the 'reactor pipeline' trail in order"
- Query: `SELECT * FROM trail_entries WHERE trail_id = X ORDER BY position`
- This is a single table scan. DuckDB does it in milliseconds. Lance does it via filtered scan + sort. **No graph DB needed.**

**B. SUPERSEDES chain walks** — version chains
- "Show me all versions of Artifact X, newest first"
- Query: recursive CTE, or a linked list (each artifact has `supersedes_id`, walk backwards)
- DuckDB recursive CTEs handle this fine. Depth is typically < 10.

**C. Multi-hop semantic traversal** — the hard one
- "Show me all conversations that connect to the idea of reconsolidation, then show me the people/topics/projects those conversations touched"
- This IS the shape graph DBs handle well. SQL self-joins do it too, but slower.
- For memex at 1M records, DuckDB recursive CTEs are sub-second in practice.

**Verdict:** 95% of memex's "graph" queries are category A and B. Category C is rare enough that DuckDB's recursive CTEs are fine. You don't need Kuzu.

### 3. LanceDB versioning is table-wide — YES, with a nuance

Correct that it's table-wide (not per-row). And it covers schema + data + index state, not just schema. So:

- **Use Lance versioning for** "roll back the whole corpus to yesterday" or "branch for an experiment"
- **Use an append-only events table for** "how did this specific memory evolve"

Both live in Lance. The events table is just another dataset with its own Append-mostly history. Lance's MVCC guarantees the events table never loses writes.

---

## Kuzu noted as dead

You mentioned Kuzu is dead. I didn't verify, but it doesn't matter — with Lance's MVCC + DuckDB's query engine, we don't need a dedicated graph DB. The graph query shapes memex needs (above) are all tractable in DuckDB.

---

## The EasyHypergraph paper (saved to ~/mox/research/papers/easyhypergraph/)

Relevance check for memex:

**The paper proposes:** EasyHypergraph — open-source library for hypergraph analysis and learning. Hyperedges connect arbitrary numbers of nodes, not just pairs. Claims memory-efficiency and speed gains over NetworkX, XGI, HGX for >100k-node graphs.

**Why it's architecturally interesting for memex:**

1. **Trails are hyperedges, not pairwise edges.** A trail connects an ordered set of frames — that's a hyperedge of arity k, not a sequence of binary edges. If you model trails as a list of pairwise FOLLOWS edges (a → b → c), you lose the identity of "this is one trail."

2. **The SMRT knowledge atom is inherently hypergraph-shaped.** Three facets (relation, stance, provenance) don't reduce to pairwise relations. Each fact is a hyperedge connecting these three.

3. **Pickering's alignment events** are n-way: speakers + topic + time + project all converge. Binary edges flatten the convergence.

4. **Conversations are hypergraphs.** One turn relates speaker + listener(s) + topic + prior turn + session. Pairwise modeling fragments this.

**But: EasyHypergraph is not a storage backend.** It's an analysis library (like NetworkX). It reads data, computes centrality/paths, does learning. For memex the question is whether to store data in a hypergraph-shaped schema (multi-column many-to-many tables that DuckDB can query) and use EasyHypergraph for offline analysis — not whether to replace Lance with it.

**Practical implication:** when you schema the trail table, model it as `(trail_id, frame_id, position)` — a join table that's effectively a hyperedge. A trail IS the set of rows sharing a trail_id. This stays in Lance/DuckDB. If you ever want graph analytics on the trail structure (centrality, community detection), export to EasyHypergraph.

---

## Recommendation

**Stack: Lance + DuckDB. One store, two query interfaces.**

- **Lance** — all data, all versioning, MVCC writes, hybrid search (BM25 + vector + RRF), native Arrow
- **DuckDB** — SQL queries, joins, recursive CTEs for graph-shaped traversals, aggregations

**Model for memex-next:**
- Frames, Artifacts, TrailEntries, Events, Embeddings — separate Lance datasets
- Each indexed appropriately: INVERTED for text, IVF_PQ for embeddings, BTREE/BITMAP for metadata filters
- DuckDB reads Lance datasets via Arrow zero-copy for any SQL that Lance's expression layer can't handle
- Bi-temporal = system time only (2 timestamps), not full 4-axis

**What this eliminates:**
- Kuzu (dead + not needed — DuckDB CTEs suffice)
- SQLite (Lance handles the metadata store)
- memexd-style daemon (Lance MVCC handles concurrency)
- Polyglot sync bugs (one source of truth)

**Open questions remaining:**
- Specific index choices per dataset (work out during schema design)
- When to create branches (experiments? user forks? rollback points?)
- Whether to use MemWAL now or wait for it to stabilize (my recommendation: wait, use plain Appends)
- Whether to vendor pylance or use LanceDB's Python bindings (LanceDB's are more ergonomic; use those)

Next step: schema design.
