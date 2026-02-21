"""MockRuntime — deterministic agent runtime for testing."""

from __future__ import annotations


class MockRuntime:
    """Returns canned responses. No API calls."""

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self._responses = responses or {}
        self._default = "Mock response"

    async def invoke(self, system: str, messages: list[dict]) -> str:
        """Return a canned response based on the last user message."""
        if messages:
            last = messages[-1].get("content", "")
            if last in self._responses:
                return self._responses[last]
        return self._default
