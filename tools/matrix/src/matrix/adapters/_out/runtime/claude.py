"""ClaudeAgent — Agent SDK adapter for the Agent protocol.

Uses claude-agent-sdk to provide full agentic capabilities:
tool use, multi-turn reasoning, and multi-agent orchestration.

Matrix's runtime layer IS an Agent SDK application. The DAG scheduler
sequences component execution; each component gets agent capabilities
through this adapter.

Requires: uv add claude-agent-sdk
"""

from __future__ import annotations

from matrix.domain.types import AgentResponse


class ClaudeAgent:
    """Implements Agent using the Claude Agent SDK.

    Each run() launches a Claude agent session. The agent already knows
    its system prompt — callers just provide the task prompt.

    Usage::

        agent = ClaudeAgent(system_prompt="You are an expert evaluator.")
        response = await agent.run("Evaluate this code...")
        # response.content, response.tool_calls, response.tokens_input, etc.
    """

    def __init__(
        self,
        system_prompt: str | None = None,
        max_turns: int = 1,
        allowed_tools: list[str] | None = None,
        plugins: list[dict] | None = None,
    ) -> None:
        try:
            import claude_agent_sdk  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "ClaudeAgent requires 'claude-agent-sdk'. Install with: uv add claude-agent-sdk"
            ) from e
        self._system_prompt = system_prompt
        self._max_turns = max_turns
        self._allowed_tools = allowed_tools or []
        self._plugins = plugins or []

    async def run(self, prompt: str) -> AgentResponse:
        """Execute a prompt via the Claude Agent SDK.

        Streams messages, extracts TextBlock + ToolUseBlock content,
        and captures usage/cost from ResultMessage.
        """
        from claude_agent_sdk import (
            AssistantMessage,
            ClaudeAgentOptions,
            ResultMessage,
            TextBlock,
            ToolUseBlock,
            query,
        )

        options = ClaudeAgentOptions(
            system_prompt=self._system_prompt,
            max_turns=self._max_turns,
            allowed_tools=self._allowed_tools,
            plugins=self._plugins,
        )

        content_parts: list[str] = []
        tool_calls: list[dict] = []
        result_msg = None

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        content_parts.append(block.text)
                    elif isinstance(block, ToolUseBlock):
                        tool_calls.append({"name": block.name, "input": block.input})
            elif isinstance(message, ResultMessage):
                result_msg = message

        usage = result_msg.usage if result_msg and hasattr(result_msg, "usage") else None

        return AgentResponse(
            content="".join(content_parts),
            tool_calls=tuple(tool_calls),
            duration_ms=getattr(result_msg, "duration_ms", 0) or 0,
            cost_usd=getattr(result_msg, "total_cost_usd", None),
            tokens_input=usage.get("input_tokens", 0) if isinstance(usage, dict) else 0,
            tokens_output=usage.get("output_tokens", 0) if isinstance(usage, dict) else 0,
            num_turns=getattr(result_msg, "num_turns", 0) or 0,
        )
