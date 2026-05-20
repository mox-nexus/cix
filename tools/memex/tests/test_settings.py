"""Tests for configuration resolution."""

import os

from memex.config.settings import Settings, _find_local_memex_dir, _parse_toml


class TestParseToml:
    def test_parses_valid_toml(self, tmp_path):
        config = tmp_path / "config.toml"
        config.write_text("""
[corpus]
path = "/custom/path"

[embedding]
onnx_batch_size = 8
onnx_threads = 4
provider = "coreml"

[ingest]
batch_size = 200

[search]
rerank_by_default = false
semantic_weight = 0.8
""")
        result = _parse_toml(config)
        assert result["corpus_path"] == "/custom/path"
        assert result["onnx_batch_size"] == 8
        assert result["onnx_threads"] == 4
        assert result["onnx_provider"] == "coreml"
        assert result["batch_size"] == 200
        assert result["rerank_by_default"] is False
        assert result["semantic_weight"] == 0.8

    def test_missing_file_returns_empty(self, tmp_path):
        assert _parse_toml(tmp_path / "nonexistent.toml") == {}

    def test_invalid_toml_returns_empty(self, tmp_path):
        config = tmp_path / "bad.toml"
        config.write_text("not valid toml {{{")
        assert _parse_toml(config) == {}

    def test_unknown_keys_ignored(self, tmp_path):
        config = tmp_path / "config.toml"
        config.write_text("""
[corpus]
path = "/test"

[unknown_section]
foo = "bar"
""")
        result = _parse_toml(config)
        assert result["corpus_path"] == "/test"
        assert "foo" not in result


class TestSettings:
    def teardown_method(self):
        # Clean up any env vars we set
        for key in list(os.environ):
            if key.startswith("MEMEX_"):
                del os.environ[key]

    def test_defaults(self):
        s = Settings()
        assert s.onnx_batch_size == 4
        assert s.onnx_threads == 2
        assert s.onnx_provider == "auto"
        assert s.rerank_by_default is True
        assert s.semantic_weight == 0.6

    def test_env_vars_override(self):
        os.environ["MEMEX_ONNX_BATCH_SIZE"] = "16"
        os.environ["MEMEX_SEMANTIC_WEIGHT"] = "0.9"
        s = Settings()
        assert s.onnx_batch_size == 16
        assert s.semantic_weight == 0.9

    def test_corpus_path_default_is_global(self, monkeypatch, tmp_path):
        """Default corpus path points to global .memex/ when no local store exists."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("MEMEX_FORCE_GLOBAL", raising=False)
        monkeypatch.delenv("MEMEX_CORPUS_PATH", raising=False)
        s = Settings()
        # Path may or may not be expanded, but must end with .memex/corpus.duckdb
        assert str(s.corpus_path).endswith(".memex/corpus.duckdb")
        assert ".memex" in s.corpus_path.parts


class TestFindLocalMemexDir:
    def test_returns_none_when_force_global(self, monkeypatch):
        monkeypatch.setenv("MEMEX_FORCE_GLOBAL", "1")
        assert _find_local_memex_dir() is None

    def test_returns_none_when_no_local_dir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("MEMEX_FORCE_GLOBAL", raising=False)
        assert _find_local_memex_dir() is None

    def test_finds_local_dir(self, tmp_path, monkeypatch):
        local_memex = tmp_path / ".memex"
        local_memex.mkdir()
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("MEMEX_FORCE_GLOBAL", raising=False)
        result = _find_local_memex_dir()
        assert result is not None
        assert result.name == ".memex"

    def test_walks_up_to_find_dir(self, tmp_path, monkeypatch):
        local_memex = tmp_path / ".memex"
        local_memex.mkdir()
        subdir = tmp_path / "src" / "deep"
        subdir.mkdir(parents=True)
        monkeypatch.chdir(subdir)
        monkeypatch.delenv("MEMEX_FORCE_GLOBAL", raising=False)
        result = _find_local_memex_dir()
        assert result is not None
        assert result == local_memex
