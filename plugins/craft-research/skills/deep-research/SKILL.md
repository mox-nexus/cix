---
name: deep-research
description: "DEPRECATED — Use the `research` hub skill instead. Load `craft-research:research` for the full pipeline with agents (elicit, scrutiny, synthesis, audit). This skill's content has been redistributed: CoVE → verifying skill, source tiers → extracting skill, research instrument → research hub skill."
---

# Deep Research (Deprecated)

This skill has been superseded by the craft-research v0.2.0 pipeline.

## What Changed

The monolithic deep-research skill has been decomposed into a hub + spoke architecture with 4 agents:

| Old Content | New Location |
|-------------|-------------|
| CoVE protocol | `verifying` skill + `scrutiny` agent |
| Source hierarchy / tiers | `extracting` skill + `elicit` agent |
| Research instrument | `research` hub skill |
| Multi-agent workflow | `research` hub skill (orchestration protocol) |
| Verification protocol | `verifying` skill |
| Structured output schema | `synthesizing` skill + `synthesis` agent |

## How to Use the New Pipeline

Load the hub skill: `craft-research:research`

The pipeline: scope (human) → extract (elicit) → verify (scrutiny) → synthesize (synthesis) → audit (audit).

## References

The original reference material is preserved at `references/deep-research.md` for historical context.
