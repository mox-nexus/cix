---
name: recon
description: "This skill should be used when the user asks to 'collect data from an API', 'scrape a website', 'mine a codebase', 'fetch from multiple sources', 'normalize this response', 'query across sources with SQL', 'build a dataset', 'monitor something over time', 'schedule a recurring survey', 'cron this', 'run a survey', 'find papers', 'scan repos for patterns', 'track releases', 'audit dependencies', 'snapshot an API', 'diff API state over time', 'extract structured records', 'build a JSONL dataset', 'use Exa', 'use Firecrawl', 'use Tavily', 'use Serper', 'use Perplexity', 'call a search API', 'convert a PDF to markdown', 'convert a DOCX', 'ingest documents', 'aggregate structured data', 'write a recon config', or needs to transform unstructured/semi-structured data from heterogeneous sources into queryable structured JSONL."
version: 0.8.0
---

# Recon

**Recon is the structured-data bridge.** Point it at any source — HTTP APIs, CLI tools, web pages, local filesystems — and it fetches responses, reshapes them into uniform JSONL, and makes the result queryable via DuckDB SQL. The reshape is declarative (normalize specs), not code. Claude writes the config, recon does the mechanical work, Claude reasons over the structured output.

## The Capability

Recon extends Claude's effective context through **structured indirection**. Instead of loading 1,000 records into Claude's prompt, recon stores them as queryable JSONL. Claude asks `SELECT title, year FROM papers WHERE citations > 100` and sees 10 rows — the other 990 never enter context. This scales Claude's effective reach by orders of magnitude, and keeps LLM inference focused on reasoning rather than on HTTP ceremony, response parsing, retry logic, or rate-limit handling.

Six capabilities it unlocks:

1. **Operate on datasets larger than the context window** — query, don't load
2. **Separate generative from mechanical work** — Claude thinks; recon fetches
3. **Reproducibility** — the config is a frozen, auditable artifact of what was collected
4. **Temporal awareness** — timestamped archives let Claude diff state over time
5. **Cross-source composition** — normalize heterogeneous sources to one schema, query across them
6. **Scheduled / offline execution** — cron it; Claude reads results later

## Domain Examples

Recon is general-purpose. The academic paper search is one instance. Other domains:

| Domain | What the config collects |
|---|---|
| Literature review | S2, arXiv, OpenAlex, Zenodo APIs |
| Code archaeology | `git log`, `gh api`, `rg` across multiple repos |
| Codebase audits | `rg` for patterns, `cargo tree`, unsafe census, TODOs |
| Release monitoring | GitHub releases, PyPI, crates.io, npm |
| Competitive analysis | Product pages, pricing, changelogs (web collector) |
| Content tracking | RSS feeds, blog indices, Substack archives |
| API state snapshots | Any REST endpoint captured periodically |
| Issue triage | `gh issue list` across repos with labels + metadata |
| Dependency audits | Package manifests, vulnerability feeds |
| Doc surveys | Scrape docs sites, extract structure |
| Benchmark collection | Tool outputs captured repeatedly over time |
| Market research | Company blogs, job boards, press releases |
| Infra inspection | `kubectl`, `docker inspect`, `terraform show` |

The common shape: *something out there has data in some response format; Claude needs to reason over it as structured records.* Recon bridges that.

---

## Contents

- [The Workflow](#the-workflow)
- [Probe Before Survey](#probe-before-survey)
- [Config Anatomy](#config-anatomy)
- [POST with JSON Body](#post-with-json-body)
- [Fan-Out](#fan-out)
- [CLI Commands](#cli-commands)
- [Writing Configs](#writing-configs)
- [Reading Results](#reading-results)
- [Sentinels and Error Signals](#sentinels-and-error-signals)
- [Preserving Raw Captures](#preserving-raw-captures)
- [Limitations](#limitations)

## The Workflow

```
Human intent
  ↓
Claude: PROBE — write minimal config, fetch 1 record, inspect raw shape
  ↓
Claude: write normalize spec from the actual response shape
  ↓
Claude: VALIDATE — re-run on the sample, confirm normalized fields
  ↓
Claude: SURVEY — bump limits, run full collection
  ↓
Recon: collect → .cix/recon/<mission>/archive/<timestamp>/*.jsonl + meta.yaml
  ↓
Claude: read JSONL directly, or `recon query <mission> "SQL"`
```

1. **Probe** — fetch a minimal sample first. Don't write normalize specs blind.
2. **Normalize** — write the reshape spec based on the actual response shape.
3. **Validate** — re-run on the sample to confirm the spec works.
4. **Survey** — full collection with correct spec and production limits.
5. **Query** — read JSONL directly, or `recon query <mission> "SQL"`.

## Probe Before Survey

**Never write a normalize spec blind.** Normalize specs map source paths to output columns — but the actual source paths only become knowable after seeing a real response. Guessing wastes rate-limit budget on records that will need to be re-fetched.

The iteration cycle:

### Step 1 — Probe (minimal config, no normalize)

Write a collector with a tiny limit and **no `normalize:` block**. Recon emits raw records (after `extract:` navigation) as-is.

```yaml
catalog:
  - name: semantic-scholar
    type: api
    url: https://api.semanticscholar.org/graph/v1
    rate_limit: { rps: 0.33, burst: 1 }

collectors:
  - name: probe
    type: api
    source: semantic-scholar
    endpoint: /paper/search
    params:
      query: "transformer attention"
      limit: "1"                    # one record is enough
      fields: "title,abstract,authors,citationCount,openAccessPdf,venue"
    extract: "data"                 # navigate to the records array
    # no normalize — emit raw shape
```

Run: `recon survey my-mission`.

### Step 2 — Inspect the raw shape

Read `.cix/recon/my-mission/archive/<latest>/probe.jsonl`. The raw JSONL reveals the actual field names, nesting, and types:

```json
{
  "paperId": "abc123",
  "title": "Attention Is All You Need",
  "abstract": "The dominant sequence...",
  "authors": [{"authorId": "1", "name": "Vaswani"}, {"authorId": "2", "name": "Shazeer"}],
  "citationCount": 94321,
  "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762"},
  "venue": "NeurIPS"
}
```

Read off the shape: `authors` is a list of `{name}` dicts, `openAccessPdf` is nested, `citationCount` is at the top level.

### Step 3 — Write the normalize spec

Add the block based on what you saw:

```yaml
    normalize:
      title: title
      abstract: abstract
      authors: "authors.*.name"           # list-map
      citations: citationCount
      pdf_url: "openAccessPdf.url"        # nested
      venue: venue
```

### Step 4 — Validate on the sample

Re-run `recon survey my-mission`. Confirm the JSONL now has the uniform columns, populated correctly. Fix path errors here — they're cheap.

### Step 5 — Survey

Bump `limit` to production values (e.g. `"20"` or `"100"`). Run the full collection. The normalize spec is validated; no field-path surprises.

### Why this matters

Skipping probe means discovering normalize bugs after fetching 100 records with wrong field paths — wasted rate-limit budget and a forced second run. Probe cost: 1 request. Mistake cost: 100 requests + rate-limit cooldown + redo. Always probe first.

### CLI / web collectors

The same workflow applies:
- **CLI**: use a pattern matching a tiny sample (e.g. `--max-count 1` on ripgrep), no normalize, inspect, then write spec
- **Web**: the web collector emits a fixed shape `{url, title, content, status_code, content_type}` — no normalize needed, but probe one URL before scaling fan-out across dozens

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
| `api` | HTTP request → JSON/XML → normalize → JSONL | `endpoint`, `params`, `method`, `body`, `extract`, `normalize` |
| `cli` | Shell command → parse stdout → normalize → JSONL | `run`, `patterns`, `normalize` |
| `web` | HTTP GET → HTML to markdown → JSONL | `endpoint` (optional) |

For normalize spec syntax and built-in transforms: see [normalize-spec.md](references/normalize-spec.md).

## POST with JSON Body

Modern search and scraping APIs (Exa, Firecrawl, Serper, Tavily, Perplexity, GraphQL endpoints) take a **POST with a JSON body**, not query-string params. Recon supports this directly.

Three config knobs make it work:

1. **`body:` on the collector** — a dict sent as the JSON request body when `method: POST` (also works for `PUT`, `PATCH`, `DELETE`).
2. **`auth.prefix:` on the source** — prepended to the resolved env value. `"Bearer "` for `Authorization: Bearer $TOKEN`, `"token "` for GitHub-style, empty for plain header auth like `x-api-key`.
3. **`{placeholder}` substitution in body strings** — values from `params:` are substituted into string values in `body` recursively, same as the `endpoint` path interpolation. The config stays a template; changing the search term is a one-line edit to `params`, not a regeneration of the whole YAML. Non-string values (ints, bools, lists, nested dicts) pass through; only string values get substituted. **Unresolved `{foo}` raises `CollectionError` before any HTTP request fires** — the collector refuses to send a body with missing placeholders, so you get a loud failure at probe time instead of silent 400s or empty results at production scale. Add every referenced key to `params:`.

### Exa — neural search

```yaml
catalog:
  - name: exa
    type: api
    url: https://api.exa.ai
    auth: { header: x-api-key, env: EXA_API_KEY }   # no prefix needed
    rate_limit: { rps: 1, burst: 2 }

collectors:
  - name: exa-search
    type: api
    source: exa
    endpoint: /search
    method: POST
    params:
      topic: "transformer attention mechanism"   # change me, don't regenerate the YAML
    body:
      query: "{topic}"                           # templated
      numResults: 10                             # literal int stays literal
      type: "neural"
      contents:
        text: true
    extract: "results"
    normalize:
      title: title
      url: url
      text: "text"
      score: score
```

### Firecrawl — scrape a URL to markdown

```yaml
catalog:
  - name: firecrawl
    type: api
    url: https://api.firecrawl.dev
    auth:
      header: Authorization
      env: FIRECRAWL_API_KEY
      prefix: "Bearer "           # ← the prefix is the important part
    rate_limit: { rps: 1, burst: 2 }

collectors:
  - name: scrape
    type: api
    source: firecrawl
    endpoint: /v1/scrape
    method: POST
    params:
      target_url: "https://example.com/article"
    body:
      url: "{target_url}"
      formats: ["markdown", "links"]
      onlyMainContent: true
    extract: "data"               # Firecrawl wraps the result in {success, data: {...}}
    normalize:
      markdown: markdown
      title: "metadata.title"
      source_url: "metadata.sourceURL"
```

### The pattern for any POST-body search API

Same shape works for Serper (`/search`), Tavily (`/search`), Perplexity (`/chat/completions`), Linkup (`/search`), You.com — swap the URL, auth, body fields, and `extract` path. See [config-patterns.md](references/config-patterns.md#modern-search-apis-post-body) for full examples including Tavily and Serper.

### Auth prefix cheatsheet

Store the raw credential in the env var; `auth.prefix` is prepended at request time.

| Service | `header` | `prefix` |
|---|---|---|
| Exa | `x-api-key` | `""` |
| Firecrawl, Tavily, Perplexity, OpenAI-compatible | `Authorization` | `"Bearer "` |
| Serper | `X-API-KEY` | `""` |
| GitHub (modern fine-grained) | `Authorization` | `"Bearer "` |
| GitHub (classic PAT) | `Authorization` | `"token "` |

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

**Always probe first** (see [Probe Before Survey](#probe-before-survey)). Write a minimal config with `limit: "1"` (or equivalent) and no `normalize:` block. Inspect the raw JSONL. Then add the normalize spec based on what you actually saw. Then bump limits and run the full survey.

**Starting points:**
- Built-in templates: `recon templates` lists them. Each is a runnable starter for a distinct capability (code forensics, GitHub audit, docs mining, release tracking, factual grounding, RSS/Atom monitoring). Scaffold with `recon init <mission> --template <name>`. Plugin-owned catalogs (e.g. craft-research's academic catalog) load via `recon init <mission> --from <path>`.
- Pattern library for other domains — see [config-patterns.md](references/config-patterns.md) (code mining single/multi-repo, code-maat forensics, release monitoring, RSS, dependency audits, doc surveys, issue triage, content tracking)

For normalize spec syntax and built-in transforms: [normalize-spec.md](references/normalize-spec.md).

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

## Sentinels and Error Signals

Recon marks three conditions explicitly so downstream tooling (and Claude reading an archive) never has to guess.

**`{"_empty": true}`** — a collector produced zero records. Recon writes this single-record sentinel to the JSONL so DuckDB `read_json_auto` has a valid file to read. Query for it with `WHERE NOT coalesce(_empty, false)` to exclude:

```sql
SELECT * FROM s2_search WHERE NOT coalesce(_empty, false)
```

**`.incomplete` file at archive root** — at least one collector errored, or `meta.yaml` itself failed to write. `recon status` shows the archive state as `incomplete`; `recon query` prints a yellow warning before running the SQL. Read `meta.yaml` to see which collectors failed:

```yaml
collectors:
  - name: arxiv-search
    status: error
    error: "[arxiv-search against 'arxiv'] HTTP request failed after retries: ..."
    seconds: 60.04
```

**Output-name collision (pre-flight abort)** — if two collectors would write to the same filename (e.g., a pinned `foo-arxiv` collector plus a fan-out `foo` over source `arxiv` — both compute `foo-arxiv.jsonl`), recon raises `ReconError` **before** creating the archive directory. No partial write can happen. The error message names the colliding output(s). Rename one of the colliding collectors to fix.

**Unresolved `{placeholder}` in body** — if an `api` collector has a `body:` that still contains `{foo}` after substitution from `params:`, recon raises `CollectionError` before the HTTP request fires, listing the missing keys. No silent 400s. Add the referenced key to `params:`.

## Preserving Raw Captures

Set `preserve_raw: true` at the top of the config to save the raw fetched bytes (HTTP response body or CLI stdout) alongside the processed JSONL:

```yaml
preserve_raw: true
catalog:
  - name: ...
collectors:
  - ...
```

Layout under `archive/<ts>/raw/<collector_name>/`:

| File | Contents |
|---|---|
| `body` | Raw HTTP response bytes (for api/web) or full CLI stdout |
| `meta.yaml` | Type-tagged metadata: `sha256`, `bytes`, `captured_at`, plus `{status, url, headers, content_type}` for HTTP or `{command, cwd, exit_code, patterns}` for CLI |

Three reasons to turn this on:
- **Re-normalize without re-fetching** — change the `normalize:` spec, re-run your downstream tooling against the raw snapshot, no rate-limit budget consumed.
- **Audit** — `sha256` + timestamp + headers prove what the server said at capture time.
- **Experimentation** — try different normalize specs, converters, or extraction paths against a frozen input.

Trade-off: ~2× disk usage per mission. Off by default.

## Timeouts and Fallbacks

Sources accept a `timeout` field (seconds, default 60). Slow sources need longer:

```yaml
catalog:
  - name: slow-api
    type: api
    url: https://example.com/api
    timeout: 90
```

When a collector fails (timeout, 429, 5xx, non-zero exit), the error is recorded in `meta.yaml` and remaining collectors continue. Read meta.yaml after the survey to check for failures — recon does not crash the whole run on one failed collector.

**Fallback pattern:** if an API fails or returns insufficient data, define a second collector using a different source type (e.g., `web` scraping when the `api` doesn't work). Recon doesn't chain fallbacks automatically — it's mechanical. Claude reads meta.yaml, sees which collectors failed, and writes a second config to try the fallback.

## Limitations

- **No pagination.** API collectors make one request per collector entry. For paginated APIs, create multiple collector entries or use CLI tools that handle pagination.
- **Sequential execution.** Collectors run one at a time. Parallelism happens at the caller level (multiple `recon survey` calls).
- **No deduplication.** Each archive is independent. Cross-archive dedup is the caller's responsibility.
- **Shell injection surface.** CLI collectors execute commands via `shell=True`. Configs should be generated by Claude, not from untrusted user input.

## References

### Reference Files

Load on demand for deeper detail. Access from Claude with `recon --skill -r <name>`:

| Need | Reference |
|------|-----------|
| Config patterns across 9 domains (code mining, code-maat forensics, release monitoring, RSS, dependency audits, doc surveys, issue triage, content tracking) | [config-patterns.md](references/config-patterns.md) |
| Normalize spec syntax, path resolution, built-in transforms | [normalize-spec.md](references/normalize-spec.md) |

### Example Configs

Ready-to-run YAML configs in `examples/`. Copy, adapt the placeholders, write to `.cix/recon/<mission>/config.yaml`:

| Example | Demonstrates |
|---------|--------------|
| [`probe-then-survey.yaml`](examples/probe-then-survey.yaml) | The three-stage iterative workflow with three annotated stages (probe → normalize → survey) for an OpenAlex search |
| [`code-mining-multi-repo.yaml`](examples/code-mining-multi-repo.yaml) | Fan-out across local repos with ripgrep patterns, git log, and unsafe census collectors |
| [`api-monitoring.yaml`](examples/api-monitoring.yaml) | Periodic state capture via cron — GitHub releases API with diff-across-archives pattern |
| [`exa-post-body.yaml`](examples/exa-post-body.yaml) | Exa neural search via POST with JSON body — `{placeholder}` templating + x-api-key auth |

### Built-in Templates

Bundled with the recon tool, loadable via `recon init <mission> --template <name>`. Each template demonstrates a distinct recon capability so the set collectively documents what the tool can do.

| Template | Demonstrates |
|----------|--------------|
| `code-forensics` | Local source + cli collectors, patterns fan-out, no HTTP/auth |
| `github-audit` | API source with optional header auth, path-level placeholders, multi-endpoint collection |
| `docs-mine` | Web source + web collectors, HTML → markdown with fixed output schema |
| `package-registries` | Multi-source API (PyPI / npm / crates.io) normalized to one common schema |
| `factual-ground` | Wikipedia MediaWiki API + Wikidata SPARQL with deeply-nested JSON unpacking |
| `rss-monitor` | `response_format: xml` with attribute extraction via `.@attr` — Atom feeds |

Domain-specific catalogs (e.g. academic literature for craft-research) live inside the consuming plugin, not inside recon. Scaffold from them via `recon init <mission> --from <path>`.
