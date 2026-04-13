---
source: kwon-2023-pagedattention
title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
authors: ["Woosuk Kwon", "Z. Li", "Siyuan Zhuang", "et al"]
year: 2023
venue: "SOSP"
citations: 897
tier: 1
rqs_primary: [RQ-B1]
source_type: abstract-only
claims_count: 4
---

# Extraction: Kwon et al 2023 — PagedAttention (vLLM)

### kwon2023:c1
- **Claim:** The key-value cache (KV cache) memory for each LLM request is huge and grows and shrinks dynamically during generation.
- **Quote:** "the key-value cache (KV cache) memory for each request is huge and grows and shrinks dynamically."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### kwon2023:c2
- **Claim:** When managed inefficiently, KV cache memory can be significantly wasted by fragmentation and redundant duplication, limiting the batch size achievable in serving.
- **Quote:** "When managed inefficiently, this memory can be significantly wasted by fragmentation and redundant duplication, limiting the batch size."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### kwon2023:c3
- **Claim:** PagedAttention is an attention algorithm inspired by classical virtual memory and paging techniques in operating systems.
- **Quote:** "we propose PagedAttention, an attention algorithm inspired by the classical virtual memory and paging techniques in operating systems."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### kwon2023:c4
- **Claim:** vLLM (built on PagedAttention) improves throughput of popular LLMs by 2-4x at the same latency compared to state-of-the-art systems.
- **Quote:** "vLLM improves the throughput of popular LLMs by 2--4x with the same level of latency compared to the state-of-the-art systems, such as FasterTransformer and Orca."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1
