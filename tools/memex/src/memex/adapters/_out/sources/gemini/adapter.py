"""Google Gemini source adapter.

Parses Google Takeout exports containing Gemini conversation history.
The export format is an HTML file (`My Activity.html`) inside a zip,
structured as Material Design Lite cards — one outer-cell div per
conversation entry.

Handles both raw HTML files and Takeout zip archives.
"""

import hashlib
import re
import zipfile
from collections.abc import Iterator
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

from memex.domain.models import Fragment, Provenance

SOURCE_GEMINI = "gemini"


class GeminiAdapter:
    """Adapter for Google Gemini Takeout exports."""

    def can_handle(self, path: Path) -> bool:
        if path.suffix == ".html" and "activity" in path.name.lower():
            return True
        if path.suffix == ".zip":
            return self._is_gemini_zip(path)
        return False

    def _is_gemini_zip(self, path: Path) -> bool:
        try:
            with zipfile.ZipFile(path, "r") as zf:
                return any(
                    "Gemini" in n and n.endswith(".html")
                    for n in zf.namelist()
                )
        except (zipfile.BadZipFile, OSError):
            return False

    def source_kind(self) -> str:
        return SOURCE_GEMINI

    def ingest(self, path: Path) -> Iterator[Fragment]:
        if path.suffix == ".zip":
            yield from self._ingest_zip(path)
        else:
            yield from self._ingest_html(path)

    def _ingest_zip(self, path: Path) -> Iterator[Fragment]:
        with zipfile.ZipFile(path, "r") as zf:
            html_files = [
                n for n in zf.namelist()
                if "Gemini" in n and n.endswith(".html") and "Activity" in n
            ]
            for html_name in html_files:
                with zf.open(html_name) as f:
                    content = f.read().decode("utf-8", errors="replace")
                    yield from self._parse_html(content)

    def _ingest_html(self, path: Path) -> Iterator[Fragment]:
        content = path.read_text(encoding="utf-8", errors="replace")
        yield from self._parse_html(content)

    def _parse_html(self, html: str) -> Iterator[Fragment]:
        parser = _GeminiHTMLParser()
        body_start = html.find("<body")
        if body_start == -1:
            body_start = 0
        parser.feed(html[body_start:])

        if parser.current_convo:
            parser.conversations.append(parser.current_convo)

        for convo in parser.conversations:
            yield from self._convo_to_fragments(convo)

    def _convo_to_fragments(
        self, convo: list[tuple[str, str]]
    ) -> Iterator[Fragment]:
        content_parts = []
        timestamp = None

        for kind, text in convo:
            if kind == "content":
                content_parts.append(text)
            elif kind == "timestamp":
                timestamp = self._parse_timestamp(text)

        if not content_parts:
            return

        full_content = "\n\n".join(content_parts)
        content_hash = hashlib.sha256(full_content[:500].encode()).hexdigest()[:16]
        frag_id = f"gemini:{content_hash}"

        yield Fragment(
            id=frag_id,
            conversation_id=frag_id,
            role="assistant",
            content=full_content,
            provenance=Provenance(
                source_kind=SOURCE_GEMINI,
                source_id=frag_id,
                timestamp=timestamp,
            ),
        )

    def _parse_timestamp(self, text: str) -> datetime | None:
        # Timestamp text looks like: "Products: Gemini Apps...10 Apr 2026, 18:40:20 GMT-05:00"
        patterns = [
            r"(\d{1,2}\s+\w+\s+\d{4},\s+\d{2}:\d{2}:\d{2})",
            r"(\w+\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    return datetime.strptime(match.group(1), "%d %b %Y, %H:%M:%S")
                except ValueError:
                    try:
                        return datetime.strptime(match.group(1), "%b %d, %Y, %I:%M:%S %p")
                    except ValueError:
                        pass
        return None


class _GeminiHTMLParser(HTMLParser):
    """Parse Gemini Takeout HTML into conversation blocks."""

    def __init__(self):
        super().__init__()
        self.in_outer = False
        self.in_content = False
        self.in_caption = False
        self.current_text = ""
        self.conversations: list[list[tuple[str, str]]] = []
        self.current_convo: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if "outer-cell" in cls:
            if self.current_convo:
                self.conversations.append(self.current_convo)
            self.current_convo = []
        if "content-cell" in cls and "body-1" in cls and "text-right" not in cls:
            self.in_content = True
            self.current_text = ""
        if "caption" in cls:
            self.in_caption = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if self.in_content and tag == "div":
            self.in_content = False
            if self.current_text.strip():
                self.current_convo.append(("content", self.current_text.strip()))
        if self.in_caption and tag == "div":
            self.in_caption = False
            if self.current_text.strip():
                self.current_convo.append(("timestamp", self.current_text.strip()))

    def handle_data(self, data):
        if self.in_content or self.in_caption:
            self.current_text += data
