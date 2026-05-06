# Inquiry Config Schema

Inquiries are YAML files at `.cix/assay/<inquiry>/inquiry.yaml`. The schema is a Pydantic model loaded by `assay.config.settings.load_inquiry`.

## Top-level fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | yes | — | Inquiry identifier (matches the directory name) |
| `description` | string | no | none | Human-readable description |
| `mechanisms` | list[MechanismSpec] | yes | — | Mechanisms to run; Phase 1 supports only `cross_family` |
| `claims_path` | string | yes | — | Path to JSONL claim file or directory of `.jsonl` files |
| `output_dir` | string | no | `.cix/assay` | Where run outputs are persisted |
| `sleep_seconds_between_calls` | float | no | `0.5` | Pause between claims to respect rate limits |

## MechanismSpec

```yaml
mechanisms:
  - name: cross_family               # mechanism family identifier
    config: { ... }                  # mechanism-specific config; schema differs per mechanism
```

## CrossFamilyConfig (mechanism `cross_family`)

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `depth` | enum | no | `reextract` | One of `anchored`, `reextract`, `blind` |
| `voices` | list[VoiceConfig] | yes | — | Voices to triangulate; minimum 1 |

## VoiceConfig

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | yes | — | Voice identifier (used in the verdict store) |
| `backend` | enum | yes | — | `anthropic`, `gemini-cli`, `mlx-server`, `ollama-server` (latter not yet implemented) |
| `model` | string | yes | — | Backend-specific model identifier |
| `base_url` | string | conditional | — | For server-backed voices (`mlx-server`, `ollama-server`) |
| `api_key_env` | string | conditional | none | Environment variable holding API key (anthropic) |
| `timeout_seconds` | float | no | `90.0` | Per-call timeout |
| `max_tokens` | int | no | `800` | Max response tokens |
| `extra` | mapping | no | `{}` | Backend-passthrough dict merged into the request body. Use for model-specific knobs (Qwen3's `chat_template_kwargs.enable_thinking`, Anthropic's `system`, sampling params, etc.) without adapter source edits. |

### Example: Qwen3 thinking-mode disable via `extra`

Qwen3-family models emit internal "thinking" content that consumes 1500–2000+ completion tokens before the visible answer. For forensic verification (which wants direct answers, not deliberation), disable thinking via:

```yaml
- name: mlx
  backend: mlx-server
  model: unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit
  base_url: http://localhost:8080
  max_tokens: 1500
  extra:
    chat_template_kwargs:
      enable_thinking: false
```

This passes `chat_template_kwargs: {enable_thinking: false}` into the chat-completions body. ~10× speedup per call (5s vs 17s on M1 Max) and avoids empty responses under tight max_tokens.

## Claim JSONL Schema

Each claim is one JSON object per line. Fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Stable claim identifier |
| `statement` | string | yes | The assertion as written |
| `source` | object \| string | yes | PrimarySource (preferred) or string id (legacy) |
| `question` | string | no | Question for BLIND-depth verification (derived if absent) |
| `expected_value` | string | no | Asserted value if value-bearing |
| `metadata` | object | no | Free-form metadata |

PrimarySource (when `source` is an object):

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Source identifier (e.g., `10-K 0001324424-26-000008 Note 9`) |
| `excerpt` | string | yes | Verbatim source text containing or relevant to the claim |
| `accession` | string | no | EDGAR accession number |
| `section` | string | no | Section / note / item locator |
| `retrieved_at` | string | no | ISO-8601 retrieval timestamp |
| `sha256` | string | no | SHA-256 of the full source document |
| `fetch_url` | string | no | URL the source was fetched from |

Legacy short form (top-level `source_id` + `source_excerpt` strings) is supported but the object form preserves chain-of-custody fields and is preferred.

## Output Schema

After `assay verify`, two JSONL files appear at `.cix/assay/<inquiry>/run-<UTC-timestamp>/`:

### mechanism_results.jsonl

One row per (claim, mechanism) pair.

| Column | Type | Description |
|---|---|---|
| `claim_id` | string | |
| `claim_sha256` | string | Content hash; detects edits across runs |
| `mechanism` | string | Mechanism family identifier |
| `verdict` | enum | `agree` / `disagree` / `uncertain` / `error` |
| `confidence` | float \| null | Mechanism-specific confidence in [0, 1] |
| `summary` | string | One-sentence summary |
| `evidence` | object | Mechanism-specific payload (voice readings, KL trace, etc.) |
| `elapsed_seconds` | float | |
| `metadata` | object | |

### adjudications.jsonl

One row per claim.

| Column | Type | Description |
|---|---|---|
| `claim_id` | string | |
| `claim_sha256` | string | |
| `mechanism_results` | list | All MechanismResults for this claim |
| `converged` | bool | All non-error mechanisms agreed |
| `diverged` | bool | At least one mechanism disagreed with another |
| `error_count` | int | Mechanisms that errored |
| `final_verdict` | enum | Aggregate; UNCERTAIN if diverged |
| `notes` | string \| null | |
| `metadata` | object | |

## Example: minimal inquiry

```yaml
name: my-verification
description: Cross-check forensic claims with three voices
mechanisms:
  - name: cross_family
    config:
      depth: reextract
      voices:
        - name: claude
          backend: anthropic
          model: claude-opus-4-7
          api_key_env: ANTHROPIC_API_KEY
        - name: gemini
          backend: gemini-cli
          model: ""
        - name: mlx
          backend: mlx-server
          model: unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit
          base_url: http://localhost:8080
claims_path: ./claims.jsonl
output_dir: .cix/assay
sleep_seconds_between_calls: 0.5
```
