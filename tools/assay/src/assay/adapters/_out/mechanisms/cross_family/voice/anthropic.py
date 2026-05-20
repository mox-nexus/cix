"""Claude voice adapter — calls Anthropic API via httpx.

Doesn't take a hard dep on the anthropic SDK; uses the messages REST endpoint
directly. Requires ANTHROPIC_API_KEY (or configured env var) at call time.
"""

from __future__ import annotations

import os
import time

import httpx

from assay.adapters._out.mechanisms.cross_family.config import CoVeDepth, VoiceConfig
from assay.adapters._out.mechanisms.cross_family.parsing import parse_response
from assay.adapters._out.mechanisms.cross_family.prompt_builder import build_prompt
from assay.adapters._out.mechanisms.cross_family.voice.port import VoiceReading
from assay.domain.models import Claim


_API_URL = "https://api.anthropic.com/v1/messages"
_API_VERSION = "2023-06-01"


class AnthropicVoice:
    name: str
    model: str

    def __init__(self, cfg: VoiceConfig) -> None:
        self.name = cfg.name
        self.model = cfg.model
        self._timeout = cfg.timeout_seconds
        self._max_tokens = cfg.max_tokens
        self._api_key_env = cfg.api_key_env or "ANTHROPIC_API_KEY"
        self._extra = dict(cfg.extra)

    def read(self, claim: Claim, depth: CoVeDepth) -> VoiceReading:
        prompt = build_prompt(claim, depth)
        api_key = os.environ.get(self._api_key_env, "")
        if not api_key:
            return _error_reading(self.name, self.model, depth, f"missing env {self._api_key_env}", "")

        t0 = time.time()
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(
                    _API_URL,
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": _API_VERSION,
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": self._max_tokens,
                        "messages": [{"role": "user", "content": prompt}],
                        **self._extra,
                    },
                )
            elapsed = time.time() - t0
            if resp.status_code != 200:
                return _error_reading(
                    self.name, self.model, depth, f"HTTP {resp.status_code}: {resp.text[:200]}", "", elapsed
                )
            data = resp.json()
            blocks = data.get("content", [])
            text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
        except Exception as e:
            return _error_reading(self.name, self.model, depth, f"exception: {e}", "", time.time() - t0)

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


def _error_reading(
    name: str, model: str, depth: CoVeDepth, reason: str, raw: str, elapsed: float = 0.0
) -> VoiceReading:
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
