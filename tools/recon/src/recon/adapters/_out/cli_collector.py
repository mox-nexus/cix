"""CliCollector — runs shell commands, returns records.

Handles subprocess execution, JSONL/text parsing, pattern expansion.
Uses source.url as cwd when source is a local directory.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from recon.application.recon import substitute
from recon.application.transforms import apply_normalize
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry


def _parse_stdout(stdout: str) -> list[dict[str, Any]]:
    """Parse command stdout — try JSONL, fall back to text lines."""
    if not stdout.strip():
        return []

    lines = stdout.strip().splitlines()
    try:
        first = json.loads(lines[0])
        if isinstance(first, dict):
            records = [first]
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parsed = json.loads(line)
                    if isinstance(parsed, dict):
                        records.append(parsed)
            return records
    except (json.JSONDecodeError, IndexError):
        pass

    return [{"line_number": i, "line": line} for i, line in enumerate(lines, 1) if line.strip()]


class CliCollector:
    """Runs shell commands, captures stdout, returns records."""

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
    ) -> list[dict[str, Any]]:
        """Execute command(s), parse output, return records."""
        if not entry.run:
            msg = f"Collector '{entry.name}' has type=cli but no 'run' field"
            raise CollectionError(msg)

        variables: dict[str, str] = {}
        cwd: Path | None = None

        if source:
            variables["url"] = source.url
            source_path = Path(source.url)
            if source_path.is_dir():
                cwd = source_path

        all_records: list[dict[str, Any]] = []

        timeout = source.timeout if source else 300

        if entry.patterns:
            for pattern in entry.patterns:
                cmd = substitute(entry.run, {**variables, "pattern": pattern})
                records = self._execute(cmd, cwd, timeout)
                for record in records:
                    record["_pattern"] = pattern
                all_records.extend(records)
        else:
            cmd = substitute(entry.run, variables)
            all_records = self._execute(cmd, cwd, timeout)

        if entry.normalize and all_records:
            all_records = [apply_normalize(record, entry.normalize) for record in all_records]

        return all_records

    def _execute(
        self,
        cmd: str,
        cwd: Path | None = None,
        timeout: float = 300,
    ) -> list[dict[str, Any]]:
        """Run a shell command, return parsed records.

        Note: shell=True is intentional — configs are trusted local input.
        The substitute() function performs no shell escaping. Template
        authors are responsible for safe quoting in their run: commands.
        """
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            msg = f"Command timed out after {timeout}s: {cmd}"
            raise CollectionError(msg) from exc

        # Many commands (rg, grep) return exit code 1 for "no matches"
        if result.returncode not in (0, 1):
            msg = f"Command failed (exit {result.returncode}): {cmd}"
            if result.stderr:
                msg += f"\n{result.stderr.strip()}"
            raise CollectionError(msg)

        return _parse_stdout(result.stdout)
