# How to Configure a Local Store

Set up a project-specific memex corpus separate from your global store.

---

## Setup

From your project root:

```bash
cd ~/myproject
memex init --local
```

This creates a `.memex/` directory:

```
myproject/
├── .memex/
│   ├── config.toml       # Optional local config overrides
│   └── corpus.duckdb     # Project-local corpus
├── src/
└── ...
```

Add `.memex/` to your `.gitignore`:

```bash
echo '.memex/' >> .gitignore
```

---

## How Resolution Works

Memex walks up from your current working directory looking for `.memex/`. This means subdirectories inherit the project store:

```bash
cd ~/myproject/src/lib
memex dig "auth"           # Uses ~/myproject/.memex/

cd ~/otherproject
memex dig "auth"           # Uses ~/.memex/ (global fallback)
```

No flags needed. The convention handles routing automatically.

---

## Ingesting Into a Local Store

When a local `.memex/` exists, `memex ingest` writes to it:

```bash
cd ~/myproject
memex ingest relevant-conversations.json    # Goes to .memex/corpus.duckdb
```

To ingest into the global store instead, work from a directory without `.memex/`:

```bash
cd ~
memex ingest all-conversations.json         # Goes to ~/.memex/corpus.duckdb
```

---

## Checking Which Store Is Active

```bash
memex status
```

This shows the active corpus path, fragment count, and capabilities. Use it to confirm which store memex is using.

---

## Override With Environment Variables

For scripts or one-off commands, override the store with `MEMEX_CORPUS_PATH`:

```bash
MEMEX_CORPUS_PATH=~/special/corpus.duckdb memex dig "query"
```

Environment variables have highest precedence, overriding both local `.memex/` and global config.
