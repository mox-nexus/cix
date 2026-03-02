---
name: synthesize-papers
description: "DEPRECATED — Use the `research` hub skill instead. Load `craft-research:research` for the full pipeline with agents (elicit, scrutiny, synthesis, audit). This skill's content has been redistributed: Claimify → extracting skill, evidence weighting → synthesizing skill, gap analysis → synthesizing skill."
---

# Synthesize Papers (Deprecated)

This skill has been superseded by the craft-research v0.2.0 pipeline.

## What Changed

The monolithic synthesize-papers skill has been decomposed into a hub + spoke architecture with 4 agents:

| Old Content | New Location |
|-------------|-------------|
| Claimify pipeline | `extracting` skill + `elicit` agent |
| Dual-LLM cross-critique | `extracting` skill (reference: claimify.md) |
| Evidence weighting | `synthesizing` skill + `synthesis` agent |
| Gap analysis (4 layers) | `synthesizing` skill |
| Plan-based synthesis | `synthesizing` skill |
| Position bias mitigation | `extracting` skill + `synthesizing` skill |

## How to Use the New Pipeline

Load the hub skill: `craft-research:research`

The pipeline: scope (human) → extract (elicit) → verify (scrutiny) → synthesize (synthesis) → audit (audit).

## References

The original reference material is preserved at `references/paper-synthesis.md` for historical context.
