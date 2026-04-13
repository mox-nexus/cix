---
source: chen-2024-m3-embedding
title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
authors: ["J.B. Chen"]
year: 2024
doi: "https://doi.org/10.48550/arxiv.2402.03216"
cited_by: 48
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C2]
extraction_date: 2026-04-13
claims_count: 6
---

# Extraction: Chen 2024 — M3-Embedding

**Full title:** M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation
**Authors:** J.B. Chen et al.
**Year:** 2024
**DOI:** https://doi.org/10.48550/arxiv.2402.03216
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C2

## Claims

### chen_2024:c1
CLAIM: A single embedding model can simultaneously support dense retrieval, multi-vector retrieval, and sparse retrieval.
QUOTE: "It can simultaneously accomplish the three common retrieval functionalities: dense retrieval, multi-vector retrieval, and sparse retrieval."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### chen_2024:c2
CLAIM: M3-Embedding provides unified semantic retrieval support for more than 100 languages within a single model.
QUOTE: "It provides a uniform support for the semantic retrieval of more than 100 working languages."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### chen_2024:c3
CLAIM: A single embedding model can process inputs ranging from short sentences to long documents of up to 8,192 tokens.
QUOTE: "it is also capable of processing inputs of different granularities, spanning from short sentences to long documents of up to 8,192 tokens."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### chen_2024:c4
CLAIM: Self-knowledge distillation — integrating relevance scores from different retrieval functionalities as a teacher signal — improves embedding training quality.
QUOTE: "we propose a novel self-knowledge distillation approach, where the relevance scores from different retrieval functionalities can be integrated as the teacher signal to enhance the training quality."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### chen_2024:c5
CLAIM: Optimized batching strategy enabling large batch sizes and high training throughput improves the discriminativeness of embeddings.
QUOTE: "We also optimize the batching strategy, which enables a large batch size and high training throughput to improve the discriminativeness of embeddings."
EVIDENCE TIER: T1 empirical
CONFIDENCE: Medium — mechanism described but comparative ablation not detailed in abstract

### chen_2024:c6
CLAIM: M3-Embedding achieves state-of-the-art results on multilingual, cross-lingual, and long-document retrieval benchmarks.
QUOTE: "M3-Embedding exhibits a superior performance in our experiment, leading to new state-of-the-art results on multilingual, cross-lingual, and long-document retrieval benchmarks."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High
