# Mem0: Architecture Reference

**Source:** arXiv:2504.19413 (Mem0 paper), docs.mem0.ai
**As of:** April 2026

---

## What It Is

A standalone memory layer for LLM agents. Two variants: **Mem0** (vector-based) and **Mem0g** (graph-based). The core idea: every conversation turn passes through a two-phase pipeline — extract candidate memories, then compare against existing memories and decide what to do.

## The Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                    EXTRACTION PHASE                      │
│                                                         │
│  Input:  (m_{t-1}, m_t)  ← current message pair        │
│          S               ← conversation summary         │
│          {m_{t-m}...}    ← last 10 messages             │
│                                                         │
│  LLM φ(S, recent, m_{t-1}, m_t) → Ω = {ω₁, ω₂, ...} │
│                                                         │
│  Output: candidate memories (natural language facts)    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     UPDATE PHASE                         │
│                                                         │
│  For each ωᵢ:                                           │
│    1. Vector search → top 10 similar existing memories  │
│    2. LLM decides operation via tool call:              │
│       ┌─────────┐                                       │
│       │   ADD   │  new info, no similar memory exists   │
│       │ UPDATE  │  augments existing memory             │
│       │ DELETE  │  contradicts existing memory          │
│       │  NOOP   │  already known, no change needed      │
│       └─────────┘                                       │
│    3. Execute operation on store                        │
│                                                         │
│  Output: updated memory store                           │
└─────────────────────────────────────────────────────────┘
```

## What the LLM Decides vs What Is Algorithmic

| Step | LLM | Algorithmic |
|------|-----|-------------|
| Context assembly (summary + recent window) | | x |
| Memory extraction from messages | x | |
| Embedding computation | | x |
| Top-10 similarity retrieval | | x |
| Operation selection (ADD/UPDATE/DELETE/NOOP) | x | |
| Operation execution (DB write) | | x |
| Retrieval at query time (vector search) | | x |
| Answer generation from retrieved memories | x | |

The LLM makes two decisions per memory candidate: (1) what to extract, (2) what to do with it. Everything else is mechanical.

## Mem0g: The Graph Variant

Directed labeled graph G = (V, E, L):
- **Nodes (V):** entities with type, embedding, timestamp (e.g., Alice:Person, San_Francisco:Location)
- **Edges (E):** relationships as triplets (v_source, relation, v_dest)
- **Labels (L):** semantic types

```
┌─────────────────────────────────────────────────────────┐
│                   MEM0g EXTRACTION                       │
│                                                         │
│  Stage 1: Entity Extractor                              │
│    text → [(entity, type)]                              │
│    e.g., "Alice moved to SF" → [(Alice, Person),        │
│                                  (SF, Location)]        │
│                                                         │
│  Stage 2: Relationship Generator                        │
│    entities + text → [(source, relation, dest)]         │
│    e.g., → (Alice, moved_to, San_Francisco)             │
│                                                         │
│  Stage 3: Node Resolution                               │
│    For each entity:                                     │
│      - compute embedding                                │
│      - search for existing node (similarity > t)        │
│      - reuse existing node OR create new                │
│                                                         │
│  Stage 4: Conflict Detection                            │
│    New edges vs existing edges → mark obsolete invalid  │
└─────────────────────────────────────────────────────────┘
```

**Retrieval (two paths):**
1. **Entity-centric:** identify entities in query → traverse graph relationships
2. **Semantic triplet:** encode query as embedding → match against all relationship triplet encodings

## Storage

| Variant | Store | Token cost per conversation |
|---------|-------|---------------------------|
| Mem0 | Vector DB (Qdrant default) | ~7k tokens |
| Mem0g | Neo4j graph DB | ~14k tokens |

Both also use SQLite for conversation history.

## Performance (LOCOMO benchmark)

- **vs OpenAI Memory:** 26% relative improvement (66.9 vs 52.9 LLM-as-Judge)
- **Search latency p95:** 200ms (lowest of all tested methods)
- **Token savings:** 90%+ vs full-context approach (1,764 vs 26,031 tokens)
- **Mem0g wins on temporal questions** (58.1 vs Mem0's 55.5) — graph structure helps when time matters
- **Zep wins on open-domain** (76.6 vs Mem0g's 75.7) — marginal

## What Mem0 Does NOT Do

- No temporal validity model (no valid_at/invalid_at on memories — memories are current or deleted, no history)
- No concept of solidification or consolidation state
- No trail or associative path through memories
- No context-dependent retrieval (retrieval is pure content similarity)
- No conversation-native storage (conversations are decomposed into extracted facts)
- Graph features gated behind $249/mo Pro tier; free/standard is vector-only

## Sources

- https://arxiv.org/abs/2504.19413
- https://docs.mem0.ai
- https://github.com/mem0ai/mem0
