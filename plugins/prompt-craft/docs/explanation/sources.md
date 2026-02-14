# Sources

Full bibliography for prompt-craft techniques.

---

## Core Research

### Many-Shot In-Context Learning
- **Citation:** Agarwal et al. (2024). "Many-Shot In-Context Learning." ACL/NeurIPS.
- **URL:** https://arxiv.org/abs/2404.11018
- **Key finding:** Performance improves consistently up to 50-100+ examples, contradicting "few-shot" assumptions.
- **Used in:** deep-research

### Chain-of-Verification (CoVe)
- **Citation:** Dhuliawala et al. (2024). "Chain-of-Verification Reduces Hallucination in Large Language Models." ACL.
- **URL:** https://arxiv.org/abs/2309.11495
- **Key finding:** 50-70% hallucination reduction through independent verification.
- **Used in:** deep-research

---

## Reasoning Models

### o1 Prompting Patterns
- **Citation:** Lenny's Newsletter (2025). "Prompt Engineering for o1."
- **Key finding:** o1 performs worse with examples; over-detailed prompts counterproductive.
- **Used in:** deep-reasoning

### Role Prompting Effectiveness
- **Citation:** Academic meta-analysis (2024).
- **Key finding:** Role prompting has "little to no effect on correctness" for advanced models.
- **Used in:** deep-reasoning

---

## Paper Synthesis

### Dual-LLM Cross-Critique
- **Citation:** (2024). Multi-document synthesis research.
- **Key finding:** 0.94 accuracy on concordant extractions; 51% of discordant responses become concordant after cross-critique.
- **Used in:** synthesize-papers

### Plan-Based Synthesis (LitLLMs)
- **Citation:** (2024). LitLLMs paper.
- **Key finding:** Plan-first synthesis outperforms direct generation, fewer hallucinations.
- **Used in:** synthesize-papers

### Claimify Pipeline
- **Citation:** (2024). Claim extraction research.
- **Key finding:** 99% claim entailment through selection → disambiguation → decomposition.
- **Used in:** synthesize-papers

---

## Platform Research

### Hallucination Rates
- **Citation:** Nature Communications (2025), Omniscience Index, Deakin University studies.
- **Key finding:** 50-90% of LLM responses not fully supported by cited sources.
- **Used in:** deep-research

### Citation Accuracy
- **Citation:** Multiple sources (2025).
- **Key finding:** Claude ~90% precision, Gemini 66% DOI errors, OpenAI 62% claim-sourced.
- **Used in:** deep-research

---

## Prompt Engineering Guides

### General
- [Prompt Engineering Guide](https://www.promptingguide.ai/) — Comprehensive techniques reference
- [Lakera Prompt Engineering Guide 2026](https://www.lakera.ai/blog/prompt-engineering-guide) — Current best practices

### Chain-of-Thought
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot) — CoT technique documentation

---

## Meta-Research

### 1,500 Papers Analysis
- **Citation:** Aakash Gupta analysis (2024).
- **Key finding:** Over-detailed prompts counterproductive with sophisticated models.
- **Used in:** deep-reasoning

---

*Last updated: February 2026*
