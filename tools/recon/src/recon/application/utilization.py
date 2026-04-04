"""Utilization controls — rate limiting for source access.

Injected into collectors that consume network resources.
Shared across collector types so API + Web hitting the same source
respect a single rate limit.
"""

from __future__ import annotations

import time

from recon.domain.models import SourceEntry


class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, rps: float, burst: int) -> None:
        self._rps = rps
        self._burst = burst
        self._tokens = float(burst)
        self._last = time.monotonic()

    def acquire(self) -> None:
        """Block until a token is available. Single-threaded only."""
        while True:
            now = time.monotonic()
            elapsed = now - self._last
            self._tokens = min(self._burst, self._tokens + elapsed * self._rps)
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                self._last = now
                return
            wait = (1.0 - self._tokens) / self._rps
            self._last = now
            time.sleep(wait)


class RateLimiter:
    """Per-source rate limiting. One bucket per source name.

    Shared across collectors — API and Web collectors hitting the same
    source share a single bucket, preventing combined over-utilization.
    """

    def __init__(self) -> None:
        self._buckets: dict[str, TokenBucket] = {}

    def acquire(self, source: SourceEntry) -> None:
        """Block until rate limit allows a request to this source."""
        if source.name not in self._buckets:
            rl = source.rate_limit
            self._buckets[source.name] = TokenBucket(rps=rl.rps, burst=rl.burst)
        self._buckets[source.name].acquire()
