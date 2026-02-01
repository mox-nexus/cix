# Memex

Excavating Collaborative Intelligence Artifacts.

## Usage

```bash
# Ingest a Claude.ai export
memex ingest ~/Downloads/claude-export.json

# Search the corpus
memex dig "auth implementation"

# View corpus stats
memex corpus

# Raw SQL (power-user)
memex query "SELECT COUNT(*) FROM fragments"
memex sql  # Interactive shell
```

## Storage

Corpus is stored at `~/.memex/corpus.duckdb`.
