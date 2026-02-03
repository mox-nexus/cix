# Observability

Make behavior visible by default.

## Why Observability Matters

Without observability:
- Can't debug when things go wrong
- Can't measure if changes help or hurt
- Users can't understand what's happening

**Goal**: Every extension and tool should answer:
- What happened?
- How long did it take?
- Did it succeed?
- Why did it fail?

---

## OpenTelemetry Basics

### Quick Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-tool")
```

### Local UI (Phoenix)

```python
import phoenix as px
px.launch_app()  # localhost:6006

from opentelemetry import trace
tracer = trace.get_tracer("my-tool")
```

---

## Minimum Attributes

Every span should capture:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `success` | bool | Did it work? |
| `duration_ms` | int | How long? |
| `error` | string | What went wrong? |

For LLM calls, add:
- `input_tokens`, `output_tokens`, `model`

For tool calls, add:
- `tool_name`, `tool_args` (truncated)

---

## By Extension Type

### Skills

```python
def trace_skill_activation(prompt: str, skills: list):
    with tracer.start_as_current_span("skill_check") as span:
        span.set_attribute("prompt", prompt[:200])

        for skill in skills:
            with tracer.start_as_current_span("skill_match") as skill_span:
                skill_span.set_attribute("skill_name", skill.name)
                matches = skill.matches(prompt)
                skill_span.set_attribute("activated", matches)
```

### Agents

```python
def run_agent(task: str):
    with tracer.start_as_current_span("agent_run") as span:
        span.set_attribute("task", task)

        while not done:
            with tracer.start_as_current_span("llm_call") as llm_span:
                response = call_llm(messages)
                llm_span.set_attribute("input_tokens", response.usage.input)
                llm_span.set_attribute("output_tokens", response.usage.output)

            for tool_call in response.tool_calls:
                with tracer.start_as_current_span("tool_call") as tool_span:
                    tool_span.set_attribute("tool_name", tool_call.name)
                    result = execute_tool(tool_call)
                    tool_span.set_attribute("success", not result.error)
```

### Hooks

```python
def trigger_hook(event: str, payload: dict):
    with tracer.start_as_current_span("hook_trigger") as span:
        span.set_attribute("event_type", event)

        for handler in handlers:
            with tracer.start_as_current_span("hook_handler") as h_span:
                h_span.set_attribute("handler_name", handler.name)
                result = handler.execute(payload)
                h_span.set_attribute("success", result.success)
```

### CLI Tools

```python
def search(query: str):
    with tracer.start_as_current_span("search") as span:
        span.set_attribute("query", query[:100])

        results = service.search(query)

        span.set_attribute("result_count", len(results))
        span.set_attribute("success", True)
        return results
```

---

## Structured Logging

For simpler needs:

```python
import structlog

log = structlog.get_logger()

def ingest(path: Path):
    log.info("ingest_started", path=str(path))

    try:
        count = service.ingest(path)
        log.info("ingest_completed", fragments=count)
    except Exception as e:
        log.error("ingest_failed", error=str(e))
        raise
```

---

## Backend Options

| Backend | Type | Best For |
|---------|------|----------|
| Phoenix | Local | Development, no cloud |
| Langfuse | Self-hosted | Production, open source |
| Console | Debug | Quick debugging |
| Datadog | Cloud | Enterprise |

---

## Common Gotchas

| Trap | Fix |
|------|-----|
| Missing parent spans | Always set parent for nested |
| Attribute size limits | Truncate to 500 chars |
| Not ending spans | Use context managers |
| Missing errors | Always `record_exception()` |
| Cardinality explosion | High-cardinality in spans, not metrics |
