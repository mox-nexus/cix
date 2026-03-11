# Rate Limiting Strategy

**Date**: 2025-01-20
**Participants**: yza, claude

yza: We're seeing 429s from the Claude API during peak hours. Need a rate limiting strategy.

claude: Current behavior: you're hitting the API directly with no client-side rate control. The 429s are Anthropic's server-side limits pushing back.

Three approaches:
1. **Token bucket** — smooth, handles bursts, standard approach
2. **Sliding window** — simpler, but bursty at window boundaries
3. **Adaptive backoff** — responds to 429s dynamically

yza: We need burst tolerance. Sometimes 10 requests arrive in 100ms from different users.

claude: Token bucket with burst capacity. Configure:
- Rate: 40 requests/minute (under the 50/min limit)
- Burst: 15 (absorb spikes without queuing)
- Retry: exponential backoff starting at 500ms, max 3 retries

**Decision**: Token bucket rate limiter. Rate=40/min, burst=15, exponential backoff from 500ms.

yza: What about per-user fairness?

claude: Add a second tier: per-user bucket at 10/min with burst of 5. Global bucket catches the aggregate; per-user prevents one heavy user from starving others.

**Final config**: Two-tier token bucket. Global: 40/min burst 15. Per-user: 10/min burst 5.
