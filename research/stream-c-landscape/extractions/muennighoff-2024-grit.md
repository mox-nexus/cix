---
source: muennighoff-2024-grit
title: "Generative Representational Instruction Tuning"
authors: ["Niklas Muennighoff"]
year: 2024
doi: "https://doi.org/10.48550/arxiv.2402.09906"
cited_by: 13
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C3]
extraction_date: 2026-04-13
claims_count: 6
---

# Extraction: Muennighoff 2024 — GRIT

**Full title:** Generative Representational Instruction Tuning
**Authors:** Niklas Muennighoff et al.
**Year:** 2024
**DOI:** https://doi.org/10.48550/arxiv.2402.09906
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C3

## Claims

### muennighoff_2024:c1
CLAIM: All text-based language problems can be reduced to either generation or embedding, and current models only perform well at one or the other.
QUOTE: "All text-based language problems can be reduced to either generation or embedding. Current models only perform well at one or the other."
EVIDENCE TIER: T2 theoretical
CONFIDENCE: High — framing claim, well-supported by literature

### muennighoff_2024:c2
CLAIM: A single large language model can be trained to handle both generative and embedding tasks by distinguishing between them through instructions.
QUOTE: "We introduce generative representational instruction tuning (GRIT) whereby a large language model is trained to handle both generative and embedding tasks by distinguishing between them through instructions."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### muennighoff_2024:c3
CLAIM: GritLM 7B sets a new state of the art on the Massive Text Embedding Benchmark (MTEB) while outperforming all models up to its size on generative tasks.
QUOTE: "our resulting GritLM 7B sets a new state of the art on the Massive Text Embedding Benchmark (MTEB) and outperforms all models up to its size on a range of generative tasks"
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### muennighoff_2024:c4
CLAIM: Scaling GRIT to a mixture-of-experts architecture (8x7B) outperforms all open generative language models while remaining among the best embedding models.
QUOTE: "By scaling up further, GritLM 8x7B outperforms all open generative language models that we tried while still being among the best embedding models."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### muennighoff_2024:c5
CLAIM: Unifying generative and embedding training via GRIT incurs no performance loss compared to training on only generative or only embedding data.
QUOTE: "we find that GRIT matches training on only generative or embedding data, thus we can unify both at no performance loss."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### muennighoff_2024:c6
CLAIM: Unifying retrieval and generation models via GRIT speeds up Retrieval-Augmented Generation (RAG) by more than 60% for long documents.
QUOTE: "the unification via GRIT speeds up Retrieval-Augmented Generation (RAG) by > 60% for long documents, by no longer requiring separate retrieval and generation models."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High
