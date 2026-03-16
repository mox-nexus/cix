# Ingest Reference

## Supported Sources

| Source | Input | Splits By |
|--------|-------|-----------|
| Text files | `.md`, `.txt`, `.rst`, `.csv`, `.log`, `.json`, `.jsonl`, `.yaml`, `.toml`, `.ini`, `.cfg`, `.conf` | Markdown headings (or single fragment) |
| Source code | `.py`, `.js`, `.ts`, `.rs`, `.go`, `.sh`, `.bash`, `.zsh`, `.html`, `.css`, `.sql`, `.xml` | Markdown headings (or single fragment) |
| PDF | `.pdf` | Pages (requires pymupdf) |
| DOCX | `.docx` | Heading paragraphs (requires python-docx) |
| Claude.ai | `.json` or `.zip` export | Messages, artifacts, attachments |
| ChatGPT | `.json` or `.zip` export | Messages |

## Ingest Commands

### Default: One-step ingest

```bash
memex ingest ~/Downloads/claude-export.zip
```

This:
1. Parses fragments from export
2. Stores in corpus (deduped by source_id)
3. Generates embeddings for semantic search
4. Rebuilds FTS index

### Directory ingest

```bash
memex ingest ~/exports/           # Recurse directory, find all matching files
```

Recursively finds files matching any known adapter (Claude exports, OpenAI exports, text, markdown, PDF, DOCX, source code) and ingests them all.

### Recovery: Finish interrupted embedding

```bash
memex backfill
memex backfill --batch-size 50  # Smaller batches for memory
```

If ingest is interrupted mid-embedding (OOM, SIGKILL), fragments are already stored. Run `backfill` to finish. Check coverage with `memex status`.

### Build edges: Connect similar fragments

```bash
memex build-edges                    # Default: threshold=0.8, k=5
memex build-edges -t 0.7 -k 10      # Custom threshold and max edges
```

Builds SIMILAR_TO edges between semantically similar fragments. Requires embeddings — run `memex backfill` first if coverage is below 100%. Then use `memex similar @N` to explore connections.

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

### Missing fragments

Check adapter compatibility:
```bash
memex sources            # See available adapters
```
