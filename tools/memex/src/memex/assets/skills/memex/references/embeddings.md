# Embeddings Reference

Memex uses embedding models to enable semantic search — finding conceptually related content, not just keyword matches.

## Current Model

| Property | Value |
|----------|-------|
| Model | `nomic-ai/nomic-embed-text-v1.5` |
| Dimensions | 768 |
| Backend | fastembed (ONNX runtime, no torch) |
| Download size | ~285 MB (cached after first use) |

The model is fixed in the composition root. No config-driven model selection exists.

## Dimension Mismatch

If the embedding model changes in a future version, existing embeddings become incompatible.

**Symptoms:**
- Error: `Embedding dimension mismatch`
- Semantic search returns garbage
- Status shows wrong dimensions

**Fix:**

```bash
# Option 1: Reset and re-ingest (clean slate)
memex reset --backup
memex ingest <your-exports>

# Option 2: Clear embeddings only (keep fragments)
memex query "UPDATE fragments SET embedding = NULL"
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

Default is 100. Reduce if OOM errors occur.

## Performance

### Embedding generation (nomic-embed-text-v1.5, CPU)

| Fragments | Approximate Time |
|-----------|-----------------|
| 1,000 | ~60s |
| 10,000 | ~10min |
| 50,000 | ~50min |

### Search latency (HNSW)

| Corpus size | Latency |
|-------------|---------|
| 10K | <10ms |
| 100K | <50ms |
| 1M | <200ms |

HNSW trades some accuracy for speed. Default `ef_search=64` balances well.

## Storage

Embeddings are stored as a column on the fragments table:

```sql
fragments (
    ...
    embedding FLOAT[768]
)
```

Storage per fragment at 768-dim: ~3 KB.
50K fragments ≈ 150 MB for embeddings alone.

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
