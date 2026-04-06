# Config Patterns

Complete config examples for common recon use cases. Copy, adapt, write to `.cix/recon/<mission>/config.yaml`.

## Contents

- [Academic Research](#academic-research)
- [Code Mining (Multi-Repo)](#code-mining-multi-repo)
- [Code Mining (Single Repo)](#code-mining-single-repo)
- [Forensic Code Analysis with code-maat](#forensic-code-analysis-with-code-maat)
- [Content Tracking (Scheduled)](#content-tracking-scheduled)
- [Release Monitoring](#release-monitoring)
- [RSS / Blog Tracking](#rss--blog-tracking)
- [Dependency Audits](#dependency-audits)
- [Doc Site Survey](#doc-site-survey)
- [Issue Triage Across Repos](#issue-triage-across-repos)

## Academic Research

Search across 4 academic APIs. Each collector pins to its source because APIs have different endpoints, params, and response shapes.

```yaml
catalog:
  - name: semantic-scholar
    type: api
    url: https://api.semanticscholar.org/graph/v1
    auth: { header: x-api-key, env: S2_API_KEY }
    rate_limit: { rps: 0.33, burst: 1 }

  - name: arxiv
    type: api
    url: https://export.arxiv.org/api

  - name: openalex
    type: api
    url: https://api.openalex.org
    auth: { param: api_key, env: OPENALEX_API_KEY }
    rate_limit: { rps: 10, burst: 5 }
    user_agent: "recon/0.7.0 (mailto:user@example.com)"

  - name: zenodo
    type: api
    url: https://zenodo.org/api
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.7.0 (https://github.com/user/project)"

collectors:
  - name: s2-search
    type: api
    source: semantic-scholar
    endpoint: /paper/search
    params:
      query: "transformer attention mechanisms"
      limit: "20"
      fields: "title,abstract,year,authors,citationCount,openAccessPdf,venue"
    extract: "data"
    normalize:
      title: title
      abstract: abstract
      authors: "authors.*.name"
      year: year
      citations: citationCount
      pdf_url: "openAccessPdf.url"
      venue: venue

  - name: arxiv-search
    type: api
    source: arxiv
    endpoint: /query
    params:
      search_query: "transformer attention mechanisms"
      max_results: "20"
    response_format: xml
    extract: "feed.entry"
    normalize:
      title: title
      abstract: summary
      authors: "author.*.name"
      year: published
      source_id: id

  - name: openalex-search
    type: api
    source: openalex
    endpoint: /works
    params:
      search: "transformer attention mechanisms"
      per_page: "20"
      select: "id,title,doi,publication_year,cited_by_count,authorships,open_access,abstract_inverted_index,primary_location"
    extract: "results"
    normalize:
      title: display_name
      abstract: "abstract_inverted_index|$inverted_index"
      authors: "authorships.*.author.display_name"
      year: publication_year
      citations: cited_by_count
      pdf_url: "open_access.oa_url"
      venue: "primary_location.source.display_name"

  - name: zenodo-search
    type: api
    source: zenodo
    endpoint: /records
    params:
      q: "transformer attention mechanisms"
      size: "20"
      sort: bestmatch
    extract: "hits.hits"
    normalize:
      title: "metadata.title"
      abstract: "metadata.description|$html2text"
      authors: "metadata.creators.*.name"
      year: "metadata.publication_date"
      source_id: doi
```

**Query example:**
```sql
SELECT title, year, citations FROM s2_search
WHERE citations > 50 ORDER BY citations DESC
```

---

## Code Mining (Multi-Repo)

Fan-out across multiple repositories. Collectors run against every catalog entry.

```yaml
catalog:
  - name: tokio
    type: local
    url: /Users/dev/oss/tokio
  - name: tower
    type: local
    url: /Users/dev/oss/tower
  - name: hyper
    type: local
    url: /Users/dev/oss/hyper
  - name: axum
    type: local
    url: /Users/dev/oss/axum

collectors:
  - name: scars
    type: cli
    run: "rg --json -C3 'note that|SAFETY|INVARIANT|must not|never|critical|be careful' --type rust"
    normalize:
      file: "data.path.text"
      line: "data.line_number"
      content: "data.lines.text|$first"

  - name: oscillations
    type: cli
    run: "git log --oneline --all --grep=revert -n 50"

  - name: signatures
    type: cli
    run: "rg --json 'pub (fn|struct|trait|enum|type)' --type rust"
    normalize:
      file: "data.path.text"
      line: "data.line_number"
      content: "data.lines.text|$first"

  - name: unsafe-census
    type: cli
    run: "rg --json 'unsafe' --type rust --count-matches"
```

**Produces:** `scars-tokio.jsonl`, `scars-tower.jsonl`, `signatures-tokio.jsonl`, etc.

**Query example:**
```sql
SELECT file, line, content FROM scars_tokio
WHERE content LIKE '%SAFETY%'
```

---

## Code Mining (Single Repo)

Pin to a specific source when working with one repository.

```yaml
catalog:
  - name: project
    type: local
    url: /Users/dev/my-project

collectors:
  - name: todos
    type: cli
    source: project
    run: "rg --json 'TODO|FIXME|HACK|XXX' --type-add 'src:*.{rs,py,ts}' --type src"
    normalize:
      file: "data.path.text"
      line: "data.line_number"
      content: "data.lines.text|$first"

  - name: recent-changes
    type: cli
    source: project
    run: "git log --format='{\"hash\":\"%H\",\"author\":\"%an\",\"date\":\"%aI\",\"subject\":\"%s\"}' -n 100"

  - name: issues
    type: cli
    run: "gh issue list --repo owner/repo --json title,body,labels,state --limit 50"
    normalize:
      title: title
      body: body
      labels: "labels.*.name"
      state: state
```

---

## Forensic Code Analysis with code-maat

[code-maat](https://github.com/adamtornhill/code-maat) is Adam Tornhill's git-history analysis tool from *Your Code as a Crime Scene*. It surfaces hotspots (files changed most often), temporal coupling (files that change together), code age (time since last modification), knowledge distribution, and effort by author. These forensic signals are things static analyzers miss — they live in the history, not the code.

code-maat emits CSV. Recon consumes JSONL. A small python pipeline bridges the two. Each collector generates a per-run logfile, runs one analysis, and pipes the CSV through `csv.DictReader` → `json.dumps`.

**Install:** `brew install code-maat` (macOS) or download the standalone jar from the release page. The binary is `maat`.

**Pattern:**

```yaml
catalog:
  - name: tokio
    type: local
    url: /Users/dev/oss/tokio
  - name: hyper
    type: local
    url: /Users/dev/oss/hyper

collectors:
  # Hotspots — files with the most revisions (candidates for refactoring)
  - name: hotspots
    type: cli
    run: |
      LOG=$(mktemp)
      git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > "$LOG"
      maat -l "$LOG" -c git2 -a revisions | \
        python3 -c "import csv,json,sys; [print(json.dumps(r)) for r in csv.DictReader(sys.stdin)]"
      rm -f "$LOG"

  # Temporal coupling — files that tend to change in the same commit
  - name: coupling
    type: cli
    run: |
      LOG=$(mktemp)
      git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > "$LOG"
      maat -l "$LOG" -c git2 -a coupling | \
        python3 -c "import csv,json,sys; [print(json.dumps(r)) for r in csv.DictReader(sys.stdin)]"
      rm -f "$LOG"

  # Code age — days since last modification (identifies stable vs churning code)
  - name: age
    type: cli
    run: |
      LOG=$(mktemp)
      git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > "$LOG"
      maat -l "$LOG" -c git2 -a age | \
        python3 -c "import csv,json,sys; [print(json.dumps(r)) for r in csv.DictReader(sys.stdin)]"
      rm -f "$LOG"

  # Entity effort — who contributed what, as a percentage per file
  - name: entity-effort
    type: cli
    run: |
      LOG=$(mktemp)
      git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > "$LOG"
      maat -l "$LOG" -c git2 -a entity-effort | \
        python3 -c "import csv,json,sys; [print(json.dumps(r)) for r in csv.DictReader(sys.stdin)]"
      rm -f "$LOG"
```

**Query examples:**

```sql
-- Top 20 hotspots across tokio
SELECT entity, "n-revs" AS revisions
FROM hotspots_tokio
ORDER BY CAST("n-revs" AS INTEGER) DESC
LIMIT 20;
```

```sql
-- Strongly-coupled file pairs in hyper (high coupling degree + enough shared commits)
SELECT entity, coupled, degree, "average-revs"
FROM coupling_hyper
WHERE CAST(degree AS INTEGER) > 50
  AND CAST("average-revs" AS INTEGER) > 10
ORDER BY CAST(degree AS INTEGER) DESC;
```

```sql
-- Cross-repo hotspot comparison
SELECT 'tokio' AS repo, entity, "n-revs" FROM hotspots_tokio
UNION ALL
SELECT 'hyper', entity, "n-revs" FROM hotspots_hyper
ORDER BY CAST("n-revs" AS INTEGER) DESC
LIMIT 30;
```

**Available analyses** (pass to `-a`):

| Analysis | Reveals |
|----------|---------|
| `revisions` | Hotspots — files with highest change frequency |
| `coupling` | Temporal coupling — files that change together |
| `age` | Days since last modification per file |
| `entity-effort` | Author contribution percentage per file |
| `main-dev` | Primary contributor per file |
| `entity-ownership` | Added lines by author per file |
| `communication` | Developer communication needs from shared files |
| `abs-churn` | Absolute code churn per date |
| `author-churn` | Churn grouped by author |

**Why this is useful:** static analysis finds bugs and code smells in a single snapshot. code-maat finds the *social* and *historical* signals — where complexity has accumulated, what changes in lockstep, which modules are owned by one person, where knowledge silos have formed. These inform architectural decisions that static tools can't see.

---

## Content Tracking (Scheduled)

Monitor content sources on a recurring schedule. Two phases: set up the config once, then schedule the survey.

### Phase 1: Setup (one-time)

Create the mission config. Use the recon skill (`--skill recon`) to have Claude generate it:

```
claude --skill recon "Set up a weekly arxiv + S2 tracker for collaborative intelligence papers"
```

Claude writes `.cix/recon/arxiv-weekly/config.yaml`:

```yaml
catalog:
  - name: arxiv
    type: api
    url: https://export.arxiv.org/api

  - name: semantic-scholar
    type: api
    url: https://api.semanticscholar.org/graph/v1
    auth: { header: x-api-key, env: S2_API_KEY }
    rate_limit: { rps: 0.33, burst: 1 }

collectors:
  - name: arxiv-new
    type: api
    source: arxiv
    endpoint: /query
    params:
      search_query: "cat:cs.AI AND abs:collaborative+intelligence"
      sortBy: submittedDate
      sortOrder: descending
      max_results: "30"
    response_format: xml
    extract: "feed.entry"
    normalize:
      title: title
      abstract: summary
      authors: "author.*.name"
      published: published
      source_id: id

  - name: s2-citations
    type: api
    source: semantic-scholar
    endpoint: /paper/search
    params:
      query: "collaborative intelligence human-AI"
      limit: "20"
      fields: "title,abstract,year,authors,citationCount,openAccessPdf"
      sort: "citationCount:desc"
    extract: "data"
    normalize:
      title: title
      abstract: abstract
      authors: "authors.*.name"
      year: year
      citations: citationCount
      pdf_url: "openAccessPdf.url"
```

### Phase 2: Schedule (recurring)

The config exists. Now schedule a recurring survey — the scheduled agent runs recon and analyzes the diff:

```
/schedule create --cron "0 9 * * 1" --prompt "Run recon survey arxiv-weekly. Read the JSONL results. If a previous archive exists, compare and report: new papers, rising citations, anything relevant to collaborative intelligence. Write a summary to .cix/recon/arxiv-weekly/digest.md."
```

Every Monday at 9am, the scheduled agent:
1. Runs `recon survey arxiv-weekly` (config already exists)
2. Reads the new archive's JSONL files
3. Compares with the previous archive
4. Writes a digest

The config never changes — only the archives accumulate.

**Query across archives:**
```sql
SELECT title, published, authors FROM arxiv_new
WHERE published > '2026-03-25'
ORDER BY published DESC
```

---

## Release Monitoring

Track GitHub releases (or PyPI / crates.io / npm) for a set of dependencies. Recurring survey — diff across archives to surface new versions.

```yaml
catalog:
  - name: github
    type: api
    url: https://api.github.com
    auth:
      header: Authorization
      env: GITHUB_TOKEN
    rate_limit: { rps: 1, burst: 2 }
    user_agent: "recon/0.7.0 (release-monitor)"

collectors:
  - name: tokio-releases
    type: api
    source: github
    endpoint: /repos/tokio-rs/tokio/releases
    params:
      per_page: "10"
    normalize:
      tag: tag_name
      name: name
      published: published_at
      author: "author.login"
      prerelease: prerelease
      url: html_url

  - name: serde-releases
    type: api
    source: github
    endpoint: /repos/serde-rs/serde/releases
    params:
      per_page: "10"
    normalize:
      tag: tag_name
      published: published_at
      author: "author.login"
      url: html_url
```

**PyPI variant** — use the web collector since PyPI's public API is JSON-over-HTTPS at well-known URLs:

```yaml
catalog:
  - name: pypi
    type: api
    url: https://pypi.org/pypi

collectors:
  - name: pydantic-releases
    type: api
    source: pypi
    endpoint: /pydantic/json
    extract: "releases"
    # Raw releases is a dict keyed by version — inspect with probe first,
    # then write a normalize spec that extracts version keys + metadata.
```

---

## RSS / Blog Tracking

Track a set of blogs or RSS feeds via the web collector. The web collector emits uniform records (`url`, `title`, `content`, `status_code`, `content_type`); feed items get parsed from the content field.

```yaml
catalog:
  - name: overreacted
    type: web
    url: https://overreacted.io
    rate_limit: { rps: 1, burst: 1 }

  - name: simonwillison
    type: web
    url: https://simonwillison.net
    rate_limit: { rps: 1, burst: 1 }

collectors:
  # Fetch the index page for each blog
  - name: index
    type: web
    # no source: → fans out across both blogs
```

**Produces:** `index-overreacted.jsonl`, `index-simonwillison.jsonl`, each with the markdown-converted homepage. Claude extracts post titles and dates from the `content` field by reading the JSONL.

For actual RSS/Atom feeds, treat them as `response_format: xml` API collectors and use `extract: "rss.channel.item"` or `extract: "feed.entry"`.

---

## Dependency Audits

Inspect installed dependencies across a codebase using native package manager CLIs. Pins to a single local source.

```yaml
catalog:
  - name: project
    type: local
    url: /Users/dev/my-project

collectors:
  - name: cargo-tree
    type: cli
    source: project
    run: "cargo tree --format '{p} {f}' --prefix none"
    # text output — one line per dependency

  - name: npm-outdated
    type: cli
    source: project
    run: "npm outdated --json || true"    # npm returns exit 1 when updates exist
    # JSON output — object keyed by package name

  - name: uv-tree
    type: cli
    source: project
    run: "uv tree --depth 1"

  - name: python-audit
    type: cli
    source: project
    run: "uv run pip-audit --format=json || true"
    # Vulnerability audit — JSON list of findings
```

**Query example:**
```sql
SELECT * FROM python_audit WHERE vulns IS NOT NULL
```

---

## Doc Site Survey

Scrape a documentation site section by section via the web collector. Useful for building a structured index of a docs tree.

```yaml
catalog:
  - name: svelte-docs
    type: web
    url: https://svelte.dev
    rate_limit: { rps: 1, burst: 1 }

collectors:
  - name: docs-intro
    type: web
    source: svelte-docs
    endpoint: /docs/svelte/overview

  - name: docs-runes
    type: web
    source: svelte-docs
    endpoint: /docs/svelte/what-are-runes

  - name: docs-state
    type: web
    source: svelte-docs
    endpoint: /docs/svelte/$state

  # ...one collector per docs page to fetch
```

Each collector produces one record per page with markdown content. Claude can then SQL-query for specific topics or diff across time to catch doc changes.

For bulk crawls (dozens of pages), prefer generating the config programmatically from a sitemap, or use a sitemap-based collector chain.

---

## Issue Triage Across Repos

Pull open issues from multiple GitHub repos for triage review. Uses `gh` CLI via the cli collector — inherits the user's gh auth automatically.

```yaml
catalog:
  - name: repo-a
    type: local
    url: /tmp                 # cwd is irrelevant here; gh uses its own auth

collectors:
  - name: issues-tokio
    type: cli
    source: repo-a
    run: "gh issue list --repo tokio-rs/tokio --state open --json number,title,labels,createdAt,author --limit 50"
    normalize:
      number: number
      title: title
      labels: "labels.*.name"
      created: createdAt
      author: "author.login"

  - name: issues-axum
    type: cli
    source: repo-a
    run: "gh issue list --repo tokio-rs/axum --state open --json number,title,labels,createdAt,author --limit 50"
    normalize:
      number: number
      title: title
      labels: "labels.*.name"
      created: createdAt
      author: "author.login"

  - name: prs-review-requested
    type: cli
    source: repo-a
    run: "gh search prs --review-requested=@me --state=open --json number,title,repository,url --limit 30"
    normalize:
      number: number
      title: title
      repo: "repository.nameWithOwner"
      url: url
```

**Cross-repo query:**
```sql
SELECT 'tokio' AS repo, title FROM issues_tokio WHERE 'bug' = ANY(labels)
UNION ALL
SELECT 'axum', title FROM issues_axum WHERE 'bug' = ANY(labels)
```
