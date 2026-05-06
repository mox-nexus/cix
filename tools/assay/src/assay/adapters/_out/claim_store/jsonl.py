"""JSONL claim store — one Claim per line in a file or directory."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from assay.domain.exceptions import InquiryConfigError
from assay.domain.models import Claim, PrimarySource


class JsonlClaimStore:
    def __init__(self, path: str) -> None:
        self._path = Path(path)
        if not self._path.exists():
            raise InquiryConfigError(f"claims_path does not exist: {self._path}")

    def iter_claims(self) -> Iterator[Claim]:
        files: list[Path]
        if self._path.is_dir():
            files = sorted(self._path.glob("*.jsonl"))
        else:
            files = [self._path]

        for f in files:
            with f.open("r", encoding="utf-8") as fh:
                for line_no, line in enumerate(fh, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        raw = json.loads(line)
                    except json.JSONDecodeError as e:
                        raise InquiryConfigError(f"{f}:{line_no} bad JSON: {e}") from e
                    yield _from_dict(raw)

    def get(self, claim_id: str) -> Claim | None:
        for c in self.iter_claims():
            if c.id == claim_id:
                return c
        return None


def _from_dict(d: dict) -> Claim:
    src_raw = d.get("source")
    if isinstance(src_raw, dict):
        source = PrimarySource(**src_raw)
    elif isinstance(src_raw, str):
        # Permit a string source field as a shorthand for {id, excerpt}
        # when the claim only carries a label without a separate excerpt.
        # For real verification, prefer the dict form.
        source = PrimarySource(id=src_raw, excerpt=d.get("source_excerpt", ""))
    else:
        # Legacy / shorthand: source_id + source_excerpt at top level
        source = PrimarySource(
            id=d.get("source_id", "(unknown)"),
            excerpt=d.get("source_excerpt", ""),
            accession=d.get("accession"),
            section=d.get("section"),
        )

    return Claim(
        id=d["id"],
        statement=d["statement"],
        source=source,
        question=d.get("question"),
        expected_value=d.get("expected_value"),
        metadata=d.get("metadata", {}),
    )
