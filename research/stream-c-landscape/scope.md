# Stream C: Technical Landscape, Hard Problems, Gaps — Research Scope

**Status:** Scope frozen.
**Frozen:** 2026-04-13
**Purpose:** Map the technical landscape of memory-augmented systems, identify hard problems, and locate gaps where memex's cognitive grounding (Streams A+B) creates genuine differentiation.
**Depends on:** Stream A (human memory architecture), Stream B (LLM memory structures)

---

## Context

Streams A and B established 16 architectural implications for memex. Stream C asks: what exists already, what's hard, and where is there room?

The architectural implications that need technical grounding:

1. **Ecphoric retrieval** — retrieval that incorporates the searcher's current cognitive state, not just content similarity. No existing system implements this (Stream A gap). Induction heads validate the two-input model (Stream B).
2. **Solidification trajectory** — tracking Frame → re-accessed → annotated → Artifact. No existing system models this (Stream A gap).
3. **RAG over fine-tuning** — catastrophic forgetting (Stream B) means external retrieval is the right memory augmentation strategy. RAG is a crowded field; what's the state of the art?
4. **Position-sensitive context loading** — lost-in-the-middle (Stream B) means recalled content placement matters. How do existing systems handle this?
5. **Hybrid search** — semantic + keyword + temporal. What combinations exist and what are the benchmarks?
6. **Lance as multimodal lakehouse** — the pre-disaster design chose Lance over Postgres+pgvector. What's the current landscape of vector storage for conversational data?
7. **MemGPT as closest prior art** — what has happened since Packer 2023? What other hierarchical memory architectures exist?

Beyond the A+B implications, the session notes identified these additional landscape questions:
- Knowledge graphs for conversational memory
- PKM tools (Roam, Obsidian, Notion) — what do they get right about personal knowledge?
- Temporal reasoning in retrieval systems
- Historical memex implementations (Bush 1945 → Nelson → modern)

---

## Research Questions

### RQ-C1 — What is the state of the art in memory-augmented LLM systems?

What systems exist that give LLMs persistent memory beyond the context window?

- MemGPT and successors — what evolved since Packer 2023?
- RAG architectures — naive RAG, advanced RAG, modular RAG. What's the current taxonomy?
- Memory-augmented agents (AutoGPT, LangChain memory modules, LlamaIndex, Cognee, Mem0)
- What retrieval strategies do they use? (embedding similarity, keyword, hybrid, graph-based)
- What storage backends? (vector DBs, knowledge graphs, relational, document stores)
- What are the measured failure modes? (retrieval noise, context pollution, staleness)

**Null hypothesis:** Existing memory-augmented systems already solve the problems memex targets; memex is redundant.

### RQ-C2 — What is the state of the art in hybrid and contextual retrieval?

Stream A says retrieval should be ecphoric (two-input: stored trace + current state). Stream B says position matters. What retrieval techniques exist?

- Dense retrieval (embedding similarity), sparse retrieval (BM25), hybrid (RRF, learned fusion)
- Contextual retrieval — does any system use the searcher's state as a retrieval signal?
- Temporal retrieval — recency weighting, decay functions, temporal ordering
- Multi-hop retrieval — following chains of related items (analogous to trail-following)
- Reranking — cross-encoders, LLM-as-judge, ColBERT-style late interaction
- Benchmarks — BEIR, MTEB, MS MARCO. What do they measure and what do they miss?

**Null hypothesis:** Standard hybrid retrieval (BM25 + dense + reranking) already approximates ecphoric retrieval well enough; the cognitive grounding adds no practical benefit.

### RQ-C3 — What is the state of vector storage and multimodal data management?

The pre-disaster design chose Lance. What's the landscape?

- Vector databases: Qdrant, Weaviate, Milvus, Pinecone, Chroma, pgvector, LanceDB
- Multimodal storage: can they handle text + embeddings + metadata + temporal ordering?
- Lakehouse vs vector-DB-as-service — trade-offs for personal/local deployment
- Embedding models: state of the art for conversational content (not just document retrieval)
- Quantization, compression, approximate NN trade-offs for local operation
- What does Lance specifically offer that others don't? (columnar, versioned, zero-copy)

**Null hypothesis:** pgvector or a hosted vector DB is sufficient; Lance's lakehouse model adds complexity without proportional benefit.

### RQ-C4 — What do PKM tools and historical memex implementations get right (and wrong)?

Bush (1945) → Nelson → Engelbart → Roam → Obsidian → Notion → Rewind/Recall → modern AI assistants.

- What design patterns recur? (trails, backlinks, spatial canvases, transclusion)
- What cognitive models do they implicitly assume? (filing cabinet? associative memory? graph?)
- Where do they fail for conversational memory specifically?
- What does the "personal AI memory" wave (Rewind, Windows Recall, Limitless, etc.) add?
- Is there evidence that any of these tools improve recall, insight, or knowledge work outcomes?

**Null hypothesis:** Existing PKM tools with AI features already solve the personal memory problem; memex is reinventing what Obsidian+AI already does.

### RQ-C5 — What are the hard, unsolved problems?

Integrating everything from A, B, and C1-C4: what problems does memex face that nobody has solved?

- Ecphoric retrieval — how to incorporate cognitive state into retrieval
- Solidification tracking — how to model the episodic→semantic transition computationally
- Conversational memory specifically — not documents, not code, but dialogues
- Identity and dedup across platforms (the reactor pipeline problem)
- Temporal reasoning — "what did I think about X before learning Y?"
- Scale — personal memory over years of conversations
- Privacy — local-first, no cloud dependency for intimate cognitive data

**Null hypothesis:** These problems are either already solved (and we haven't found the solutions) or are intractable (and memex can't solve them either).

---

## Collection Strategy

Stream C is a TECHNICAL landscape survey, not a cognitive science literature review. Sources include:

1. **Academic papers** — via OpenAlex/Semantic Scholar for RAG architectures, hybrid retrieval, vector storage benchmarks
2. **Technical documentation** — LanceDB, MemGPT/Letta, LlamaIndex, LangChain, Mem0 docs
3. **Blog posts and technical reports** — from companies building memory-augmented systems (Anthropic, OpenAI, Cohere on RAG; Pinecone, Weaviate on vector search)
4. **Benchmarks** — MTEB, BEIR, retrieval benchmark results
5. **Historical sources** — Bush 1945 "As We May Think," Nelson on transclusion

The extraction standard is the same as A+B: atomic claims with verbatim quotes and evidence tiers.

---

## Scope Boundaries

**In scope:**
- Systems that give LLMs persistent memory
- Retrieval techniques relevant to conversational content
- Storage backends suitable for personal, local-first operation
- PKM tools and their implicit cognitive models
- Hard problems identified by A+B that need technical solutions

**Out of scope:**
- General-purpose information retrieval (web search, enterprise search)
- LLM training techniques (RLHF, DPO, etc.) except where they affect memory
- Agent frameworks beyond their memory components
- Social/collaborative knowledge management (this is personal memory)
