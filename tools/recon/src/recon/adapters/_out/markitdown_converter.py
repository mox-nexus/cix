"""MarkitdownConverter — DocumentConverter adapter using Microsoft's markitdown.

Handles HTML, PDF, DOCX, PPTX, XLSX, EPub, CSV, JSON, XML, ZIP, images (OCR),
audio (transcription), YouTube URLs, and more. Installed via `markitdown[all]`
which pulls the format-specific plugins (pdfminer, python-docx, python-pptx,
openpyxl, pillow, speechrecognition, yt-dlp, etc.).

Lazy-imports markitdown so plain `import recon` stays fast.
"""

from __future__ import annotations

import io

from recon.domain.converters import ConversionResult
from recon.domain.exceptions import CollectionError


class MarkitdownConverter:
    """Convert document bytes via markitdown."""

    def convert(self, content: bytes, content_type: str, url: str) -> ConversionResult:
        from markitdown import MarkItDown

        try:
            result = MarkItDown().convert_stream(io.BytesIO(content), url=url)
        except Exception as exc:
            msg = f"markitdown conversion failed for {url}: {exc}"
            raise CollectionError(msg) from exc

        if result is None:
            return ConversionResult(title="", text="")

        return ConversionResult(
            title=(getattr(result, "title", "") or ""),
            text=(getattr(result, "text_content", "") or ""),
        )
