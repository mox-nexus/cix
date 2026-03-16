# Use Cases Reference

## Agent Memory

Ingest a directory of text files to give agents searchable long-term memory.

### Setup

```bash
memex init --local                    # Project-local corpus at ./.memex/
memex ingest ~/research/              # Recurse, import all matching files
memex status                          # Verify ingest + embedding coverage
```

### Typical sources

| Source | Example | What happens |
|--------|---------|-------------|
| Research notes | `~/research/*.md` | Split by markdown headings |
| Source code | `src/**/*.py` | Single fragment per file (no headings) |
| Log files | `logs/*.log` | Single fragment per file |
| Config files | `*.yaml`, `*.toml` | Single fragment per file |
| PDFs | `papers/*.pdf` | Split by page (requires pymupdf) |
| DOCX | `reports/*.docx` | Split by heading paragraphs (requires python-docx) |
| JSONL | `logs/*.jsonl` | One fragment per JSON line (structured) |

### Querying

```bash
memex dig "authentication patterns"       # Hybrid search (best quality)
memex keyword "OAuth2"                    # Exact term match
memex semantic "how to handle auth"       # Conceptual similarity
memex query "SELECT * FROM fragments WHERE source_kind = 'plaintext' ORDER BY timestamp DESC LIMIT 20"
```

## Conversation History

Import AI conversation exports for cross-session search.

### Claude.ai

```bash
# Export from claude.ai → Settings → Export Data
memex ingest ~/Downloads/claude-conversations.zip
memex dig "what did I decide about the database?"
```

Splits by: messages, artifacts, attachments.

### ChatGPT

```bash
# Export from chatgpt.com → Settings → Data controls → Export data
memex ingest ~/Downloads/conversations.json
memex dig "auth implementation"
```

Splits by: messages.

### Combined corpus

```bash
memex ingest ~/Downloads/claude-export.zip
memex ingest ~/Downloads/chatgpt-export.json
memex ingest ~/research/
memex dig "authentication"              # Searches across ALL sources
```

## Project-Local Knowledge Base

Create a searchable index of a project's docs and source code.

```bash
cd myproject/
memex init --local                      # .memex/ in project root
memex ingest docs/ src/                 # Index documentation and source
memex dig "error handling patterns"
memex build-edges                       # Connect similar fragments
memex similar @3                        # Find related content
```

Add `.memex/` to `.gitignore`. The local store is isolated from the global `~/.memex/` store.

### Multi-store pattern

```bash
cd ~/work/project-a/
memex dig "auth"                        # Searches project-a's .memex/

cd ~/work/project-b/
memex dig "auth"                        # Searches project-b's .memex/

cd ~
memex dig "auth"                        # Searches global ~/.memex/
```

## Research Synthesis

Build a searchable corpus of research papers and notes, then use trails to create reading paths.

```bash
memex init --local
memex ingest papers/ notes/             # PDFs + markdown notes
memex dig "effect of AI on learning"
memex build-edges                       # Connect similar fragments

# Create a trail through related findings
memex trail create "AI learning effects"
memex dig "AI learning"
memex trail add "AI learning effects" @1
memex trail add "AI learning effects" @3
memex trail follow "AI learning effects"
```

## Code Search

Index source code for semantic search across a codebase.

```bash
memex init --local
memex ingest src/                       # .py, .ts, .rs, .go, etc.
memex dig "database connection pooling"
memex semantic "retry with backoff"     # Finds conceptually similar code
```

Source code files without markdown headings become single fragments. For large files, this means one fragment per file — semantic search still finds relevant files by content similarity.

## Supported File Types

### Native (no extra deps)

`.md`, `.txt`, `.rst`, `.csv`, `.log`, `.json`, `.jsonl`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.conf`, `.sh`, `.bash`, `.zsh`, `.py`, `.js`, `.ts`, `.rs`, `.go`, `.html`, `.css`, `.sql`, `.xml`

### With optional deps

| Extension | Dependency | Install |
|-----------|-----------|---------|
| `.pdf` | pymupdf | `uv add pymupdf` |
| `.docx` | python-docx | `uv add python-docx` |

### Structured exports

| Source | Extensions | Adapter |
|--------|-----------|---------|
| Claude.ai | `.json`, `.zip` | ClaudeConversationsAdapter |
| ChatGPT | `.json`, `.zip` | OpenAIConversationsAdapter |

## JSONL Files

JSONL files (`.jsonl`) are ingested structurally — each JSON line becomes one fragment. The adapter uses Pydantic to extract text content from common fields (`content`, `text`, `message`, `body`, `description`) and timestamps (`timestamp`, `created_at`, `date`, `ts`). Remaining JSON fields are preserved in fragment metadata.

```bash
memex ingest logs/*.jsonl                # One fragment per JSON line
memex dig "error handling"               # Searches across JSONL content
```

For raw JSONL exploration without ingestion, DuckDB can read files directly:

```bash
memex query "SELECT * FROM read_json_auto('path/to/file.jsonl') LIMIT 10"
```
