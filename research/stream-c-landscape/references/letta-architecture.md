# Letta (MemGPT): Architecture Reference

**Source:** arXiv:2310.08560 (MemGPT paper), docs.letta.com, letta.com/blog
**As of:** April 2026

---

## What It Is

The LLM manages its own memory. The context window is "RAM," external storage is "disk," and the LLM is the processor. The agent has tool calls to read and write its own memory tiers. Memory quality depends on model quality — there is no independent memory system.

## Memory Tiers

```
┌─────────────────────────────────────────────────────────┐
│                   CONTEXT WINDOW ("RAM")                 │
│                                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │  System Instructions (read-only)              │       │
│  │  - how to use memory tools                    │       │
│  │  - behavioral guidelines                      │       │
│  └──────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────┐       │
│  │  Core Memory Blocks (read-write, always in)   │       │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │       │
│  │  │  human   │  │  persona │  │ custom... │   │       │
│  │  │ 2k chars │  │ 2k chars │  │ 2k chars │   │       │
│  │  └──────────┘  └──────────┘  └──────────┘   │       │
│  └──────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────┐       │
│  │  Message Buffer (FIFO, subject to eviction)   │       │
│  │  [user msg] [asst msg] [tool call] [result]   │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  EXTERNAL STORAGE ("Disk")                │
│                                                         │
│  ┌────────────────────────┐  ┌────────────────────────┐ │
│  │   Recall Memory        │  │   Archival Memory      │ │
│  │   (PostgreSQL)         │  │   (pgvector)           │ │
│  │                        │  │                        │ │
│  │   Complete message     │  │   Agent-curated        │ │
│  │   history: user msgs,  │  │   knowledge: facts,    │ │
│  │   assistant msgs,      │  │   summaries, external  │ │
│  │   tool calls, traces   │  │   data the agent chose │ │
│  │                        │  │   to preserve          │ │
│  │   → text search        │  │   → vector search      │ │
│  │   → date range search  │  │                        │ │
│  └────────────────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Memory Tools (Agent's API to Itself)

| Tool | What it does |
|------|-------------|
| `core_memory_append(name, content)` | Append to a named block |
| `core_memory_replace(name, old, new)` | Find-and-replace within a block |
| `conversation_search(query, page?)` | Text search over recall memory |
| `conversation_search_date(start, end, page?)` | Date-range search over recall |
| `archival_memory_insert(content)` | Write to long-term vector store |
| `archival_memory_search(query, page?)` | Similarity search over archival |

The agent calls these as standard tool calls during inference. The decision of WHAT to remember is entirely prompt-engineered — the system prompt says "core memory is limited and precious, store only the most important facts."

## How the Agent Decides What to Remember

**Prompt-engineered, not learned.** The system prompt tells the agent:
- Core memory is precious — only the most important facts
- Use append/replace to maintain beliefs about the user
- Use archival_memory_insert for detailed knowledge
- Search recall/archival when you need context

There is no trained memory controller, no extraction pipeline, no dedup logic. The LLM's own judgment (shaped by the system prompt) is the entire memory management strategy.

## Eviction / Context Compaction

When the message buffer fills the context window:
1. A **reflection subagent** summarizes the conversation history
2. Summary replaces raw messages in the buffer
3. All original messages remain in recall memory (PostgreSQL) — never lost
4. Core memory blocks are **never evicted** (always in context)

## MemGPT v0 → Letta V1 Transition

| | MemGPT v0 (paper) | Letta V1 (Oct 2025) |
|---|---|---|
| Agent loop | Heartbeat mechanism: `request_heartbeat=true` triggers another inference | Native multi-step tool calling |
| User output | Explicit `send_message()` tool call | Direct assistant messages |
| Design principle | Custom control flow | Stay "in-distribution" with model training |

V1 insight: agent architectures should stay in-distribution with how models are trained. Fighting the model's natural patterns (heartbeats, explicit send_message) was creating friction.

## Conversations API (Jan 2026)

Multiple users can message one agent through independent conversation threads. Each conversation has its own message buffer, but core memory blocks are shared across all conversations. The agent accumulates knowledge from all interactions.

## Persistence

All state lives in **PostgreSQL** (~42 tables). Context window is **recompiled from DB on each request** — no client-side state. Production: Amazon Aurora PostgreSQL.

## What Letta Does NOT Do

- No independent memory system — the LLM IS the memory manager
- No extraction pipeline — the agent writes what it judges important
- No dedup/merge — the agent manually replaces old facts via core_memory_replace
- No temporal validity model — memories are current text in blocks, no history
- No solidification tracking — no concept of episodic→semantic transition
- No trail or associative path
- No ecphoric retrieval — archival search is pure vector similarity
- Core memory limited to ~2k chars per block — highly compressed

## The Fundamental Trade-off

Letta gives the LLM full control over its own memory. This means:
- **Strength:** The agent can be strategic about what it remembers
- **Weakness:** Memory quality = model quality. A worse model = worse memory. No separation of concerns.
- **Contrast with Mem0:** Mem0 runs a structured pipeline (extract → compare → operate) that is partially algorithmic. Letta delegates the entire decision to the LLM.

## Sources

- https://arxiv.org/abs/2310.08560
- https://docs.letta.com/concepts/memgpt/
- https://docs.letta.com/advanced/memory-management/
- https://www.letta.com/blog/letta-v1-agent
- https://www.letta.com/blog/agent-memory
