# Config Patterns

Complete config examples for common recon use cases. Copy, adapt, write to `.cix/recon/<mission>/config.yaml`.

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
