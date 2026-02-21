"""MockAgent for dry-run mode. No API calls.

Implements Agent protocol (run(prompt) → AgentResponse).
Simulates activation based on probe expectations:
- must_trigger probes: 90% chance of Skill tool call in response
- should_not_trigger probes: 10% chance

Returns structured AgentResponse with tool call dicts —
same shape as ClaudeAgent, so sensors work identically in mock and live mode.
"""

import random

from matrix import AgentResponse


class MockAgent:
    """Dry-run agent. Simulates realistic activation rates.

    Returns structured AgentResponse (not raw strings). Sensors see the
    same type in mock and live mode — no divergence.
    """

    def __init__(
        self,
        expected_skill: str = "build-eval",
        seed: int | None = None,
        expectations: dict[str, bool] | None = None,
    ):
        self._expected_skill = expected_skill
        self._rng = random.Random(seed)
        self._expectations = expectations or {}

    async def run(self, prompt: str) -> AgentResponse:
        """Simulate an agent interaction.

        If expectations were provided (by composition root), use them
        for realistic activation rates. Otherwise, always activate.
        """
        should_activate = self._expectations.get(prompt)

        if should_activate is None:
            # No expectation mapped — always activate (simple mode)
            return AgentResponse(
                content=f"I'll use the Skill tool to invoke {self._expected_skill} "
                f"to help with: {prompt[:50]}",
                tool_calls=({"name": "Skill", "input": {"skill": self._expected_skill}},),
            )

        # Stochastic mode: 90/10 split based on expectation
        rate = 0.9 if should_activate else 0.1
        activated = self._rng.random() < rate

        if activated:
            return AgentResponse(
                content=f"Let me use the Skill tool with {self._expected_skill} "
                f"for '{prompt[:40]}'",
                tool_calls=({"name": "Skill", "input": {"skill": self._expected_skill}},),
            )
        return AgentResponse(content=f"Here's a direct answer about '{prompt[:40]}'")
