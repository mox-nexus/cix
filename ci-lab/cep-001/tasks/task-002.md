---
id: task-002
category: specific-detail
expectation: must_trigger
expected_command: dig
---
Search memex for the rate limiting strategy. Based on what you find, generate the following YAML config file with the exact numbers from the decision.

```yaml
# rate-limiter.yaml
algorithm: ""              # algorithm name (e.g. sliding window, token bucket)
tiers: 0                   # number of tiers
global_rate_per_min: 0     # global tier: requests per minute
global_burst: 0            # global tier: burst capacity
per_user_rate_per_min: 0   # per-user tier: requests per minute
per_user_burst: 0          # per-user tier: burst capacity
backoff_initial_ms: 0      # initial backoff in milliseconds
```
