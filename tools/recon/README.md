# recon

> Heterogeneous sources in, structured data out. Claude queries the result.

Recon fetches from HTTP APIs, runs CLI tools, and scrapes web pages, then reshapes every response into uniform JSONL that Claude can query with SQL. The reshape is declarative, not code. Write a YAML config once; recon runs it mechanically — no LLM in the loop.

## Why

Claude reasons well but spends inference cycles badly when asked to babysit HTTP. Parsing JSON, retrying 429s, normalizing nested fields, handling pagination math — all of it is mechanical work that costs the same inference budget as actual reasoning. Recon takes that off Claude's critical path.

What's left for Claude is the work only Claude can do: deciding what matters, spotting patterns across sources, connecting findings that nobody wrote down as findings.

A recon archive with 5,000 records is queryable without loading 5,000 records into Claude's prompt. That's the deeper capability: **recon extends Claude's effective context through structured indirection**. The data lives in a file Claude can ask questions of, not in the prompt.

For the full argument, see [docs/explanation/capability.md](docs/explanation/capability.md).

## Install

```bash
uv tool install --editable tools/recon
```

Verify:

```bash
recon --version
```

Claude loads the skill on demand via `recon --skill` — no plugin registration needed. The tool ships its own documentation.

## Quick start

```bash
# Scaffold a mission from a built-in template
recon init papers --template research

# Edit the config to point at real queries (the template has placeholders)
$EDITOR .cix/recon/papers/config.yaml

# Run — archives land under .cix/recon/papers/archive/<timestamp>/
recon survey papers

# Query the result with SQL (DuckDB reads JSONL natively)
recon query papers "SELECT title, year FROM s2_search ORDER BY year DESC LIMIT 10"
```

For an end-to-end walkthrough of the probe → normalize → survey workflow against a non-academic task, see [docs/how-to/first-survey.md](docs/how-to/first-survey.md).

## Domains

Recon is general-purpose. The built-in `research` template is one instance. Common uses across domains:

| Domain | What the config collects |
|---|---|
| Code mining | `rg`, `git log`, `gh api` across multiple repos via fan-out |
| Release monitoring | GitHub releases, PyPI, crates.io, npm |
| Dependency audits | `cargo tree`, `npm ls`, `pip-audit` |
| Literature review | Semantic Scholar, arXiv, OpenAlex, Zenodo |
| Competitive analysis | Product pages, pricing, changelogs (web collector) |
| Doc site survey | Scrape docs trees, extract structure |
| Issue triage | `gh issue list` across repos with labels |
| API state snapshots | Any REST endpoint captured periodically |
| Content tracking | RSS feeds, blog indices, changelog pages |

The common shape: *something out there has data in some response format, and Claude needs to reason over it as structured records.* Recon bridges that.

## Commands

```
recon init <mission> --template <name>    scaffold from a built-in template
recon survey <mission>                    run the collection
recon status                              list missions and their archives
recon query <mission> "SQL"               DuckDB query against the latest archive
recon templates                           list built-in templates
recon --skill                             print recon's skill (for Claude to load)
recon --skill -r <reference>              load a specific reference file
```

## What recon is not

- **Not an agent.** Recon doesn't use an LLM during execution. It runs the config you wrote. Intelligence lives outside the tool.
- **Not a research autopilot.** Tools like gpt-researcher try to autonomously produce finished reports from a single prompt. Recon produces structured data; synthesis stays with Claude and with the human.
- **Not a stream processor.** Each run produces a timestamped snapshot. Recon does one-shot collection, not pub/sub.

## Design

Hexagonal architecture. Pure domain models (Pydantic, frozen). One port: `Collector`. Three adapters: `api`, `cli`, `web`. Composition root in `adapters/_in/cli.py` wires them. Transforms (including `$pdf2text`, `$inverted_index`, `$html2text`) are declarative pipe syntax applied after path resolution via [glom](https://glom.readthedocs.io/).

Ninety tests covering domain, application, adapters, and live integration against OpenAlex, arXiv, Semantic Scholar, and Zenodo.

## Docs

- [docs/explanation/capability.md](docs/explanation/capability.md) — what recon does for Claude and why
- [docs/how-to/first-survey.md](docs/how-to/first-survey.md) — concrete first-mission walkthrough
- `recon --skill` — the full skill Claude uses to author configs (authoritative)
- `recon --skill -r config-patterns` — nine domain patterns with complete configs
- `recon --skill -r normalize-spec` — normalize spec syntax, path resolution, transforms

## License

MIT
