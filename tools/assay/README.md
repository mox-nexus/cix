# assay

> Independent voices in, reconciled verdicts out. Cross-family verification for AI-generated claims.

assay sits between [recon](../recon) (mechanical collection) and synthesis tools
in the cix toolchain. Where recon brings primary data in and craft-research
turns it into explained claims, assay tests whether those claims actually hold
against the primary sources — using independent verification voices from
different model families so the verdict isn't anchored to one architecture's
training set.

## Why

Single-family verification (a Claude evaluator critiquing Claude's answer) shares
training-set blind spots. When all six voices in a parallel evaluator panel are
Claude, what looks like consensus is correlated error. Cross-family triangulation
(Claude + Gemini + local MLX-Qwen) makes the consensus actually mean something:
three different training architectures, three different inductive biases, three
independent reads of the same source.

assay also reserves the seam for additional verification mechanisms beyond
cross-family voicing — see the Roadmap below.

## Install

```bash
uv tool install "git+https://github.com/mox-nexus/cix#subdirectory=tools/assay"
```

Or, for local development inside the cix monorepo:

```bash
uv tool install --editable tools/assay
```

Verify:

```bash
assay --version
```

Claude loads the skill on demand via `assay --skill` — no plugin registration needed.

## Quick start

```bash
# List built-in inquiry templates
assay templates

# Scaffold an inquiry from a template
assay init my-verification --template forensic-claim-verification

# Edit the inquiry config — set claims_path and any voice-specific knobs
$EDITOR .cix/assay/my-verification/inquiry.yaml

# Pre-flight check
assay validate my-verification

# Run the inquiry
assay verify my-verification

# Single-claim debug
assay verify my-verification --claim F003-cap-rate-FY2025

# Query the run
assay query my-verification "SELECT claim_id, final_verdict FROM adjudications WHERE diverged"

# Per-mechanism breakdown for one claim
assay show my-verification F003-cap-rate-FY2025
```

## Voices (Phase 1)

Three voice backends ship with the cross-family mechanism:

| Backend | Setup | Notes |
|---|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` env var | Claude family; calls REST API directly |
| `gemini-cli` | `gemini` CLI on PATH (oauth in `~/.gemini/`) | Gemini family; subprocess wrapping headless mode |
| `mlx-server` | Run `mlx_lm.server --model <repo> --port 8080` separately | Local MLX inference; OpenAI-compatible HTTP |

For the Apple-Silicon MLX backend, recommended model is
`unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit` (MoE 35B/3B-active, ~20 GB on disk,
~70 tokens/sec on M1 Max).

## CoVE depths

The `cross_family` mechanism dispatches to one of three Chain-of-Verification
depths per [Dhuliawala 2023](https://arxiv.org/abs/2309.11495):

- **ANCHORED** — voice sees claim + source. Catches transcription errors only.
- **REEXTRACT** — voice sees source + question, re-derives the value, then
  comparison happens externally. Catches transcription + selection-bias errors.
- **BLIND** — voice sees source + question cold, no claim, no asserted value.
  Voice answers independently. Catches transcription + selection + framing
  errors. Independence is the mechanism.

Default is REEXTRACT. Use BLIND for high-stakes claims where framing-blindness
matters (executive-summary statements, "things to note" sentences).

## Architecture

Hexagonal — domain pure, mechanisms are adapters.

```
src/assay/
├── domain/
│   ├── models.py             # Claim, PrimarySource, MechanismResult, Adjudication, Verdict, InquiryConfig
│   ├── ports/_out/           # Mechanism, ClaimStore, VerdictStore (Protocol classes)
│   └── services/             # adjudicate(), InquiryRunner
├── adapters/
│   ├── _in/cli/              # click CLI
│   └── _out/
│       ├── mechanisms/       # mechanism implementations
│       │   └── cross_family/ # Phase 1 sole mechanism (composes voice sub-adapters)
│       ├── claim_store/      # JSONL loader
│       └── verdict_store/    # DuckDB-queryable JSONL append-store
├── composition/root.py       # DI wiring
├── config/settings.py        # YAML inquiry config loader
└── configs/                  # built-in inquiry templates (YAML)
```

The domain knows about Claims, Mechanisms, MechanismResults, and Adjudications.
It does NOT know about voices, CoVE depths, logprobs, hidden states, or debate
transcripts. Those are mechanism-specific concerns owned by mechanism adapters.

## Roadmap

Phase 1 (this release) ships ONE mechanism: `cross_family`. The Mechanism port
is the seam that admits four additional mechanism families without domain
surgery:

| Mechanism | What it tests | Backend requirement | Phase |
|---|---|---|---|
| `cross_family` | Independent voices converge on the same answer | LLM API access | **1 (now)** |
| `trace_budget` | The cited span actually conditioned the claim (logprob KL) | Backend exposing token logprobs (Gemini, local MLX) | 3 |
| `semantic_entropy` | Voice's uncertainty in its own answer (Farquhar 2024 / Kossen 2024 SEPs) | Backend exposing hidden states (local MLX only) | 3 |
| `debate` | Answer survives multi-round adversarial critique by other voices | Multi-turn-capable backend | 3 |
| `linguistic` | Verb-fidelity, hedge detection, numeric normalization, citation-span alignment (UDPipe-class deterministic NLP) | None (deterministic) | 3 |

Each Phase-3 mechanism is a sibling adapter at the same architectural level as
`cross_family`. The InquiryRunner depends on the Mechanism port; new mechanisms
slot in by implementing the port. The MechanismResult contract carries
mechanism-specific evidence in an opaque `evidence` dict, so heterogeneous
mechanism outputs don't force domain changes.

## Fidelity

This is a **cobble-road release** — happy path works on three voice backends
with three CoVE depths, mission-config-driven, queryable output, refactor-safe
contracts for Phase 3. Validated end-to-end:

- ✅ MLX-Qwen voice via `mlx_lm.server` HTTP (~5s/call with thinking disabled)
- ✅ Gemini voice via `gemini -p` CLI subprocess (~22s/call, oauth via `~/.gemini/`)
- ✅ Cross-family divergence captured live on a real forensic claim (Gemini 19.9% AGREE vs MLX-Qwen 24.9% DISAGREE on cap-rate convention)
- ✅ Run-dirs PID-suffixed for concurrent-client safety
- ✅ `claim_sha256` recorded on every reading + adjudication (re-run-edit detection ready)
- ✅ Backend-passthrough `extra` config field for model-specific knobs (Qwen3 thinking-disable, etc.) without adapter source edits

Anthropic voice adapter written but not yet smoke-tested (requires `ANTHROPIC_API_KEY`).

Not yet:

- Per-voice retry policy (currently one shot, fail-soft as `Verdict.ERROR`)
- Mission-level resume on partial completion
- Multi-run diff (`assay diff <inquiry> <run-A> <run-B>`)
- xuma rule-tree-driven voice-output parsing (Phase 1 uses Python regex)

### Phase 1.5 — matrix + agent-tier rebuild (planned)

Phase 1 is built on a sequential `InquiryRunner` (`for claim: for mechanism: ...`)
and three runtime-specific voice adapters (httpx for Anthropic, subprocess for
Gemini CLI, HTTP for MLX server). This is the **wrong architectural shape** for
the long term; the rebuild is queued as Phase 1.5:

- **Substrate**: replace `InquiryRunner` with `matrix.Orchestrator`
  ([cix matrix](../matrix/)) — each (claim × voice × round) becomes a matrix
  Component on the Construct (append-only blackboard).
- **Pattern**: blackboard with N consecutive rounds. Each round, agents read
  the current Construct (input + accumulated artifacts) and append their own
  reading. No direct message-passing; communication is through the persistent
  shared state.
- **Runtime taxonomy**: voices become agent-tier Components — Claude Agent SDK,
  Google ADK (with cloud or local model backends), all uniform under the
  Component protocol.
- **Mechanism semantics preserved**: cross-family stays one round (single-shot
  voices); Phase 3 mechanisms like debate use N-round iteration.

The Phase 1 cobble validates the verification semantics (Claims, Mechanisms,
Adjudications, CoVE depths). The Phase 1.5 rebuild changes the substrate, not
the semantics — domain models and CLI surface are stable contracts.

## License

MIT
