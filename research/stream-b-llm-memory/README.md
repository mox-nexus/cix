# Stream B — LLMs and Memory Structurally

**Status:** SHIP (verified Round 1 + Round 2 cross-model)

## Research questions

B1 (mechanism), B2 (failure modes), B3 (post-training memory), B4 (augmentation), B-bridge (substrate parallels with Stream A)

## Corpus

- **10 papers extracted (mostly abstract-only)**
- **44 total atomic claims**

## Verification

Round 1: 15 load-bearing (14 V, 1 C, 0 R). Round 2: 19 synthesis-cited (17 V, 2 C, 0 R, 0 I, all verbatim).

Round 1 used Claude (same model as extraction) for CoVE. Round 2 used Gemini for genuine cross-model independence. No claims refuted across either round.

## Layout

```
stream-b-llm-memory/
├── README.md             this file
├── scope.md              research questions, null hypotheses, source-landscape priors
├── data/                 raw recon sweep outputs (OpenAlex / S2 JSONL)
├── sources/              consolidated source material
│   ├── inventory.md      what was collected and why
│   └── full-text/        full-text papers (where available; per-paper .md)
├── extractions/          per-paper Claimify output (atomic claim + verbatim quote per claim)
├── verification/         CoVE artifacts
│   ├── load-bearing-claims.md       Round 1 (Claude, selective load-bearing claims)
│   ├── cove-gemini-round-2.jsonl    Round 2 (Gemini, all unverified synthesis-cited)
│   └── unverified-cited.txt         claim manifest used for Round 2
├── synthesis/
│   └── findings.md       cross-source integration + architectural implications
└── audit/
    └── provenance-audit.md          chain integrity check + ship verdict
```

## Reading paths

- **Just want the design implications?** → `synthesis/findings.md` "Architectural Implications" sections
- **Want to verify a specific claim?** → search `extractions/*.md` for `:cN` where N is the claim number; cross-check `verification/cove-gemini-round-2.jsonl`
- **Want to see what was discarded vs kept?** → `data/` (raw sweeps) and stream-specific triage files (`extraction-targets.{md,json}`, `triage.md`)
