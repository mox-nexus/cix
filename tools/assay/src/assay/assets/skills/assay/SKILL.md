---
name: assay
description: "This skill should be used when the user asks to 'verify these claims', 'cross-check this against the source', 'verify with multiple voices', 'triangulate this claim', 'fact-check this against the primary source', 'check if this is hallucinated', 'set up an inquiry', 'scaffold a verification mission', 'what do other models say about this finding', 'run cross-family verification', 'verify with gemini and claude', 'use local mlx for verification', 'validate this finding against source', 'run a verification round', 'run an assay', 'assay verify', 'assay init', 'cross-family triangulation', 'CoVE verification', 'Chain-of-Verification', 'check for hallucinations across models', or needs to test AI-generated claims against primary sources using independent verification voices from different model families."
version: 0.1.0
---

# Assay

**Assay is the cross-family verification harness.** Independent voices from different model families test claims against primary sources, reconciled into convergent or divergent verdicts. Where a single-family evaluator (six Claude personas reviewing Claude's answer) shares training-set blind spots, three voices from different architectures (Claude, Gemini, local MLX-Qwen) surface disagreements that single-family review correlates away.

Assay sits between [recon](https://github.com/mox-nexus/cix/tree/main/tools/recon) (mechanical collection) and synthesis tools in the cix toolchain. Recon brings primary data in. Synthesis turns it into explained claims. Assay tests whether those claims actually hold against the primary sources before they ship.

## The Capability

Three verification mechanisms compose at maturity; one ships in Phase 1:

1. **cross_family** (Phase 1) — independent LLM voices read the same claim against the same source; their verdicts converge or split. Convergence = warranted. Divergence = the diagnostic.
2. **trace_budget** (Phase 3) — logprob-based check that the cited span actually conditioned the answer (vs. paraphrased from training memory).
3. **semantic_entropy** (Phase 3) — per-claim continuous uncertainty score on hidden states.
4. **debate** (Phase 3) — multi-round adversarial critique across voices.
5. **linguistic** (Phase 3) — deterministic NLP checks: verb fidelity, hedge detection, numeric normalization, citation-span alignment.

The Mechanism port is the seam that admits new mechanism families without domain change.

## Mental Model

- A **Claim** is a verifiable assertion bound to a **PrimarySource** (with chain-of-custody attestation).
- A **Mechanism** is one verification approach.
- A **MechanismResult** is one mechanism's reading on one claim — `verdict` plus opaque mechanism-specific evidence.
- An **Adjudication** reconciles all MechanismResults for one claim into a final Verdict.
- An **Inquiry** is the YAML-driven verification mission.

## Workflow

```
List templates    →    Scaffold inquiry   →    Validate    →    Verify    →    Query
assay templates        assay init             assay validate    assay verify    assay query
```

1. **List** built-in inquiry templates with `assay templates`.
2. **Scaffold** an inquiry from a template into `.cix/assay/<inquiry>/inquiry.yaml`.
3. **Edit** the inquiry — set `claims_path`, configure voice backends, choose CoVE depth.
4. **Validate** before running — schema check, voice backend reachability, claim source existence.
5. **Verify** — runs all configured mechanisms across all claims, persists verdicts.
6. **Query** results via DuckDB SQL through `assay query <inquiry> "<sql>"`.

## CoVE Depths

The `cross_family` mechanism dispatches to one of three Chain-of-Verification depths per Dhuliawala 2023 ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)). Each names what the voice is allowed to see — independence is the mechanism, and depth controls independence.

| Depth | Voice sees | Catches | Use when |
|---|---|---|---|
| `anchored` | Claim + source | Transcription errors only | Spot-checking large fact tables |
| `reextract` | Source + question; compares to claim | Transcription + selection-bias | Default for value-bearing claims |
| `blind` | Source + question only — no claim, no expected value | Transcription + selection + framing errors | Executive-summary statements; "things to note" sentences; claims where framing matters |

Default is `reextract`. Use `blind` for high-stakes claims where framing-blindness matters most.

For full depth semantics with worked examples, see `references/cove-depths.md`.

## Voice Backends (Phase 1)

Three backends ship with the cross-family mechanism. Configure each voice in the inquiry YAML under `mechanisms[0].config.voices`:

| Backend | Setup | Notes |
|---|---|---|
| `anthropic` | Set `ANTHROPIC_API_KEY` env var | Claude family; calls REST API directly via httpx |
| `gemini-cli` | Install `gemini` CLI; oauth in `~/.gemini/` | Gemini family; subprocess wrapping headless mode |
| `mlx-server` | Run `mlx_lm.server --model <repo> --port 8080` separately | Local MLX inference; OpenAI-compatible HTTP; recommended model `unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit` on Apple Silicon |

For per-backend setup detail (auth, env vars, server startup), see `references/voice-backends.md`.

## CLI Commands

```
assay templates                          # list built-in inquiry templates
assay init <inquiry> --template <name>   # scaffold inquiry config
assay validate <inquiry>                 # pre-flight schema + reachability
assay verify <inquiry> [--claim <id>]    # run inquiry; --claim for single-claim debug
assay query <inquiry> "<sql>"            # DuckDB query against the latest run
assay show <inquiry> <claim-id>          # per-mechanism breakdown for one claim
assay status                             # list inquiries + runs
assay --skill                            # print this skill description
assay --skill -r <name>                  # print a reference file (see list below)
assay --version                          # version
```

For the full inquiry YAML schema, see `references/inquiry-config-schema.md`.

## Inquiry Layout

Each inquiry lives at `.cix/assay/<name>/`:

```
.cix/assay/<inquiry>/
  inquiry.yaml                            # mission spec
  run-<UTC-timestamp>/
    mechanism_results.jsonl               # one record per (claim, mechanism)
    adjudications.jsonl                   # one record per claim
```

Both JSONL files are queryable via `assay query <inquiry> "<sql>"`. The DuckDB store registers them as views named `mechanism_results` and `adjudications`.

## Common Queries

```sql
-- All divergent claims (where mechanisms disagreed)
SELECT claim_id, final_verdict FROM adjudications WHERE diverged

-- Per-mechanism summary
SELECT mechanism, verdict, COUNT(*) FROM mechanism_results GROUP BY mechanism, verdict

-- Slowest claims
SELECT claim_id, mechanism, elapsed_seconds FROM mechanism_results ORDER BY elapsed_seconds DESC LIMIT 10

-- Specific claim breakdown
SELECT * FROM mechanism_results WHERE claim_id = 'F003-cap-rate-FY2025'
```

## Claim JSONL Format

One Claim per line. The minimum fields are `id`, `statement`, and `source`:

```jsonl
{"id": "F003-cap-rate-FY2025", "statement": "EXPE FY2025 SBC capitalization rate is 19.9%", "expected_value": "19.9%", "question": "What is the SBC capitalization rate for FY2025?", "source": {"id": "10-K 0001324424-26-000008 Note 9", "accession": "0001324424-26-000008", "section": "Note 9", "excerpt": "We capitalized $99 million of stock-based compensation expense ..."}}
```

A working example claim file is at `examples/forensic-claim.jsonl`.

## Mechanism Roadmap

Phase 1 ships only `cross_family`. Phase 3 adds four more mechanism families that slot into the same Mechanism port without domain change. For the full roadmap with per-mechanism rationale and integration sketch, see `references/mechanism-roadmap.md`.

## Architecture

Hexagonal — domain pure, mechanisms are adapters.

```
src/assay/
├── domain/                               # Claims, MechanismResults, Adjudications, Verdict, InquiryConfig
│   ├── ports/_out/                       # Mechanism, ClaimStore, VerdictStore (Protocol classes)
│   └── services/                         # adjudicate(), InquiryRunner
├── adapters/_out/
│   ├── mechanisms/cross_family/          # Phase 1 sole mechanism (composes voice sub-adapters)
│   ├── claim_store/jsonl.py
│   └── verdict_store/duckdb.py
└── composition/root.py                   # DI wiring
```

The domain knows about Claims, Mechanisms, MechanismResults, Adjudications. It does NOT know about voices, CoVE depths, logprobs, hidden states, or debate transcripts — those are mechanism-specific concerns owned by mechanism adapters. New mechanisms (trace_budget, semantic_entropy, debate, linguistic) are sibling adapters at the same level as cross_family.

## Limitations (cobble-road release)

Phase 1 is a cobblestone, not tarmac. Known gaps:
- One mechanism only (`cross_family`); Phase 3 mechanisms not yet implemented
- One shot per voice; no per-voice retry policy on transient API errors
- Inquiry runs do not resume on partial completion — re-running creates a new timestamped run dir
- No `assay diff <inquiry> <run-A> <run-B>` yet — planned, with `claim_sha256` already stored on every result
- Voice-output parsing uses Python regex; xuma rule-tree replacement deferred

## Additional Resources

### Reference Files

For detailed content, consult:

- **`references/cove-depths.md`** — ANCHORED / REEXTRACT / BLIND with worked examples
- **`references/voice-backends.md`** — per-backend setup, auth, server startup
- **`references/inquiry-config-schema.md`** — full YAML schema with field-by-field reference
- **`references/mechanism-roadmap.md`** — Phase 3 mechanisms (Berry, SEP, debate, linguistic) integration sketch

### Examples

Working examples in `examples/`:

- **`forensic-claim.jsonl`** — sample claim with full PrimarySource
- **`inquiry-cross-family.yaml`** — sample inquiry with all three voice backends configured
