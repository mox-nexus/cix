# Comparative Architecture: Memory Systems Landscape

**Purpose:** See what each system actually does, where they converge, and where the gap is.

---

## The Four Systems at a Glance

```
                    WHO MANAGES MEMORY?
                    
    LLM manages          Independent pipeline
    its own memory        manages memory
         │                      │
         │                      │
       Letta              Mem0    Zep    Cognee
         │                 │       │       │
         │                 │       │       │
    "I'll decide       "Extract  "Build  "Build
     what matters"      → compare  a       a
                         → operate temporal knowledge
                         on store" graph"  graph"
```

## Pipeline Comparison

| | Letta | Mem0 | Zep/Graphiti | Cognee |
|---|---|---|---|---|
| **Ingestion** | Agent writes to memory blocks via tool calls | LLM extracts facts → compare → ADD/UPDATE/DELETE/NOOP | LLM extracts entities + relations → resolve → temporal edges | LLM extracts typed graph nodes + edges via Pydantic schema |
| **What gets stored** | Agent-curated text in named blocks (2k chars each) | Natural language facts (Mem0) or entity-relationship triplets (Mem0g) | Entities + temporal relationships + raw episodes | Typed entities + relationships + chunk embeddings + summaries |
| **Retrieval** | Vector search over archival; text/date search over recall | Vector similarity over stored facts | Semantic + BM25 + graph traversal, fused via RRF. **No LLM at query time** | Vector similarity OR graph traversal OR LLM-routed |
| **Temporal model** | None. Text in blocks is "current state." | None. Memories are current or deleted. | **Bi-temporal.** Four timestamps per edge: t_created, t_expired, t_valid, t_invalid | None |
| **Dedup/conflict** | Agent manually replaces text | LLM compares new fact against top-10 similar → operation selection | Tiered: exact match → fuzzy → LLM. Contradictions → old edge invalidated, not deleted | Not documented |
| **Who decides what to remember** | The reasoning LLM (prompt-engineered) | A separate LLM call (extraction phase) | A separate LLM call (entity extraction) | A separate LLM call (schema-constrained extraction) |
| **Storage** | PostgreSQL + pgvector | Qdrant (vector) + Neo4j (graph, Pro tier) + SQLite | Neo4j (or Kuzu/FalkorDB) | Kuzu + LanceDB + SQLite (all embedded) |
| **Local-first** | Requires PostgreSQL server | Qdrant can run locally | Requires Neo4j (or Kuzu for embedded) | **Yes.** All defaults file-based, zero infrastructure |

## What They All Share

Every system in this landscape:
1. **Uses an LLM to decide what to remember.** Whether it's the reasoning LLM (Letta) or a separate extraction call (Mem0, Zep, Cognee), the memory formation step requires LLM judgment.
2. **Stores extracted facts, not raw conversations.** Conversations are decomposed into facts, entities, or blocks. The original dialogue structure is not preserved as a queryable unit.
3. **Retrieves by content similarity.** Vector search (sometimes + keyword + graph traversal), but always matching query content against stored content. None use the searcher's context as a retrieval signal.
4. **Has no concept of solidification.** Memories are either current or deleted/invalidated. None track the progression from tentative mention to consolidated understanding.
5. **Has no concept of trails.** No system offers named, temporal, shareable paths through memory.

## Where Each System Is Strongest

```
                Letta          Mem0           Zep            Cognee
                  │              │              │              │
Simplicity      ██████        ████           ██             █████
Temporal          ░░            ░░           ██████           ░░
Graph depth       ░░           ███           █████          ██████
Local-first      ██            ███            ██            ██████
Benchmarks       ██           █████          ████            ███
Retrieval speed  ██            ████          ██████          ████

██ = strong   ░░ = absent/weak
```

- **Letta:** Simplest model. One LLM, one database. Agent manages everything.
- **Mem0:** Best benchmarks. Strongest extraction/update pipeline. Production-proven at scale.
- **Zep:** Only system with genuine temporal model. LLM-free retrieval is fast and predictable.
- **Cognee:** Most local-first. Graph is open-source, not paywalled. LanceDB as vector store.

## The Actual Gap

Here is what "cognitive science grounding" means concretely — five things no system does, mapped to the specific cognitive science finding that says they should:

### 1. Ecphoric Retrieval

**What it is:** Retrieval that uses the searcher's current cognitive state — not just the query text, but what project they're in, what they've been discussing, what trail they're following — as a retrieval signal.

**Why it matters:** Tulving (1984): "synergistic ecphory" — recall is the joint product of stored trace AND current cognitive state. Wiseman & Tulving (1976): people recall words they fail to recognize, because the right cue (one present at encoding) succeeds where a copy of the item fails.

**What exists:** All four systems do content-similarity retrieval. Zep adds graph traversal. None incorporate the searcher's context.

**What memex would do:** Hybrid search + context vector (recent conversation embedding, active project, current trail position) as additional retrieval signals.

### 2. Conversation as Native Unit

**What it is:** Storing and retrieving dialogues with their structure intact — speaker roles, turn sequence, topic flow — not decomposing them into extracted facts.

**Why it matters:** Stafford (1984): 90% of conversation content lost in 5 minutes. Pickering & Garrod (2004): dialogue involves interactive alignment — what's stored may be the alignment state, not individual utterances.

**What exists:** All four systems decompose conversations into facts (Mem0), entities (Zep, Cognee), or block text (Letta). The dialogue structure is discarded.

**What memex would do:** Frame = a message with speaker, timestamp, position in conversation. Archive = a full conversation with structure preserved. The conversation is the retrieval unit, not the extracted fact.

### 3. Solidification Tracking

**What it is:** Tracking how an idea progresses from first mention through repeated access and annotation to crystallized understanding.

**Why it matters:** Squire (1982): specific episodes dissipate but shape durable schemas. Wilson (2002): fresh memories have "reliving" quality that crystallizes through retelling. Nader (2009): every retrieval is a reconsolidation event that modifies the memory.

**What exists:** Zep tracks temporal validity (when a fact was true). Mem0 does UPDATE/DELETE. None track the trajectory from "mentioned once" to "deeply understood."

**What memex would do:** Access count, annotation density, version chain (Frame → annotated Frame → Artifact v1 → v2). The solidification state is queryable: "show me ideas I've revisited 5+ times but never crystallized into an artifact."

### 4. Trails as First-Class Objects

**What it is:** Named, temporal, shareable associative paths through memory — not just links between items, but authored sequences with narrative intent.

**Why it matters:** Bush (1945): "The human mind operates by association. With one item in its grasp, it snaps instantly to the next." The trail was the core innovation of the original memex.

**What exists:** Zep has graph traversal (exploratory, not authored). Cognee has graph completion (follows relationships, not authored sequences). None have named, temporal, shareable trails.

**What memex would do:** Trail = a named, ordered sequence of frames/artifacts with annotations. Trails are first-class objects that can be shared, forked, and versioned. Trail-following is a retrieval mode.

### 5. Post-Hoc Annotation (Delayed, Not Inline)

**What it is:** Annotating memories after a delay rather than during the conversation, because delayed reflection is more metacognitively accurate.

**Why it matters:** Thiede (2003): delayed keyword generation → better monitoring accuracy. Metcalfe (1986): insight cannot be predicted pre-hoc. Lutz & Thompson (2003): generating reports about experience can modify that experience.

**What exists:** Letta annotates inline (the agent updates core memory during conversation). Mem0 extracts inline. None separate the "capture" phase from the "annotate" phase with a deliberate delay.

**What memex would do:** Capture is automatic (ingest conversation). Annotation is separate (trail building, tagging, artifact creation) — and the system encourages it to happen later, not during the live conversation.

---

## Summary

The gap is not "these systems are bad." Mem0's extraction pipeline is elegant. Zep's bi-temporal model is genuine engineering. Cognee's schema-constrained graph extraction is smart. Letta's simplicity is a feature.

The gap is that none of them asked: "how does memory actually work in humans, and what does that imply for the system design?" They started from engineering constraints (context window overflow, latency, cost) and built solutions to those constraints. Memex starts from cognitive science findings and builds a system that models how memory forms, consolidates, and is recalled — and then solves the engineering constraints within that framework.

That's not a claim of superiority. It's a different starting point that leads to different design decisions.
