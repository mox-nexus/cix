"""AnthropicAgent — simple single-turn API adapter.

For experiments that need a single prompt->response without tool use,
multi-turn reasoning, or agentic capabilities. Uses the Anthropic SDK
directly — no subprocess, no Claude Code.

ClaudeAgent is for agentic sessions. AnthropicAgent is for simple calls.

Requires: uv add anthropic
"""

from __future__ import annotations

import os
from pathlib import Path

from matrix.domain.types import AgentResponse

# Short name -> full model ID
_MODEL_ALIASES = {
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514",
    "haiku": "claude-haiku-4-5-20251001",
}

_SECRETS_PATH = Path.home() / ".secrets" / "claude-api"


def _resolve_api_key() -> str:
    """Resolve API key: ~/.secrets/claude-api > ANTHROPIC_API_KEY env var."""
    if _SECRETS_PATH.exists():
        return _SECRETS_PATH.read_text().strip()
    return os.environ.get("ANTHROPIC_API_KEY", "")


def _resolve_model(model: str) -> str:
    """Resolve short model name to full ID."""
    return _MODEL_ALIASES.get(model, model)


class AnthropicAgent:
    """Single-turn agent using the Anthropic API directly.

    Supports optional tool definitions — the API returns tool_use blocks
    when the model decides to invoke a tool. Tool results are NOT executed;
    the response captures the model's intent (tool name + input).

    Usage::

        agent = AnthropicAgent(system_prompt="You are an expert.")
        response = await agent.run("Write a safe calculator...")
        # response.content, response.tool_calls
    """

    def __init__(
        self,
        system_prompt: str | None = None,
        model: str = "sonnet",
        max_tokens: int = 4096,
        allowed_tools: list[str] | None = None,
        temperature: float | None = None,
    ) -> None:
        try:
            import anthropic  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "AnthropicAgent requires 'anthropic'. Install with: uv add anthropic"
            ) from e
        self._system_prompt = system_prompt
        self._model = _resolve_model(model)
        self._max_tokens = max_tokens
        self._allowed_tools = allowed_tools or []
        self._temperature = temperature

    async def run(self, prompt: str) -> AgentResponse:
        """Single-turn API call with optional tool use."""
        import anthropic

        client = anthropic.Anthropic(api_key=_resolve_api_key())

        kwargs: dict = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "system": self._system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
        }

        if self._allowed_tools:
            kwargs["tools"] = [_tool_definition(name) for name in self._allowed_tools]

        if self._temperature is not None:
            kwargs["temperature"] = self._temperature

        response = client.messages.create(**kwargs)

        content = ""
        tool_calls: list[dict] = []
        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append({"name": block.name, "input": block.input})

        usage = response.usage

        return AgentResponse(
            content=content,
            tool_calls=tuple(tool_calls),
            tokens_input=usage.input_tokens if usage else 0,
            tokens_output=usage.output_tokens if usage else 0,
        )


# --- Tool Definitions ---

_TOOL_SCHEMAS: dict[str, dict] = {
    "Skill": {
        "name": "Skill",
        "description": "Invoke a specialized skill by name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "skill": {
                    "type": "string",
                    "description": "The skill name to invoke",
                },
                "args": {
                    "type": "string",
                    "description": "Optional arguments for the skill",
                },
            },
            "required": ["skill"],
        },
    },
    "memex": {
        "name": "memex",
        "description": "Execute a memex command to search, ingest, or explore knowledge artifacts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The memex subcommand (dig, keyword, semantic, ingest, backfill)",
                },
                "query": {
                    "type": "string",
                    "description": "Search query or path argument",
                },
                "options": {
                    "type": "object",
                    "description": "Additional options (limit, source_kind, etc.)",
                },
            },
            "required": ["command"],
        },
    },
    "nexus": {
        "name": "nexus",
        "description": "Execute a nexus command to manage knowledge artifacts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The nexus subcommand (excavate, locate, survey, absorb, connect, trace)",
                },
                "query": {
                    "type": "string",
                    "description": "Search query, identifier, or path argument",
                },
                "options": {
                    "type": "object",
                    "description": "Additional options",
                },
            },
            "required": ["command"],
        },
    },
    "memex": {
        "name": "memex",
        "description": "Query and manage your AI conversation history.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The memex subcommand (dig, keyword, semantic, thread, timeline, similar, trail, ingest, backfill, rebuild, reset, status, init, query, sql, corpus, sources, schema)",
                },
                "query": {
                    "type": "string",
                    "description": "Search query, conversation ID, trail name, SQL query, or path argument",
                },
                "options": {
                    "type": "object",
                    "description": "Additional options (limit, source, format, etc.)",
                },
            },
            "required": ["command"],
        },
    },
}


def _tool_definition(name: str) -> dict:
    """Look up a tool definition by name. Falls back to a generic schema."""
    if name in _TOOL_SCHEMAS:
        return _TOOL_SCHEMAS[name]
    return {
        "name": name,
        "description": f"Invoke the {name} tool.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    }
