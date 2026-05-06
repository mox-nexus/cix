# Collecting from a POST-body search API

Modern search and scraping APIs — Exa, Firecrawl, Tavily, Serper, Perplexity, Linkup — don't take GET + query-string. They take a **POST with a JSON body**. Recon handles this directly, the config stays a template, and swapping the search term is a one-line edit.

This walkthrough uses **Exa** (neural search) because the auth is simple and the response shape is clean. The same pattern applies to any POST-body API — swap the URL, auth, and body fields.

## Before you start

Install recon as an editable tool:

```bash
uv tool install --editable tools/recon
recon --version
```

Get an Exa API key (free tier available at [exa.ai](https://exa.ai)) and export it:

```bash
export EXA_API_KEY=your-key-here
```

## Three new things to know

Three config knobs make POST-body APIs work:

1. **`method: POST`** on the collector — recon sends a POST instead of a GET.
2. **`body:`** on the collector — a dict sent as the JSON request body. Works for `POST`, `PUT`, `PATCH`, `DELETE`.
3. **`auth.prefix:`** on the source — prepended to the resolved env value. Empty for `x-api-key` style auth (Exa). `"Bearer "` for `Authorization: Bearer <token>` style (Firecrawl, Tavily, Perplexity, most OpenAI-compatible endpoints). `"token "` for classic GitHub PATs.

Plus one templating knob that keeps the config generic:

4. **`{placeholder}` substitution in body strings** — values from `params:` are substituted recursively into string values in `body:`. Non-strings (ints, bools, lists, nested dicts) pass through untouched. This is the same `substitute()` mechanism recon already uses for `endpoint` path interpolation and `cli.run` commands. **If any `{foo}` remains unresolved after substitution, recon raises `CollectionError` before sending the request** — loud local failure beats silent server-side 400s or empty results. Add every `{foo}` you reference to `params:`.

## Create the mission

```bash
mkdir -p .cix/recon/exa-discovery
$EDITOR .cix/recon/exa-discovery/config.yaml
```

## Stage 1 — Probe

Minimal config. One catalog entry, one collector, `numResults: 1`, **no normalize block**.

```yaml
catalog:
  - name: exa
    type: api
    url: https://api.exa.ai
    auth:
      header: x-api-key
      env: EXA_API_KEY
      # no prefix — Exa uses raw x-api-key
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.8.0 (exa-discovery walkthrough)"

collectors:
  - name: probe
    type: api
    source: exa
    endpoint: /search
    method: POST
    params:
      topic: "transformer attention mechanism"   # ← change me, don't regenerate YAML
    body:
      query: "{topic}"                            # ← templated
      numResults: 1                               # ← literal int
      type: "neural"
      contents:
        text: true
    extract: "results"
    # no normalize — emit the raw record
```

Run it:

```bash
recon survey exa-discovery
```

Expected output:

```
Mission: exa-discovery — 1 collector(s), 1 source(s)
  probe: 1 records
/Users/you/project/.cix/recon/exa-discovery/archive/2026-04-19-113022-123456/
```

## Stage 2 — Inspect the raw shape

```bash
cat .cix/recon/exa-discovery/archive/*/probe.jsonl | jq .
```

Exa returns records shaped like:

```json
{
  "title": "Attention Is All You Need",
  "url": "https://arxiv.org/abs/1706.03762",
  "publishedDate": "2017-06-12T00:00:00.000Z",
  "author": "Ashish Vaswani",
  "score": 0.234,
  "id": "https://arxiv.org/abs/1706.03762",
  "text": "The dominant sequence transduction models are based on..."
}
```

Read off the shape: `title`, `url`, `publishedDate`, `score`, `text` are all top-level strings/floats. `author` is a string (not a list in Exa's `/search` response — note the contrast with other APIs).

## Stage 3 — Write the normalize spec

Add a `normalize:` block based on what you saw:

```yaml
collectors:
  - name: probe
    type: api
    source: exa
    endpoint: /search
    method: POST
    params:
      topic: "transformer attention mechanism"
    body:
      query: "{topic}"
      numResults: 1
      type: "neural"
      contents:
        text: true
    extract: "results"
    normalize:
      title: title
      url: url
      published: publishedDate
      author: author
      score: score
      text: text
```

Re-run on the same one-record sample:

```bash
recon survey exa-discovery
cat .cix/recon/exa-discovery/archive/*/probe.jsonl | jq .
```

Uniform columns, populated. If a path was wrong, the field would be `null` — fix and re-run. Iteration is cheap because `numResults: 1` keeps the probe one request.

## Stage 4 — Survey

Bump `numResults` and rename the collector. Change the search term by editing one line in `params:` — **no regeneration of the whole YAML**:

```yaml
catalog:
  - name: exa
    type: api
    url: https://api.exa.ai
    auth:
      header: x-api-key
      env: EXA_API_KEY
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.8.0 (exa-discovery survey)"

collectors:
  - name: neural-search
    type: api
    source: exa
    endpoint: /search
    method: POST
    params:
      topic: "state-space models post-Mamba"    # ← only this line changes per variation
    body:
      query: "{topic}"
      numResults: 15
      type: "neural"
      contents:
        text: true
    extract: "results"
    normalize:
      title: title
      url: url
      published: publishedDate
      author: author
      score: score
      text: text
```

Run the survey:

```bash
recon survey exa-discovery
```

```
Mission: exa-discovery — 1 collector(s), 1 source(s)
  neural-search: 15 records
```

## Stage 5 — Query

```bash
recon query exa-discovery "SELECT title, url, score FROM neural_search WHERE score > 0.5 ORDER BY score DESC LIMIT 10"
```

## Other POST-body APIs — same shape, different knobs

The whole workflow above is identical for the other major POST-body search APIs. The only things that change are URL, auth, body field names, and `extract:` path.

**Firecrawl** (scrape a URL to markdown):

```yaml
catalog:
  - name: firecrawl
    type: api
    url: https://api.firecrawl.dev
    auth:
      header: Authorization
      env: FIRECRAWL_API_KEY
      prefix: "Bearer "          # ← Firecrawl needs Bearer

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
    extract: "data"              # Firecrawl wraps result in {success, data: {...}}
    normalize:
      markdown: markdown
      title: "metadata.title"
      source_url: "metadata.sourceURL"
```

**Tavily** (LLM-optimized search):

```yaml
catalog:
  - name: tavily
    type: api
    url: https://api.tavily.com
    auth:
      header: Authorization
      env: TAVILY_API_KEY
      prefix: "Bearer "

collectors:
  - name: tavily-search
    type: api
    source: tavily
    endpoint: /search
    method: POST
    params:
      topic: "recent advances in state-space models"
    body:
      query: "{topic}"
      search_depth: "advanced"
      max_results: 10
      include_raw_content: true
    extract: "results"
    normalize:
      title: title
      url: url
      content: content
      raw_content: raw_content
      score: score
```

**Serper** (Google results via API — no Bearer prefix):

```yaml
catalog:
  - name: serper
    type: api
    url: https://google.serper.dev
    auth:
      header: X-API-KEY
      env: SERPER_API_KEY
      # no prefix — Serper uses raw X-API-KEY

collectors:
  - name: serper-web
    type: api
    source: serper
    endpoint: /search
    method: POST
    params:
      query: "arxiv transformer survey 2025"
    body:
      q: "{query}"
      num: 20
      gl: "us"
      hl: "en"
    extract: "organic"           # Serper returns {organic: [...], knowledgeGraph: {...}}
    normalize:
      title: title
      url: link
      snippet: snippet
      position: position
```

## Auth prefix cheatsheet

| Service | `header` | `prefix` |
|---|---|---|
| Exa | `x-api-key` | `""` |
| Firecrawl | `Authorization` | `"Bearer "` |
| Tavily | `Authorization` | `"Bearer "` |
| Serper | `X-API-KEY` | `""` |
| Perplexity | `Authorization` | `"Bearer "` |
| OpenAI-compatible | `Authorization` | `"Bearer "` |
| GitHub (modern) | `Authorization` | `"Bearer "` |
| GitHub (classic PAT) | `Authorization` | `"token "` |

In all cases the env var holds the raw credential. The prefix is prepended at request time.

## What you just did

You converted a POST-body search API into a queryable structured dataset with the same **probe → normalize → survey** workflow that `first-survey.md` used for GET. The differences were entirely in the config surface — `method: POST`, `body:`, and `auth.prefix:`. The substitution engine keeps the config generic, so future variations (different search term, different target URL) are one-line edits rather than YAML regenerations.

## Where to go next

- [first-survey.md](./first-survey.md) — the GET walkthrough (GitHub releases)
- `recon --skill` — the full skill Claude loads to author configs
- `recon --skill -r config-patterns` — broader config patterns, including the full "Modern Search APIs (POST body)" section with Perplexity and the composed Exa→Firecrawl pattern
- `recon --skill -r normalize-spec` — normalize spec syntax and built-in transforms
- [capability.md](../explanation/capability.md) — the deeper "why" behind the tool
