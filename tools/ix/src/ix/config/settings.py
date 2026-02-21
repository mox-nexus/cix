"""ix configuration.

Lab resolution: a lab is a directory containing experiment.yaml subdirectories.
  - Explicit: --lab <name>
  - Auto-detect: walk up from CWD looking for experiment.yaml in child dirs
"""

from pathlib import Path


def find_lab(lab_name: str | None = None) -> Path:
    """Resolve a lab directory.

    Resolution order:
    1. Explicit lab name → search for it relative to project root
    2. Walk up from CWD — if CWD is inside a lab, use it

    A lab is a directory that contains experiment subdirectories
    (each with an experiment.yaml).
    """
    if lab_name:
        root = find_project_root()
        candidate = root / lab_name
        if candidate.is_dir():
            return candidate
        raise FileNotFoundError(
            f"Lab '{lab_name}' not found at {candidate}.\nCreate it with: ix lab init {lab_name}"
        )

    current = Path.cwd()
    for parent in [current, *current.parents]:
        if is_lab(parent):
            return parent

    raise FileNotFoundError("No lab found. Create one with: ix lab init <name>")


def is_lab(path: Path) -> bool:
    """A directory is a lab if it contains at least one experiment.yaml in a subdirectory."""
    if not path.is_dir():
        return False
    for child in path.iterdir():
        if child.is_dir() and (child / "experiment.yaml").exists():
            return True
    return False


def find_project_root() -> Path:
    """Walk up from CWD to find project root.

    Prefers .git (true project root) over pyproject.toml (could be a tool subpackage).
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return current
