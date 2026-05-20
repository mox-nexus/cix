"""Composition root — wire ports to adapters from an InquiryConfig.

Single location for dependency injection. The CLI imports from here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from assay.adapters._out.claim_store.jsonl import JsonlClaimStore
from assay.adapters._out.mechanisms.cross_family.config import CrossFamilyConfig, VoiceConfig
from assay.adapters._out.mechanisms.cross_family.mechanism import CrossFamilyMechanism
from assay.adapters._out.mechanisms.cross_family.voice.anthropic import AnthropicVoice
from assay.adapters._out.mechanisms.cross_family.voice.gemini_cli import GeminiCliVoice
from assay.adapters._out.mechanisms.cross_family.voice.mlx_server import MlxServerVoice
from assay.adapters._out.mechanisms.cross_family.voice.port import Voice
from assay.adapters._out.verdict_store.duckdb import DuckdbVerdictStore
from assay.domain.exceptions import InquiryConfigError
from assay.domain.models import InquiryConfig, MechanismSpec
from assay.domain.ports._out.mechanism import Mechanism
from assay.domain.services.inquiry_runner import InquiryRunner

# --- Voice factory (cross-family) ---


_VOICE_BACKENDS = {
    "anthropic": AnthropicVoice,
    "gemini-cli": GeminiCliVoice,
    "mlx-server": MlxServerVoice,
}


def _build_voice(cfg: VoiceConfig) -> Voice:
    backend = cfg.backend
    cls = _VOICE_BACKENDS.get(backend)
    if cls is None:
        raise InquiryConfigError(
            f"unknown voice backend: {backend!r} (known: {list(_VOICE_BACKENDS)})"
        )
    return cls(cfg)


# --- Mechanism factory ---


def _build_cross_family(spec: MechanismSpec) -> CrossFamilyMechanism:
    cfg = CrossFamilyConfig(**spec.config)
    voices = [_build_voice(v) for v in cfg.voices]
    return CrossFamilyMechanism(voices=voices, config=cfg)


_MECHANISM_BUILDERS = {
    "cross_family": _build_cross_family,
}


def _build_mechanism(spec: MechanismSpec) -> Mechanism:
    builder = _MECHANISM_BUILDERS.get(spec.name)
    if builder is None:
        raise InquiryConfigError(
            f"unknown mechanism: {spec.name!r} (known: {list(_MECHANISM_BUILDERS)})"
        )
    return builder(spec)


# --- Top-level compose ---


def compose(config: InquiryConfig, run_dir: str | None = None) -> tuple[InquiryRunner, Path]:
    """Build the InquiryRunner from the config. Returns (runner, run_dir).

    Run directories are PID-suffixed at millisecond resolution so two
    concurrent `verify` calls on the same inquiry never collide on the
    output dir — the conservative fix for the same-inquiry concurrency
    race documented in the README.
    """
    if run_dir is None:
        import os

        now = datetime.now(UTC)
        ts = now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond // 1000:03d}Z"
        run_dir_path = Path(config.output_dir) / config.name / f"run-{ts}-pid{os.getpid()}"
    else:
        run_dir_path = Path(run_dir)
    run_dir_path.mkdir(parents=True, exist_ok=True)

    claim_store = JsonlClaimStore(config.claims_path)
    mechanisms = [_build_mechanism(s) for s in config.mechanisms]
    verdict_store = DuckdbVerdictStore(str(run_dir_path))
    runner = InquiryRunner(
        claim_store=claim_store,
        mechanisms=mechanisms,
        verdict_store=verdict_store,
        sleep_seconds_between_claims=config.sleep_seconds_between_calls,
    )
    return runner, run_dir_path
