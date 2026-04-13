# Verification: Stream B Load-Bearing Claims

**Protocol:** CoVE — independent re-read of source abstracts (all available in extractions-input.json), adversarial comparison against extracted claims.
**Claims verified:** 15 (architecturally load-bearing for memex)

---

## Summary

| Verdict | Count |
|---|---|
| VERIFIED | 14 |
| CORRECTED | 1 |
| REFUTED | 0 |

---

## Claim-by-Claim

### olsson2022:c1 — VERIFIED
CLAIM: Induction heads implement [A][B]...[A]->[B] token completion.
QUOTE CHECK: "are attention heads that implement a simple algorithm to complete token sequences like [A][B] ... [A] -> [B]" — verbatim, verified against abstract.

### olsson2022:c2 — CORRECTED
CLAIM: Induction heads may constitute the mechanism for the majority of all ICL.
QUOTE CHECK: "preliminary and indirect evidence for a hypothesis that induction heads might constitute the mechanism" — verbatim.
CORRECTION: The extraction's claim text should preserve the hedges "preliminary," "indirect," and "might." The claim is a HYPOTHESIS with preliminary evidence, not an established finding. Extraction preserves this in the Note but the claim text should be more hedged.
CORRECTED CLAIM: "The authors present preliminary and indirect evidence for the hypothesis that induction heads might be the mechanism for the majority of in-context learning."

### olsson2022:c3 — VERIFIED
CLAIM: Induction heads develop at the same training point as the ICL phase change.
QUOTE CHECK: "induction heads develop at precisely the same point as a sudden sharp increase in in-context learning ability" — verbatim.

### vonoswald2022:c1 — VERIFIED
CLAIM: Training transformers on auto-regressive objectives is closely related to gradient-based meta-learning.
QUOTE CHECK: "training Transformers on auto-regressive objectives is closely related to gradient-based meta-learning formulations" — verbatim.

### vonoswald2022:c4 — VERIFIED
CLAIM: Trained transformers become mesa-optimizers performing gradient descent in their forward pass.
QUOTE CHECK: "trained Transformers become mesa-optimizers i.e. learn models by gradient descent in their forward pass" — verbatim.

### kwon2023:c1 — VERIFIED
CLAIM: KV cache memory is huge and grows/shrinks dynamically.
QUOTE CHECK: "the key-value cache (KV cache) memory for each request is huge and grows and shrinks dynamically" — verbatim.

### an2024:c1 — VERIFIED
CLAIM: LLMs struggle to utilize information in long contexts (lost-in-the-middle).
QUOTE CHECK: "they still struggle to fully utilize information within the long context, known as the lost-in-the-middle challenge" — verbatim.

### an2024:c4 — VERIFIED
CLAIM: FILM-7B robustly retrieves from different positions in 32K context.
QUOTE CHECK: "FILM-7B can robustly retrieve information from different positions in its 32K context window" — verbatim.

### garcia2024:c1 — VERIFIED
CLAIM: Acronym prediction circuit is 8 attention heads (~5% of total).
QUOTE CHECK: "a circuit composed of 8 attention heads (~5% of the total heads)" — verbatim.

### luo2023:c1 — VERIFIED
CLAIM: Catastrophic forgetting generally observed in 1B-7B LLMs during continual fine-tuning.
QUOTE CHECK: "catastrophic forgetting is generally observed in LLMs ranging from 1b to 7b parameters" — verbatim.

### luo2023:c2 — VERIFIED
CLAIM: Severity of forgetting intensifies as model scale increases in the 1B-7B range.
QUOTE CHECK: "as the model scale increases, the severity of forgetting intensifies in such a model scale range" — verbatim.

### packer2023:c2 — VERIFIED
CLAIM: MemGPT uses virtual context management inspired by OS hierarchical memory.
QUOTE CHECK: "virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems" — verbatim.

### packer2023:c5 — VERIFIED
CLAIM: MemGPT agents remember, reflect, and evolve through long-term interactions.
QUOTE CHECK: "conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users" — verbatim.

### huang2023:c1 — VERIFIED
CLAIM: LLMs generate plausible yet nonfactual content (hallucination).
QUOTE CHECK: "LLMs are prone to hallucination, generating plausible yet nonfactual content" — verbatim.

### marblestone2016:c1 — VERIFIED
CLAIM: Three hypotheses for brain-DL integration: cost function optimization, diverse cost functions, pre-structured architecture.
QUOTE CHECK: "We hypothesize that (1) the brain optimizes cost functions, (2) the cost functions are diverse across brain areas and change over development, and (3) optimization operates within a pre-structured architecture" — verbatim.

---

## Verification Coverage
- 15 of 44 claims verified (34%)
- All load-bearing claims for the 4 RQs covered
- 1 correction: olsson2022:c2 needs stronger hedging (hypothesis, not finding)
- 0 refutations
