"""Matrix types: Artifact, Construct, Component, AgentResponse.

Kind-agnostic DAG orchestration types + agent response model.
Artifacts are self-describing data units following xDS TypedExtensionConfig.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, NamedTuple, Protocol, runtime_checkable

from pydantic import BaseModel


class TypedStruct(NamedTuple):
    """Self-describing output — component declares both type and value.

    Follows the xDS TypedExtensionConfig pattern. The component owns its
    output contract: type_url says what it is, value carries the data.

    NamedTuple for zero overhead, structural typing compatibility,
    and no import required for external consumers.
    """

    type_url: str
    value: Any


class ContractError(Exception):
    """Component's runtime type_url doesn't match its compile-time declaration."""


class Artifact(BaseModel, frozen=True):
    """Self-describing data unit in the Construct ledger.

    Follows the xDS TypedExtensionConfig pattern: every piece of data
    flowing through the DAG is typed, traceable, and replayable.

    type_url convention: <namespace>.v<version>/<resource>
      - matrix.v1/agent.response
      - ix.v1/eval.readings
      - test.v1/...
    """

    type_url: str
    producer: str
    data: Any
    id: str
    timestamp: datetime

    @staticmethod
    def create(*, type_url: str, producer: str, data: Any) -> Artifact:
        """Factory that stamps UUID + UTC timestamp."""
        return Artifact(
            type_url=type_url,
            producer=producer,
            data=data,
            id=str(uuid.uuid4()),
            timestamp=datetime.now(UTC),
        )


class Construct:
    """Append-only artifact ledger for DAG execution.

    Components append typed Artifacts. Downstream components query by type_url.
    The ledger IS the trace — self-describing, replayable execution history.
    """

    def __init__(self) -> None:
        self._ledger: list[Artifact] = []
        self._by_type: dict[str, list[Artifact]] = {}

    def append(self, artifact: Artifact) -> None:
        """Append an artifact to the ledger."""
        self._ledger.append(artifact)
        self._by_type.setdefault(artifact.type_url, []).append(artifact)

    def query(self, type_url: str) -> list[Artifact]:
        """All artifacts of the given type, in append order."""
        return list(self._by_type.get(type_url, []))

    def last(self, type_url: str) -> Artifact:
        """Most recent artifact of the given type. Raises on missing."""
        artifacts = self._by_type.get(type_url)
        if not artifacts:
            available = ", ".join(sorted(self._by_type)) or "(none)"
            raise LookupError(f"No artifact for type_url {type_url!r}. Available: {available}")
        return artifacts[-1]

    @property
    def ledger(self) -> tuple[Artifact, ...]:
        """Immutable snapshot of the full ledger."""
        return tuple(self._ledger)

    def __getitem__(self, type_url: str) -> Any:
        """Backward compat: construct["type_url"] returns last artifact's data."""
        return self.last(type_url).data

    def __contains__(self, type_url: str) -> bool:
        return type_url in self._by_type

    def kinds(self) -> frozenset[str]:
        return frozenset(self._by_type)

    def __len__(self) -> int:
        return len(self._by_type)


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
    consumes: frozenset[str]
    produces: str

    async def run(self, construct: Construct) -> TypedStruct:
        """Execute and return self-describing output.

        Returns TypedStruct(type_url, value) — the component owns its output
        contract. The Orchestrator validates type_url matches self.produces
        (double-entry bookkeeping) and unwraps value into an Artifact.
        """
        ...
