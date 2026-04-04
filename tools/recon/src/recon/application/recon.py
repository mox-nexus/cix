"""Recon — the dispatch loop.

Iterates collector entries, dispatches by type via Protocol registry,
handles fan-out across catalog sources, writes JSONL output.

No direct adapter imports — hex arch clean.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from recon.domain.collector import Collector
from recon.domain.models import ReconConfig, SourceEntry


def substitute(template: str, variables: dict[str, str]) -> str:
    """Replace {key} placeholders in a template string.

    Shared across application and adapter layers. Single copy.
    """

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return variables.get(key, match.group(0))

    return re.sub(r"\{(\w+)\}", replacer, template)


def run(
    config: ReconConfig,
    collectors: dict[str, Collector],
    mission_dir: Path,
) -> Path:
    """Execute all collectors, produce an archive directory.

    Fan-out: if a collector has no source, it runs against every catalog entry.
    If a collector names a source, it runs against that source only.
    If there's no catalog, collectors run once with no source.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S-%f")
    archive_dir = mission_dir / "archive" / timestamp
    archive_dir.mkdir(parents=True, exist_ok=True)

    catalog: dict[str, SourceEntry] = {s.name: s for s in config.catalog}

    results: list[dict[str, Any]] = []

    for entry in config.collectors:
        collector = collectors.get(entry.type)
        if not collector:
            results.append({
                "name": entry.name,
                "status": "error",
                "error": f"No collector registered for type: {entry.type}",
            })
            print(f"  {entry.name}: ERROR — unknown type '{entry.type}'", file=sys.stderr)
            continue

        # Determine targets: pinned source, fan-out, or standalone
        if entry.source:
            if entry.source not in catalog:
                results.append({
                    "name": entry.name,
                    "status": "error",
                    "error": f"Source '{entry.source}' not in catalog. Available: {', '.join(sorted(catalog)) or '(none)'}",
                })
                print(f"  {entry.name}: ERROR — source '{entry.source}' not found", file=sys.stderr)
                continue
            targets = [(catalog[entry.source], entry.name)]
        elif config.catalog:
            targets = [(src, f"{entry.name}-{src.name}") for src in config.catalog]
        else:
            targets = [(None, entry.name)]

        for source, output_name in targets:
            start = datetime.now(timezone.utc)
            try:
                records = collector.collect(entry, source)
                if not records:
                    records = [{"_empty": True}]

                _write_jsonl(records, archive_dir / f"{output_name}.jsonl")

                elapsed = (datetime.now(timezone.utc) - start).total_seconds()
                results.append({
                    "name": output_name,
                    "status": "ok",
                    "file": f"{output_name}.jsonl",
                    "records": len(records),
                    "seconds": round(elapsed, 2),
                })
                print(f"  {output_name}: {len(records)} records", file=sys.stderr)

            except Exception as exc:
                elapsed = (datetime.now(timezone.utc) - start).total_seconds()
                results.append({
                    "name": output_name,
                    "status": "error",
                    "error": str(exc),
                    "seconds": round(elapsed, 2),
                })
                print(f"  {output_name}: ERROR — {exc}", file=sys.stderr)

    meta = {
        "format_version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "collectors": results,
    }
    meta_path = archive_dir / "meta.yaml"
    try:
        meta_path.write_text(yaml.dump(meta, default_flow_style=False, sort_keys=False))
    except OSError as exc:
        print(f"  WARNING: failed to write meta.yaml — {exc}", file=sys.stderr)

    return archive_dir


def _write_jsonl(records: list[dict[str, Any]], path: Path) -> None:
    """Write records as JSONL (one JSON object per line)."""
    with open(path, "w") as f:
        for record in records:
            f.write(json.dumps(record, default=str) + "\n")
