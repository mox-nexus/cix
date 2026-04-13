# Stream B: LLMs and Memory Structurally — Research Scope

**Status:** Scope frozen.
**Frozen:** 2026-04-13
**Purpose:** Understand LLMs' structural relationship with memory — what do they actually do, and where does the analogy to human memory hold or break?
**Depends on:** Stream A findings (human memory architecture) for the cross-stream bridges.

---

## Context

Stream A established what cognitive science says about human memory. Key findings:
- Memory is reconstructive (Bartlett), not reproductive
- Every retrieval modifies the memory (reconsolidation, Nader)
- Retrieval requires BOTH stored trace AND current cognitive state (synergistic ecphory, Tulving)
- Insight has measurable neural precursors but cannot be predicted by metacognitive self-report
- 90% of conversational content is lost within 5 minutes (Stafford)

Stream B asks: what is the LLM analogue of each of these? Where does the structural parallel hold, and where does it break?

The user's triggering question: "say you have 100 skills loaded, and I say a phrase, what makes you likely to move your attention to that skill?" — this is the LLM version of the retrieval cue question.

---

## Research Questions

### RQ-B1 — What are the structural analogues of memory in LLMs?

How do LLMs "remember"? What mechanisms serve as functional analogues of human memory systems?

- Context window as working memory — is this analogy structurally valid or misleading?
- Weights as long-term memory — what does "stored in weights" actually mean for retrieval?
- KV cache as episodic buffer — does the cache behave like episodic memory?
- RAG as external memory — how does retrieval-augmented generation map to the extended mind thesis?
- In-context learning vs weight-based learning — two distinct memory mechanisms?

### RQ-B2 — How does attention function as a retrieval mechanism?

When an LLM has 100 skills loaded in context and the user says a phrase, what determines which skill gets attended to?

- Attention patterns as associative retrieval — does transformer attention implement something like ecphory?
- Key-query matching vs content-based retrieval — is attention more like encoding specificity or content similarity?
- How does context length affect retrieval quality? Is there a "forgetting curve" in long contexts?
- What does mechanistic interpretability say about how information is retrieved from context?

### RQ-B3 — Where do the human-LLM memory analogies break?

Which structural parallels are genuine and which are misleading metaphors?

- Does anything in LLMs correspond to reconsolidation (memory modification on retrieval)?
- Is there an LLM analogue of insight (sudden restructuring of representations)?
- Catastrophic forgetting vs human forgetting — same mechanism or surface similarity?
- Sample efficiency: humans need few observations for insight (Friston), LLMs need millions. Why?
- Is the "stored in weights" metaphor accurate, or are weights better understood as a generative model (not a memory store)?

### RQ-B4 — What memory architectures exist for LLM-based systems?

What approaches have been built to give LLMs persistent memory?

- MemGPT / memory-augmented architectures — how do they work?
- Long-context models (Gemini 1M, Claude 200K) — does more context change the memory picture?
- Episodic memory buffers in agents (AutoGPT-style scratchpads)
- Knowledge graphs + vector retrieval as external memory
- Fine-tuning as memory formation — what does it encode and what does it lose?

---

## Boundaries

### In scope
- Transformer attention mechanisms and their relationship to memory/retrieval
- Mechanistic interpretability findings on how information flows in transformers
- RAG architectures and their memory-theoretic properties
- Memory-augmented LLM systems (MemGPT, scratchpads, episodic buffers)
- Long-context scaling and its effects on retrieval quality
- Catastrophic forgetting and continual learning
- In-context learning as a memory mechanism
- The "what makes attention move" question specifically

### Out of scope
- LLM training methodology details (pretraining data, RLHF specifics)
- Benchmark performance on memory-unrelated tasks
- Commercial product comparisons
- Safety/alignment (except where it intersects memory, e.g., RLHF affecting what's "remembered")
- Multimodal memory (vision-language models) — defer to Stream C if relevant

---

## Source Hierarchy

| Priority | Source family | Why |
|----------|--------------|-----|
| **1** | Mechanistic interpretability (Anthropic, EleutherAI, Neel Nanda) | Direct evidence on how transformers retrieve and process information |
| **1** | Attention mechanism research (Vaswani original + subsequent analysis) | Foundation for understanding retrieval |
| **1** | In-context learning theory (Olsson et al on induction heads, Garg et al) | How LLMs learn from context — the most memory-like mechanism |
| **1** | Memory-augmented LLM systems (MemGPT, RETRO, RAG surveys) | Direct attempts to add memory to LLMs |
| **2** | Long-context research (scaling laws, lost-in-the-middle, needle-in-haystack) | Empirical evidence on context-as-memory limits |
| **2** | Catastrophic forgetting / continual learning | The failure mode of weight-based memory |
| **2** | Cognitive architectures for AI (ACT-R inspired, SOAR-like) | Historical attempts to build memory into AI |
| **3** | Popular technical writing (Lilian Weng, Jay Alammar, Simon Willison) | Accessible synthesis for orientation |

---

## Success Criteria

Done when:
- [ ] Each RQ-B1 through RQ-B4 has findings with at least 3 sources
- [ ] The human-LLM memory analogy is explicitly mapped: which parallels are structural, which are metaphorical, which break
- [ ] Stream A findings (ecphory, reconsolidation, insight mechanism, metacognition asymmetry) are each evaluated for LLM analogues
- [ ] Architectural implications for memex from the LLM side are named (how should memex interact with LLM memory?)

## Null Hypotheses

- **RQ-B1 null:** The "memory" metaphor for LLMs is fundamentally misleading. LLMs don't have memory in any structurally meaningful sense — they have pattern completion. Treating them as having memory leads to wrong architectural choices.
- **RQ-B2 null:** Attention is not retrieval. It's a weighted mixing operation with no structural analogy to human memory retrieval. The "attention as ecphory" mapping is a category error.
- **RQ-B3 null:** All human-LLM memory analogies are surface-level. The mechanisms are so different that no useful architectural insight comes from the comparison. Memex should be designed for human memory alone, ignoring the LLM side.
- **RQ-B4 null:** Existing memory architectures for LLMs are engineering hacks, not principled solutions. None of them address the fundamental problem (LLMs don't have memory) — they just paper over it with external storage.
