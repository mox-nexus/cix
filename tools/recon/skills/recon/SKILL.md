---
name: recon
description: "This skill should be used when the user asks to 'find papers', 'survey papers on a topic', 'search for research on', 'search academic databases', 'collect data from APIs', 'mine code repositories', 'scan for patterns', 'run recon', 'write a recon config', 'query recon results', or needs config-driven mechanical data collection from HTTP APIs, CLI tools, or local repositories into queryable JSONL."
version: 0.7.0
---

# Recon

Mechanical collection system. Config-driven, no LLM. Fetches from HTTP APIs, runs CLI tools, normalizes output into JSONL files queryable via DuckDB. Intelligence lives outside — Claude writes the config, recon executes it, Claude reasons over the results.

**Craft-research integration:** Recon provides source discovery and metadata for the [craft-research pipeline](../../../../plugins/craft-research/). Use recon to find papers, then feed results into the research workspace.

---

## Contents

- [The Workflow](#the-workflow)
- [Config Anatomy](#config-anatomy)
- [Fan-Out](#fan-out)
- [CLI Commands](#cli-commands)
- [Writing Configs](#writing-configs)
- [Reading Results](#reading-results)
- [Limitations](#limitations)

## The Workflow

```
Human: "find papers on transformer attention mechanisms"
  ↓
Claude: generate config → write to .cix/recon/<mission>/config.yaml
  ↓
Claude: run `recon survey <mission>`
  ↓
Recon: collect → .cix/recon/<mission>/archive/<timestamp>/*.jsonl + meta.yaml
  ↓
Claude: read JSONL directly, or `recon query <mission> "SQL"`
```

1. **Generate config** — translate user intent into a YAML config with catalog (sources) and collectors (what to ask). Bake values directly into the config — no runtime variable substitution.
2. **Create mission directory** — `mkdir -p .cix/recon/<mission>/` and write `config.yaml`.
3. **Run survey** — `recon survey <mission>`. Output lands in `archive/<timestamp>/`.
4. **Read results** — JSONL files are plain text. Read directly or query with DuckDB SQL.

## Config Anatomy

Every config has two sections: **catalog** (where to look) and **collectors** (what to ask).

```yaml
catalog:
  - name: semantic-scholar
    type: api                    # api | web | local
    url: https://api.semanticscholar.org/graph/v1
    auth: { header: x-api-key, env: S2_API_KEY }
    rate_limit: { rps: 0.33, burst: 1 }

collectors:
  - name: s2-search
    type: api                    # api | cli | web
    source: semantic-scholar     # pin to specific source (omit for fan-out)
    endpoint: /paper/search
    params:
      query: "transformer attention"
      limit: "20"
      fields: "title,abstract,year,authors,citationCount"
    extract: "data"              # dotted path to record array in response
    normalize:                   # output column: source path [|$transform]
      title: title
      authors: "authors.*.name"
      year: year
      citations: citationCount
```

### Source Types

| Type | Purpose | `url` holds |
|------|---------|-------------|
| `api` | HTTP endpoints with auth, rate limits | Base URL |
| `web` | Web pages, HTML → markdown via markdownify | Site URL |
| `local` | Filesystem directories for CLI tools | Directory path |

### Collector Types

| Type | How it works | Key fields |
|------|-------------|------------|
| `api` | HTTP request → JSON/XML → normalize → JSONL | `endpoint`, `params`, `extract`, `normalize` |
| `cli` | Shell command → parse stdout → normalize → JSONL | `run`, `patterns`, `normalize` |
| `web` | HTTP GET → HTML to markdown → JSONL | `endpoint` (optional) |

For normalize spec syntax and built-in transforms: see [normalize-spec.md](references/normalize-spec.md).

## Fan-Out

Collector with no `source:` runs against **every catalog entry**. Specify `source:` to pin.

```yaml
catalog:
  - name: tokio
    type: local
    url: /Users/dev/oss/tokio
  - name: bytes
    type: local
    url: /Users/dev/oss/bytes

collectors:
  - name: scars
    type: cli
    # no source → fans out across tokio AND bytes
    run: "rg --json -C5 'note that|critical|must|never' --type rust"
```

Produces: `scars-tokio.jsonl`, `scars-bytes.jsonl`. For pinned collectors: `s2-search.jsonl`.

For CLI collectors, `source.url` is used as the working directory (`cwd`) when it's a valid local path.

## CLI Commands

```
recon survey <name>                    # run collection mission
recon status                           # list missions + archive count
recon query <name> "SQL"               # DuckDB query on latest archive
recon query <name> "SQL" --run <ts>    # query specific archive
recon query <name> "SQL" --json        # JSON output for piping
```

Project root discovery: walks up from cwd looking for `.git/`. Mission data lives at `<project>/.cix/recon/<name>/`.

## Writing Configs

Translate user intent into a complete config. Do not leave `{placeholder}` values — bake all query terms, limits, and paths directly into the YAML.

**Starting point:** Copy the built-in template at `tools/recon/src/recon/configs/research.yaml`, replace all `{query}` and `{limit}` placeholders with the user's actual values, then write to the mission directory.

For complete config examples (academic research, multi-repo code mining, single-repo analysis, job tracking): see [config-patterns.md](references/config-patterns.md).

## Reading Results

### Direct Read

JSONL files are one JSON object per line. Read them directly:

```python
# Claude reads .cix/recon/<mission>/archive/<latest>/*.jsonl
```

### DuckDB Query

DuckDB reads JSONL natively. Table names derive from filenames (hyphens → underscores):

```sql
-- After: recon query attention-mechanisms "SQL"
SELECT title, year, citations
FROM s2_search
WHERE citations > 100
ORDER BY citations DESC
```

### Meta.yaml

Each archive includes `meta.yaml` with run metadata: timestamp, collector results (status, record count, timing).

## Timeouts and Fallbacks

Sources accept a `timeout` field (seconds, default 60). Slow APIs like arXiv need longer:

```yaml
catalog:
  - name: arxiv
    type: api
    url: https://export.arxiv.org/api
    timeout: 90
```

When an API collector fails (timeout, 429, 5xx), the error is recorded in `meta.yaml` and remaining collectors continue. Read meta.yaml after the survey to check for failures.

**Fallback pattern:** if an API fails, retry with the web collector. Recon doesn't do this automatically — it's mechanical. Instead, read meta.yaml, see the error, and run a second survey with a web-based config:

```yaml
# Fallback: scrape arXiv web search instead of API
collectors:
  - name: arxiv-web
    type: web
    source: arxiv-web
    endpoint: /search/?query=attention+mechanism
```

## Limitations

- **No pagination.** API collectors make one request per collector entry. For paginated APIs, create multiple collector entries or use CLI tools that handle pagination.
- **Sequential execution.** Collectors run one at a time. Parallelism happens at the caller level (multiple `recon survey` calls).
- **No deduplication.** Each archive is independent. Cross-archive dedup is the caller's responsibility.
- **Shell injection surface.** CLI collectors execute commands via `shell=True`. Configs should be generated by Claude, not from untrusted user input.

## References

| Need | Load |
|------|------|
| Config examples (research, code mining, content tracking) | [config-patterns.md](references/config-patterns.md) |
| Normalize spec syntax + transforms | [normalize-spec.md](references/normalize-spec.md) |
| Built-in research template | `tools/recon/src/recon/configs/research.yaml` |
