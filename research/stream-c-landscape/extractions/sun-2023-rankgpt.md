---
source: sun-2023-rankgpt
title: "Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents"
authors: ["Weiwei Sun"]
year: 2023
doi: "https://doi.org/10.48550/arxiv.2304.09542"
cited_by: 23
source_type: abstract-only (OpenAlex)
rqs_primary: [RQ-C2]
extraction_date: 2026-04-13
claims_count: 6
---

# Extraction: Sun 2023 — RankGPT

**Full title:** Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents
**Authors:** Weiwei Sun et al.
**Year:** 2023
**DOI:** https://doi.org/10.48550/arxiv.2304.09542
**Source type:** Abstract-only (OpenAlex)
**Target RQ:** RQ-C2

## Claims

### sun_2023:c1
CLAIM: Properly instructed LLMs (ChatGPT, GPT-4) can deliver competitive or superior relevance ranking results compared to state-of-the-art supervised methods on popular IR benchmarks.
QUOTE: "properly instructed LLMs can deliver competitive, even superior results to state-of-the-art supervised methods on popular IR benchmarks."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### sun_2023:c2
CLAIM: Existing work uses the generative ability of LLMs for information retrieval rather than direct passage ranking, creating a gap between pre-training objectives and ranking objectives.
QUOTE: "existing work utilizes the generative ability of LLMs for Information Retrieval (IR) rather than direct passage ranking. The discrepancy between the pre-training objectives of LLMs and the ranking objective poses another challenge."
EVIDENCE TIER: T2 theoretical
CONFIDENCE: High

### sun_2023:c3
CLAIM: LLM ranking capabilities can be distilled into small specialized models using a permutation distillation scheme.
QUOTE: "we delve into the potential for distilling the ranking capabilities of ChatGPT into small specialized models using a permutation distillation scheme."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### sun_2023:c4
CLAIM: A distilled 440M parameter model outperforms a 3B supervised model on the BEIR benchmark, demonstrating effective knowledge transfer from LLM re-rankers.
QUOTE: "a distilled 440M model outperforms a 3B supervised model on the BEIR benchmark."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High

### sun_2023:c5
CLAIM: LLMs demonstrate remarkable zero-shot generalization across language-related tasks, including search-relevant tasks.
QUOTE: "Large Language Models (LLMs) have demonstrated remarkable zero-shot generalization across various language-related tasks, including search engines."
EVIDENCE TIER: T2 theoretical
CONFIDENCE: High

### sun_2023:c6
CLAIM: Data contamination is a concern when evaluating LLMs on existing IR benchmarks, motivating the creation of a new test set (NovelEval) based on the latest knowledge.
QUOTE: "to address concerns about data contamination of LLMs, we collect a new test set called NovelEval, based on the latest knowledge and aiming to verify the model's ability to rank unknown knowledge."
EVIDENCE TIER: T1 empirical
CONFIDENCE: High
