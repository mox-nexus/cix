---
source: luo-2023-catastrophic-forgetting
title: "An Empirical Study of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning"
authors: ["Yun Luo", "Zhen Yang", "Fandong Meng", "et al"]
year: 2023
venue: "arXiv"
citations: 56
tier: 1
rqs_primary: [RQ-B3]
source_type: abstract-only
claims_count: 5
---

# Extraction: Luo et al 2023 — Catastrophic Forgetting in LLMs

### luo2023:c1
- **Claim:** Catastrophic forgetting is generally observed in LLMs ranging from 1B to 7B parameters during continual instruction tuning.
- **Quote:** "The experiments reveal that catastrophic forgetting is generally observed in LLMs ranging from 1b to 7b parameters."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B3

### luo2023:c2
- **Claim:** As model scale increases (within the 1B-7B range), the severity of forgetting intensifies, which may result from the much more significant initial performance of larger LLMs.
- **Quote:** "as the model scale increases, the severity of forgetting intensifies in such a model scale range which may result from the much significant initial performance in the larger LLM."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B3
- **Note:** Counter-intuitive — larger models forget MORE, not less, possibly because they had more to lose.

### luo2023:c3
- **Claim:** Comparing decoder-only (BLOOMZ) and encoder-decoder (mT0) architectures, BLOOMZ exhibits less forgetting and retains more knowledge.
- **Quote:** "Comparing the decoder-only model BLOOMZ with the encoder-decoder model mT0, BLOOMZ exhibits less forgetting and retains more knowledge."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B3

### luo2023:c4
- **Claim:** LLMs can mitigate language biases (such as gender bias) during continual fine-tuning — forgetting is not uniformly negative.
- **Quote:** "we also observe that LLMs can mitigate language biases, such as gender bias, during continual fine-tuning."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B3

### luo2023:c5
- **Claim:** General instruction tuning can help alleviate the forgetting phenomenon in LLMs during subsequent fine-tuning.
- **Quote:** "general instruction tuning can help alleviate the forgetting phenomenon in LLMs during subsequent fine-tuning."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B3
