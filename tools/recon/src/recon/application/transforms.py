"""Transforms — registered field-level transforms + normalize spec engine.

Normalize specs map output column names to source paths with optional transforms:
  title: title                          # direct field
  abstract: summary                     # rename
  pdf_url: "openAccessPdf.url"          # nested access
  authors: "authors.*.name"             # list-map
  abstract: "description|$html2text"    # access + transform

Path resolution uses glom. Our '*' list-map syntax translates to glom tuple specs.
The '|$transform' pipe syntax is ours — applied after path resolution.
"""

from __future__ import annotations

from collections.abc import Callable
from html.parser import HTMLParser
from typing import Any

from glom import GlomError, glom


# --- Transforms ---


class _TextExtractor(HTMLParser):
    """HTML text extractor via stdlib."""

    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"):
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._parts.append(data)


def html2text(html: str) -> str:
    """Strip HTML tags, scripts, styles. Preserve paragraph breaks."""
    if not html:
        return ""
    parser = _TextExtractor()
    parser.feed(html)
    lines = "".join(parser._parts).splitlines()
    return "\n".join(line.strip() for line in lines if line.strip())


def inverted_index(index: dict[str, list[int]] | None) -> str:
    """Reconstruct text from OpenAlex inverted index format."""
    if not index:
        return ""
    word_positions: list[tuple[int, str]] = []
    for word, positions in index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(word for _, word in word_positions)


def join(items: list | None, separator: str = ", ") -> str:
    """Join list elements into a string."""
    if not items:
        return ""
    return separator.join(str(item) for item in items)


def first(items: list | None) -> Any:
    """Return first element or None."""
    if not items:
        return None
    return items[0]


TRANSFORMS: dict[str, Callable] = {
    "$html2text": html2text,
    "$inverted_index": inverted_index,
    "$join": join,
    "$first": first,
}


def register_transform(name: str, fn: Callable) -> None:
    """Register a named transform (for adapter-layer transforms like $pdf2text)."""
    TRANSFORMS[name] = fn


# --- Normalize Spec Engine ---


def _build_glom_spec(path: str) -> Any:
    """Translate our path syntax to a glom spec.

    Simple:  "title"                         → "title"
    Dotted:  "openAccessPdf.url"             → "openAccessPdf.url"
    ListMap: "authors.*.name"                → ("authors", ["name"])
    Deep:    "authorships.*.author.name"     → ("authorships", ["author.name"])
    Bare:    "items.*"                       → "items"
    """
    if "*" not in path:
        return path

    if path == "*":
        return path  # glom iterates dict values — likely a config mistake, but valid

    if path.endswith(".*"):
        return path[:-2]

    parts = path.split(".*.", maxsplit=1)
    if len(parts) == 2:
        if "*" in parts[1]:
            msg = f"Nested list-maps not supported: {path!r}"
            raise ValueError(msg)
        return (parts[0], [parts[1]])

    return path


def resolve_path(data: Any, path: str) -> Any:
    """Navigate a dotted path with list-map support via '*'.

    Uses glom for path resolution with our '*' list-map syntax on top.
    """
    spec = _build_glom_spec(path)
    try:
        return glom(data, spec)
    except (GlomError, KeyError, TypeError):
        return None


def apply_normalize(raw: dict[str, Any], spec: dict[str, str]) -> dict[str, Any]:
    """Apply a normalize spec to a raw dict.

    Each spec entry is: output_column: "source.path|$transform"
    The pipe and transform are optional.
    """
    result: dict[str, Any] = {}
    for output_col, expr in spec.items():
        if "|" in expr:
            path, transform_name = expr.rsplit("|", 1)
            transform_name = transform_name.strip()
            path = path.strip()
        else:
            path = expr
            transform_name = None

        value = resolve_path(raw, path)

        if transform_name and transform_name in TRANSFORMS:
            value = TRANSFORMS[transform_name](value)

        result[output_col] = value

    return result
