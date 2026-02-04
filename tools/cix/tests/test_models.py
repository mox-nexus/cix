"""Tests for domain models."""

from cix.domain.models import (
    Extension,
    ExtensionKind,
    Extensions,
    Package,
    Source,
)


class TestExtensions:
    """Tests for Extensions collection."""

    def test_total_empty(self):
        """Empty extensions should have total 0."""
        ext = Extensions()
        assert ext.total == 0

    def test_total_with_items(self):
        """Total counts all extension types."""
        ext = Extensions(
            skills=["s1", "s2"],
            agents=["a1"],
            hooks=["h1", "h2", "h3"],
        )
        assert ext.total == 6

    def test_is_empty_true(self):
        """Empty extensions should be marked as empty."""
        assert Extensions().is_empty is True

    def test_is_empty_false(self):
        """Non-empty extensions should not be marked as empty."""
        assert Extensions(skills=["s1"]).is_empty is False

    def test_summary_empty(self):
        """Empty extensions summary."""
        assert Extensions().summary == "empty"

    def test_summary_single_skill(self):
        """Summary with single skill."""
        assert Extensions(skills=["s1"]).summary == "1 skill"

    def test_summary_multiple_skills(self):
        """Summary with multiple skills."""
        assert Extensions(skills=["s1", "s2"]).summary == "2 skills"

    def test_summary_mixed(self):
        """Summary with multiple types."""
        ext = Extensions(skills=["s1"], agents=["a1", "a2"], hooks=["h1"])
        assert ext.summary == "1 skill, 2 agents, 1 hook"


class TestSource:
    """Tests for Source model."""

    def test_is_pinned_false(self):
        """Source without ref is not pinned."""
        src = Source(name="test", url="https://example.com")
        assert src.is_pinned is False

    def test_is_pinned_true(self):
        """Source with ref is pinned."""
        src = Source(name="test", url="https://example.com", ref="v1.0.0")
        assert src.is_pinned is True

    def test_default_false(self):
        """Default should be False by default."""
        src = Source(name="test", url="https://example.com")
        assert src.default is False


class TestPackage:
    """Tests for Package model."""

    def test_qualified_name(self, tmp_path):
        """Qualified name includes version."""
        pkg = Package(
            name="my-pkg",
            description="Test",
            version="2.0.0",
            path=tmp_path,
        )
        assert pkg.qualified_name == "my-pkg@2.0.0"

    def test_default_extensions(self, tmp_path):
        """Package has empty extensions by default."""
        pkg = Package(
            name="my-pkg",
            description="Test",
            version="1.0.0",
            path=tmp_path,
        )
        assert pkg.extensions.is_empty


class TestExtension:
    """Tests for Extension model."""

    def test_display_name(self):
        """Display name includes kind."""
        ext = Extension(name="test", kind=ExtensionKind.SKILL)
        assert ext.display_name == "test [skill]"

    def test_extension_kinds(self):
        """All extension kinds are valid."""
        assert ExtensionKind.SKILL == "skill"
        assert ExtensionKind.AGENT == "agent"
        assert ExtensionKind.HOOK == "hook"
        assert ExtensionKind.MCP == "mcp"


class TestInstallation:
    """Tests for Installation model."""

    def test_id(self, sample_installation):
        """Installation ID is source/package."""
        assert sample_installation.id == "test-source/test-package"

    def test_age_days(self, sample_installation):
        """Age should be 0 for new installation."""
        assert sample_installation.age_days == 0
