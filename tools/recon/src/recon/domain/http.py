"""HttpResponse — domain value object for HTTP results.

Adapters construct HttpResponse from httpx.Response (or any transport);
collectors consume only the domain type. This keeps httpx out of the
application and domain layers — collectors never import httpx.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HttpResponse(BaseModel, frozen=True, arbitrary_types_allowed=True):
    """The minimal HTTP shape collectors need.

    `body` is raw bytes so binary content (PDFs, images) flows through
    without forced text decoding. `text` is the decoded string, eagerly
    resolved so it is safe to read multiple times. `iter_lines` is a
    hook for streaming responses; it may be None when the full body was
    buffered.
    """

    status_code: int
    headers: dict[str, str]
    body: bytes
    text: str
    url: str
    content_type: str
    iter_lines: Any = None  # Iterator[str] | None — opt-in streaming
