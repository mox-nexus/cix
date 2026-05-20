"""Recon — the dispatch loop (reactor).

Iterates collector entries, fans out across catalog sources, composes the
collect → shape → sink pipeline per target. Collectors return iterators;
sink streams records to JSONL line-by-line. Generator cleanup is guaranteed
via contextlib.closing — consumer-abandoned collectors always release
their resources.

No direct adapter imports — hex arch clean.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from recon.application.raw_store import FilesystemRawStore, NullRawStore, RawStore
from recon.domain.collector import Collector
from recon.domain.exceptions import CollectionError, ReconError
from recon.domain.models import CollectorEntry, ReconConfig, SourceEntry

EventCallback = Callable[[dict[str, Any]], None]


class CollectorError(CollectionError):
    """Wraps a collector's raised exception with the entry + source it came from.

    Raised at the run_collector boundary so downstream code (sink, dispatch)
    knows which collector failed without having to unpack the cause itself.
    """

    def __init__(self, collector_name: str, source_name: str | None, cause: BaseException):
        self.collector_name = collector_name
        self.source_name = source_name
        self.cause = cause
        loc = f"{collector_name}" + (f" against '{source_name}'" if source_name else "")
        super().__init__(f"[{loc}] {cause}")


def _plan_output_names(config: ReconConfig) -> list[str]:
    """Compute the output_name each (collector, target) pair will produce.

    Mirrors the dispatch logic in run() so we can detect collisions before
    any writes happen. Unknown-type or unresolved-source entries are skipped
    here — run() handles their errors. Only well-formed pairs produce names.
    """
    catalog = {s.name: s for s in config.catalog}
    names: list[str] = []
    for entry in config.collectors:
        if entry.source:
            if entry.source in catalog:
                names.append(entry.name)
        elif config.catalog:
            names.extend(f"{entry.name}-{src.name}" for src in config.catalog)
        else:
            names.append(entry.name)
    return names


def substitute(value: Any, variables: dict[str, str]) -> Any:
    """Apply `{key}` substitution to string values, recursing into dicts and
    lists. Non-string scalars (ints, bools, None) pass through unchanged.

    Single function, single concept: "fill template from variables."
    """
    if isinstance(value, str):

        def replacer(match: re.Match) -> str:
            key = match.group(1)
            return variables.get(key, match.group(0))

        return re.sub(r"\{(\w+)\}", replacer, value)
    if isinstance(value, dict):
        return {k: substitute(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, variables) for v in value]
    return value


def find_unresolved(value: Any) -> list[str]:
    """Walk a substituted structure and return every `{placeholder}` still
    present in string values. Empty list means all placeholders resolved.
    """
    unresolved: list[str] = []

    def walk(v: Any) -> None:
        if isinstance(v, str):
            unresolved.extend(re.findall(r"\{(\w+)\}", v))
        elif isinstance(v, dict):
            for item in v.values():
                walk(item)
        elif isinstance(v, list):
            for item in v:
                walk(item)

    walk(value)
    return unresolved


def _tag_errors(
    collector: Collector,
    entry: CollectorEntry,
    source: SourceEntry | None,
    raw_store: RawStore | None = None,
) -> Iterator[dict[str, Any]]:
    """Wrap a collector's iterator so any exception it raises (eagerly or
    mid-stream) surfaces as CollectorError with entry + source attribution.

    Without this, an exception raised deep inside `collector.collect()` would
    reach sink() with no information about *which* collector produced it.
    """
    source_name = source.name if source else None
    try:
        yield from collector.collect(entry, source, raw_store=raw_store)
    except CollectorError:
        raise  # already tagged
    except Exception as exc:
        raise CollectorError(entry.name, source_name, exc) from exc


def _sink(records: Iterator[dict[str, Any]], path: Path, *, fsync_every: int = 1000) -> int:
    """Stream records to JSONL atomically; return the number written.

    Writes to <path>.tmp line-by-line; fsyncs every `fsync_every` records so
    durability loss on crash is bounded. On any error the partial .tmp is
    removed and the exception propagates. On success, atomic rename to final.

    Guarantees generator cleanup via contextlib.closing — if an exception
    interrupts iteration, the upstream collector's try/finally still runs
    (subprocess kill, httpx client close, rate-limit token release).
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    count = 0
    try:
        with contextlib.closing(records), open(tmp, "w") as f:
            for record in records:
                f.write(json.dumps(record, default=str) + "\n")
                count += 1
                if count % fsync_every == 0:
                    f.flush()
                    os.fsync(f.fileno())
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise
    return count


def run(
    config: ReconConfig,
    collectors: dict[str, Collector],
    mission_dir: Path,
    on_event: EventCallback | None = None,
) -> tuple[Path, list[dict[str, Any]]]:
    """Execute all collectors, produce an archive directory.

    Fan-out: if a collector has no source, it runs against every catalog entry.
    If a collector names a source, it runs against that source only.
    If there's no catalog, collectors run once with no source.

    Outcome events are reported via `on_event` if provided. Each event is a
    dict with at least a `kind` field: "ok", "error", or "archive_warning".
    The caller formats output; this function does no console I/O.

    Returns (archive_dir, results) where results is the same list of per-
    collector status dicts that also lands in meta.yaml.
    """
    # Pre-flight: detect output_name collisions before any writes.
    planned = _plan_output_names(config)
    seen: set[str] = set()
    collisions: set[str] = set()
    for n in planned:
        if n in seen:
            collisions.add(n)
        seen.add(n)
    if collisions:
        msg = (
            f"Output name collision: {', '.join(sorted(collisions))}. "
            "Two collectors would write to the same file. "
            "Rename one of the colliding collectors so each produces a unique JSONL."
        )
        raise ReconError(msg)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d-%H%M%S-%f")
    archive_dir = mission_dir / "archive" / timestamp
    archive_dir.mkdir(parents=True, exist_ok=True)

    # If the mission preserves raw captures, wire a filesystem-backed store
    # rooted at archive_dir/raw/. Otherwise a NullRawStore — collectors can
    # call raw_store methods unconditionally without checking.
    raw_store: RawStore = FilesystemRawStore(archive_dir) if config.preserve_raw else NullRawStore()

    catalog: dict[str, SourceEntry] = {s.name: s for s in config.catalog}

    def emit(event: dict[str, Any]) -> None:
        if on_event is not None:
            on_event(event)

    results: list[dict[str, Any]] = []

    for entry in config.collectors:
        collector = collectors.get(entry.type)
        if not collector:
            results.append(
                {
                    "name": entry.name,
                    "status": "error",
                    "error": f"No collector registered for type: {entry.type}",
                }
            )
            emit({"kind": "error", "name": entry.name, "reason": f"unknown type '{entry.type}'"})
            continue

        # Determine targets: pinned source, fan-out, or standalone
        if entry.source:
            if entry.source not in catalog:
                results.append(
                    {
                        "name": entry.name,
                        "status": "error",
                        "error": (
                            f"Source '{entry.source}' not in catalog. "
                            f"Available: {', '.join(sorted(catalog)) or '(none)'}"
                        ),
                    }
                )
                emit(
                    {
                        "kind": "error",
                        "name": entry.name,
                        "reason": f"source '{entry.source}' not found",
                    }
                )
                continue
            targets = [(catalog[entry.source], entry.name)]
        elif config.catalog:
            targets = [(src, f"{entry.name}-{src.name}") for src in config.catalog]
        else:
            targets = [(None, entry.name)]

        for source, output_name in targets:
            start = datetime.now(UTC)
            try:
                # Pass the raw_store only when enabled (NullRawStore when not).
                # Fan-out uses the output_name-keyed path so each target's raw
                # lands in its own subdir, matching the JSONL naming.
                per_target_entry = (
                    entry
                    if output_name == entry.name
                    else entry.model_copy(update={"name": output_name})
                )
                records = _tag_errors(
                    collector,
                    per_target_entry,
                    source,
                    raw_store=raw_store if config.preserve_raw else None,
                )

                # Empty-collector sentinel: if the collector yields nothing,
                # still produce a single {"_empty": True} record so downstream
                # tools (DuckDB read_json_auto) have a file to read.
                def _with_sentinel(r: Iterator[dict[str, Any]]) -> Iterator[dict[str, Any]]:
                    any_yielded = False
                    for record in r:
                        any_yielded = True
                        yield record
                    if not any_yielded:
                        yield {"_empty": True}

                count = _sink(_with_sentinel(records), archive_dir / f"{output_name}.jsonl")

                elapsed = (datetime.now(UTC) - start).total_seconds()
                results.append(
                    {
                        "name": output_name,
                        "status": "ok",
                        "file": f"{output_name}.jsonl",
                        "records": count,
                        "seconds": round(elapsed, 2),
                    }
                )
                emit({"kind": "ok", "name": output_name, "records": count})

            except Exception as exc:
                elapsed = (datetime.now(UTC) - start).total_seconds()
                results.append(
                    {
                        "name": output_name,
                        "status": "error",
                        "error": str(exc),
                        "seconds": round(elapsed, 2),
                    }
                )
                emit({"kind": "error", "name": output_name, "reason": str(exc)})

    # If any collector errored, leave a sentinel so `status` and `query` know
    # this archive is partial.
    had_errors = any(r.get("status") == "error" for r in results)
    if had_errors:
        try:
            (archive_dir / ".incomplete").write_text("")
        except OSError as exc:
            emit({"kind": "archive_warning", "reason": f".incomplete write failed: {exc}"})

    meta = {
        "format_version": 1,
        "timestamp": datetime.now(UTC).isoformat(),
        "collectors": results,
    }
    meta_path = archive_dir / "meta.yaml"
    meta_tmp = meta_path.with_suffix(".yaml.tmp")
    try:
        meta_tmp.write_text(yaml.dump(meta, default_flow_style=False, sort_keys=False))
        meta_tmp.replace(meta_path)
    except OSError as exc:
        try:
            meta_tmp.unlink()
        except OSError:
            pass
        try:
            (archive_dir / ".incomplete").write_text("")
        except OSError:
            pass
        emit(
            {
                "kind": "archive_warning",
                "reason": f"meta.yaml write failed: {exc}",
                "results": results,
            }
        )

    return archive_dir, results
