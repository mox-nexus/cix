"""Memex skill loader - loads skill documentation from package assets.

Skills are versioned with the package in src/memex/assets/skills/.
"""

from importlib import resources
from pathlib import Path


def _get_skill_files() -> resources.abc.Traversable:
    """Get the skills directory from package assets."""
    return resources.files("memex.assets") / "skills" / "memex"


def get_skill(reference: str | None = None) -> str:
    """Load skill content from package assets."""
    skill_dir = _get_skill_files()

    if reference:
        ref_file = skill_dir / "references" / f"{reference}.md"
        try:
            return ref_file.read_text()
        except FileNotFoundError:
            available = list_references()
            return f"Unknown reference: {reference}\nAvailable: {', '.join(available)}"

    skill_file = skill_dir / "SKILL.md"
    try:
        return skill_file.read_text()
    except FileNotFoundError:
        return "Skill not found."


def list_references() -> list[str]:
    """List available references."""
    skill_dir = _get_skill_files()
    refs_dir = skill_dir / "references"

    try:
        return [p.name.removesuffix(".md") for p in refs_dir.iterdir() if p.name.endswith(".md")]
    except (FileNotFoundError, TypeError):
        return []
