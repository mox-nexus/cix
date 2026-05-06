"""Configuration for the cross_family mechanism.

CoVeDepth lives here (not in domain) — depth is a cross-family-mechanism
parameter, not a universal verification concept. Berry's "scrub granularity"
and SEP's "sample count" live in their own respective mechanism configs.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CoVeDepth(str, Enum):
    """Depth of cross-examination per Dhuliawala 2023 CoVE.

    Names describe the mechanism (independence-from-the-claim), not the cost.

    ANCHORED  — voice sees the claim AND the source; checks transcription only.
    REEXTRACT — voice sees source + question; re-derives the value, then we
                compare to the claim externally.
    BLIND     — voice sees source + question cold, no claim, no expected value;
                voice answers independently; comparison happens in the
                CrossFamilyMechanism. Independence is the mechanism.
    """

    ANCHORED = "anchored"
    REEXTRACT = "reextract"
    BLIND = "blind"


class VoiceConfig(BaseModel):
    """Spec for one voice within the cross-family mechanism.

    `extra` is a backend-passthrough dict merged into the request body when
    the adapter calls the backend. Use it for model-specific knobs that
    vary by backend (e.g., Qwen3's `chat_template_kwargs.enable_thinking`,
    Anthropic's `system`, Gemini's `safety_settings`).
    """

    name: str
    backend: Literal["anthropic", "gemini-cli", "mlx-server", "ollama-server"]
    model: str
    base_url: str | None = None
    api_key_env: str | None = None
    timeout_seconds: float = 90.0
    max_tokens: int = 800
    extra: dict[str, object] = Field(default_factory=dict)


class CrossFamilyConfig(BaseModel):
    """Mechanism-specific config parsed from InquirySpec.mechanisms[i].config."""

    voices: list[VoiceConfig]
    depth: CoVeDepth = Field(default=CoVeDepth.REEXTRACT)
