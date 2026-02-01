# Ingest Reference

## Supported Sources

| Source | Export Location | Format |
|--------|----------------|--------|
| Claude.ai | Settings → Account → Export Data | JSON in zip |
| ChatGPT | Settings → Data Controls → Export | JSON in zip |

## Commands

```bash
# Ingest Claude.ai export
memex ingest ~/Downloads/claude-export.zip

# Ingest ChatGPT export
memex ingest ~/Downloads/chatgpt-export.zip

# Check what's ingested
memex corpus

# See available adapters
memex sources
```

## Idempotent

Re-ingesting the same file is safe - duplicates are ignored via `(source_kind, source_id)` unique constraint.
