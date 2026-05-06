"""CliCollector — runs shell commands, yields records line-by-line.

Uses subprocess.Popen with a streaming stdout pipe so large outputs (e.g.
`rg --json` across a huge tree) don't materialize in memory before parsing.
Each stdout line is parsed and yielded as a record; memory usage is O(1) in
the number of records produced.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Protocol

from recon.application.recon import substitute
from recon.application.transforms import apply_normalize
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry


class ShellRunner(Protocol):
    """The port: given a command, yield stdout lines as they arrive.

    Implementations own the subprocess lifecycle. Timeout raises
    CollectionError; non-zero exit codes (other than 0/1) raise too.

    When `capture_path` is provided, each stdout line is also written to
    that file as it flows — a streaming tee. Memory stays O(1).
    `capture_exit` is filled with the process exit code at the end (for
    metadata capture by the caller).
    """

    def run_lines(
        self,
        cmd: str,
        cwd: Path | None,
        timeout: float,
        *,
        capture_path: Path | None = None,
        capture_exit: list[int] | None = None,
    ) -> Iterator[str]: ...


class PopenRunner:
    """Default ShellRunner — Popen + iterate stdout lines, optional tee."""

    def run_lines(
        self,
        cmd: str,
        cwd: Path | None,
        timeout: float,
        *,
        capture_path: Path | None = None,
        capture_exit: list[int] | None = None,
    ) -> Iterator[str]:
        import os
        import signal

        # shell=True is intentional — configs are trusted local input.
        proc = subprocess.Popen(  # noqa: S602
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            # Start the child in its own process group so timeout kills the
            # whole tree, not just the shell.
            preexec_fn=os.setsid if os.name == "posix" else None,
        )

        tee_file = None
        if capture_path is not None:
            # Append mode: if called twice (e.g., patterns fan-out across one
            # entry), concatenate into one captured body.
            capture_path.parent.mkdir(parents=True, exist_ok=True)
            tee_file = open(capture_path, "a")  # noqa: SIM115

        try:
            assert proc.stdout is not None
            # Iterate stdout as lines flow. Pull-based backpressure applies;
            # tee writes happen at the same rate as consumer reads.
            for raw_line in proc.stdout:
                if tee_file is not None:
                    tee_file.write(raw_line)
                yield raw_line.rstrip("\n")

            try:
                _stdout, stderr = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired as exc:
                if os.name == "posix":
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                else:
                    proc.kill()
                proc.wait()
                msg = f"Command timed out after {timeout}s: {cmd}"
                raise CollectionError(msg) from exc

            if proc.returncode not in (0, 1):
                err = (stderr or "").strip()
                detail = f"\n{err}" if err else ""
                msg = f"Command failed (exit {proc.returncode}): {cmd}{detail}"
                raise CollectionError(msg)

            if capture_exit is not None:
                capture_exit.append(proc.returncode)
        finally:
            if tee_file is not None:
                try:
                    tee_file.flush()
                    tee_file.close()
                except Exception:  # noqa: BLE001
                    pass
            # Guarantee cleanup on consumer abandonment (GeneratorExit).
            try:
                if proc.poll() is None:
                    if os.name == "posix":
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                    proc.wait(timeout=5)
            except Exception:  # noqa: BLE001
                pass


def _parse_line(line: str, index: int) -> dict[str, Any] | None:
    """Parse one stdout line. JSON object wins; otherwise {line_number, line}."""
    stripped = line.strip()
    if not stripped:
        return None
    try:
        obj = json.loads(stripped)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    return {"line_number": index, "line": line}


class CliCollector:
    """Runs shell commands, yields parsed stdout records as they stream."""

    def __init__(self, runner: ShellRunner | None = None) -> None:
        self._runner = runner if runner is not None else PopenRunner()

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
        *,
        raw_store: Any | None = None,
    ) -> Iterator[dict[str, Any]]:
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
        timeout = source.timeout if source else 300.0

        patterns = list(entry.patterns) if entry.patterns else [None]

        # Raw capture: tee each invocation's stdout into a single body file
        # per collector entry (patterns concatenate). Path is None when no store.
        capture_path = raw_store.stream_path(entry.name) if raw_store is not None else None
        last_cmd = ""
        exit_codes: list[int] = []

        try:
            for pattern in patterns:
                cmd_vars = {**variables, "pattern": pattern} if pattern is not None else variables
                cmd = substitute(entry.run, cmd_vars)
                last_cmd = cmd

                index = 0
                for line in self._runner.run_lines(
                    cmd,
                    cwd,
                    timeout,
                    capture_path=capture_path,
                    capture_exit=exit_codes,
                ):
                    index += 1
                    record = _parse_line(line, index)
                    if record is None:
                        continue
                    if pattern is not None:
                        record["_pattern"] = pattern
                    if entry.normalize:
                        record = apply_normalize(record, entry.normalize)
                    yield record
        finally:
            if raw_store is not None:
                # Finalize even on mid-iteration abandonment — preserves partial
                # captures for audit.
                raw_store.finalize_stream(
                    entry.name,
                    command=last_cmd,
                    cwd=str(cwd) if cwd else None,
                    exit_code=exit_codes[-1] if exit_codes else -1,
                    patterns=[p for p in patterns if p is not None] or None,
                )
