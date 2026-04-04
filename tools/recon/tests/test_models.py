"""Tests for domain models — validation, defaults, edge cases."""

import pytest
from pydantic import ValidationError

from recon.domain.models import (
    AuthConfig,
    CollectorEntry,
    RateLimitConfig,
    ReconConfig,
    SourceEntry,
)


class TestAuthConfig:
    def test_defaults(self):
        auth = AuthConfig()
        assert auth.header == ""
        assert auth.param == ""
        assert auth.env == ""

    def test_header_auth(self):
        auth = AuthConfig(header="x-api-key", env="S2_API_KEY")
        assert auth.header == "x-api-key"

    def test_param_auth(self):
        auth = AuthConfig(param="api_key", env="OPENALEX_API_KEY")
        assert auth.param == "api_key"


class TestSourceEntry:
    def test_minimal(self):
        src = SourceEntry(name="test", url="https://example.com")
        assert src.type == "api"
        assert src.auth == AuthConfig()
        assert src.rate_limit.rps == 10.0

    def test_full(self):
        src = SourceEntry(
            name="s2",
            type="api",
            url="https://api.semanticscholar.org",
            auth=AuthConfig(header="x-api-key", env="S2_API_KEY"),
            rate_limit=RateLimitConfig(rps=0.33, burst=1),
            user_agent="test/1.0",
        )
        assert src.rate_limit.rps == 0.33
        assert src.user_agent == "test/1.0"

    def test_local_type(self):
        src = SourceEntry(name="tokio", type="local", url="/Users/dev/oss/tokio")
        assert src.type == "local"

    def test_git_type_rejected(self):
        with pytest.raises(ValidationError):
            SourceEntry(name="repo", type="git", url="https://github.com/x/y")


class TestCollectorEntry:
    def test_cli(self):
        entry = CollectorEntry(
            name="grep",
            type="cli",
            run="rg --json '{pattern}'",
            patterns=["fixme", "todo"],
        )
        assert entry.type == "cli"
        assert entry.source is None

    def test_api(self):
        entry = CollectorEntry(
            name="search",
            type="api",
            source="s2",
            endpoint="/paper/search",
            params={"query": "transformer attention", "limit": "20"},
            extract="data",
            normalize={"title": "title", "authors": "authors.*.name"},
        )
        assert entry.source == "s2"
        assert len(entry.normalize) == 2

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            CollectorEntry(name="bad", type="ftp")

    def test_old_types_rejected(self):
        with pytest.raises(ValidationError):
            CollectorEntry(name="old", type="command")
        with pytest.raises(ValidationError):
            CollectorEntry(name="old", type="http")


class TestReconConfig:
    def test_minimal(self):
        config = ReconConfig(collectors=[
            CollectorEntry(name="test", type="cli", run="echo hi"),
        ])
        assert config.catalog == []
        assert len(config.collectors) == 1

    def test_from_yaml_dict(self):
        """Simulates loading from YAML."""
        raw = {
            "catalog": [
                {"name": "s2", "url": "https://api.semanticscholar.org/graph/v1"},
            ],
            "collectors": [
                {
                    "name": "s2-search",
                    "type": "api",
                    "source": "s2",
                    "endpoint": "/paper/search",
                    "params": {"query": "test"},
                    "extract": "data",
                    "normalize": {"title": "title"},
                },
            ],
        }
        config = ReconConfig.model_validate(raw)
        assert config.catalog[0].name == "s2"
        assert config.collectors[0].normalize == {"title": "title"}

    def test_no_collectors_fails(self):
        with pytest.raises(ValidationError):
            ReconConfig.model_validate({"catalog": []})

    def test_collectors_only(self):
        """No catalog needed for CLI collectors."""
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "local", "type": "cli", "run": "ls"},
            ],
        })
        assert config.catalog == []

    def test_local_sources(self):
        """Local sources for CLI fan-out."""
        config = ReconConfig.model_validate({
            "catalog": [
                {"name": "repo-a", "type": "local", "url": "/tmp/a"},
                {"name": "repo-b", "type": "local", "url": "/tmp/b"},
            ],
            "collectors": [
                {"name": "scan", "type": "cli", "run": "echo hello"},
            ],
        })
        assert len(config.catalog) == 2
        assert config.catalog[0].type == "local"
