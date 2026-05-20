"""Inquiry config loading — YAML to InquiryConfig."""

from __future__ import annotations

from pathlib import Path

import yaml

from assay.domain.exceptions import InquiryConfigError
from assay.domain.models import InquiryConfig


def load_inquiry(path: str | Path) -> InquiryConfig:
    p = Path(path)
    if not p.exists():
        raise InquiryConfigError(f"inquiry config not found: {p}")
    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise InquiryConfigError(f"inquiry config must be a mapping, got {type(raw).__name__}")
    try:
        return InquiryConfig(**raw)
    except Exception as e:
        raise InquiryConfigError(f"inquiry config validation failed: {e}") from e
