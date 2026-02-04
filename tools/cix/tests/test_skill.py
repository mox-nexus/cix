"""Tests for skill loader."""

from cix import skill


class TestSkillLoader:
    """Tests for skill.py module."""

    def test_get_skill_returns_content(self):
        """get_skill returns SKILL.md content."""
        content = skill.get_skill()
        assert "# cix Skill" in content
        assert "## When to Use" in content

    def test_get_skill_with_reference(self):
        """get_skill with reference returns specific content."""
        content = skill.get_skill("sources")
        assert "# Source Reference" in content
        assert "## Adding Sources" in content

    def test_get_skill_invalid_reference(self):
        """get_skill with invalid reference returns error message."""
        content = skill.get_skill("nonexistent")
        assert "Unknown reference: nonexistent" in content

    def test_list_references(self):
        """list_references returns available references."""
        refs = skill.list_references()
        assert "sources" in refs
        assert "install" in refs
        assert len(refs) >= 2
