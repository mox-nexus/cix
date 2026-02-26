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

    Usage::

        agent = AnthropicAgent(system_prompt="You are an expert.")
        response = await agent.run("Write a safe calculator...")
        # response.content has the text
    """

    def __init__(
        self,
        system_prompt: str | None = None,
        model: str = "sonnet",
        max_tokens: int = 4096,
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

    async def run(self, prompt: str) -> AgentResponse:
        """Single-turn API call. No tools, no multi-turn."""
        import anthropic

        client = anthropic.Anthropic(api_key=_resolve_api_key())
        response = client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=self._system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
        )

        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text

        usage = response.usage

        return AgentResponse(
            content=content,
            tokens_input=usage.input_tokens if usage else 0,
            tokens_output=usage.output_tokens if usage else 0,
        )
