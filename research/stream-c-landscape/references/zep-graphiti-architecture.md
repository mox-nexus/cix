# Zep / Graphiti: Architecture Reference

**Source:** arXiv:2501.13956 (Zep paper), github.com/getzep/graphiti, docs.getzep.com
**As of:** April 2026

---

## What It Is

A temporal knowledge graph for agent memory. **Graphiti** is the open-source engine (`graphiti-core` on PyPI). **Zep** is the commercial platform wrapping it. The core idea: conversations become a graph of entities and relationships, where every relationship carries four timestamps tracking when it was true and when the system knew it.

## The Graph Model

Three-tier hierarchical subgraph G = (N, E, φ):

```
┌─────────────────────────────────────────────────────────┐
│  TIER 3: Community Subgraph (Gc)                        │
│  Clusters of strongly-connected entities                │
│  Label propagation (incremental, not Leiden)            │
│  LLM-generated summaries per community                  │
│                                                         │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐              │
│  │  Work    │   │  Health │   │  Hobbies│              │
│  │ cluster  │   │ cluster │   │ cluster │              │
│  └────┬────┘   └────┬────┘   └────┬────┘              │
│       │              │              │                    │
├───────┼──────────────┼──────────────┼────────────────────┤
│  TIER 2: Semantic Entity Subgraph (Gs)                  │
│  Entities + relationships with temporal validity         │
│                                                         │
│  (Alice)──works_at──▶(Acme)──located_in──▶(Berlin)     │
│     │                  │                                │
│     │ t_valid: 2024-01 │ t_valid: 2020-06              │
│     │ t_invalid: ∅     │ t_invalid: ∅                  │
│     │                  │                                │
│  (Alice)──works_at──▶(OldCo)                           │
│     │ t_valid: 2020-03                                  │
│     │ t_invalid: 2024-01  ← invalidated by new edge    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  TIER 1: Episodic Subgraph (Ge)                         │
│  Raw episodes (messages, documents, snapshots)           │
│  Ground truth corpus, never modified                     │
│  Bidirectional links: episode ↔ extracted entities       │
│                                                         │
│  [msg_001]──extracted──▶(Alice)                         │
│  [msg_001]──extracted──▶(Acme)                          │
│  [msg_042]──extracted──▶(Alice)                         │
│  [msg_042]──extracted──▶(OldCo)                         │
└─────────────────────────────────────────────────────────┘
```

## The Bi-Temporal Model

Every semantic edge carries **four timestamps**:

| Timestamp | Meaning | Example |
|-----------|---------|---------|
| `t_created` | When the system ingested this fact | 2026-04-13T14:00Z |
| `t_expired` | When the system invalidated this fact | ∅ (still active) |
| `t_valid` | When this fact became true in reality | 2024-01-15 |
| `t_invalid` | When this fact stopped being true | ∅ (still true) |

System time (created/expired) is independent of valid time (valid/invalid). This enables:
- "What did I know at time T?" → filter on `t_created <= T < t_expired`
- "What was true at time T?" → filter on `t_valid <= T < t_invalid`

## The Ingestion Pipeline

```
Episode arrives (message, document, etc.)
        │
        ▼
┌─────────────────────┐
│ 1. Store episode     │  Raw content → Tier 1 node
│    (ground truth)    │  with original timestamp
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 2. Entity extraction │  LLM: text + last n messages
│    (LLM)            │  → candidate entities + types
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. Entity resolution │  Three-tier dedup:
│    (hybrid)          │  a. Exact string match
│                      │  b. Fuzzy similarity (algorithmic)
│                      │  c. LLM reasoning (fallback only)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 4. Edge extraction   │  LLM: entities + text
│    (LLM)            │  → relationship triplets
│                      │  → embeddings per fact
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 5. Temporal          │  LLM: resolve relative timestamps
│    extraction (LLM)  │  "two weeks ago" → absolute date
│                      │  using episode t_ref
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 6. Contradiction     │  New edges vs similar existing edges
│    detection (LLM)   │  → if contradiction with temporal
│                      │    overlap: set old edge t_invalid
│                      │  Old edge NOT deleted — validity
│                      │  window closed, edge preserved
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 7. Community update  │  Label propagation (incremental)
│    (algorithmic)     │  Regenerate summaries as needed
└─────────────────────┘
```

Each step has its own dedicated LLM prompt. Separation enables parallelization and testability.

## What the LLM Decides vs What Is Algorithmic

| Step | LLM | Algorithmic |
|------|-----|-------------|
| Episode storage | | x |
| Entity extraction from text | x | |
| Exact/fuzzy entity matching | | x |
| Entity resolution (ambiguous cases) | x | |
| Relationship extraction | x | |
| Temporal extraction (date parsing) | x | |
| Contradiction detection | x | |
| Edge invalidation mechanics | | x |
| Embedding computation | | x |
| Label propagation (community detection) | | x |
| Community summary generation | x | |
| **All retrieval** | | **x** |

**Key design choice:** Ingestion is LLM-heavy, retrieval is LLM-free. Pay compute at write time to build structure; get fast deterministic reads (~300ms p95).

## Retrieval Pipeline (No LLM)

Three parallel search paths, fused via RRF:

```
Query
  │
  ├──▶ Semantic search (vector similarity on entity/edge embeddings)
  │
  ├──▶ BM25 keyword search (full-text on names and summaries)
  │
  ├──▶ Graph traversal (neighborhood exploration from known entities)
  │
  └──▶ Reciprocal Rank Fusion → ranked results
```

P95 latency: ~300ms. No LLM call at query time.

## Storage

Primary: **Neo4j** (v5.26+). Also supports FalkorDB, Kuzu (embedded), Amazon Neptune. Embeddings stored alongside nodes/edges in the graph database.

## Performance

- DMR benchmark: Zep 94.8% vs MemGPT 93.4%
- LOCOMO open-domain: Zep 76.6 (beats Mem0g's 75.7)
- Retrieval p95: ~300ms (LLM-free)

## What Zep/Graphiti Does NOT Do

- No concept of solidification or consolidation state (tracks temporal validity, not epistemic confidence)
- No trail or associative path (graph traversal is exploratory, not authored sequences)
- No conversation-native storage (episodes are decomposed into entity-relationship triplets)
- No context-dependent retrieval (retrieval is content-based: embedding + keyword + graph traversal)
- Ingestion is LLM-heavy and potentially expensive for high-volume use
- Requires Neo4j (or equivalent) — heavier infrastructure than embedded stores

## What Zep/Graphiti Gets Right

- **Bi-temporal model is genuine.** Four timestamps per edge is the real thing, not a simplified "last updated."
- **Non-lossy.** Episodes preserved as ground truth. Facts invalidated, never deleted.
- **Entity resolution is tiered** — deterministic first, LLM only as fallback. Minimizes LLM cost.
- **Retrieval is LLM-free.** Read-heavy workloads are fast and predictable.

## Sources

- https://arxiv.org/abs/2501.13956
- https://github.com/getzep/graphiti
- https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/
- https://help.getzep.com/graphiti/getting-started/overview
