# Ingest Reference

## Supported Sources

| Source | Export Location | Format |
|--------|----------------|--------|
| Claude.ai | Settings > Account > Export Data | JSON in zip |
| ChatGPT | Settings > Data Controls > Export | JSON in zip |

## Ingest Commands

### Default: Ingest with embeddings

```bash
memex ingest ~/Downloads/claude-export.zip
```

This:
1. Parses fragments from export
2. Stores in corpus (deduped by source_id)
3. Generates embeddings for semantic search
4. Rebuilds FTS index

### Fast: Ingest without embeddings

```bash
memex ingest ~/Downloads/claude-export.zip --no-embed
```

Keyword search works immediately. Run `backfill` later for semantic.

### Backfill: Add embeddings to existing fragments

```bash
memex backfill
memex backfill --batch-size 50  # Smaller batches for memory
```

Check coverage with `memex status`.

### Rebuild: Fix broken indexes

```bash
memex rebuild
```

Rebuilds FTS (BM25) index. VSS (embedding) index is auto-managed.

### Reset: Start fresh

```bash
memex reset              # Interactive confirmation
memex reset --yes        # Skip confirmation
memex reset --backup     # Backup to corpus.duckdb.bak first
```

Required when changing embedding models (different dimensions).

## Embedding vs No-Embed Decision

| Scenario | Command |
|----------|---------|
| First import, want full search | `memex ingest <file>` |
| Large corpus, want to test first | `memex ingest <file> --no-embed` |
| Adding more data later | `memex ingest <file>` (will embed new) |
| Changing embedding model | `memex reset --backup` then `ingest` |

## Idempotency

Re-ingesting the same file is safe. Duplicates are ignored via `(source_kind, source_id)` unique constraint.

```bash
# Safe to run multiple times
memex ingest ~/Downloads/claude-export.zip
memex ingest ~/Downloads/claude-export.zip  # No duplicates
```

## Troubleshooting

### "Dimension mismatch" error

Corpus has embeddings from a different model. Options:

```bash
memex reset --backup     # Delete and re-import
memex ingest <file>      # Will use new model
```

### Slow import

Use `--no-embed` for initial import, then `backfill` in background.

### Missing fragments

Check adapter compatibility:
```bash
memex sources            # See available adapters
```
