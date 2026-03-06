# craft-research

Systematic research with evidentiary provenance. Every claim traces to a source quote, through discourse, extraction, verification, and synthesis.

## When to Use

- Scoping research questions and identifying sources
- Extracting atomic claims from academic papers
- Verifying citations and claims against sources
- Synthesizing findings across multiple papers
- Literature review with traceable provenance
- Research gap analysis (theoretical, methodological, empirical, practical)
- Quality audit of research outputs

## Pipeline

```
discourse (elicit) → extract (extract) → verify (scrutiny) → synthesize (synthesis) → audit (audit)
```

Elicit draws out the inquiry. Agents execute the methodology. Human reviews and decides.

## Agents

| Agent | Role | Phase |
|-------|------|-------|
| **elicit** | Draw out research questions, boundaries, sources | Discourse |
| **extract** | Extract atomic claims from sources (Claimify pipeline) | Extraction |
| **scrutiny** | CoVE verification — independently verify claims | Verification |
| **synthesis** | Cross-source integration, convergence/divergence/gaps | Synthesis |
| **audit** | Quality gate — trace provenance chain, ship/return | Audit |

## Skills

| Skill | Type | Content |
|-------|------|---------|
| **research** | Hub | Pipeline, workspace, orchestration, routing |
| **eliciting** | Spoke | Research discourse, question sharpening, source identification |
| **extracting** | Spoke | Claimify pipeline, source tiers, extraction protocol |
| **verifying** | Spoke | CoVE protocol, verification verdicts, independence |
| **synthesizing** | Spoke | Evidence weighting, convergence/divergence, gap analysis |
| **auditing** | Spoke | Provenance chain, chain integrity, ship/return |

## Workspace

```
.research/
├── scope.md              # Co-created (elicit + human): questions, boundaries
├── PLAN.md               # Orchestrator tracking
├── sources/inventory.md  # Co-created (elicit + human): source list with metadata
├── extraction/           # Per-source claim files
├── verification/         # Per-source verified claims
├── synthesis/            # Per-question findings
└── audit/report.md       # Evaluation report
```

## The Provenance Chain

```
Source quote (verbatim) → Extracted claim → Verified claim → Finding → Audit trace
```

Confidence can only decrease through the pipeline — never increase without new evidence.

## Key Principles

- **Discourse first** — draw out the inquiry before any pipeline work
- **Evidentiary provenance** — every claim traceable to a source quote
- **Independence** — verification re-reads sources independently (CoVE)
- **Structural confidence** — evidence patterns determine confidence, not assertions
- **Named gaps** — what's missing is as important as what's found
- **Human scoping** — no agent substitutes for defining what questions matter

## License

MIT
