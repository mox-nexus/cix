# Your first recon survey

A concrete walkthrough. The goal: build a queryable dataset of recent GitHub releases for a set of libraries — so the next time Claude is asked "what changed in these deps lately?", the answer comes from real data, not from guessing.

You'll learn the **probe → normalize → survey** workflow by doing it. Total time: about ten minutes.

## Before you start

Install recon as an editable tool:

```bash
uv tool install --editable tools/recon
recon --version
```

Export a GitHub personal access token so the API gives you the real rate limit (5,000/hr instead of 60/hr):

```bash
export GITHUB_TOKEN=ghp_...
```

Any fine-grained or classic token with public-repo read is enough.

## Create the mission

A mission is a named unit of work. Each mission gets its own directory under `.cix/recon/`. Pick a descriptive name:

```bash
mkdir -p .cix/recon/dep-releases
$EDITOR .cix/recon/dep-releases/config.yaml
```

The config has two sections: **catalog** (where to look) and **collectors** (what to ask). You'll build it in three stages.

## Stage 1 — Probe

**Never write a normalize spec blind.** Normalize specs map source paths to output columns, but you don't know the source paths until you've seen a real response. Guessing wastes rate-limit budget on records you'll have to re-fetch with the right spec.

Start minimal: one source, one collector, limit of one, **no normalize block**:

```yaml
catalog:
  - name: github
    type: api
    url: https://api.github.com
    auth:
      header: Authorization
      env: GITHUB_TOKEN
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.7.0 (first-survey walkthrough)"

collectors:
  - name: probe
    type: api
    source: github
    endpoint: /repos/tokio-rs/tokio/releases
    params:
      per_page: "1"
    # no normalize block — emit the raw record
```

Run it:

```bash
recon survey dep-releases
```

You should see:

```
Mission: dep-releases — 1 collector(s), 1 source(s)
  probe: 1 records
/Users/you/project/.cix/recon/dep-releases/archive/2026-04-06-143022-123456/
```

One request, one record, one timestamped archive.

## Stage 2 — Inspect the raw shape

Look at what GitHub actually returned:

```bash
cat .cix/recon/dep-releases/archive/*/probe.jsonl | jq .
```

```json
{
  "url": "https://api.github.com/repos/tokio-rs/tokio/releases/...",
  "html_url": "https://github.com/tokio-rs/tokio/releases/tag/tokio-1.46.0",
  "tag_name": "tokio-1.46.0",
  "name": "Tokio v1.46.0",
  "author": { "login": "Darksonn", "id": 6716370 },
  "prerelease": false,
  "published_at": "2026-03-15T18:42:31Z",
  "body": "### Added\n- ..."
}
```

Read off the shape: `tag_name` is at the top level, `published_at` is a string timestamp, `author` is a nested object where `login` is the field that matters, `html_url` is the web-viewable link. There's a lot of noise in the raw response — URLs for the API's own routing, numeric IDs that don't matter, metadata fields that are never queried. The normalize spec is about throwing the noise away and keeping what's load-bearing.

## Stage 3 — Write the normalize spec

Add a `normalize:` block to the collector based on what the raw record actually contains:

```yaml
collectors:
  - name: probe
    type: api
    source: github
    endpoint: /repos/tokio-rs/tokio/releases
    params:
      per_page: "1"
    normalize:
      tag: tag_name
      name: name
      published: published_at
      author: "author.login"        # nested dot path
      prerelease: prerelease
      url: html_url
```

Re-run on the same one-record sample:

```bash
recon survey dep-releases
cat .cix/recon/dep-releases/archive/*/probe.jsonl | jq .
```

```json
{
  "tag": "tokio-1.46.0",
  "name": "Tokio v1.46.0",
  "published": "2026-03-15T18:42:31Z",
  "author": "Darksonn",
  "prerelease": false,
  "url": "https://github.com/tokio-rs/tokio/releases/tag/tokio-1.46.0"
}
```

Uniform columns, populated. If a path was wrong, that field would be `null` — fix the path in the config and re-run. Iteration is cheap because the sample is one record and the rate limit budget is tiny per attempt.

This is the whole point of probing first: the iteration loop happens at the cheapest possible scale.

## Stage 4 — Survey

The normalize spec is validated. Now scale it out. Bump the per-page limit and add the other repos you actually care about:

```yaml
catalog:
  - name: github
    type: api
    url: https://api.github.com
    auth:
      header: Authorization
      env: GITHUB_TOKEN
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.7.0 (dep-releases monitor)"

collectors:
  - name: tokio
    type: api
    source: github
    endpoint: /repos/tokio-rs/tokio/releases
    params: { per_page: "10" }
    normalize:
      tag: tag_name
      name: name
      published: published_at
      author: "author.login"
      prerelease: prerelease
      url: html_url

  - name: axum
    type: api
    source: github
    endpoint: /repos/tokio-rs/axum/releases
    params: { per_page: "10" }
    normalize:
      tag: tag_name
      published: published_at
      author: "author.login"
      url: html_url

  - name: serde
    type: api
    source: github
    endpoint: /repos/serde-rs/serde/releases
    params: { per_page: "10" }
    normalize:
      tag: tag_name
      published: published_at
      url: html_url
```

Run the survey:

```bash
recon survey dep-releases
```

```
Mission: dep-releases — 3 collector(s), 1 source(s)
  tokio: 10 records
  axum: 10 records
  serde: 10 records
```

Three JSONL files in the latest archive, one per collector. The `probe` collector is gone because you renamed it — that file only lives in the earlier archive.

## Stage 5 — Query

DuckDB reads JSONL natively. Table names derive from filenames (hyphens become underscores). Query the latest archive:

```bash
recon query dep-releases "SELECT tag, published FROM tokio ORDER BY published DESC LIMIT 5"
```

Cross-repo query with `UNION ALL`:

```bash
recon query dep-releases "
  SELECT 'tokio' AS repo, tag, published FROM tokio
  UNION ALL
  SELECT 'axum', tag, published FROM axum
  UNION ALL
  SELECT 'serde', tag, published FROM serde
  ORDER BY published DESC
  LIMIT 20
"
```

The cross-source view — "what has shipped across my dependency tree recently, regardless of which repo it came from" — is the payoff. Three sources, one schema, one SQL query, and Claude never had to read 30 raw GitHub release records to get there.

## What you just did

You took a messy HTTP response shape and turned it into a queryable structured dataset — without writing any code. The normalize spec did the reshape declaratively. The probe step made the iteration cheap. The survey step scaled the validated spec across sources.

This is the shape of every recon mission, regardless of domain. Fetch a sample, see the shape, write the reshape, scale it out, query the result. Whether the source is GitHub, Semantic Scholar, an internal metrics API, a docs site, or `rg` across twelve repositories — the workflow is the same.

## Running this on a schedule

Recon is mechanical, so it runs without Claude present. A cron entry:

```cron
0 * * * * cd /path/to/project && recon survey dep-releases
```

Every hour, a fresh timestamped archive lands under `.cix/recon/dep-releases/archive/`. The next time Claude looks, it can diff the latest archive against the previous one to find releases that are new — without needing to have been awake when they shipped.

## Where to go next

- `recon --skill` — the full skill Claude loads to author configs
- `recon --skill -r config-patterns` — nine domain patterns (code mining, RSS, dependency audits, issue triage, doc surveys, and more) as complete copy-and-adapt configs
- `recon --skill -r normalize-spec` — full normalize spec syntax including transforms (`$html2text`, `$inverted_index`, `$pdf2text`, `$join`, `$first`)
- [capability.md](../explanation/capability.md) — the deeper "why" behind the tool
- The `examples/` directory in the skill bundle — ready-to-run configs for probe-then-survey, code mining, and API monitoring
