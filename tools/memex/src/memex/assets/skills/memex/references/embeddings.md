# Embeddings Reference

Memex uses embedding models to enable semantic search — finding conceptually related content, not just keyword matches.

## Current Configuration

| Setting | Value |
|---------|-------|
| Model | `all-MiniLM-L6-v2` |
| Dimensions | 384 |
| Backend | sentence-transformers |
| Index | HNSW via DuckDB VSS |

## Model Selection

| Model | Dims | Speed | Quality | Memory | macOS 14 |
|-------|------|-------|---------|--------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | Low | ✅ Stable |
| `nomic-ai/nomic-embed-text-v1.5` | 768 | Medium | Better | Medium | ⚠️ Flaky |
| `BAAI/bge-large-en-v1.5` | 1024 | Slow | Best | High | ⚠️ Flaky |

**Tradeoffs:**
- Higher dimensions = better semantic capture, more storage, slower search
- MiniLM: best for quick local use, 384-dim is ~50% faster to search, **stable on macOS 14**
- Nomic: good balance, open weights, but has MPS issues on macOS 14
- BGE: academic benchmark leader, heavy

## macOS 14 (Sonoma) Compatibility

**Known Issue:** Nomic and larger models fail silently on macOS 14 with Apple Silicon.

**Root cause:** PyTorch MPS backend limitation. Matrix operations exceeding 2³² entries fail with:
```
RuntimeError: Tiling of batch matmul for larger than 2**32 entries
only available from MacOS15 onwards
```

**When it happens:**
- Long text fragments (>10K characters) + high-dim embeddings (768+)
- Batch processing amplifies the issue
- Fails silently with no error message

**Recommendation:**
- **macOS 14:** Use MiniLM (384-dim) — stable
- **macOS 15+:** Nomic (768-dim) should work
- **Workaround:** `PYTORCH_ENABLE_MPS_FALLBACK=1` forces CPU (slow but works)

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

```sql
-- Embeddings stored in separate table
embeddings (
    fragment_id VARCHAR PRIMARY KEY,
    embedding FLOAT[768]  -- or FLOAT[384] for MiniLM
)
```

Storage per fragment:
- 384-dim: ~1.5 KB
- 768-dim: ~3 KB
- 1024-dim: ~4 KB

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

Check `~/.memex/config.toml` or environment:
```bash
export MEMEX_EMBEDDING_MODEL="all-MiniLM-L6-v2"
memex reset --backup
memex ingest <exports>
```
