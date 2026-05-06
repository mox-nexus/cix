"""Local MLX voice adapter — hits a running mlx_lm.server via HTTP.

mlx_lm.server exposes an OpenAI-compatible /v1/chat/completions endpoint.
The server must be started separately; this adapter does not start or stop it.

Strips Qwen3-style "Thinking Process:" preamble from responses.
"""

from __future__ import annotations

import re
import time

import httpx

from assay.adapters._out.mechanisms.cross_family.config import CoVeDepth, VoiceConfig
from assay.adapters._out.mechanisms.cross_family.parsing import parse_response
from assay.adapters._out.mechanisms.cross_family.prompt_builder import build_prompt
from assay.adapters._out.mechanisms.cross_family.voice.port import VoiceReading
from assay.domain.models import Claim


# Qwen3 emits internal reasoning either as <think>...</think> tags (when
# the server doesn't pre-strip them) or as a "Thinking Process:" preamble
# followed by "==========" separator. Both are stripped defensively in case
# disable_thinking does not take effect (e.g., on a different model).
_THINK_TAG_RX = re.compile(r"<think>.*?</think>", re.DOTALL)
_THINK_HEADER_RX = re.compile(
    r"^\s*Thinking Process:.*?(?:={3,}|\n\n)", re.DOTALL | re.IGNORECASE
)


class MlxServerVoice:
    name: str
    model: str

    def __init__(self, cfg: VoiceConfig) -> None:
        self.name = cfg.name
        self.model = cfg.model
        self._base_url = (cfg.base_url or "http://localhost:8080").rstrip("/")
        self._timeout = cfg.timeout_seconds
        self._max_tokens = cfg.max_tokens
        self._extra = dict(cfg.extra)

    def read(self, claim: Claim, depth: CoVeDepth) -> VoiceReading:
        prompt = build_prompt(claim, depth)

        body = {
            "model": self.model,
            "max_tokens": self._max_tokens,
            "temperature": 0.0,
            "messages": [{"role": "user", "content": prompt}],
        }
        # Merge backend-passthrough config from VoiceConfig.extra. Lets the
        # inquiry YAML control model-specific knobs (Qwen3's
        # chat_template_kwargs.enable_thinking, sampling params, etc.)
        # without adapter source edits.
        if self._extra:
            body.update(self._extra)

        t0 = time.time()
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(
                    f"{self._base_url}/v1/chat/completions",
                    json=body,
                )
        except Exception as e:
            return _error_reading(self.name, self.model, depth, f"exception: {e}", "", time.time() - t0)
        elapsed = time.time() - t0

        if resp.status_code != 200:
            return _error_reading(
                self.name, self.model, depth, f"HTTP {resp.status_code}: {resp.text[:200]}", "", elapsed
            )

        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return _error_reading(self.name, self.model, depth, "no choices in response", str(data)[:200], elapsed)

        text = choices[0].get("message", {}).get("content", "").strip()
        # Defense-in-depth: strip thinking artifacts even if disable did not take effect.
        text = _THINK_TAG_RX.sub("", text)
        text = _THINK_HEADER_RX.sub("", text)
        text = text.strip()

        parsed = parse_response(text)
        return VoiceReading(
            voice_name=self.name,
            voice_model=self.model,
            depth=depth,
            verdict=parsed["verdict"],
            reasoning=parsed["reason"],
            extracted_value=parsed["extracted"],
            supporting_span=parsed["supporting_span"],
            elapsed_seconds=elapsed,
            raw_response=text,
        )


def _error_reading(name: str, model: str, depth: CoVeDepth, reason: str, raw: str, elapsed: float = 0.0) -> VoiceReading:
    return VoiceReading(
        voice_name=name,
        voice_model=model,
        depth=depth,
        verdict="error",
        reasoning=reason,
        extracted_value=None,
        supporting_span=None,
        elapsed_seconds=elapsed,
        raw_response=raw,
    )
