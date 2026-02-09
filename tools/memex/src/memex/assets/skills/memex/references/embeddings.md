# Embeddings Reference

Memex uses embedding models to enable semantic search — finding conceptually related content, not just keyword matches.

## Current Configuration

Configured per-store in `.memex/config.toml` or `~/.memex/config.toml`:

```toml
[embedding]
model = "nomic"   # "nomic" (768-dim, recommended) or "minilm" (384-dim, legacy)
```

## Model Selection

| Model | Dims | Speed | Quality | Backend |
|-------|------|-------|---------|---------|
| `nomic-embed-text-v1.5` | 768 | ~15 inputs/s | Better | GPT4All (Metal on macOS) |
| `all-MiniLM-L6-v2` | 384 | ~90 inputs/s | Good | sentence-transformers |

**Recommendation: Nomic for new stores.** Higher dimensions = better semantic discrimination. The 768-dim embeddings find conceptually relevant content that 384-dim misses.

Benchmark on 45,674 fragments (same corpus, 10 queries):
- Nomic avg similarity: 0.69, MiniLM avg: 0.54
- Only 17% overlap in top-10 results — models find different documents
- Nomic query latency: 107ms, MiniLM: 113ms (Nomic faster on Metal)

**Tradeoffs:**
- Nomic: better quality, ~2x storage, needs GPT4All backend
- MiniLM: faster embedding generation (6x), lighter, sentence-transformers

## Dimension Mismatch

If you change embedding models, existing embeddings become incompatible.

**Symptoms:**
- Error: `Embedding dimension mismatch`
- Semantic search returns garbage
- Status shows wrong dimensions

**Fix:**

```bash
# Option 1: Reset and re-ingest (clean slate)
memex reset --backup
memex ingest <your-exports>

# Option 2: Delete embeddings only (keep fragments)
memex query "DELETE FROM embeddings"
memex backfill
```

## Backfill Patterns

### Quick import, embed later

```bash
memex ingest export.zip --no-embed  # Fast: keyword search only
# ... later when you have time ...
memex backfill                      # Generate embeddings
```

### Monitor progress

```bash
memex status  # Shows embedding coverage: X/Y (Z%)
```

### Batch size tuning

```bash
memex backfill --batch-size 50   # Lower memory, slower
memex backfill --batch-size 200  # Higher memory, faster
```

Default is 100. Reduce if you see OOM errors.

## Performance

### Embedding generation

| Fragments | MiniLM (384) | Nomic (768) |
|-----------|--------------|-------------|
| 1,000 | ~30s | ~60s |
| 10,000 | ~5min | ~10min |
| 50,000 | ~25min | ~50min |

On CPU. GPU would be 10-50x faster.

### Search latency

| Corpus size | HNSW search |
|-------------|-------------|
| 10K | <10ms |
| 100K | <50ms |
| 1M | <200ms |

HNSW trades some accuracy for speed. Default `ef_search=64` balances well.

## Storage

Embeddings are stored as a column on the fragments table:

```sql
fragments (
    ...
    embedding FLOAT[768]  -- or FLOAT[384] for MiniLM
)
```

Storage per fragment:
- 384-dim: ~1.5 KB
- 768-dim: ~3 KB

50K fragments at 768-dim ≈ 150 MB for embeddings alone.

## Hybrid Search

Memex combines keyword (BM25) and semantic search via RRF fusion:

```
RRF(d) = Σ 1/(k + rank(d))
```

Default `semantic_weight=0.6` means:
- 60% weight to semantic ranking
- 40% weight to BM25 ranking

Tune with:
```bash
memex dig "query" --semantic-weight 0.8  # Favor semantic
memex dig "query" --semantic-weight 0.3  # Favor keyword
```

## No GPU?

Embedding generation is CPU-bound without GPU. Options:

1. **Use smaller model**: MiniLM is 3x faster than Nomic
2. **Pre-embed once**: After backfill, embeddings are stored
3. **Incremental ingest**: Embed as you ingest (`memex ingest` default)
4. **Background task**: Run `memex backfill &` in background

## Troubleshooting

### "No semantic results"

```bash
memex status  # Check: Embeddings: 0/X (0%)
memex backfill
```

### "Backfill stuck"

DuckDB single-writer lock. Only one memex process can write at a time.

```bash
ps aux | grep memex  # Check for existing process
kill <pid>           # If stuck, kill it
memex backfill       # Restart
```

### "Out of memory"

```bash
memex backfill --batch-size 25  # Smaller batches
```

### "Wrong model loaded"

Check active config (`memex status` shows which store) or environment:
```bash
# Check which store is active
memex status

# Override via env var
export MEMEX_EMBEDDING_MODEL="nomic"
memex reset --backup
memex ingest <exports>

# Or edit the config directly
# Local: .memex/config.toml
# Global: ~/.memex/config.toml
```
