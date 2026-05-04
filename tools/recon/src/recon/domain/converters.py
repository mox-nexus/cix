"""Document conversion port.

A converter takes the raw bytes of a document (HTML, PDF, DOCX, PPTX, XLSX,
EPub, image, CSV, JSON, XML, ZIP) plus its Content-Type and source URL,
and returns a title + markdown body. The domain knows the shape; adapters
pick the library (markitdown, pandoc, a hosted service).

Collectors consume ConversionResult; they never import the concrete adapter.
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel


class ConversionResult(BaseModel, frozen=True):
    """Outcome of converting a document to markdown.

    `title` is best-effort (HTML <title>, PDF metadata, DOCX properties, etc.).
    `text` is the markdown body — safe to store as-is in JSONL `content` fields.
    """

    title: str
    text: str


class DocumentConverter(Protocol):
    """Convert a document's bytes to structured markdown."""

    def convert(self, content: bytes, content_type: str, url: str) -> ConversionResult: ...
