---
source: olsson-2022-induction-heads
title: "In-context Learning and Induction Heads"
authors: ["Catherine Olsson", "Nelson Elhage", "Neel Nanda", "et al"]
year: 2022
venue: "arXiv (Anthropic)"
citations: 84
tier: 1
rqs_primary: [RQ-B1, RQ-B2]
source_type: abstract-only
claims_count: 5
---

# Extraction: Olsson et al 2022 — Induction Heads

### olsson2022:c1
- **Claim:** "Induction heads" are attention heads that implement a specific algorithm: completing token sequences of the form [A][B] ... [A] -> [B] by finding a previous occurrence of the current token and predicting what followed.
- **Quote:** "'Induction heads' are attention heads that implement a simple algorithm to complete token sequences like [A][B] ... [A] -> [B]."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1, RQ-B2

### olsson2022:c2
- **Claim:** The authors present preliminary evidence that induction heads may constitute the mechanism for the majority of all in-context learning in large transformer models.
- **Quote:** "we present preliminary and indirect evidence for a hypothesis that induction heads might constitute the mechanism for the majority of all 'in-context learning' in large transformer models"
- **Tier:** 1 | **Confidence:** Medium | **RQ:** RQ-B1
- **Note:** Hedged — "preliminary and indirect evidence" for a "hypothesis." Not established fact.

### olsson2022:c3
- **Claim:** Induction heads develop at precisely the same point during training as a sudden sharp increase in in-context learning ability, visible as a bump in the training loss.
- **Quote:** "induction heads develop at precisely the same point as a sudden sharp increase in in-context learning ability, visible as a bump in the training loss."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### olsson2022:c4
- **Claim:** For small attention-only models, the evidence that induction heads cause in-context learning is strong and causal. For larger models with MLPs, the evidence is correlational.
- **Quote:** "For small attention-only models, we present strong, causal evidence; for larger models with MLPs, we present correlational evidence."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1
- **Note:** Critical qualifier — the strong causal claim only holds for small attention-only models. The claim for production-scale LLMs is correlational.

### olsson2022:c5
- **Claim:** In-context learning is operationalized as decreasing loss at increasing token indices — the model gets better at predicting later tokens by using earlier context.
- **Quote:** "i.e. decreasing loss at increasing token indices"
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1
