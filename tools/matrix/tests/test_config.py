"""Tests for Matrix config composition — types, sources, loading."""

import pytest
from matrix.adapters._out.config.yaml_source import YamlConfigSource
from matrix.composition.config import deep_merge, load_config
from matrix.domain.config import Config, MatrixConfig, RuntimeSettings
from pydantic import BaseModel, ConfigDict, ValidationError

# --- Test client schema ---


class SampleClientConfig(BaseModel):
    """Minimal client config for testing."""

    model_config = ConfigDict(frozen=True)

    trials: int = 5
    sensor: str = "activation"


# --- deep_merge ---


class TestDeepMerge:
    def test_flat_override(self):
        assert deep_merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_nested_override(self):
        base = {"matrix": {"runtime": {"model": "old"}}}
        override = {"matrix": {"runtime": {"model": "new"}}}
        result = deep_merge(base, override)
        assert result["matrix"]["runtime"]["model"] == "new"

    def test_nested_partial_override(self):
        """Override one nested key without clobbering siblings."""
        base = {"matrix": {"runtime": {"model": "old", "max_tokens": 2048}}}
        override = {"matrix": {"runtime": {"model": "new"}}}
        result = deep_merge(base, override)
        assert result["matrix"]["runtime"]["model"] == "new"
        assert result["matrix"]["runtime"]["max_tokens"] == 2048

    def test_list_replaces(self):
        """Lists replace entirely — no merging."""
        assert deep_merge({"a": [1, 2]}, {"a": [3]}) == {"a": [3]}

    def test_new_keys_added(self):
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_empty_override(self):
        assert deep_merge({"a": 1}, {}) == {"a": 1}

    def test_empty_base(self):
        assert deep_merge({}, {"a": 1}) == {"a": 1}

    def test_both_empty(self):
        assert deep_merge({}, {}) == {}


# --- MatrixConfig defaults ---


class TestMatrixConfig:
    def test_defaults(self):
        config = MatrixConfig()
        assert config.runtime.model == "claude-sonnet-4-5-20250929"
        assert config.runtime.max_tokens == 2048

    def test_custom_runtime(self):
        config = MatrixConfig(runtime=RuntimeSettings(model="gpt-4o", max_tokens=4096))
        assert config.runtime.model == "gpt-4o"
        assert config.runtime.max_tokens == 4096

    def test_frozen(self):
        config = MatrixConfig()
        with pytest.raises(ValidationError):
            config.runtime = RuntimeSettings(model="changed")


# --- Config[C] composition ---


class TestConfig:
    def test_compose_with_client(self):
        config = Config(client=SampleClientConfig(trials=10))
        assert config.matrix.runtime.model == "claude-sonnet-4-5-20250929"
        assert config.client.trials == 10

    def test_matrix_defaults_when_absent(self):
        """Matrix section uses defaults when not explicitly provided."""
        config = Config(client=SampleClientConfig())
        assert config.matrix == MatrixConfig()

    def test_custom_matrix(self):
        config = Config(
            matrix=MatrixConfig(runtime=RuntimeSettings(max_tokens=8192)),
            client=SampleClientConfig(),
        )
        assert config.matrix.runtime.max_tokens == 8192
        assert config.client.sensor == "activation"

    def test_frozen(self):
        config = Config(client=SampleClientConfig())
        with pytest.raises(ValidationError):
            config.client = SampleClientConfig(trials=99)


# --- YamlConfigSource ---


class TestYamlConfigSource:
    def test_reads_yaml(self, tmp_path):
        f = tmp_path / "config.yaml"
        f.write_text("matrix:\n  runtime:\n    model: test-model\n")
        source = YamlConfigSource(f)
        data = source.read()
        assert data["matrix"]["runtime"]["model"] == "test-model"

    def test_missing_file_returns_empty(self, tmp_path):
        source = YamlConfigSource(tmp_path / "nonexistent.yaml")
        assert source.read() == {}

    def test_empty_file_returns_empty(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text("")
        source = YamlConfigSource(f)
        assert source.read() == {}

    def test_non_dict_returns_empty(self, tmp_path):
        """YAML that parses to a scalar or list returns empty dict."""
        f = tmp_path / "scalar.yaml"
        f.write_text("just a string")
        source = YamlConfigSource(f)
        assert source.read() == {}


# --- load_config ---


class TestLoadConfig:
    def test_no_files_uses_defaults(self, tmp_path):
        """When no config files exist, Pydantic defaults apply."""
        config = load_config(
            SampleClientConfig,
            client_key="ix",
            sources=[tmp_path / "nonexistent.yaml"],
        )
        assert config.matrix == MatrixConfig()
        assert config.client.trials == 5

    def test_single_source(self, tmp_path):
        f = tmp_path / "matrix.yaml"
        f.write_text("matrix:\n  runtime:\n    model: custom-model\nix:\n  trials: 20\n")
        config = load_config(SampleClientConfig, client_key="ix", sources=[f])
        assert config.matrix.runtime.model == "custom-model"
        assert config.client.trials == 20

    def test_project_overrides_user(self, tmp_path):
        """Later sources override earlier ones."""
        user = tmp_path / "user.yaml"
        user.write_text("matrix:\n  runtime:\n    model: user-model\nix:\n  trials: 10\n")

        project = tmp_path / "project.yaml"
        project.write_text("matrix:\n  runtime:\n    model: project-model\n")

        config = load_config(SampleClientConfig, client_key="ix", sources=[user, project])
        assert config.matrix.runtime.model == "project-model"
        assert config.client.trials == 10  # not overridden by project

    def test_custom_client_key(self, tmp_path):
        f = tmp_path / "matrix.yaml"
        f.write_text("radix:\n  trials: 42\n")
        config = load_config(SampleClientConfig, client_key="radix", sources=[f])
        assert config.client.trials == 42

    def test_partial_override_preserves_sibling(self, tmp_path):
        """Override model but keep max_tokens default."""
        f = tmp_path / "matrix.yaml"
        f.write_text("matrix:\n  runtime:\n    model: fast-model\n")
        config = load_config(SampleClientConfig, client_key="ix", sources=[f])
        assert config.matrix.runtime.model == "fast-model"
        assert config.matrix.runtime.max_tokens == 2048  # default preserved
