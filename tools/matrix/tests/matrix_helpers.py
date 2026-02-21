"""Test helpers for matrix tests."""

from matrix import Construct


class FakeComponent:
    """Minimal component for testing — satisfies the Component protocol."""

    def __init__(
        self,
        name: str,
        requires: frozenset[str],
        provides: str,
        data=None,
    ):
        self.name = name
        self.requires = requires
        self.provides = provides
        self._data = data

    async def run(self, construct: Construct) -> str:
        if self._data is not None:
            return self._data
        return f"{self.name}-output"
