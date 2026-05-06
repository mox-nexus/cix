# Voice Backends

Three backends ship with the Phase 1 `cross_family` mechanism. Each implements the Voice sub-port internally and is selected via the inquiry YAML.

## anthropic — Claude family

**Setup**: set `ANTHROPIC_API_KEY` (or any environment variable named in `api_key_env`) to a valid Anthropic API key.

**Mechanism**: subprocess-free; calls Anthropic's REST `/v1/messages` endpoint via httpx. No SDK dependency.

**YAML**:

```yaml
- name: claude
  backend: anthropic
  model: claude-opus-4-7              # or claude-sonnet-4-6, claude-haiku-4-5-20251001
  api_key_env: ANTHROPIC_API_KEY      # which env var holds the key
  timeout_seconds: 90.0
  max_tokens: 800
```

**Failure modes**: missing env var, HTTP non-200 (rate limit, auth, server error), network timeout. All return `Verdict.ERROR` on the resulting MechanismResult voice reading; the inquiry continues.

**Latency**: ~5–15s per call, depends on model and prompt length.

## gemini-cli — Gemini family

**Setup**: install Gemini CLI (`brew install gemini-cli`), authenticate via `gemini` interactive login (oauth credentials cached at `~/.gemini/`). No env var required.

**Mechanism**: subprocess `gemini -p <prompt>` via Python `subprocess.run`. Captures stdout, parses for VERDICT/EXTRACTED/SUPPORTING SPAN/REASON blocks.

**YAML**:

```yaml
- name: gemini
  backend: gemini-cli
  model: ""                            # empty = CLI default model; or "gemini-2.0-flash" etc.
  timeout_seconds: 90.0
```

**Failure modes**: `gemini` not on PATH, subprocess timeout, non-zero exit code. Return `Verdict.ERROR`.

**Latency**: ~10–25s per call (subprocess startup + model inference).

## mlx-server — Local MLX (Apple Silicon)

**Setup**: separately start the mlx-lm OpenAI-compatible server pointing at an MLX-format model. The server is NOT started or stopped by assay.

```bash
# One-time install
uv tool install mlx-lm

# Start server
mlx_lm.server --model unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit --port 8080
```

First run downloads ~20 GB to `~/.cache/huggingface/hub/`. Subsequent starts are instant.

**Mechanism**: HTTP POST to `<base_url>/v1/chat/completions` (OpenAI-compatible). Strips Qwen3-style `<think>...</think>` internal-reasoning blocks from responses before parsing.

**YAML**:

```yaml
- name: mlx
  backend: mlx-server
  model: unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit
  base_url: http://localhost:8080
  timeout_seconds: 120.0
  max_tokens: 800
```

**Failure modes**: server not running (HTTP connection error), non-200 response, JSON parse failure. Return `Verdict.ERROR`.

**Latency**: ~3–10s per call on M1 Max with the recommended MoE model (3B active params despite 35B total).

## Recommended model for mlx-server

On Apple Silicon (M1 Max / M2 Pro / M3 / M4 with ≥32 GB RAM):

- **`unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit`** — Qwen3.6 MoE, 35B total / 3B active per token. ~20 GB on disk. ~70 tokens/sec on M1 Max. Best speed/quality ratio. Unsloth's UD (Unsloth Dynamic) quantization preserves benchmark accuracy better than vanilla GGUF Q4.

Alternatives:
- `unsloth/Qwen3.6-27B-MLX-8bit` — dense 27B at 8-bit (~27 GB). Higher quality, slower inference.
- `mlx-community/Qwen3.6-35B-A3B-4bit` — community MLX quant if Unsloth's UD is unavailable.

Avoid 3-bit quants for forensic verification; too aggressive.

## Triangulation discipline

The point of cross-family is independence. Configure voices from genuinely different model families:

- Claude (Anthropic) + Gemini (Google) + Qwen (Alibaba via MLX) → three architectures, three training sets, three inductive biases.
- Two Claude voices at different versions (Opus + Sonnet) is NOT cross-family; same training architecture.

When a fourth or fifth voice is added (e.g., DeepSeek, Llama), prefer additional family diversity over additional same-family models.

## Verifying backend reachability

Use `assay validate <inquiry>` before `verify`. It composes the runner without making model calls — surfaces missing env vars, unknown backends, malformed YAML, missing claim files. It does not currently ping the MLX server or verify the Gemini CLI works; consider doing those manually:

```bash
# Anthropic
echo "$ANTHROPIC_API_KEY" | wc -c   # > 1 means set

# Gemini
gemini -p "Reply: PONG" -m gemini-2.0-flash

# MLX
curl -s http://localhost:8080/v1/models
```
