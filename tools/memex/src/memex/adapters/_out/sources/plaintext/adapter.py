"""Plaintext and document source adapter.

Handles:
- Text files: .md, .txt, .rst, .csv, .log, .json, .yaml, .yml, .toml, and source code
- JSONL files: .jsonl (each line parsed as JSON, one fragment per entry)
- PDF files: .pdf (via pymupdf)
- DOCX files: .docx (via python-docx)

Text files are split by markdown headings (## sections) into fragments.
JSONL splits by line (each JSON object → one fragment).
PDF splits by page. DOCX splits by heading paragraphs.
"""

import hashlib
import json
import re
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, model_validator

from memex.domain.models import Fragment, Provenance

# Extensions handled natively (no extra deps)
_TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".rst",
    ".csv",
    ".log",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".sh",
    ".bash",
    ".zsh",
    ".py",
    ".js",
    ".ts",
    ".rs",
    ".go",
    ".html",
    ".css",
    ".sql",
    ".xml",
}

# Structured line-delimited JSON (each line is a JSON object)
_JSONL_EXTENSIONS = {".jsonl"}

# Extensions requiring optional deps
_PDF_EXTENSIONS = {".pdf"}
_DOCX_EXTENSIONS = {".docx"}

# Minimum content length to create a fragment (skip empty/trivial sections)
_MIN_FRAGMENT_LENGTH = 50


class JsonlEntry(BaseModel):
    """Pydantic model for a single JSONL line.

    Accepts any JSON object and extracts text content + timestamp
    via validation. No manual field walking — declare the extraction
    logic once, Pydantic handles parsing and validation.
    """

    content: str
    timestamp: datetime | None = None
    raw: dict[str, Any] = {}

    @model_validator(mode="before")
    @classmethod
    def extract_fields(cls, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            return {"content": json.dumps(data, ensure_ascii=False), "raw": {}}

        # Extract text: try common fields, then nested message.content
        text = _extract_content(data)
        ts = _extract_ts(data)

        return {"content": text, "timestamp": ts, "raw": data}


def _extract_content(obj: dict) -> str:
    """Extract text from a JSON object via known field patterns."""
    # Direct text fields
    for field in ("content", "text", "message", "body", "description"):
        val = obj.get(field)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # Nested: message.content (Claude Code JSONL pattern)
    msg = obj.get("message")
    if isinstance(msg, dict):
        for field in ("content", "text"):
            val = msg.get(field)
            if isinstance(val, str) and val.strip():
                return val.strip()
            # content can be [{type: "text", text: "..."}]
            if isinstance(val, list):
                texts = [
                    block.get("text", "")
                    for block in val
                    if isinstance(block, dict) and block.get("type") == "text"
                ]
                if any(texts):
                    return "\n\n".join(t for t in texts if t)

    # Fallback: pretty-print
    return json.dumps(obj, indent=2, ensure_ascii=False)


def _extract_ts(obj: dict) -> datetime | None:
    """Extract timestamp from common JSON fields."""
    for field in ("timestamp", "created_at", "date", "time", "ts"):
        val = obj.get(field)
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except ValueError:
                continue
        if isinstance(val, (int, float)):
            try:
                return datetime.fromtimestamp(val, tz=UTC)
            except (ValueError, OSError):
                continue
    return None


def _stable_id(path: Path, section: str) -> str:
    """Deterministic fragment ID from file path + section identifier."""
    key = f"{path.resolve()}:{section}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _file_timestamp(path: Path) -> datetime:
    """Get file modification time as timezone-aware datetime."""
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)


class PlaintextAdapter:
    """Adapter for text files, markdown, PDF, and DOCX.

    Splits text files by markdown headings into fragments.
    PDF splits by page. DOCX splits by heading paragraphs.
    """

    SOURCE_KIND = "plaintext"

    def can_handle(self, path: Path) -> bool:
        """Check if this adapter can handle the given path."""
        suffix = path.suffix.lower()
        return suffix in _TEXT_EXTENSIONS | _JSONL_EXTENSIONS | _PDF_EXTENSIONS | _DOCX_EXTENSIONS

    def source_kind(self) -> str:
        return self.SOURCE_KIND

    def ingest(self, path: Path) -> Iterator[Fragment]:
        """Ingest a file and yield Fragments."""
        suffix = path.suffix.lower()
        if suffix in _PDF_EXTENSIONS:
            yield from self._ingest_pdf(path)
        elif suffix in _DOCX_EXTENSIONS:
            yield from self._ingest_docx(path)
        elif suffix in _JSONL_EXTENSIONS:
            yield from self._ingest_jsonl(path)
        else:
            yield from self._ingest_text(path)

    # ── Text / Markdown ───────────────────────────────────────────

    def _ingest_text(self, path: Path) -> Iterator[Fragment]:
        """Split text file by markdown headings into fragments.

        Files without headings become a single fragment.
        """
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="latin-1")

        if not content.strip():
            return

        timestamp = _file_timestamp(path)
        file_id = str(path.resolve())

        # Split by markdown headings (any level)
        sections = re.split(r"(?m)^(#{1,6}\s+.+)$", content)

        if len(sections) <= 1:
            # No headings — single fragment for the whole file
            yield self._make_fragment(
                path, file_id, "whole", path.name, content.strip(), timestamp
            )
            return

        # First section before any heading (preamble)
        preamble = sections[0].strip()
        if preamble and len(preamble) >= _MIN_FRAGMENT_LENGTH:
            yield self._make_fragment(
                path, file_id, "preamble", path.name, preamble, timestamp
            )

        # Heading + body pairs
        for i in range(1, len(sections), 2):
            heading = sections[i].strip()
            body = sections[i + 1].strip() if i + 1 < len(sections) else ""
            section_content = f"{heading}\n\n{body}".strip()

            if len(section_content) < _MIN_FRAGMENT_LENGTH:
                continue

            section_slug = re.sub(r"[^a-z0-9]+", "-", heading.lower().lstrip("#").strip())
            yield self._make_fragment(
                path, file_id, section_slug, heading.lstrip("#").strip(), section_content, timestamp
            )

    # ── JSONL ──────────────────────────────────────────────────────

    def _ingest_jsonl(self, path: Path) -> Iterator[Fragment]:
        """Parse JSONL — one fragment per JSON line.

        Uses JsonlEntry Pydantic model for parsing and field extraction.
        """
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="latin-1").splitlines()

        timestamp = _file_timestamp(path)
        file_id = str(path.resolve())

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry = JsonlEntry.model_validate(obj)

            if len(entry.content) < _MIN_FRAGMENT_LENGTH:
                continue

            # Curate raw: exclude content field (already in Fragment.content)
            curated_raw = {k: v for k, v in entry.raw.items() if k != "content"} if entry.raw else None
            yield self._make_fragment(
                path,
                file_id,
                f"line-{line_num}",
                f"{path.name}:{line_num}",
                entry.content,
                entry.timestamp or timestamp,
                metadata={"line": line_num, **(curated_raw or {})},
            )

    # ── PDF ────────────────────────────────────────────────────────

    def _ingest_pdf(self, path: Path) -> Iterator[Fragment]:
        """Extract text from PDF pages."""
        import pymupdf

        timestamp = _file_timestamp(path)
        file_id = str(path.resolve())

        doc = pymupdf.open(path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()

            if not text or len(text) < _MIN_FRAGMENT_LENGTH:
                continue

            yield self._make_fragment(
                path,
                file_id,
                f"page-{page_num + 1}",
                f"{path.name} — page {page_num + 1}",
                text,
                timestamp,
                metadata={"page": page_num + 1},
            )
        doc.close()

    # ── DOCX ───────────────────────────────────────────────────────

    def _ingest_docx(self, path: Path) -> Iterator[Fragment]:
        """Extract text from DOCX, split by headings."""
        import docx

        timestamp = _file_timestamp(path)
        file_id = str(path.resolve())

        doc = docx.Document(path)
        current_heading = path.name
        current_content: list[str] = []
        section_idx = 0

        for para in doc.paragraphs:
            if para.style and para.style.name and para.style.name.startswith("Heading"):
                # Flush previous section
                if current_content:
                    body = "\n\n".join(current_content).strip()
                    if len(body) >= _MIN_FRAGMENT_LENGTH:
                        yield self._make_fragment(
                            path, file_id, f"section-{section_idx}",
                            current_heading, body, timestamp,
                        )
                    section_idx += 1

                current_heading = para.text.strip() or path.name
                current_content = [f"# {current_heading}"]
            elif para.text.strip():
                current_content.append(para.text.strip())

        # Flush final section
        if current_content:
            body = "\n\n".join(current_content).strip()
            if len(body) >= _MIN_FRAGMENT_LENGTH:
                yield self._make_fragment(
                    path, file_id, f"section-{section_idx}",
                    current_heading, body, timestamp,
                )

    # ── Helpers ────────────────────────────────────────────────────

    def _make_fragment(
        self,
        path: Path,
        file_id: str,
        section: str,
        title: str,
        content: str,
        timestamp: datetime,
        metadata: dict[str, Any] | None = None,
    ) -> Fragment:
        frag_id = _stable_id(path, section)
        meta = {"title": title, "file": path.name}
        if metadata:
            meta.update(metadata)
        return Fragment(
            id=frag_id,
            conversation_id=file_id,
            role="document",
            content=content,
            provenance=Provenance(
                source_kind=self.SOURCE_KIND,
                source_id=f"{file_id}:{section}",
                timestamp=timestamp,
            ),
            metadata=meta,
        )
