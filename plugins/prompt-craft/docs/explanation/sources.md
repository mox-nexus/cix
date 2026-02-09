# Sources

Full bibliography for prompt-craft techniques.

---

## Core Research

### Many-Shot In-Context Learning
- **Citation:** Agarwal et al. (2024). "Many-Shot In-Context Learning." ACL/NeurIPS.
- **URL:** https://arxiv.org/abs/2404.11018
- **Key finding:** Performance improves consistently up to 50-100+ examples, contradicting "few-shot" assumptions.
- **Used in:** deep-research, assimilate-writing

### Prompt Repetition
- **Citation:** Leviathan, Kalman, Matias (2025). "Prompt Repetition Improves Non-Reasoning LLMs." Google Research.
- **URL:** https://arxiv.org/abs/2512.14982
- **Key finding:** Repeating prompt twice improves accuracy (47/70 wins, 0 losses). One task: 21% → 97%.
- **Used in:** assimilate-writing

### Chain-of-Verification (CoVe)
- **Citation:** Dhuliawala et al. (2024). "Chain-of-Verification Reduces Hallucination in Large Language Models." ACL.
- **URL:** https://arxiv.org/abs/2309.11495
- **Key finding:** 50-70% hallucination reduction through independent verification.
- **Used in:** deep-research

### One-Shot Style Transfer (OSST)
- **Citation:** (2025). "LLM One-Shot Style Transfer for Authorship Attribution and Verification."
- **URL:** https://arxiv.org/abs/2510.13302
- **Key finding:** Neutralize→transfer approach outperforms direct style imitation with minimal examples.
- **Used in:** assimilate-writing

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

## Style & Writing

### LLM Stylistic Fingerprints
- **Citation:** (2025). "Detecting Stylistic Fingerprints of Large Language Models."
- **URL:** https://arxiv.org/abs/2503.01659
- **Key finding:** LLMs have detectable, persistent stylistic fingerprints across prompting styles.
- **Used in:** assimilate-writing

### Do LLMs Write Like Humans?
- **Citation:** PNAS (2025). "Do LLMs Write Like Humans? Variation in Grammatical and Rhetorical Styles."
- **URL:** https://www.pnas.org/doi/10.1073/pnas.2422455122
- **Key finding:** LLMs are noun-heavy, underuse discourse markers compared to human writing.
- **Used in:** assimilate-writing

### StyleDistance
- **Citation:** (2024). "StyleDistance: Stronger Content-Independent Style Embeddings."
- **URL:** https://arxiv.org/abs/2410.12757
- **Key finding:** Content-independent style embeddings enable better style similarity measurement.
- **Used in:** assimilate-writing

### Iterative Paraphrasing
- **Citation:** (2024). "The Erosion of LLM Signatures Through Iterative Paraphrasing."
- **URL:** https://arxiv.org/abs/2512.05311
- **Key finding:** LLM signatures fade after 3-5 paraphrasing rounds.
- **Used in:** assimilate-writing

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
