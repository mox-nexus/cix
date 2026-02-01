# Schema Reference

## fragments (main table)

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR | Primary key, from source |
| conversation_id | VARCHAR | Groups messages in conversation |
| role | VARCHAR | 'user' or 'assistant' |
| content | TEXT | Message text |
| timestamp | TIMESTAMPTZ | When message was created |
| source_kind | VARCHAR | 'claude_conversations', 'openai', etc. |
| source_id | VARCHAR | Unique ID within source |

## raw_fragments (immutable archive)

Stores original JSON for rebuild capability. Don't query directly.

## Indexes

- `idx_fragments_timestamp` - for date queries
- `idx_fragments_conversation` - for thread queries
- `idx_fragments_source` - for source filtering

## Source Kinds

| Value | Description |
|-------|-------------|
| `claude_conversations` | Claude.ai exports |
| `openai` | ChatGPT exports |
| `claude_code_logs` | Claude Code session logs (future) |
| `gemini` | Google Gemini (future) |
