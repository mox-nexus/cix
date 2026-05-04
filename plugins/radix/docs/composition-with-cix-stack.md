# Composition with downstream consumers

This document is for humans deciding when to chain radix output into other tools. The skill itself works standalone; this is wider-pipeline context.

## What radix produces

Typed JSONL files in a workspace `extracts/` directory, plus markdown synthesis in `synthesis/`:

```
<workspace>/extracts/
├── <source>.oscillations.jsonl
├── <source>.scars.jsonl
├── <source>.signatures.jsonl
├── <source>.schemas.jsonl
└── ...
<workspace>/synthesis/
├── models.jsonl       (cross-source: program-model + domain-model artifacts)
├── tradeoffs.jsonl    (cross-source: decisions with alternatives + rationale)
├── antipatterns.jsonl (cross-source: looks-reasonable-fails)
├── aesthetics.jsonl   (cross-source: what "right" feels like)
├── principles.md      (rule-of-three promotion across synthesis modes)
├── divergences.md     (where elite sources disagree)
└── SUMMARY.md
```

Each row is `{surface, canonical, lineage}` with the canonical projection per mode (see `skills/radix/references/table-shapes.md`).

## Standalone usage

Most of the time, the workspace IS the product. Query it with `jq`, `rg`, or DuckDB-over-JSONL:

```bash
# Top recurring patterns by source count
cd <workspace>/extracts/
cat *.signatures.jsonl | jq -r '.canonical.signature_text' | sort | uniq -c | sort -rn | head -20

# Tradeoffs about a specific topic
jq -c 'select(.canonical.context // "" | test("async"; "i"))' <workspace>/synthesis/tradeoffs.jsonl

# DuckDB across all extracts
duckdb <<EOF
CREATE TABLE rows AS SELECT * FROM read_json_auto('extracts/*.jsonl', maximum_object_size=1048576);
SELECT lineage->>'$.source' AS source, COUNT(*) AS rows FROM rows GROUP BY source;
EOF
```

The synthesis files (`principles.md`, `divergences.md`, `SUMMARY.md`) are markdown — read them directly.

## Pairing with research-pipeline tools

If your domain mixes papers + datasets + repos and you need verified-claim discipline (CoVE-style verification), pair radix with a paper-side research-pipeline skill (in cix: `craft-research`):

- Paper-side: scope → collect → extract → verify → synthesize → audit (paper-shaped sources, prose claims, verified provenance).
- Repo-side: workspace → plan → per-repo extraction → synthesis (this skill).
- Cross-reference manually: when a paper-side claim and a repo-side pattern align, you have triangulation.

The two skills share row conventions (verbatim surface, lineage with `extracted_at` + `extracted_by`) so cross-reference is mechanical.

## Trust handoff to downstream consumers

radix produces a corpus from untrusted input. If you chain the corpus into:

- **Training pipelines** (fine-tuning data construction)
- **Eval generators** (probe-suite construction)
- **Skill builders** (deployable skill construction)

…those downstream consumers inherit the trust burden. The corpus contains verbatim surfaces from arbitrary repos. **Sanitize before training, before eval-suite generation, before skill compilation.** The threat-model guards in `skills/radix/SKILL.md` (Threat model and guards section) cover the mining surface; downstream tools need their own sanitization for *their* surface.

`session_log.jsonl` and `STATUS.md` log every repo URL/path touched plus mined commit messages verbatim — treat as private-by-default; don't share as artifacts without scrub.

## When NOT to chain

Most users want the knowledge artifacts, not the full pipeline. Don't reflexively chain to training / eval / skill builders just because the chain exists. Stop at the workspace if:

- You're exploring a domain to understand it.
- You're writing a doc / talk / blog post backed by mined evidence.
- You want to feed claims into a downstream tool you already have (e.g., your own RAG store).

Chain further only when a downstream consumer's value justifies the additional pipeline cost.

## Pointers

Sibling tools and plugins in the cix ecosystem (consult your cix installation for current versions and locations):

- **Heterogeneous-source ingestion** — for sources beyond git repos (HTTP APIs, CLI tools, web scrapes, paper databases): pair with `recon`.
- **Paper-side research workflow** — for prose-shaped sources with claim-extraction discipline: pair with `craft-research`.
- **Experiment / eval framework** — for testing model behavior against probe suites: see `ix`.
- **Component / orchestration substrate** — for multi-tool pipelines as DAGs: see `matrix`.
