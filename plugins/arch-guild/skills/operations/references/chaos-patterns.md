# Chaos Engineering Patterns

Operational scaffolds for chaos experiments. Not the theory (Claude knows that) — the templates and checklists for actually running them.

## Steady State Hypothesis

Before breaking things, define "normal" so you can measure deviation:

```yaml
steady_state:
  metrics:
    - name: error_rate
      threshold: "< 1%"
    - name: p99_latency
      threshold: "< 500ms"
    - name: availability
      threshold: "> 99.9%"

  assertions:
    - "Users can complete [critical path]"
    - "[Key operation] completes within [SLA]"
```

## Experiment Format

```yaml
experiment:
  name: "{What you're testing}"
  hypothesis: "When [failure], then [service] will [expected behavior]"

  steady_state:
    - "{Metric 1} {operator} {threshold}"
    - "{Metric 2} {operator} {threshold}"

  method:
    - action: "{Failure injection}"
      duration: "{How long}"

  expected:
    - "{Circuit breaker opens after N failures}"
    - "{Fallback behavior activates}"
    - "{Recovery within Ns of restoration}"

  abort_if:
    - "Error rate > 5%"
    - "Customer impact detected"
    - "On-call paged"
    - "Monitoring unhealthy"
```

## GameDay Checklist

### Before

```
□ Rollback procedure documented and tested
□ Monitoring dashboards open
□ Team in war room (or channel)
□ Customer support notified
□ No other changes scheduled
□ Blast radius level agreed (1-5)
```

### During

```
□ Start small, escalate gradually
□ Monitor metrics continuously
□ Document observations real-time
□ Stop immediately if unexpected
```

### After

```
□ Return to steady state verified
□ Document findings
□ Create action items
□ Update runbooks
□ Share learnings
```

## GameDay Report Template

```markdown
# GameDay: [Service] [Date]

## Hypothesis
If [failure], then [service] will [expected behavior].

## Scope
- Services: [list]
- Failure type: [type]
- Duration: [time]
- Blast radius level: [1-5]

## Steady State (Pre-Experiment)
- Error rate: [measured]
- p99 latency: [measured]
- Throughput: [measured]

## Results
- Hypothesis confirmed/rejected: [which]
- Actual behavior: [what happened]
- Recovery time: [measured]

## Surprises
- [Things that happened that we didn't expect]

## Action Items
- [ ] [Finding → action → owner]
```

## Blast Radius Levels

```
Level 1: Single instance, non-critical path → Start here
Level 2: Single instance, critical path
Level 3: Multiple instances, single AZ
Level 4: Entire AZ
Level 5: Cross-region (extreme caution)
```

Graduate from each level only after confirming steady state at the current level.
