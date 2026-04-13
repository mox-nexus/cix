---
source: lee-2024-nv-embed
title: "NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models"
authors: ["Chankyu Lee"]
year: 2024
doi: "https://doi.org/10.48550/arxiv.2405.17428"
cited_by: 10
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C3]
extraction_date: 2026-04-13
claims_count: 7
---

# Extraction: Lee 2024 — NV-Embed

**Full title:** NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models
**Authors:** Chankyu Lee et al.
**Year:** 2024
**DOI:** https://doi.org/10.48550/arxiv.2405.17428
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C3

## Claims

### lee_2024:c1
CLAIM: Decoder-only LLM-based embedding models are beginning to outperform BERT or T5-based embedding models in general-purpose text embedding tasks.
QUOTE: "Decoder-only LLM-based embedding models are beginning to outperform BERT or T5-based embedding models in general-purpose text embedding tasks, including dense vector-based retrieval."
EVIDENCE TIER: T3 review
CONFIDENCE: High — positions within observed trend

### lee_2024:c2
CLAIM: A latent attention layer for obtaining pooled embeddings consistently improves retrieval and downstream task accuracy compared to mean pooling or using the last token embedding from LLMs.
QUOTE: "we propose a latent attention layer to obtain pooled embeddings, which consistently improves retrieval and downstream task accuracy compared to mean pooling or using the last token embedding from LLMs."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### lee_2024:c3
CLAIM: Removing the causal attention mask of LLMs during contrastive training enhances representation learning for embeddings.
QUOTE: "To enhance representation learning, we remove the causal attention mask of LLMs during contrastive training."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### lee_2024:c4
CLAIM: A two-stage contrastive instruction-tuning method — first training on retrieval datasets, then blending non-retrieval tasks — improves both retrieval and non-retrieval task accuracy.
QUOTE: "we introduce a two-stage contrastive instruction-tuning method. It first applies contrastive training with instructions on retrieval datasets, utilizing in-batch negatives and curated hard negative examples. At stage-2, it blends various non-retrieval into instruction tuning, which not only enhances non-retrieval task accuracy but also improves retrieval performance."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### lee_2024:c5
CLAIM: Hard-negative mining, synthetic data generation, and existing public datasets combined together boost embedding model performance.
QUOTE: "we utilize the hard-negative mining, synthetic data generation and existing public available datasets to boost the performance of embedding model."
EVIDENCE TIER: T1 empirical
CONFIDENCE: Medium — enumerated but ablation detail not in abstract

### lee_2024:c6
CLAIM: NV-Embed achieved the number one position on the MTEB leaderboard across 56 tasks (as of May 24 and August 30, 2024).
QUOTE: "our NV-Embed-v1 and NV-Embed-v2 models obtained the No.1 position on the MTEB leaderboard (as of May 24 and August 30, 2024, respectively) across 56 tasks"
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### lee_2024:c7
CLAIM: NV-Embed achieved the highest scores in the Long Doc section and second-highest in the QA section of the AIR Benchmark, demonstrating out-of-domain generalization beyond MTEB.
QUOTE: "It also achieved the highest scores in the Long Doc section and the second-highest scores in the QA section of the AIR Benchmark, which covers a range of out-of-domain information retrieval topics beyond those in MTEB."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High
