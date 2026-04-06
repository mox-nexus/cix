---
name: collecting
description: "This skill should be used when the user asks to 'collect sources for research', 'find papers on a topic', 'set up source collection', 'build a recon config from my research scope', or needs to bridge a research scope into mechanical source collection via recon."
version: 0.1.0
---

# Collecting

> Turn the source inventory into structured data Claude can reason over.

Collecting bridges eliciting and extracting. Eliciting produces `scope.md` and `sources/inventory.md` — what to research and where to look. Extracting reads source material and pulls atomic claims. Between them, something has to fetch the actual data. That's this step.

The orchestrator (main Claude) runs this step directly — no subagent. The work is mechanical: translate the inventory into a recon config, run the survey, stage the results for extraction.

## Contents

- [When to Collect](#when-to-collect)
- [The Bridge Pattern](#the-bridge-pattern)
- [Translating Inventory to Config](#translating-inventory-to-config)
- [After Collection](#after-collection)
- [When to Skip](#when-to-skip)

## When to Collect

Collect whenever sources need to be fetched OR structured. Recon handles remote and local sources equally:

| Source state | Recon approach |
|---|---|
| Named in inventory, not yet retrieved | API or web collectors fetch from remote |
| PDFs on disk | Local source + CLI collector with `$pdf2text` transform |
| Cloned repositories | Local source + CLI collectors (`rg`, `git log`, `ast-grep`) with fan-out |
| Mix of remote and local | Both source types in the same config |

**Skip only when** the source count is trivially small (1-2 files) and Claude can read them directly faster than writing a config.

## The Bridge Pattern

```
sources/inventory.md (from eliciting)
  ↓
Orchestrator reads inventory, identifies what needs fetching
  ↓
Orchestrator writes recon config to .research/recon/config.yaml
  ↓
`recon survey <mission>`
  ↓
JSONL results land at .cix/recon/<mission>/archive/<timestamp>/
  ↓
Orchestrator reads JSONL, stages source material for extraction
```

The recon skill has the full config syntax, normalize spec reference, and domain-specific patterns. Load it with `recon --skill` before writing configs. Probe before writing normalize specs — see [Probe Before Survey](recon --skill) for the iterative workflow.

## Translating Inventory to Config

`sources/inventory.md` from eliciting has source metadata: names, URLs, types, search terms, tier estimates. Translate each entry into recon config components:

**For academic sources** (papers, preprints):

| Inventory entry | Recon config |
|---|---|
| "Search Semantic Scholar for X" | API collector: S2 `/paper/search` endpoint |
| "Search arXiv for X" | API collector: arXiv `/query` endpoint (XML) |
| "Check OpenAlex for X" | API collector: OpenAlex `/works` endpoint |
| "Search Zenodo for datasets" | API collector: Zenodo `/records` endpoint |

Use the built-in research template as a starting point: `recon init <mission> --template research`. Replace the `{query}` and `{limit}` placeholders with actual values from the inventory.

**For code sources** (repositories, codebases):

| Inventory entry | Recon config |
|---|---|
| "Survey patterns in repo X" | Local source + CLI collector (`rg`, `git log`) |
| "Check GitHub issues for X" | CLI collector (`gh issue list`) |
| "Compare across repos A, B, C" | Multiple local sources, fan-out |

**For web sources** (docs, blogs, reports):

| Inventory entry | Recon config |
|---|---|
| "Read the methodology page at URL" | Web source + web collector |
| "Monitor blog X" | Web source + web collector |

Always use the probe-then-survey workflow: start with `limit: "1"`, inspect raw JSONL, write the normalize spec from the actual response, then scale up. Load `recon --skill` for full syntax.

## After Collection

Once recon completes:

1. **Read `meta.yaml`** — check which collectors succeeded and which failed. Failed collectors get error messages with specifics (429, timeout, missing source).

2. **Read the JSONL** — the normalized records are the source material for extraction. For each source, confirm the records have usable content (title, abstract, authors populated; not truncated or empty).

3. **Stage for extraction** — extraction agents read source material. For papers, the JSONL provides metadata (title, abstract, authors, year) and sometimes `pdf_url`. If PDFs are needed for full-text extraction, download them separately.

4. **Update PLAN.md** — record which sources were collected, how many records, any failures. The extraction step needs to know what's available.

**Gate: collection → extraction**
- [ ] Recon survey completed (check meta.yaml)
- [ ] Normalized JSONL readable with expected columns
- [ ] Failed collectors identified and handled (retry, alternate source, or mark as unavailable)
- [ ] PLAN.md updated with collection results

## When to Skip

Skip collection only when the setup cost exceeds the benefit:

| Situation | Action |
|---|---|
| 1-2 files Claude can read directly | Skip — direct read is faster |
| Everything else | Collect — even local files benefit from structured output + SQL queries |

Recon's value is proportional to source count, heterogeneity, and repeatability. PDFs on disk, cloned repos, and remote APIs all benefit from the same pipeline: recon normalizes them into one schema, DuckDB queries across them.

## What Collecting Does Not Do

- **Decide what to search for.** That's eliciting — scope.md has the questions, inventory.md has the sources.
- **Read or comprehend source material.** That's extraction — the Claimify pipeline.
- **Verify claims.** That's scrutiny — CoVE protocol.
- **Produce finished research.** It produces structured data for the pipeline to consume.

Collecting is mechanical. Intelligence stays in the surrounding steps.
