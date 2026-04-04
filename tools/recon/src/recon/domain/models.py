"""Recon domain models — pure, frozen Pydantic types.

No infrastructure dependencies. These flow through the hexagon.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

# --- Value Objects ---


class AuthConfig(BaseModel, frozen=True):
    """How to authenticate with a source.

    Use `header` for header-based auth (e.g., x-api-key).
    Use `param` for query-string auth (e.g., OpenAlex api_key).
    `env` names the environment variable holding the secret.
    """

    header: str = ""
    param: str = ""
    env: str = ""


class RateLimitConfig(BaseModel, frozen=True):
    """Per-source rate limiting via token bucket."""

    rps: float = 10.0
    burst: int = 3


# --- Source Entry ---


class SourceEntry(BaseModel, frozen=True):
    """A source in the catalog — where to look.

    API sources provide URL + auth + rate limits.
    Web sources provide URL + rate limits for page fetching.
    Local sources provide a filesystem path (used as cwd by CLI collectors).
    """

    name: str
    type: Literal["api", "web", "local"] = "api"
    url: str
    auth: AuthConfig = AuthConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    user_agent: str | None = None
    timeout: float = 60.0


# --- Collector Entry ---


class CollectorEntry(BaseModel, frozen=True):
    """A collection step — what to do.

    `type` discriminates which fields are relevant:
    - cli: `run`, `patterns`, `normalize`
    - api: `endpoint`, `params`, `method`, `response_format`, `extract`, `normalize`
    - web: `endpoint` (optional, appended to source URL)
    """

    name: str
    type: Literal["cli", "api", "web"]
    source: str | None = None

    # cli fields
    run: str | None = None
    patterns: list[str] | None = None

    # api fields
    endpoint: str | None = None
    params: dict[str, str] | None = None
    method: Literal["GET", "POST"] = "GET"
    response_format: Literal["json", "xml", "html", "text"] = "json"
    extract: str | None = None

    # shared: field mapping spec (output_col: "path.to.field|$transform")
    normalize: dict[str, str] | None = None


# --- Top-level Config ---


class ReconConfig(BaseModel, frozen=True):
    """One YAML file per mission. Catalog + collectors."""

    catalog: list[SourceEntry] = []
    collectors: list[CollectorEntry]
