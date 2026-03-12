# How to Ingest Content

Import text files, documents, and conversation exports into your memex corpus.

---

## Directory of Text Files

Point memex at a directory — it recursively finds all supported files:

```bash
memex ingest ~/research/
memex ingest ~/notes/
memex ingest ./src/            # Source code too
```

Supported: `.md`, `.txt`, `.rst`, `.pdf`, `.docx`, `.py`, `.js`, `.ts`, `.rs`, `.go`, `.sh`, `.sql`, `.html`, `.css`, `.xml`, `.json`, `.yaml`, `.toml`, `.csv`, `.log`, and more.

Splitting strategy:
- **Markdown**: sections by headings (`##`)
- **PDF**: one fragment per page
- **DOCX**: sections by heading paragraphs
- **Other text**: whole file as one fragment

---

## Claude.ai Export

1. Go to [claude.ai/settings](https://claude.ai/settings)
2. Request a data export (arrives as a `.zip` or `.json`)
3. Ingest:

```bash
memex ingest ~/Downloads/claude-export.zip
```

---

## ChatGPT Export

1. Go to ChatGPT Settings > Data Controls > Export Data
2. Download the export
3. Ingest:

```bash
memex ingest ~/Downloads/chatgpt-export.zip
```

---

## Multiple Sources

Ingest from multiple platforms and file types into the same corpus. Memex tracks provenance per fragment:

```bash
memex ingest ~/research/papers/
memex ingest ~/Downloads/claude-export.zip
memex dig "authentication decisions"     # Searches across everything
```

---

## Recovery

Ingest parses, stores, embeds, and indexes in one step. If interrupted mid-embedding (e.g., OOM or SIGKILL), fragments are already stored — run backfill to finish:

```bash
memex backfill
```

---

## Re-ingestion

Memex deduplicates by source ID. Re-ingesting the same file is safe — existing fragments are skipped, new ones are added.
