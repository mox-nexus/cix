"""Shared fixtures for cix tests."""

from datetime import datetime

import pytest
from cix.domain.models import Extensions, Installation, Package, Source


@pytest.fixture
def sample_source():
    """Sample source for testing."""
    return Source(
        name="test-source",
        url="https://github.com/test/repo",
        default=True,
    )


@pytest.fixture
def sample_package(tmp_path):
    """Sample package for testing."""
    # Create package directory structure
    pkg_path = tmp_path / "test-package"
    pkg_path.mkdir()
    (pkg_path / ".claude-plugin").mkdir()
    (pkg_path / ".claude-plugin" / "plugin.json").write_text('{"name": "test-package"}')
    (pkg_path / "skills").mkdir()
    (pkg_path / "skills" / "test-skill").mkdir()

    return Package(
        name="test-package",
        description="A test package",
        version="1.0.0",
        path=pkg_path,
        extensions=Extensions(skills=["test-skill"]),
    )


@pytest.fixture
def sample_installation(sample_source, sample_package):
    """Sample installation for testing."""
    return Installation(
        package=sample_package,
        source=sample_source,
        installed_at=datetime.now(),
        commit="abc123",
        target="claude-code",
    )
