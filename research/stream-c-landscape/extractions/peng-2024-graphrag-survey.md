---
source: peng-2024-graphrag-survey
title: "Graph Retrieval-Augmented Generation: A Survey"
authors: ["Boci Peng"]
year: 2024
doi: "https://doi.org/10.48550/arxiv.2408.08921"
cited_by: 22
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C2]
extraction_date: 2026-04-13
claims_count: 6
---

# Extraction: Peng 2024 — GraphRAG Survey

**Full title:** Graph Retrieval-Augmented Generation: A Survey
**Authors:** Boci Peng et al.
**Year:** 2024
**DOI:** https://doi.org/10.48550/arxiv.2408.08921
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C2

## Claims

### peng_2024:c1
CLAIM: RAG addresses LLM challenges (hallucination, lack of domain knowledge, outdated information) by referencing an external knowledge base, without requiring retraining.
QUOTE: "By referencing an external knowledge base, RAG refines LLM outputs, effectively mitigating issues such as ``hallucination'', lack of domain-specific knowledge, and outdated information."
EVIDENCE TIER: T3 review
CONFIDENCE: High

### peng_2024:c2
CLAIM: Complex relational structure among entities in databases presents challenges for standard RAG systems.
QUOTE: "the complex structure of relationships among different entities in databases presents challenges for RAG systems."
EVIDENCE TIER: T3 review
CONFIDENCE: High

### peng_2024:c3
CLAIM: GraphRAG leverages structural information across entities to enable more precise and comprehensive retrieval than standard RAG.
QUOTE: "GraphRAG leverages structural information across entities to enable more precise and comprehensive retrieval, capturing relational knowledge and facilitating more accurate, context-aware responses."
EVIDENCE TIER: T3 review
CONFIDENCE: High

### peng_2024:c4
CLAIM: GraphRAG captures relational knowledge, enabling more accurate and context-aware responses compared to flat-document retrieval.
QUOTE: "capturing relational knowledge and facilitating more accurate, context-aware responses."
EVIDENCE TIER: T3 review
CONFIDENCE: Medium — stated as motivation, not empirically demonstrated in the abstract

### peng_2024:c5
CLAIM: The GraphRAG workflow can be formalized into three stages: Graph-Based Indexing, Graph-Guided Retrieval, and Graph-Enhanced Generation.
QUOTE: "We formalize the GraphRAG workflow, encompassing Graph-Based Indexing, Graph-Guided Retrieval, and Graph-Enhanced Generation."
EVIDENCE TIER: T3 review
CONFIDENCE: High

### peng_2024:c6
CLAIM: This is the first comprehensive overview of GraphRAG methodologies, indicating the field's novelty as of 2024.
QUOTE: "This paper provides the first comprehensive overview of GraphRAG methodologies."
EVIDENCE TIER: T3 review
CONFIDENCE: Medium — self-reported novelty claim
