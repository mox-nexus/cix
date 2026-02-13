# How to Ingest Conversations

Import conversation exports from Claude.ai and ChatGPT into your memex corpus.

---

## Claude.ai Export

1. Go to [claude.ai/settings](https://claude.ai/settings)
2. Request a data export (arrives as a `.zip` or `.json`)
3. Ingest:

```bash
memex ingest ~/Downloads/claude-export.json
```

Memex auto-detects the Claude conversation format and extracts fragments with provenance metadata (timestamps, conversation IDs).

### Large Exports

For large exports (1000+ conversations), ingest without embeddings first, then backfill:

```bash
memex ingest ~/Downloads/claude-export.json --no-embed
memex backfill
```

This separates the I/O-bound ingestion from the CPU-bound embedding generation, and shows progress for each phase independently.

---

## ChatGPT Export

1. Go to ChatGPT Settings > Data Controls > Export Data
2. Download the export (arrives as a `.zip` containing `conversations.json`)
3. Extract and ingest:

```bash
unzip chatgpt-export.zip
memex ingest conversations.json
```

The OpenAI source adapter handles the ChatGPT conversation format.

---

## Verifying Ingestion

After ingesting, check corpus stats:

```bash
memex corpus
```

This shows total fragments, source breakdown, and embedding coverage. If embedding coverage is below 100%, run `memex backfill` to generate missing embeddings.

---

## Multiple Sources

You can ingest from multiple platforms into the same corpus. Memex tracks provenance per fragment, so search results show where each fragment came from:

```bash
memex ingest ~/Downloads/claude-export.json
memex ingest ~/Downloads/chatgpt-conversations.json
memex dig "authentication decisions"   # Searches across both
```

---

## Re-ingestion

Memex deduplicates by source ID. Re-ingesting the same export is safe -- existing fragments are skipped, new ones are added.

```bash
# Safe to run multiple times
memex ingest ~/Downloads/claude-export-v2.json
```
