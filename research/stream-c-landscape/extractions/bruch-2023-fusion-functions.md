---
source: bruch-2023-fusion-functions
title: "An Analysis of Fusion Functions for Hybrid Retrieval"
authors: ["Sebastian Bruch"]
year: 2023
doi: "https://doi.org/10.1145/3596512"
cited_by: 34
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C2]
extraction_date: 2026-04-13
claims_count: 6
---

# Extraction: Bruch 2023 — Fusion Functions for Hybrid Retrieval

**Full title:** An Analysis of Fusion Functions for Hybrid Retrieval
**Authors:** Sebastian Bruch et al.
**Year:** 2023
**DOI:** https://doi.org/10.1145/3596512
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C2

## Claims

### bruch_2023:c1
CLAIM: Lexical and semantic search are complementary in how they model relevance, motivating hybrid fusion approaches.
QUOTE: "lexical and semantic search are fused together with the intuition that the two are complementary in how they model relevance."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### bruch_2023:c2
CLAIM: Reciprocal rank fusion (RRF) is sensitive to its parameters, contrary to prior findings suggesting parameter robustness.
QUOTE: "Contrary to existing studies, we find RRF to be sensitive to its parameters"
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### bruch_2023:c3
CLAIM: Learning a convex combination fusion is generally agnostic to the choice of score normalization.
QUOTE: "the learning of a convex combination fusion is generally agnostic to the choice of score normalization"
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### bruch_2023:c4
CLAIM: Convex combination fusion outperforms reciprocal rank fusion in both in-domain and out-of-domain settings.
QUOTE: "convex combination outperforms RRF in in-domain and out-of-domain settings"
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### bruch_2023:c5
CLAIM: Convex combination fusion is sample efficient, requiring only a small set of training examples to tune its single parameter to a target domain.
QUOTE: "convex combination is sample efficient, requiring only a small set of training examples to tune its only parameter to a target domain."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### bruch_2023:c6
CLAIM: Hybrid search in text retrieval can be achieved by convex combination of lexical and semantic scores or by reciprocal rank fusion.
QUOTE: "we examine fusion by a convex combination of lexical and semantic scores, as well as the reciprocal rank fusion (RRF) method"
EVIDENCE TIER: T2 theoretical
CONFIDENCE: High
