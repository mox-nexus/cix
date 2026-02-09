# Observability for Extensions

Make extension behavior measurable, debuggable, and controllable.

---

## Contents

- [Claude Code Native Telemetry](#claude-code-native-telemetry)
- [Hook-Based Observability](#hook-based-observability)
- [OTel Implementation](#otel-implementation)
- [GenAI Semantic Conventions](#genai-semantic-conventions)
- [Per-Extension Spans](#per-extension-spans)
- [Backend Options](#backend-options)
- [Gotchas](#gotchas)

---

## Claude Code Native Telemetry

Enable with environment variables:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Events emitted natively:**

| Event | Description |
|-------|-------------|
| `claude_code.user_prompt` | User submits prompt |
| `claude_code.tool_result` | Tool completes |
| `claude_code.api_request` | API call made |
| `claude_code.api_error` | API call failed |
| `claude_code.tool_decision` | Permission decision |

**Architecture insight:** Claude Agent SDK uses IPC/WebSocket to communicate with Claude Code CLI, not direct HTTP to api.anthropic.com. Traditional HTTP monitoring tools are blind to this layer. You need hook-based or SDK-level observability.

---

## Hook-Based Observability

The most flexible approach for Claude Code plugins.

### Configuration

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [
        { "type": "command", "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/observe.py --event PreToolUse" }
      ]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [
        { "type": "command", "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/observe.py --event PostToolUse" }
      ]
    }]
  }
}
```

### Hook Events

| Event | When | Payload |
|-------|------|---------|
| `PreToolUse` | Before tool execution | tool_name, tool_input |
| `PostToolUse` | After tool success | tool_name, tool_result |
| `Stop` | Session ends | reason |
| `SubagentStop` | Subagent completes | agent_id, result |
| `UserPromptSubmit` | User sends prompt | prompt |
| `SessionStart` | Session begins | config |
| `Notification` | Alert raised | message, level |

### Observer Pattern

```python
#!/usr/bin/env python3
"""Hook observer that emits OTel spans for Claude Code events."""
import json, sys
from datetime import datetime
from opentelemetry import trace

tracer = trace.get_tracer("claude-code-hooks")

def observe_hook(event_type: str, payload: dict):
    with tracer.start_as_current_span(f"hook_{event_type.lower()}") as span:
        span.set_attribute("event_type", event_type)
        span.set_attribute("timestamp", datetime.utcnow().isoformat())

        if event_type == "PreToolUse":
            span.set_attribute("tool_name", payload.get("tool_name", ""))
        elif event_type == "PostToolUse":
            span.set_attribute("tool_name", payload.get("tool_name", ""))
            span.set_attribute("success", not payload.get("error"))

        print(json.dumps({"continue": True}))

if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    event_type = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    observe_hook(event_type, payload)
```

---

## OTel Implementation

### Quick Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-extension")
```

### Local UI with Phoenix

```python
import phoenix as px
px.launch_app()  # localhost:6006

from openinference.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()
```

---

## GenAI Semantic Conventions

Use OTel's standardized attribute names (v1.37+) for vendor interoperability:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `gen_ai.system` | Provider | `anthropic` |
| `gen_ai.request.model` | Model ID | `claude-sonnet-4-20250514` |
| `gen_ai.usage.input_tokens` | Input tokens | `1500` |
| `gen_ai.usage.output_tokens` | Output tokens | `500` |
| `gen_ai.tool.name` | Tool/function name | `read_file` |
| `gen_ai.tool.call.id` | Unique call identifier | `call_abc123` |
| `gen_ai.response.finish_reason` | Why stopped | `stop`, `max_tokens` |

### Cardinality Guidelines

Default OTel limit: 2000 per metric.

| Attribute Type | Where | Why |
|----------------|-------|-----|
| Low cardinality (http.method, tool_name) | Metrics | Safe for aggregation |
| High cardinality (user_id, trace_id) | Spans/logs only | Avoid metric explosion |
| Unbounded (prompt text, full response) | Truncate to 500 chars | Attribute size limits |

**Rule:** High-cardinality details in span attributes, not metric labels.

---

## Per-Extension Spans

### Required (Agents, MCP, SDK Apps)

| Extension | Span | Key Attributes |
|-----------|------|----------------|
| **Agent** | `agent_run` | task, total_steps, success |
| **Agent** | `llm_call` | step, model, input_tokens, output_tokens |
| **Agent** | `tool_call` | tool_name, tool_args (truncated), success |
| **MCP** | `mcp_server` | server_name, version |
| **MCP** | `mcp_discover` | tool_count, tool_names |
| **MCP** | `mcp_call` | server_name, tool_name, success, result_size |
| **SDK** | `session` | user_id, session_id |
| **SDK** | `turn` | user_input (truncated), turn_tokens |

### Recommended (Skills, Hooks, Commands)

| Extension | Span | Key Attributes |
|-----------|------|----------------|
| **Skill** | `skill_check` | prompt (truncated), available_skills, activation_count |
| **Skill** | `skill_match` | skill_name, activated |
| **Skill** | `skill_load` | skill_name, content_size, load_time_ms |
| **Hook** | `hook_trigger` | event_type, handler_count |
| **Hook** | `hook_handler` | handler_name, success, exit_code |
| **Command** | `command` | command_name, arg_count, duration_ms |
| **Command** | `command_execute` | success, output_size |

---

## Backend Options

| Backend | Type | Best For |
|---------|------|----------|
| [Phoenix](https://docs.arize.com/phoenix) | Local UI | Development, no cloud required |
| [Langfuse](https://langfuse.com/) | Self-hosted | Production, open source |
| [Datadog](https://www.datadoghq.com/) | Cloud | Enterprise, native GenAI support |
| [Honeycomb](https://www.honeycomb.io/) | Cloud | High-cardinality queries |
| Console exporter | Debug | Quick debugging, no setup |

---

## Gotchas

| Trap | Fix |
|------|-----|
| Missing parent spans | Always set parent for nested spans |
| Attribute size limits | Truncate large values (500 chars) |
| Not ending spans | Use context managers or try/finally |
| Missing errors | Always `record_exception()` on failures |
| No session correlation | Pass session_id through all spans |
| Cardinality explosion | High-cardinality in spans, not metrics |
| HTTP monitoring blind spot | Use hooks or SDK-level tracing, not HTTP intercepts |

---

## Sources

- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage) — Native OTel support
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks) — Hook event reference
- [OpenTelemetry GenAI](https://opentelemetry.io/blog/2025/ai-agent-observability/) — Semantic conventions for AI agents
- [Phoenix](https://docs.arize.com/phoenix) — Local LLM observability UI
