# radix

> Mine the *why* behind expert engineering — what public datasets miss.

Latin *radix* — root. Point radix at a codebase, a collection, or a domain, and it runs an iterative, multi-session extraction workflow that produces a typed JSONL corpus capturing stewardship-tacit knowledge: oscillations (why the code changed), battle scars (why this code is correct despite looking dangerous), and signature recurrences (why this exact shape converges across elite codebases).

Each row preserves its **surface** (verbatim source quote with addressable location) and a **canonical** projection per mode. The surface is the provenance anchor; the canonical is what downstream tools query against.

## The thesis

Public training datasets — TheStack, BigCode, language-specific curated corpora, official docs in pretraining — cover the *what* layer of any well-documented language. A model trained on them knows journeyman-level idioms, syntax, common patterns, standard-library usage.

What public datasets miss is the *why*:

- Why the code changed (failure modes encoded in revert messages — static snapshots only have the settle)
- Why this code is correct despite looking dangerous (cross-references between battle-scar comments and the invariants they protect)
- Why this exact shape recurs across elite codebases (cross-codebase aggregation, not single-source signatures)
- Why an RFC's rejected alternatives were rejected (deliberation, not the accepted RFC)

That gap **is** stewardship-tacit expertise. radix mines it.

## What's in this plugin

```
plugins/radix/
├── README.md                                    # this file
├── docs/                                        # human-oriented design rationale
│   ├── why-radix.md                             # cog-sci backbone (Brooks/Letovsky/Soloway-Ehrlich/Pennington/Burkhardt + Falessi 2013)
│   └── composition-with-cix-stack.md            # when/how to chain with other cix tools
└── skills/radix/
    ├── SKILL.md                                 # operational workflow (Claude reads this)
    └── references/
        ├── dataset-selection.md                 # pick single / collection / domain; identify elite repos
        ├── tools.md                             # locator tools (git, rg, gh, ast-grep, code-maat, ...) + per-mode tool fit
        ├── mining-recipes.md                    # commands per mode and per artifact source
        ├── table-shapes.md                      # per-mode canonical row shape + exemplars
        ├── journeyman-filter.md                 # discipline for skipping public-dataset content
        └── exemplars/
            ├── rust.md                          # worked example: curated starter list for elite Rust
            └── python.md                        # worked example: curated starter list for Python data/ML
```

The split is deliberate:
- **`skills/radix/`** is operational, lean, written for Claude. Imperative form, decision rules, recipes.
- **`docs/`** is rationale, written for humans evaluating *why* the skill is shaped this way. Literature anchors, design context, future-runtime considerations.

## When to use

- "Mine this codebase / these repos / this domain for expert knowledge"
- "Extract stewardship-tacit knowledge from \<X\>"
- "Capture the design rationale public datasets miss"
- "Set up multi-session expert-mining for \<domain\>"
- "Find what's invariant across these maintainers"

The skill works with three dataset modes:

- **Single** — one repo (just clone and mine)
- **Collection** — list of repos (mine each, synthesize across)
- **Domain** — Claude identifies the elite repos for the domain, vets with the user, then proceeds as collection

Pair with `craft-research` if your domain mixes papers + datasets + repos and you need verified-claim discipline.

## How to use

The skill drives a five-phase workflow:

1. **Workspace setup** — persistent, multi-session, outside the plugin
2. **Dataset selection + plan** — pick mode, pick mining modes, set success criteria
3. **Per-source extraction** — clone (commit-pinned) → reconnaissance → one-mode-per-pass extraction → STATUS update
4. **Cross-source synthesis** — rule of three (≥3 sources = candidate principle); cross-paradigm is gold
5. **Stop and archive** — when success criteria met, not when sources run out

The first-class deliverable is the **typed JSONL corpus** in the workspace. Eval suites and training triples are derived products built *from* the corpus separately — not part of v0.1.

## Status

**v0.3.2** — language-and-domain-agnostic workflow skill. Eight mining modes across two phases:
- **Extraction** (Phase 3c, per-row): `oscillations`, `scars`, `signatures`, `schemas`
- **Synthesis** (Phase 4, cross-row): `models` (program-model + domain-model), `tradeoffs`, `antipatterns`, `aesthetics`
- **Principles** are not a separate mode — they're a promotion criterion (rule of three across synthesis-mode rows)

Output format (JSONL with verbatim surface + canonical projection + lineage) is stable; the row shapes in `skills/radix/references/table-shapes.md` are the contract.

## Install

Part of the cix marketplace.

## License

MIT
