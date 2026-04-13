---
source: von-oswald-2022-icl-gradient-descent
title: "Transformers learn in-context by gradient descent"
authors: ["Johannes von Oswald", "Eyvind Niklasson", "Ettore Randazzo", "et al"]
year: 2022
venue: "arXiv"
citations: 89
tier: 1
rqs_primary: [RQ-B1, RQ-B3]
source_type: abstract-only
claims_count: 5
---

# Extraction: von Oswald et al 2022 — ICL as Gradient Descent

### vonoswald2022:c1
- **Claim:** Training transformers on auto-regressive objectives is closely related to gradient-based meta-learning formulations.
- **Quote:** "training Transformers on auto-regressive objectives is closely related to gradient-based meta-learning formulations."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### vonoswald2022:c2
- **Claim:** A single linear self-attention layer induces data transformations equivalent to one step of gradient descent on a regression loss.
- **Quote:** "we show the equivalence of data transformations induced by 1) a single linear self-attention layer and by 2) gradient-descent (GD) on a regression loss."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### vonoswald2022:c3
- **Claim:** When training self-attention-only transformers on simple regression tasks, the models learned by GD and transformers show great similarity, and the weights found by optimization match the analytical construction.
- **Quote:** "when training self-attention-only Transformers on simple regression tasks either the models learned by GD and Transformers show great similarity or, remarkably, the weights found by optimization match the construction."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1

### vonoswald2022:c4
- **Claim:** Trained transformers become mesa-optimizers — they learn to perform gradient descent as part of their forward pass.
- **Quote:** "Thus we show how trained Transformers become mesa-optimizers i.e. learn models by gradient descent in their forward pass."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1, RQ-B3

### vonoswald2022:c5
- **Claim:** Transformers surpass the performance of plain gradient descent by learning iterative curvature correction and by learning linear models on deep data representations.
- **Quote:** "we furthermore identify how Transformers surpass the performance of plain gradient descent by learning an iterative curvature correction and learn linear models on deep data representations to solve non-linear regression tasks."
- **Tier:** 1 | **Confidence:** High | **RQ:** RQ-B1
