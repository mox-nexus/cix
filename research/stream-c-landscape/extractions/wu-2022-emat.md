---
source: wu-2022-emat
title: "An Efficient Memory-Augmented Transformer for Knowledge-Intensive NLP Tasks"
authors: ["Yuxiang Wu"]
year: 2022
doi: "https://doi.org/10.18653/v1/2022.emnlp-main.346"
openalex_id: "https://openalex.org/W4411630063"
tier: 1
rqs_primary: [RQ-C1]
rqs_secondary: []
extraction_date: 2026-04-13
source_type: abstract-only (OpenAlex)
claims_count: 7
---

# Extraction: Wu 2022 — Efficient Memory-Augmented Transformer (EMAT)

**Full title:** An Efficient Memory-Augmented Transformer for Knowledge-Intensive NLP Tasks
**Authors:** Yuxiang Wu et al.
**Year:** 2022
**DOI:** https://doi.org/10.18653/v1/2022.emnlp-main.346
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C1

## Claims

### wu_2022:c1
- **Claim:** Parametric models and retrieval-augmented models have complementary strengths in computational efficiency and predictive accuracy.
- **Quote:** "Parametric and retrieval-augmented models have complementary strengths in terms of computational efficiency and predictive accuracy."
- **Tier:** T2 theoretical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c2
- **Claim:** EMAT encodes external knowledge into a key-value memory and uses fast maximum inner product search for memory querying.
- **Quote:** "it encodes external knowledge into a key-value memory and exploits the fast maximum inner product search for memory querying."
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c3
- **Claim:** EMAT introduces pre-training tasks that enable encoding of informative key-value representations.
- **Quote:** "We also introduce pre-training tasks that allow EMAT to encode informative key-value representations"
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c4
- **Claim:** EMAT learns an implicit strategy to integrate multiple memory slots into the transformer.
- **Quote:** "and to learn an implicit strategy to integrate multiple memory slots into the transformer."
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c5
- **Claim:** Augmenting T5-base with EMAT on Natural Questions improved exact match from 25.8 to 44.3 while retaining 1000 queries/s throughput.
- **Quote:** "simply augmenting parametric models (T5-base) using our method produces more accurate results (e.g., 25.8 to 44.3 EM on NQ) while retaining a high throughput (e.g., 1000 queries/s on NQ)."
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c6
- **Claim:** EMAT runs substantially faster than retrieval-augmented models across all tested tasks.
- **Quote:** "Compared to retrieval-augmented models, EMAT runs substantially faster across the board"
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1

### wu_2022:c7
- **Claim:** EMAT produces more accurate results than retrieval-augmented models on Wizard of Wikipedia and ELI5 datasets.
- **Quote:** "and produces more accurate results on WoW and ELI5."
- **Tier:** T1 empirical | **Confidence:** High | **RQ:** RQ-C1
