"""Matrix types: Construct, Component, AgentResponse.

Kind-agnostic DAG orchestration types + agent response model.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel


class Construct:
    """Append-only result store for DAG execution.

    Components read by kind key, engine writes after each component.
    Thin wrapper over dict with informative errors.
    """

    def __init__(self) -> None:
        self._results: dict[str, Any] = {}

    def __getitem__(self, kind: str) -> Any:
        try:
            return self._results[kind]
        except KeyError:
            available = ", ".join(sorted(self._results)) or "(none)"
            raise LookupError(f"No result for kind {kind!r}. Available: {available}")

    def __contains__(self, kind: str) -> bool:
        return kind in self._results

    def kinds(self) -> frozenset[str]:
        return frozenset(self._results)

    def __len__(self) -> int:
        return len(self._results)


class AgentResponse(BaseModel, frozen=True):
    """Structured response from an agent execution.

    Captures everything the Agent SDK returns: content, tool calls,
    token usage, timing, cost, and turn count. Replaces the old
    string-only return that threw away structured SDK data.

    tool_calls are plain dicts ({name, input}) — no wrapper type.
    Stays flat for DataFrame compatibility.
    """

    content: str = ""
    tool_calls: tuple[dict, ...] = ()
    tokens_input: int = 0
    tokens_output: int = 0
    duration_ms: int = 0
    cost_usd: float | None = None
    num_turns: int = 0


@runtime_checkable
class Component(Protocol):
    """A processing unit in the DAG. Structural typing — implement without importing matrix."""

    name: str
    requires: frozenset[str]
    provides: str

    async def run(self, construct: Construct) -> Any:
        """Process the construct and return raw data.

        The engine stores the return value in the construct under self.provides.
        To halt execution, raise an exception.
        """
        ...
