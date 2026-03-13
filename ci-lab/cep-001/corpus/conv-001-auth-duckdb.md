# Auth Token Storage Decision

**Date**: 2025-01-15
**Participants**: user, claude

user: We need to decide where to store auth tokens. Redis vs DuckDB vs SQLite.

claude: Let me analyze the trade-offs:

**Redis**: Fast, TTL support built-in, but requires a separate service. Good for distributed systems.

**DuckDB**: Columnar, great for analytics queries on token usage. Single-file, no server. But no built-in TTL — you'd need a cleanup job.

**SQLite**: Battle-tested, single-file, WAL mode for concurrent reads. But row-oriented, slower for analytical queries.

user: We're single-node for now. Analytics on token usage patterns matters — we want to query "which services consume the most tokens per hour?"

claude: Then DuckDB is the right choice. Single-file deployment matches your constraint. Columnar storage makes the analytics queries fast. You lose TTL automation but a simple cron job handles that.

**Decision**: DuckDB for auth token storage. Rationale: single-node deployment + analytics requirement on token usage patterns.

**Key fact**: The cleanup cron runs every 6 hours, purging tokens older than 24h.
