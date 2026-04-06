---
name: recon
description: "This skill should be used when the user asks to 'collect data from an API', 'scrape a website', 'mine a codebase', 'fetch from multiple sources', 'normalize this response', 'query across sources with SQL', 'build a dataset', 'monitor something over time', 'run a survey', 'find papers', 'scan repos for patterns', 'track releases', 'audit dependencies', 'aggregate structured data', 'write a recon config', or needs to transform unstructured/semi-structured data from heterogeneous sources into queryable structured JSONL."
version: 0.7.0
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
- [Fan-Out](#fan-out)
- [CLI Commands](#cli-commands)
- [Writing Configs](#writing-configs)
- [Reading Results](#reading-results)
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

**Always probe first** (see [Probe Before Survey](#probe-before-survey)). Write a minimal config with `limit: "1"` (or equivalent) and no `normalize:` block. Inspect the raw JSONL. Then add the normalize spec based on what you actually saw. Then bump limits and run the full survey.

**Starting points:**
- Built-in research template: `recon init <mission> --template research` (academic paper search across S2 / arXiv / OpenAlex / Zenodo)
- Pattern library for other domains — see [config-patterns.md](references/config-patterns.md) (academic, code mining single/multi-repo, content tracking)

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
| Config patterns across 9 domains (academic, code mining, release monitoring, RSS, dependency audits, doc surveys, issue triage, content tracking) | [config-patterns.md](references/config-patterns.md) |
| Normalize spec syntax, path resolution, built-in transforms | [normalize-spec.md](references/normalize-spec.md) |

### Example Configs

Ready-to-run YAML configs in `examples/`. Copy, adapt the placeholders, write to `.cix/recon/<mission>/config.yaml`:

| Example | Demonstrates |
|---------|--------------|
| [`probe-then-survey.yaml`](examples/probe-then-survey.yaml) | The three-stage iterative workflow with three annotated stages (probe → normalize → survey) for an OpenAlex search |
| [`code-mining-multi-repo.yaml`](examples/code-mining-multi-repo.yaml) | Fan-out across local repos with ripgrep patterns, git log, and unsafe census collectors |
| [`api-monitoring.yaml`](examples/api-monitoring.yaml) | Periodic state capture via cron — GitHub releases API with diff-across-archives pattern |

### Built-in Templates

Bundled with the recon tool, loadable via `recon init <mission> --template <name>`:

| Template | Domain |
|----------|--------|
| `research` | Academic paper search across Semantic Scholar, arXiv, OpenAlex, Zenodo |
