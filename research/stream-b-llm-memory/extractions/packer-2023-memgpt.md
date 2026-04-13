---
source: packer-2023-memgpt
title: "MemGPT: Towards LLMs as Operating Systems"
authors: ["Charles Packer", "Sarah Wooders", "Kevin Lin", "et al"]
year: 2023
venue: "arXiv"
citations: 35
tier: 1
rqs_primary: [RQ-B4]
source_type: abstract-only
claims_count: 5
---

# Extraction: Packer et al 2023 — MemGPT

### packer2023:c1
- **Claim:** LLMs are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis.
- **Quote:** "Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B4

### packer2023:c2
- **Claim:** MemGPT proposes virtual context management, drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory.
- **Quote:** "we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B4

### packer2023:c3
- **Claim:** MemGPT intelligently manages different memory tiers to effectively provide extended context within the LLM's limited context window, and uses interrupts to manage control flow between itself and the user.
- **Quote:** "MemGPT (Memory-GPT), a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window, and utilizes interrupts to manage control flow between itself and the user."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B4

### packer2023:c4
- **Claim:** In document analysis, MemGPT can analyze large documents that far exceed the underlying LLM's context window.
- **Quote:** "document analysis, where MemGPT is able to analyze large documents that far exceed the underlying LLM's context window"
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B4

### packer2023:c5
- **Claim:** In multi-session chat, MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with users.
- **Quote:** "multi-session chat, where MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B4
