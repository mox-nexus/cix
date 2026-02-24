# Metacognition Reference

Practical techniques for building agents that know what they know and know what they don't know. Synthesized from two research reports: agentic metacognition (CoVe, SSR, self-consistency, calibration) and radical doubt (four-pass reading, gap-state tracking, adversarial self-questioning).

## CoVe Factored Execution

**Source**: Dhuliawala et al. ACL 2024. **Effect**: 50-70% hallucination reduction.

Four stages with structural independence:
1. **Draft** — Generate initial understanding
2. **Plan verification questions** — Target specific claims
3. **Answer independently** — Each question answered in isolation, no access to draft
4. **Synthesize** — Produce revised understanding, correcting inconsistencies

The critical design: factored execution. Each verification question gets its own context. The model isn't seeking facts to confirm its draft — it's answering cold. This prevents initial bias from corrupting verification.

**Token cost**: 3-5x base generation. Worth it for correctness-critical content.

**When to use**: Research synthesis, novel domains, any content where misunderstanding compounds downstream.

## The Full Discovery Protocol

For correctness-critical content, the full protocol combines techniques:

### Phase 1: Initial Reading (Metacognitive Prompting)

Apply Wang & Zhao (NAACL 2024) five stages:
1. Parse: What are the explicit claims?
2. Preliminary interpretation: What do I think this means?
3. Critical evaluation: Where might I be wrong? What am I assuming?
4. Revised understanding: After reflection, I believe...
5. Confidence mapping: Confident about X, uncertain about Y, don't understand Z

### Phase 2: Verification (CoVe + Self-Consistency)

1. Generate verification questions targeting each claim
2. Answer each question independently (factored — no access to initial interpretation)
3. Generate 3+ alternative interpretations of ambiguous sections
4. Check convergence: where do interpretations agree? Where do they diverge?
5. Flag divergent areas as genuine uncertainty

### Phase 3: Comprehension Testing (SSR + Perturbation)

1. Decompose understanding into atomic sub-claims
2. For each, independently re-derive from source
3. Score confidence per sub-claim (re-derivation convergence)
4. Apply comprehension tests: rephrase, implication, boundary, novelty
5. Target lowest-confidence sub-claims for re-reading

### Phase 4: Adversarial Self-Examination

1. "Could I be wrong about X?" for each major claim
2. "What would someone who disagrees say?"
3. "Am I following the source or my prior beliefs?"
4. Apply MAPS Critic: existential, consistency, boundary checks

### Phase 5: Honest Uncertainty Declaration

Categorize understanding into: Solid / Probable / Uncertain / Unknown.
Carry these categories into the explanation — never present "uncertain" as "solid."

## Token Budget Estimates

| Step | Tokens | Notes |
|------|--------|-------|
| Four-pass reading | ~1000-2000 | Depends on source length |
| Gap-state tracking | ~300-800 | Maintained incrementally |
| Adversarial questioning | ~500-1000 | Per key claim |
| CoVe verification | ~500-1500 | Per verification question |
| Explain-back | ~500-1500 | Per iteration |
| **Total overhead** | **~3000-7000** | Before writing begins |

For a typical explanation of ~2000 tokens, this represents 1.5-3.5x overhead. Significant but justified for correctness-critical content.

## Where Techniques Live in the Architecture

| Technique | Level | Cost | When |
|-----------|-------|------|------|
| Four-pass reading | Agent prompt (feynman) | Low | Always |
| Gap-state tracking | Agent prompt (feynman) | Low | Always |
| Adversarial self-questioning | Agent prompt (feynman) | Moderate | Always for key claims |
| Five Whys | Agent prompt (feynman) | Low | Central claims |
| CoVe verification | Skill reference (here) | Moderate | Correctness-critical |
| Explain-back (interactive) | Skill workflow | Variable | Novel domains |
| Explain-back (internal) | Agent prompt (feynman) | Moderate | Routine docs |
| Full protocol | Skill reference (here) | High | Research synthesis |

**Design principle**: Embed four-pass reading, gap-state tracking, and adversarial self-questioning in the agent prompt (always active, low cost). Make CoVe and interactive explain-back available as skill-level protocols for high-stakes content.

## Failure Modes

| Failure | Description | Mitigation |
|---------|-------------|------------|
| **Performative metacognition** | Goes through motions without genuine reflection | Use structural checks (convergence), not verbal self-assessment |
| **Confident refinement** | More polished but equally wrong output | Require re-derivation from source, not just revision of draft |
| **Circular verification** | Verifies using same biases that produced claims | Factored execution (CoVe), independent re-derivation |
| **Sycophantic doubt** | Performs doubt but doesn't change answer | Check: does doubt produce different interpretations? |
| **Parametric override** | Prior knowledge overrides faithful reading | Context-faithfulness testing, explicit source-vs-belief separation |
| **Metacognitive overhead** | So much verification the agent never reaches explanation | Budget effort by confidence — verify uncertain claims, not certain ones |

## Key Effect Sizes

| Technique | Effect | Source |
|-----------|--------|--------|
| CoVe (factored) | 50-70% hallucination reduction | Dhuliawala et al. ACL 2024 |
| Self-Consistency | +6-18% on reasoning benchmarks | Wang et al. ICLR 2023 |
| SSR decomposition | 67.57% relative improvement over CoT | Shi et al. 2025 |
| Metacognitive Prompting | Outperforms CoT on majority NLU tasks | Wang & Zhao NAACL 2024 |
| "Could You Be Wrong?" | Effective debiasing across reasoning biases | Zavala et al. MDPI AI 2025 |

## Sources

- Dhuliawala et al. (2024). "Chain-of-Verification Reduces Hallucination." ACL 2024.
- Han et al. (2025). "Read Before You Think." arXiv:2504.09402.
- Huang et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet." ICLR 2024.
- Park et al. (2024). "LLMs' Reading Comprehension Is Affected by Parametric Knowledge." arXiv:2404.06283.
- Shi et al. (2025). "SSR: Socratic Self-Refine." arXiv:2511.10621.
- Wang & Zhao (2024). "Metacognitive Prompting Improves Understanding." NAACL 2024.
- Xiong et al. (2024). "Can LLMs Express Their Uncertainty?" ICLR 2024.
- Zavala et al. (2025). "Could You Be Wrong." MDPI AI 7(1).
- MAPS (2025). arXiv:2503.16905.
- MemR3 (2024). arXiv:2512.20237.
