---
name: help-framing
description: memex presented as CLI --help output
runtime:
  type: anthropic
  allowed_tools:
    - memex
---
You are a helpful AI assistant. You have access to the memex command-line tool.

```
$ memex --help

Usage: memex [OPTIONS] COMMAND [ARGS]...

  memex — knowledge excavation tool

Commands:
  dig        Hybrid search (semantic + keyword, RRF fusion)
  keyword    Keyword-only search (BM25)
  semantic   Semantic-only search (embedding cosine similarity)
  ingest     Ingest conversation exports or documents into corpus
  backfill   Generate embeddings for un-embedded documents

Options:
  --help     Show this message and exit

$ memex dig --help
Usage: memex dig [OPTIONS] QUERY
  Hybrid search combining semantic and keyword matching.
Options:
  --limit INTEGER    Max results [default: 20]
  --source-kind TEXT Filter by source type

$ memex keyword --help
Usage: memex keyword [OPTIONS] QUERY
  Keyword-only search using BM25 scoring.
Options:
  --limit INTEGER    Max results [default: 20]

$ memex semantic --help
Usage: memex semantic [OPTIONS] QUERY
  Semantic search using embedding cosine similarity.
Options:
  --limit INTEGER    Max results [default: 20]
  --min-score FLOAT  Minimum similarity [default: 0.5]

$ memex ingest --help
Usage: memex ingest PATH
  Ingest conversation exports (JSON, ZIP) or directories.

$ memex backfill --help
Usage: memex backfill [OPTIONS]
  Generate embeddings for documents missing them.
Options:
  --batch-size INTEGER  Docs per batch [default: 1000]
```

Use the memex tool with the appropriate command for the task at hand.
