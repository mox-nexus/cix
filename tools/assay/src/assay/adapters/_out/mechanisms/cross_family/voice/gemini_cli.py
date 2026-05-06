"""Gemini voice adapter — invokes `gemini -p` headless mode via subprocess.

The Gemini CLI handles auth (oauth credentials cached in ~/.gemini/) so no
API key env var is required.
"""

from __future__ import annotations

import subprocess
import time

from assay.adapters._out.mechanisms.cross_family.config import CoVeDepth, VoiceConfig
from assay.adapters._out.mechanisms.cross_family.parsing import parse_response
from assay.adapters._out.mechanisms.cross_family.prompt_builder import build_prompt
from assay.adapters._out.mechanisms.cross_family.voice.port import VoiceReading
from assay.domain.models import Claim


class GeminiCliVoice:
    name: str
    model: str

    def __init__(self, cfg: VoiceConfig) -> None:
        self.name = cfg.name
        self.model = cfg.model
        self._timeout = cfg.timeout_seconds

    def read(self, claim: Claim, depth: CoVeDepth) -> VoiceReading:
        prompt = build_prompt(claim, depth)
        cmd = ["gemini", "-p", prompt]
        if self.model:
            cmd.extend(["-m", self.model])

        t0 = time.time()
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=self._timeout)
        except subprocess.TimeoutExpired:
            return _error_reading(self.name, self.model, depth, f"timeout after {self._timeout}s", "")
        except FileNotFoundError:
            return _error_reading(self.name, self.model, depth, "gemini CLI not on PATH", "")
        elapsed = time.time() - t0

        if res.returncode != 0:
            return _error_reading(
                self.name, self.model, depth, f"gemini exit {res.returncode}: {res.stderr[:200]}", res.stdout, elapsed
            )

        text = res.stdout.strip()
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
