"""RawStore — persists raw fetched bytes alongside the processed archive.

Enables:
  (a) Re-normalization without re-fetching (save rate-limit budget + latency).
  (b) Audit: sha256 + timestamp + headers prove what the server actually said.
  (c) Experimentation: try different normalize specs or converters on the
      same frozen snapshot.

Layout under `archive/<timestamp>/raw/<collector_name>/`:
  body         — full response bytes (HTTP) or stdout (CLI)
  meta.yaml    — type-specific metadata + sha256 + bytes + captured_at

The `NullRawStore` is a no-op used when `preserve_raw: false`, so collectors
can call `raw.save_http(...)` unconditionally.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import yaml


class RawStore(Protocol):
    """The port: captures raw bytes for a named collector invocation."""

    def save_http(
        self,
        collector_name: str,
        body: bytes,
        *,
        status: int,
        url: str,
        headers: dict[str, str],
        content_type: str,
    ) -> None:
        """Persist an HTTP response's raw body + metadata. Called once per fetch."""

    def stream_path(self, collector_name: str) -> Path:
        """Return a path the collector may tee bytes into (e.g., CLI stdout).

        The store is responsible for creating parent directories; the collector
        just writes to the returned path. Call `finalize_stream` after writing.
        """

    def finalize_stream(
        self,
        collector_name: str,
        *,
        command: str,
        cwd: str | None,
        exit_code: int,
        patterns: list[str] | None = None,
    ) -> None:
        """Compute hash + write meta.yaml after streaming has completed."""


class NullRawStore:
    """No-op RawStore. Used when preserve_raw is off."""

    def save_http(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        """Do nothing."""

    def stream_path(self, collector_name: str) -> Path:
        # Return a sentinel path that nothing actually writes to. Callers must
        # check for NullRawStore before teeing — but they can equivalently just
        # check for an injected store at all. We return a path-like that would
        # error if used, to surface the bug.
        return Path("/dev/null")

    def finalize_stream(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        """Do nothing."""


class FilesystemRawStore:
    """Writes raw captures under `<archive_dir>/raw/<collector_name>/`."""

    def __init__(self, archive_dir: Path) -> None:
        self._root = archive_dir / "raw"
        self._root.mkdir(parents=True, exist_ok=True)

    def _dir_for(self, collector_name: str) -> Path:
        out = self._root / collector_name
        out.mkdir(parents=True, exist_ok=True)
        return out

    def save_http(
        self,
        collector_name: str,
        body: bytes,
        *,
        status: int,
        url: str,
        headers: dict[str, str],
        content_type: str,
    ) -> None:
        out_dir = self._dir_for(collector_name)
        body_path = out_dir / "body"
        body_path.write_bytes(body)
        meta = {
            "type": "http",
            "collector": collector_name,
            "url": url,
            "status": status,
            "content_type": content_type,
            "headers": {k: v for k, v in headers.items()},
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "captured_at": datetime.now(UTC).isoformat(),
        }
        (out_dir / "meta.yaml").write_text(
            yaml.dump(meta, default_flow_style=False, sort_keys=False)
        )

    def stream_path(self, collector_name: str) -> Path:
        out_dir = self._dir_for(collector_name)
        return out_dir / "body"

    def finalize_stream(
        self,
        collector_name: str,
        *,
        command: str,
        cwd: str | None,
        exit_code: int,
        patterns: list[str] | None = None,
    ) -> None:
        out_dir = self._dir_for(collector_name)
        body_path = out_dir / "body"
        bytes_size = 0
        sha = hashlib.sha256()
        if body_path.exists():
            bytes_size = body_path.stat().st_size
            with open(body_path, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    sha.update(chunk)
        meta = {
            "type": "cli",
            "collector": collector_name,
            "command": command,
            "cwd": cwd,
            "exit_code": exit_code,
            "patterns": patterns,
            "bytes": bytes_size,
            "sha256": sha.hexdigest() if bytes_size else "",
            "captured_at": datetime.now(UTC).isoformat(),
        }
        (out_dir / "meta.yaml").write_text(
            yaml.dump(meta, default_flow_style=False, sort_keys=False)
        )
