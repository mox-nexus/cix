# Stream C Synthesis: Technical Landscape, Hard Problems, Gaps

**Scope:** research/stream-c-landscape/scope.md
**Sources:** 13 papers (85 claims, abstract-only) + 3 web research synthesis documents
**Depends on:** Stream A (human memory), Stream B (LLM memory structures)

---

## RQ-C1 — What is the state of the art in memory-augmented LLM systems?

### Finding C1.1: Memory-augmented LLM systems fall into three architectural patterns

CLAIM: The landscape of memory-augmented LLM systems has converged on three patterns: (1) LLM-managed memory (the agent decides what to remember), (2) external memory layer (a separate system manages memory), and (3) cognitive architecture (modular memory components with structured action spaces).

EVIDENCE:
- [web:memory-augmented-systems] Letta V1 exemplifies pattern 1: all agent state persisted in DB, agent modifies its own memory blocks through tool calls
- [web:memory-augmented-systems] Mem0, Zep, Cognee exemplify pattern 2: standalone memory layers, framework-agnostic
- [sumers_2023:c3-c4] CoALA proposes pattern 3: "modular memory components, a structured action space to interact with internal memory and external environments, and a generalized decision-making process"
- [li_2024:c4] Personal LLM Agents are "LLM-based agents deeply integrated with personal data and personal devices"

CONFIDENCE: HIGH — convergent across academic and industry sources
ARCHITECTURAL IMPLICATION: Memex is pattern 2 (external memory layer) with pattern 3 aspirations (cognitive architecture grounding). This is distinct from Letta's pattern 1, where memory quality depends on model quality. Memex's value proposition: a principled memory layer that any model can use, grounded in cognitive science rather than ad hoc design.

### Finding C1.2: Long-term memory demonstrably improves engagement and disclosure in deployed systems

CLAIM: Empirical evidence from deployed LLM chatbots shows that long-term memory enhances user engagement, self-disclosure, and perception of familiarity — but introduces challenges around privacy and topic sensitivity.

EVIDENCE:
- [jo_2024:c5] "LTM enhanced health disclosure and fostered positive perceptions of the chatbot by offering familiarity"
- [jo_2024:c6] "challenges in promoting self-disclosure through LTM, particularly around addressing chronic health conditions and privacy concerns"
- [jo_2024:c4] Based on 1,252 call logs and 9 user interviews — rare empirical evidence from real deployment

CONFIDENCE: MEDIUM — single deployed study, specific to health domain
ARCHITECTURAL IMPLICATION: LTM works and users value it. But what to remember is a design decision, not just a technical one. Memex should default to broad capture (purpose-neutral, per Stream A finding 2.4) but provide user control over what surfaces in retrieval. Privacy is not just a security concern — it affects willingness to use the system.

### Finding C1.3: Existing models fail at long-term multi-session conversation

CLAIM: Standard dialogue models trained on short conversations perform poorly when conversations span multiple sessions over time. Retrieval-augmented and summarize-and-recall methods outperform standard architectures.

EVIDENCE:
- [xu_2022:c1] "state-of-the-art models are trained and evaluated on short conversations with little context. In contrast, the long-term conversation setting has hardly been studied"
- [xu_2022:c3] "existing models trained on existing datasets perform poorly in this long-term conversation setting"
- [xu_2022:c5] "retrieval-augmented methods and methods with an ability to summarize and recall previous conversations outperform the standard encoder-decoder architectures"

CONFIDENCE: HIGH — empirical with human evaluation
ARCHITECTURAL IMPLICATION: This validates memex's core approach: external retrieval into context (RAG), not reliance on the model's native ability to remember across sessions. The "goldfish memory" problem is real and well-documented.

### Finding C1.4: No existing system grounds memory architecture in cognitive science [CORRECTED]

CLAIM: Current memory-augmented systems split into two patterns: (1) reasoning LLM manages its own memory (Letta — coupling memory quality to model quality), and (2) standalone memory pipeline using LLMs as extraction tools (Mem0, Zep, Cognee — architecturally separate from reasoning). Neither pattern grounds its memory architecture in cognitive science. [CORRECTED — original claim conflated these two patterns, overstating that ALL systems couple memory to reasoning. Mem0/Zep/Cognee ARE architecturally separate standalone layers.]

EVIDENCE:
- [web:memory-augmented-systems] Letta: "the agent decides what to remember" — pattern 1, coupled
- [web:memory-augmented-systems] Mem0, Zep, Cognee are "standalone memory layers (framework-agnostic)" — pattern 2, separate
- [web:memory-augmented-systems] Both patterns use LLMs somewhere in the memory pipeline, but pattern 2 does NOT couple memory to the reasoning LLM
- [sumers_2023:c2] "we lack a systematic framework to organize existing agents"
- [li_2024:c1] Existing IPAs lack "personal data management" as a distinct capability

CONFIDENCE: HIGH — consistent across all surveyed systems
DIVERGENCE: CoALA (Sumers 2023) proposes modular memory as a CONCEPT. Mem0/Zep implement architectural separation. But none ground their design in how human memory actually works.
ARCHITECTURAL IMPLICATION: **THIS IS MEMEX'S DIFFERENTIATION.** Not architectural separation (Mem0 already has that) but cognitive grounding. Memex treats memory as a subsystem with its own principles derived from Streams A+B: reconstruction-based storage, ecphoric retrieval, solidification trajectory, purpose-neutral encoding. The LLM is a reasoning engine that CONSUMES recalled content — it doesn't manage the memory system. And the memory system's design follows from cognitive science, not ad hoc engineering.

---

## RQ-C2 — What is the state of the art in hybrid and contextual retrieval?

### Finding C2.1: Hybrid search (dense + sparse) is the converged baseline, not a differentiator

CLAIM: The combination of dense retrieval (embedding similarity) and sparse retrieval (BM25) via score fusion is now the default architecture for production retrieval systems. It is no longer a research contribution — it's table stakes.

EVIDENCE:
- [bruch_2023:c1] "lexical and semantic search are complementary in how they model relevance"
- [web:vector-db-hybrid-retrieval] "Hybrid search + reranking is now the default, not a differentiator"
- [zhao_2022] Dense text retrieval survey: 300+ references on the architecture, training, and integration of dense retrieval
- [web:vector-db-hybrid-retrieval] LanceDB, Qdrant, Weaviate, Elasticsearch all converge on BM25 + vector + RRF

CONFIDENCE: HIGH
ARCHITECTURAL IMPLICATION: Memex's hybrid search (BM25 + semantic + recency via RRF) is the right baseline, but it's not differentiation. The differentiation comes from what ADDITIONAL signals drive retrieval (ecphoric cues — see C2.4).

### Finding C2.2: Convex combination outperforms RRF when tunable, but RRF is the safer default

CLAIM: Contrary to prior claims of RRF parameter robustness, RRF is sensitive to its parameters. Learned convex combination of scores outperforms RRF in both in-domain and out-of-domain settings and is sample-efficient.

EVIDENCE:
- [bruch_2023:c2] "Contrary to existing studies, we find RRF to be sensitive to its parameters"
- [bruch_2023:c4] "convex combination outperforms RRF in in-domain and out-of-domain settings"
- [bruch_2023:c5] "convex combination is sample efficient, requiring only a small set of training examples"

CONFIDENCE: HIGH — empirical, published in ACM TOIS
ARCHITECTURAL IMPLICATION: Start with RRF (zero-shot, works out of the box), but plan migration path to learned convex combination once memex has enough retrieval feedback data. The "small set of training examples" requirement could be met by implicit user feedback (what recalled content was actually useful).

### Finding C2.3: LLM-based reranking matches or beats supervised methods and distills to small models

CLAIM: Instructed LLMs can deliver competitive or superior reranking results compared to supervised methods, and this capability distills into models 7x smaller than supervised baselines.

EVIDENCE:
- [sun_2023:c1] "properly instructed LLMs can deliver competitive, even superior results to state-of-the-art supervised methods on popular IR benchmarks"
- [sun_2023:c4] "a distilled 440M model outperforms a 3B supervised model on the BEIR benchmark"

CONFIDENCE: HIGH — empirical across multiple benchmarks
ARCHITECTURAL IMPLICATION: For memex's local-first constraint, a distilled reranker (440M) is viable. The retrieval pipeline becomes: BM25 + dense → RRF fusion → small reranker → context loading. This is efficient enough for local operation.

### Finding C2.4: No system implements context-dependent (ecphoric) retrieval

CLAIM: All existing retrieval systems — including hybrid search, GraphRAG, and reranking — operate on content similarity. None incorporate the searcher's current cognitive state as a retrieval signal.

EVIDENCE:
- [web:memory-augmented-systems] "No system implements ecphoric retrieval. All retrieval is content-similarity or keyword-based"
- [web:pkm-memex-history] "No tool treats a trail as a first-class, named, temporal, shareable object"
- [zhao_2022] Dense text retrieval survey covers architecture, training, indexing, integration — all content-based
- Stream A Finding 3.1: Tulving's synergistic ecphory requires BOTH stored trace AND current cognitive state

CONFIDENCE: HIGH — absence confirmed across academic survey (300+ papers) and industry landscape
ARCHITECTURAL IMPLICATION: **THIS IS THE OPEN PROBLEM.** Ecphoric retrieval means: given the user's current project, recent conversation topics, and active trail context, boost recall of content encoded under similar conditions. Implementation candidates: (1) conversation embedding as a context signal alongside query embedding, (2) project/trail metadata as filter+boost dimensions, (3) "what has the user been reading recently" as a recency-weighted context vector.

### Finding C2.5: Graph-based retrieval enables relational and structured retrieval beyond flat vector search [CORRECTED]

CLAIM: GraphRAG formalizes graph-based indexing, retrieval, and generation, enabling relational retrieval that flat vector search does not naturally support. Multi-hop benchmarks show 4-10% F1 gains over flat retrieval approaches. [CORRECTED — "multi-hop reasoning" evidence is from web source benchmarks, not Peng 2024 extraction. "Cannot" softened to "does not naturally support" — flat vector search can partially address multi-hop through iterative retrieval; GraphRAG does it more naturally via graph traversal.]

EVIDENCE:
- [peng_2024:c3] GraphRAG "capturing relational knowledge and facilitating more accurate, context-aware responses" (academic extraction)
- [peng_2024:c5] Formalizes workflow into "Graph-Based Indexing, Graph-Guided Retrieval, and Graph-Enhanced Generation" (academic extraction)
- [web:memory-augmented-systems] "4-10% F1 gains on multi-hop benchmarks (HotpotQA, MuSiQue)" (web source — benchmark evidence)
- [pan_2023:c4] "it is complementary to unify LLMs and KGs together and simultaneously leverage their advantages"
- [web:memory-augmented-systems] Zep/Graphiti: temporal knowledge graph with valid_at/invalid_at timestamps

CONFIDENCE: HIGH — convergent across academic surveys and deployed systems
ARCHITECTURAL IMPLICATION: Flat vector retrieval does not naturally answer "what did I think about X before learning Y?" — that requires temporal graph traversal. Memex's trail model already encodes sequential relationships between frames. A lightweight knowledge graph layer (entity-relationship with temporal validity, a la Zep) could complement the vector store for structured queries. This is an enhancement, not a replacement for hybrid search.

---

## RQ-C3 — What is the state of vector storage and multimodal data management?

### Finding C3.1: LanceDB confirms as the right choice for local-first personal memory

CLAIM: Among vector databases suitable for local personal use (<1M vectors), LanceDB uniquely combines embedded operation, native hybrid search, zero-copy versioning, and columnar multimodal storage.

EVIDENCE:
- [web:vector-db-hybrid-retrieval] LanceDB: embedded, Tantivy FTS, RRF built-in, Lance v2.2 format, Apache 2.0
- [web:vector-db-hybrid-retrieval] "LanceDB wins on hybrid search (native BM25+vector), versioning, and multimodal columnar storage"
- [web:vector-db-hybrid-retrieval] "the vector DB choice accounts for roughly 5-10% of RAG quality — chunking, embedding model, and retrieval pipeline matter far more"

CONFIDENCE: HIGH
ARCHITECTURAL IMPLICATION: The pre-disaster design choice (Lance over pgvector) is validated. LanceDB's native hybrid search (BM25 + vector + RRF) means the baseline retrieval pipeline requires no additional infrastructure. Versioning maps to memex's append-only trail model — each write creates a new version, enabling "time travel" queries.

### Finding C3.2: Unified generation+embedding models eliminate the two-model penalty in RAG

CLAIM: A single LLM can handle both generative and embedding tasks via instruction tuning (GRIT), with no performance loss versus specialized models and >60% RAG speedup for long documents.

EVIDENCE:
- [muennighoff_2024:c2] "a large language model is trained to handle both generative and embedding tasks by distinguishing between them through instructions"
- [muennighoff_2024:c5] "GRIT matches training on only generative or embedding data, thus we can unify both at no performance loss"
- [muennighoff_2024:c6] "the unification via GRIT speeds up Retrieval-Augmented Generation (RAG) by > 60% for long documents"

CONFIDENCE: HIGH — empirical, MTEB SOTA at time of publication
ARCHITECTURAL IMPLICATION: For memex's local deployment, a unified model (embedding + generation) reduces memory footprint and latency. However, current GRIT models (7B+) may be too large for local operation alongside the main reasoning LLM. Watch for smaller GRIT-style models. In the meantime, separate embedding model (Snowflake Arctic 334M or Nomic 137M) is the pragmatic choice.

### Finding C3.3: No embedding model is optimized for conversational content

CLAIM: Standard embedding benchmarks (MTEB) evaluate document retrieval, STS, and classification. No benchmark specifically targets dialogue/conversation retrieval, and no embedding model is optimized for conversational content.

EVIDENCE:
- [web:vector-db-hybrid-retrieval] "No MTEB task specifically benchmarks dialogue/conversation retrieval"
- [web:vector-db-hybrid-retrieval] "Conversational content has unique properties (turn-taking, coreference, implicit context) that standard benchmarks don't capture"
- [lee_2024] NV-Embed achieves #1 on MTEB but tasks are all document/passage-oriented

CONFIDENCE: HIGH — confirmed by benchmark survey
ARCHITECTURAL IMPLICATION: Memex will need to evaluate embedding quality empirically on its own conversation data. The conversational retrieval gap is a research opportunity: a benchmark and fine-tuned model for dialogue retrieval could be a genuine contribution. For now, use Snowflake Arctic Embed v2.0 or Nomic Embed v1.5 and measure retrieval quality on a held-out set of real conversations.

---

## RQ-C4 — What do PKM tools and historical memex implementations get right (and wrong)?

### Finding C4.1: Bush's trails — the original memex insight — remain unimplemented

CLAIM: Bush's 1945 memex centered on "trails" — named, reusable, shareable associative paths through personal information. No modern tool implements trails as first-class objects. Backlinks and graph views approximate but do not replicate this.

EVIDENCE:
- [web:pkm-memex-history] Bush: "The human mind operates by association. With one item in its grasp, it snaps instantly to the next"
- [web:pkm-memex-history] "No tool treats a trail as a first-class, named, temporal, shareable object"
- [web:pkm-memex-history] Roam backlinks are emergent (discovered), not authored (intentionally constructed)
- [web:pkm-memex-history] Nelson's transclusion and bidirectional links also never mainstreamed

CONFIDENCE: HIGH — confirmed across tool survey and historical analysis
ARCHITECTURAL IMPLICATION: Memex's Trail primitive IS Bush's trail. This is not an accident — it's the design's genealogy. The Trail should be first-class: named, temporal, shareable, with narrative intent. This alone differentiates memex from every PKM tool.

### Finding C4.2: All PKM tools assume manual decomposition; none model conversation as a native unit

CLAIM: Obsidian, Roam, Logseq, Tana, and Notion all assume the user will manually decompose experience into notes or blocks. None model dialogue as a unit with speaker attribution, turn structure, and temporal ordering.

EVIDENCE:
- [web:pkm-memex-history] Common failure: "All assume the human will manually decompose experience into notes/blocks"
- [web:pkm-memex-history] "None model the conversation as a native unit"
- [web:pkm-memex-history] "None track how understanding evolves over time (solidification trajectory)"

CONFIDENCE: HIGH
ARCHITECTURAL IMPLICATION: Memex's Frame (raw conversation message) and Archive (full conversation) are native dialogue primitives. The conversation is the input unit — no manual decomposition required. This is the opposite of PKM's "you build the graph" model. Memex's model: "conversations happen, memory forms, you curate trails through it."

### Finding C4.3: No evidence that PKM tools actually improve cognitive outcomes

CLAIM: The PKM field lacks randomized controlled trials or rigorous empirical evidence showing that tools like Obsidian or Roam improve recall, insight generation, or knowledge work outcomes.

EVIDENCE:
- [web:pkm-memex-history] "No randomized controlled trials testing whether PKM tools improve recall, insight generation, or knowledge work outcomes"
- [web:pkm-memex-history] "The PKM field operates largely on anecdote and plausible cognitive-science reasoning"
- [web:pkm-memex-history] Matuschak: spaced repetition has stronger evidence than note-taking systems

CONFIDENCE: HIGH — absence of evidence, well-surveyed
ARCHITECTURAL IMPLICATION: Memex should be designed to be TESTABLE. If grounded in cognitive science (Streams A+B), it can make specific, falsifiable predictions: e.g., "ecphoric retrieval surfaces more relevant results than pure semantic search" or "trail-curated content is recalled better than uncurated." Building evaluation into the system from day one differentiates it from the anecdote-driven PKM field.

---

## RQ-C5 — What are the hard, unsolved problems?

### Finding C5.1: Ecphoric retrieval — incorporating cognitive state into search

**STATUS: UNSOLVED. No known implementation.**

Stream A established that retrieval requires both stored trace AND current cognitive state (Tulving's synergistic ecphory). Stream C confirms no system implements this. All retrieval is content-based.

CANDIDATE APPROACHES:
- Context embedding: embed the recent conversation (last N turns) as a context vector; use it as a secondary retrieval signal alongside the explicit query
- Project/trail metadata: filter and boost by active project, current trail, recent topics
- Temporal-contextual decay: weight by recency but modulated by contextual similarity (Re3 approach — learnable query-aware gating)
- Conversation trajectory similarity: match not just content but the SHAPE of the conversation (exploratory? convergent? debugging?)

DIFFICULTY: HIGH — requires novel retrieval architecture with no established benchmark
STREAM A GROUNDING: tulving1984:c10 (ecphory), nader2009:c12 (context-dependent reconsolidation)
STREAM B GROUNDING: Induction heads as two-input retrieval (olsson2022:c1)

### Finding C5.2: Solidification tracking — modeling the episodic→semantic transition

**STATUS: UNSOLVED. Zep tracks temporal validity but not consolidation state.**

Stream A established that memories transition from vivid episodes to crystallized semantic knowledge through repeated access and annotation (Finding X.1). No system tracks this trajectory.

CANDIDATE APPROACHES:
- Access count + annotation density as proxy for crystallization
- Version chain length (Frame → annotated Frame → Artifact v1 → v2 → v3)
- Embedding drift: track how the embedding of a concept changes as it gets refined across conversations
- Explicit state machine: episodic → accessed → annotated → crystallized (with transitions triggered by user actions)

DIFFICULTY: MEDIUM — the model is well-defined (Stream A), the implementation is novel but tractable
STREAM A GROUNDING: squire1982:c16 (schema persistence), wilson2002:c15 (reliving→crystallization), nader2009:c5 (reconsolidation)

### Finding C5.3: Conversational memory as a specific domain

**STATUS: UNDERSERVED. "Beyond Goldfish Memory" (Xu 2022) is nearly alone.**

Conversations have properties that documents don't: turn-taking, speaker roles, coreference chains, implicit context, temporal ordering, joint construction (Pickering's interactive alignment). No retrieval system, embedding model, or benchmark specifically targets conversational memory.

CANDIDATE APPROACHES:
- Conversation-specific chunking: chunk by topic shift or speaker turn, not fixed token count
- Speaker-attributed embeddings: embed with speaker role metadata
- Dialogue act classification: tag turns as question/answer/clarification/insight/agreement
- Alignment detection: identify moments of convergence or divergence between speakers (Pickering 2004 from Stream A)

DIFFICULTY: MEDIUM — well-defined problem, no existing benchmark, moderate engineering
STREAM A GROUNDING: stafford1984:c1-c2 (conversational memory fragility), pickering2004:c2 (interactive alignment)
STREAM B GROUNDING: xu_2022:c1-c5 (existing models fail at multi-session conversation)

### Finding C5.4: Temporal reasoning in memory systems

**STATUS: PARTIALLY SOLVED. Zep/Graphiti has temporal edges; Milvus has decay rankers. No system combines temporal graph + temporal retrieval + temporal reasoning.**

Questions like "what did I think about X before learning Y?" or "how did my understanding of Z evolve?" require temporal graph traversal, not just recency-weighted retrieval.

CANDIDATE APPROACHES:
- Temporal knowledge graph (Zep model): entity-relationship edges with valid_at/invalid_at
- Query-aware temporal gating (Re3 model): learn when time matters for a given query
- Trail-based temporal ordering: trails encode temporal and narrative sequence
- Version chain traversal: follow the SUPERSEDES chain to see how an artifact evolved

DIFFICULTY: HIGH for full temporal reasoning; MEDIUM for temporal retrieval alone
STREAM A GROUNDING: nader2009:c12 (context-dependent reconsolidation), finding X.1 (solidification trajectory)

### Finding C5.5: Privacy and local-first operation

**STATUS: PARTIALLY SOLVED. LanceDB enables local storage; embedding models run locally. Unsolved: local LLM for memory extraction without cloud dependency.**

EVIDENCE:
- [web:memory-augmented-systems] Limitless acquired by Meta — privacy concern realized
- [web:memory-augmented-systems] Screenpipe is the open-source local-first alternative
- [jo_2024:c6] Privacy concerns observed as friction point for LTM-driven self-disclosure
- [web:vector-db-hybrid-retrieval] Snowflake Arctic Embed (334M) and Nomic Embed (137M) run locally

DIFFICULTY: MEDIUM — local embedding and storage are solved; local LLM inference is large but feasible (Llama 3 8B, Gemma 2B); the bottleneck is the memory extraction pass (currently requires a capable LLM to decide what to remember)
ARCHITECTURAL IMPLICATION: Memex's pattern 2 architecture (external memory layer) is advantageous here. If the memory layer is principled enough, the extraction pass can use a smaller model or heuristic rules rather than requiring GPT-4-class reasoning.

---

## Cross-Stream Integration

### The Memex Differentiation Stack

Integrating Streams A, B, and C, memex's genuine differentiation from existing systems rests on five pillars:

| Differentiation | Grounded in | No existing system does this |
|---|---|---|
| **Ecphoric retrieval** | Tulving ecphory (A), induction heads as two-input retrieval (B) | All retrieval is content-based (C) |
| **Trails as first-class objects** | Bush 1945 original vision (C), solidification trajectory (A) | Backlinks approximate; none implement authored trails (C) |
| **Conversation as native unit** | Stafford 90% loss (A), Pickering alignment (A), Xu goldfish memory (C) | All PKM assumes manual note decomposition (C) |
| **Solidification tracking** | Episodic→semantic transition (A), reconsolidation (A) | Zep tracks time; none track consolidation state (C) |
| **Cognitive science grounding** | All of Stream A, structural parallels from Stream B | MemGPT/Letta is OS-inspired; Mem0 is ad hoc; none are cognition-grounded (C) |

### What Memex Should NOT Try To Do

1. **Compete on RAG infrastructure** — hybrid search + reranking is commodity. Use LanceDB's native capabilities. Don't build a retrieval engine.
2. **Compete on memory extraction** — Mem0's extract-compare-merge pipeline is mature. Either use it or build a simpler version. Don't reinvent this.
3. **Build a general-purpose agent framework** — CoALA/Letta/LangChain own this space. Memex is a memory LAYER, not an agent.
4. **Build a PKM tool** — Obsidian has the note-taking market. Memex is for conversational memory, not manual knowledge management.

### What Memex SHOULD Build

1. **The memory layer** — ingest conversations, form frames, embed broadly (purpose-neutral), store in Lance with temporal metadata
2. **Ecphoric retrieval** — hybrid search + context signal (project, trail, recent activity) as a differentiating retrieval architecture
3. **Trail curation** — first-class trail objects that capture the solidification trajectory
4. **Recall API** — a clean interface for any LLM/agent to query the memory layer, with position-aware context loading (important content at beginning/end, not middle)

---

## Null Hypothesis Evaluation

| Null Hypothesis | Verdict | Evidence |
|---|---|---|
| C1: Existing systems already solve what memex targets | **REFUTED.** No system combines ecphoric retrieval, trail-based curation, conversation-native storage, and solidification tracking. | MemGPT, Mem0, Zep each solve part of the problem but miss the cognitive grounding. |
| C2: Standard hybrid retrieval approximates ecphoric retrieval well enough | **UNTESTED but UNLIKELY.** No system has tried ecphoric retrieval, so there's no comparison. The theoretical gap (content-similarity vs context-dependent retrieval) is well-established. | Tulving 1984, confirmed by absence in C2 landscape survey |
| C3: pgvector or hosted vector DB is sufficient; Lance adds complexity | **REFUTED for the specific use case.** LanceDB's embedded operation, native hybrid search, and zero-copy versioning are uniquely suited to local-first personal memory. | Web research comparison; versioning maps to append-only trail model |
| C4: Existing PKM tools with AI features already solve personal memory | **REFUTED.** All PKM tools assume manual decomposition; none model conversation natively; none track solidification; no evidence they improve cognitive outcomes. | Tool comparison + effectiveness evidence gap |
| C5: Hard problems are either solved or intractable | **PARTIALLY REFUTED.** Ecphoric retrieval and solidification tracking are hard but tractable. Candidate approaches identified for each. | Stream A provides the theoretical model; Stream C confirms no implementation exists |

---

## Gap Analysis

### Gaps Remaining After Three Streams

1. **Peircean semiotics** — Still absent from the evidence base. Stream A scope flagged this; not addressed in C. The sign→interpretant→mark vocabulary may add something the cognitive science vocabulary doesn't, or it may be isomorphic. Unknown.
2. **Ecological validity of insight in conversation** — Still no studies. All insight research is lab-based (Stream A gap). Whether conversational clicks follow the same pattern is unknown.
3. **Conversational forgetting curve beyond 5 minutes** — Stafford 1984 gives 10% at 5 min. No data on hours/days/weeks. Critical for memex's value proposition.
4. **Benchmarking ecphoric retrieval** — No benchmark exists. Memex would need to create one to validate the approach.
5. **Embedding model quality for conversation** — No existing benchmark. Needs empirical evaluation on real conversation data.

### What Stream C Covered That A+B Didn't

- The full landscape of memory-augmented systems (MemGPT, Mem0, Zep, Cognee)
- RAG evolution from naive to agentic
- Hybrid retrieval best practices and benchmarks (Bruch fusion analysis)
- Vector DB comparison for local-first use
- PKM tool survey and Bush→modern lineage
- Temporal retrieval approaches (Milvus decay, Re3 adaptive gating)
- Graph-based retrieval (GraphRAG, LLM+KG unification)
- Evidence gap for PKM effectiveness

---

## Architectural Implications for Memex (consolidated across all three streams)

### From Stream A (Human Memory):
1. Recall is a write operation (reconsolidation)
2. Store both episodes and schemas (Frame + Artifact)
3. Insight detection is post-hoc only
4. The fog-match is real — it's ecphory
5. 90% conversation loss in 5 minutes
6. Purpose-neutral storage is correct
7. Delayed annotation > immediate annotation
8. Track the solidification trajectory

### From Stream B (LLM Memory):
9. Ecphoric retrieval is architecturally valid (induction heads)
10. Position in context matters (lost-in-the-middle)
11. Use RAG, not fine-tuning (catastrophic forgetting)
12. Both human memory and LLM output confabulate
13. MemGPT is closest prior art
14. No LLM analogue of insight
15. ICL as gradient descent — form of recalled content matters
16. KV cache IS the episodic buffer

### From Stream C (Technical Landscape):
17. Hybrid search is table stakes — differentiate on ecphoric signals
18. Convex combination > RRF when tunable; start with RRF
19. LLM reranking distills to small models (440M viable locally)
20. LanceDB confirmed as right storage choice
21. No embedding model optimized for conversation — evaluate empirically
22. Trails are Bush's unfinished business — make them first-class
23. Conversation as native unit differentiates from all PKM tools
24. Memory layer should be model-agnostic (pattern 2, not pattern 1)
25. Build for testability — the PKM field lacks evidence; memex can provide it
26. Graph layer (lightweight, temporal) complements vector store for structured queries
