# Memex

> Excavating Collaborative Intelligence Artifacts

Memex retrieves and connects historical human-AI collaboration artifacts across heterogeneous sources. Named for Vannevar Bush's 1945 vision of an "enlarged intimate supplement to memory."

---

## Architecture Overview

### Hexagonal Structure

```
┌─────────────────────────────────────────────────────┐
│ DRIVING (User-Facing)                               │
│ └── CLI: dig, query, ingest, corpus, sql           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DOMAIN (Pure, No Dependencies)                      │
│ ├── Fragment, Provenance                           │
│ └── ExcavationService                              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DRIVEN (Infrastructure)                             │
│ ├── CorpusPort → DuckDB adapter                    │
│ └── SourceAdapterPort → Claude, OpenAI adapters    │
└─────────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `tools/memex/src/memex/domain/models.py` | Fragment, Provenance domain entities |
| `tools/memex/src/memex/domain/ports/_out/corpus.py` | CorpusPort interface |
| `tools/memex/src/memex/domain/ports/_out/source.py` | SourceAdapterPort interface |
| `tools/memex/src/memex/domain/services/excavate.py` | ExcavationService orchestration |
| `tools/memex/src/memex/adapters/_out/corpus/duckdb/adapter.py` | DuckDB implementation |
| `tools/memex/src/memex/adapters/_in/cli/main.py` | CLI commands |

### Domain Entities

**Fragment** — The atomic unit of excavation (not too small like a message, not too large like a conversation):
```python
@dataclass
class Fragment:
    id: str
    conversation_id: str | None
    role: str
    content: str
    provenance: Provenance
    timestamp: datetime | None
```

**Provenance** — Source-agnostic origin tracking:
```python
@dataclass
class Provenance:
    source_kind: str  # "claude_conversations", "openai", etc.
    source_id: str
    timestamp: datetime | None
```

### Port Contracts

**CorpusPort** (what the domain needs for persistence):
```python
class CorpusPort(Protocol):
    def store(self, fragments: Iterable[Fragment]) -> int: ...
    def search(self, query: str, limit: int = 20) -> list[Fragment]: ...
    def find_by_conversation(self, conversation_id: str) -> list[Fragment]: ...
    def stats(self) -> dict: ...
```

**SourceAdapterPort** (what the domain needs for ingestion):
```python
class SourceAdapterPort(Protocol):
    def can_handle(self, path: Path) -> bool: ...
    def ingest(self, path: Path) -> Iterator[Fragment]: ...
    def source_kind(self) -> str: ...
```

---

## Search Architecture

### Hybrid Search (Default)

`memex dig` now uses **hybrid search** combining:
1. **BM25 keyword search** via DuckDB FTS extension
2. **Semantic search** via embeddings (cosine similarity)
3. **Reciprocal Rank Fusion (RRF)** to combine results

```python
# RRF formula (k=60, production standard)
score = 1/(bm25_rank + 60) + 1/(semantic_rank + 60)
```

### Search Modes

| Command | Method | Best For |
|---------|--------|----------|
| `memex dig` | Hybrid (BM25 + semantic + RRF) | General use (recommended) |
| `memex keyword` | BM25 only | Exact terms, code |
| `memex semantic` | Embeddings only | Conceptual queries |

### BM25 vs ILIKE

Previous implementation used naive `ILIKE '%word%'` matching. Now uses **BM25** which accounts for:
- Term frequency (how often word appears)
- Inverse document frequency (rare words matter more)
- Document length normalization

### Intent Interpretation

**Claude is the intent interpreter** when memex is used as a skill:

```
User: "where did I decide on auth?"
     ↓
Claude interprets intent, uses hybrid search
     ↓
memex dig "authentication decisions"
     ↓
Claude synthesizes fragments into answer
```

The CLI provides search primitives. Claude provides semantic understanding.

---

## DX Review (Updated)

**Verdict: RESOLVED** — All critical issues addressed.

### Implemented

| Issue | Status |
|-------|--------|
| Search semantics mismatch | ✅ Hybrid search with BM25 + semantic |
| No-results guidance | ✅ Shows corpus stats, embedding coverage |
| Post-fetch source filtering | ✅ Fixed in query-time WHERE clause |
| Missing output formats | ✅ `--format panel|json|ids` on all search commands |
| Command naming confusion | ✅ `dig` = hybrid (default), `keyword` = BM25, `semantic` = embeddings |

### Current Architecture

- **Hybrid by default**: `dig` uses RRF (keyword + semantic)
- **Explicit modes**: `keyword` and `semantic` for specific needs
- **BM25 via FTS**: Proper text search, not naive ILIKE
- **Embeddings**: Via sentence-transformers (local, free)
- **Index management**: `rebuild` and auto-rebuild on ingest

---

## CLI Reference

```bash
# Primary Search (Hybrid: BM25 + Semantic with RRF)
memex dig "query"                        # Recommended default
memex dig "query" --semantic-weight 0.8  # More semantic matching
memex dig "query" --limit 50             # More results

# Alternative Search Modes
memex keyword "query"                    # BM25 only (faster, no embeddings)
memex semantic "query"                   # Embeddings only (conceptual)
memex semantic "query" --min-score 0.5   # Higher threshold

# Embedding Management
memex backfill                           # Generate embeddings for corpus
memex rebuild                            # Rebuild FTS index

# Discovery
memex corpus                             # Show stats
memex sources                            # List adapters
memex schema                             # Show DB schema

# Ingestion
memex ingest <file>                      # Ingest conversation export

# 20% Power-User (SQL escape hatch)
memex query "SELECT ..."                 # Raw SQL
memex query "..." --format json          # Output formats
memex sql                                # Interactive shell
```

---

## Storage

- **Corpus**: `~/.memex/corpus.duckdb`
- **Schema**: Single `fragments` table with indexes on timestamp, conversation_id, source_kind

---

*Analysis by Wolf (architecture) and Ace (DX review), 2026-02-02*
