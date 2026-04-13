# Memory-Augmented LLM Systems Landscape (2025-2026)

**Source type:** Web research synthesis
**Collected:** 2026-04-13
**Coverage:** MemGPT/Letta, Mem0, Zep, Cognee, LangChain, LlamaIndex, RAG SOTA, contextual retrieval, personal AI memory products

---

## 1. MemGPT / Letta Evolution

MemGPT (Packer et al., 2023) coined the "LLM as operating system" metaphor — the LLM manages its own memory via tool calls that read/write tiered storage. The project rebranded: **MemGPT** now refers to the original agent design pattern; **Letta** is the company and framework built around it.

**Letta V1 architecture** (Oct 2025) is a significant rearchitecture. The original MemGPT relied on "heartbeat" loops and `send_message` as a tool call — every action was a tool call. V1 drops heartbeats and send_message, converging toward the agentic patterns that modern models (GPT-5, Claude 4.5 Sonnet) are post-trained on: multi-step tool calling with interleaved reasoning and self-directed termination. The insight: agent architectures should stay "in-distribution" relative to model training, not fight it.

**Memory tiers remain the core idea:** All agent state (memories, messages, reasoning, tool calls) is persisted in a database. "Core memories" are injected into the context window; the agent modifies its own memory blocks through tools. Evicted context is never lost — it moves to archival storage and can be recalled. Letta added a Conversations API (Jan 2026) for shared memory across parallel agent-user interactions.

**Architectural trade-off:** Letta couples memory management to the LLM itself (the agent decides what to remember). This is powerful but means memory quality depends on model quality. No separation of concerns between reasoning and memory management.

Sources:
- https://www.letta.com/blog/letta-v1-agent
- https://docs.letta.com/concepts/memgpt/
- https://www.letta.com/blog/agent-memory

## 2. LLM Memory Frameworks

**Mem0** — The strongest standalone option. Two-phase pipeline: (1) Extraction — ingests latest exchange + rolling summary + recent messages, LLM extracts candidate memories; (2) Update — each new fact is compared against top similar entries in vector DB for dedup/merge. **Mem0g** variant adds a graph layer (Neo4j or Kuzu) storing memories as directed labeled graphs with entity extraction and relation inference. Published as a paper (arXiv:2504.19413). Claims 26% uplift over OpenAI's memory on LOCOMO benchmark, 91% reduction in p95 latency, 90% reduction in token consumption vs. full-context approaches.

**Zep** — Purpose-built for temporal awareness. Tracks when memories were formed and modified. Community Edition for local deployment; Cloud edition adds classification and session management. Best for use cases where "when did I learn X" matters.

**Cognee** — Knowledge-graph-first. Converts unstructured data into structured, queryable knowledge graphs. Best for local-first, privacy-critical deployments with graph reasoning.

**LangChain Memory** — Multiple memory types (buffer, summary, entity, knowledge graph) that plug into the LangChain ecosystem. Limitation: ecosystem lock-in. Not standalone.

**LlamaIndex Memory** — Unifies chat history with document retrieval. Composable memory modules that work with LlamaIndex query engines. Strong for agents needing to search both conversations and referenced documents.

**Key distinction:** Mem0, Zep, and Cognee are standalone memory layers (framework-agnostic). LangChain/LlamaIndex memories are ecosystem-coupled. For memex, standalone matters.

Sources:
- https://arxiv.org/abs/2504.19413
- https://mem0.ai/blog/state-of-ai-agent-memory-2026
- https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks
- https://vectorize.io/articles/best-ai-agent-memory-systems

## 3. RAG State of the Art (2025-2026)

The field has moved through three generations:
- **Naive RAG** (2023): chunk, embed, retrieve top-k, generate. High noise, no reasoning.
- **Advanced RAG** (2024): query rewriting, hybrid search (BM25 + dense), reranking (cross-encoders), contextual chunking. This is now baseline.
- **Modular/Agentic RAG** (2025-2026): the current frontier. Pipeline decomposed into specialized, interchangeable modules (query planners, retrievers, rerankers, generators) orchestrated by a controller agent. The RAG system itself becomes agentic — it decides when to retrieve, what to retrieve, and whether to retrieve at all.

**Graph RAG** is a major 2025 theme: storing retrieved knowledge in graph structures, enabling multi-hop reasoning. Microsoft's GraphRAG and academic variants (GFM-RAG, KG2RAG, Cog-RAG) show 4-10% F1 gains on multi-hop benchmarks (HotpotQA, MuSiQue).

**Hybrid search + reranking is now the default**, not a differentiator. The open question is what sits *above* retrieval — the orchestration logic.

Sources:
- https://arxiv.org/abs/2410.12837
- https://arxiv.org/abs/2506.00054
- https://squirro.com/squirro-blog/state-of-rag-genai

## 4. Contextual Retrieval

Anthropic's approach (Sept 2024): prepend chunk-specific context to each chunk before embedding and BM25 indexing. Results: 35% reduction in top-20 retrieval failure rate for contextual embeddings alone; 49% reduction when combined with contextual BM25. Cost: ~$1.02 per million document tokens with prompt caching.

**Adoption status:** AWS integrated it into Bedrock Knowledge Bases (June 2025). LlamaIndex has a cookbook implementation. It is becoming a recognized best practice but is **not yet universal** — most RAG tutorials still show naive chunking. The cost of the context-generation pass is the barrier for high-volume use cases.

**No other approach has matched its simplicity.** Alternatives exist (late chunking via ColBERT-style late interaction, document-level embeddings with hierarchical retrieval) but contextual retrieval's "just prepend context" approach is the most adopted context-aware chunking method.

Sources:
- https://www.anthropic.com/news/contextual-retrieval
- https://aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-using-amazon-bedrock-knowledge-bases/

## 5. Personal AI Memory Products

**Limitless (formerly Rewind):** Pivoted from screen capture to wearable (Limitless Pendant) focused on meeting transcription and summarization. **Acquired by Meta in Dec 2025.** The Rewind Mac app shut down; screen/audio capture disabled. Users migrated to Meta's terms. The open-source alternative **Screenpipe** is the closest successor for local-first screen+audio capture.

**Microsoft Recall:** Launched controversially in 2024 (privacy backlash), then pulled back. Shipped in Windows 12 (2026) with on-device processing. Captures screen snapshots, indexes them locally, enables natural-language search over your computing history. Now "baked into the OS" rather than feeling like a bolt-on.

**Apple Intelligence Personal Context:** Still delayed. Apple targeting spring 2026 for "Personal Context" — Siri indexing emails, messages, files, photos locally, with anonymized sub-tasks sent to cloud.

**Architectural pattern across all three:** Capture everything, index locally, search via natural language. None of them model memory solidification, associative retrieval, or cognitive state. They are search engines over activity logs, not memory systems.

Sources:
- https://screenpi.pe/blog/rewind-ai-alternative-2026
- https://www.macrumors.com/2025/06/12/apple-intelligence-siri-spring-2026/
