---
source: garcia-2024-gpt2-acronyms
title: "How does GPT-2 Predict Acronyms? Extracting and Understanding a Circuit via Mechanistic Interpretability"
authors: ["Jorge Garcia-Carrasco", "Alejandro Mate", "Juan Trujillo"]
year: 2024
venue: "arXiv"
citations: 2
tier: 2
rqs_primary: [RQ-B2]
source_type: abstract-only
claims_count: 4
---

# Extraction: Garcia-Carrasco et al 2024 — GPT-2 Acronym Circuit

### garcia2024:c1
- **Claim:** The prediction of three-letter acronyms in GPT-2 Small is performed by a circuit composed of 8 attention heads, which is approximately 5% of the total heads in the model.
- **Quote:** "the prediction is performed by a circuit composed of 8 attention heads (~5% of the total heads)"
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B2

### garcia2024:c2
- **Claim:** The 8 attention heads were classified into three groups according to their role in the acronym prediction task.
- **Quote:** "which we classified in three groups according to their role."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B2

### garcia2024:c3
- **Claim:** The circuit's attention heads concentrate the acronym prediction functionality — they are necessary and specific to this task.
- **Quote:** "We also demonstrate that these heads concentrate the acronym prediction functionality."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B2

### garcia2024:c4
- **Claim:** The most relevant heads in the circuit use positional information propagated via the causal mask mechanism to perform their retrieval function.
- **Quote:** "we mechanistically interpret the most relevant heads of the circuit and find out that they use positional information which is propagated via the causal mask mechanism."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B2
