"""Agent — universal agent execution protocol.

Backend-agnostic. Adapters implement this for Claude, Google ADK, Ollama, etc.
The Agent already knows its system prompt — callers just send a prompt.
"""

from typing import Protocol

from matrix.domain.types import AgentResponse


class Agent(Protocol):
    """Execute a prompt and return a structured response."""

    async def run(self, prompt: str) -> AgentResponse: ...
