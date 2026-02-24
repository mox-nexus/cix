# LLM-Assisted Academic Paper Synthesis: High-Fidelity Techniques

**Research Date:** 2026-02-24
**Focus:** Provenance, verbatim grounding, metacognitive scaffolds, multi-paper synthesis integrity
**Method:** Systematic web search of academic papers, technical reports, and practitioner guides (2024-2026)
**Priority:** Empirical results over opinion pieces

---

## Context

This research targets a specific problem: using LLMs as agents in a multi-paper academic synthesis pipeline where every claim must trace to a verbatim passage from a source document. The failure modes are well-documented: LLMs hallucinate citations at rates from 14% to 95% depending on model and domain (GhostCite, 2026; SPY Lab/arXiv analysis), fabricated references appear in peer-reviewed venues (100+ hallucinated citations found across 53 NeurIPS 2025 papers), and chimeric references that blend elements from multiple real papers are particularly insidious.

The techniques below are ordered by the pipeline stage where they apply: extraction, verification, synthesis, and metacognitive scaffolding.

---

## 1. Direct Quote Extraction Techniques

### 1.1 Deterministic Quoting (Invetech/Yeung, 2024)

**Technique:** Separate the quote selection from the quote retrieval. The LLM chooses *which* passage to cite, but the actual text is retrieved via traditional database lookup — never passed through the LLM.

**Key Property:** The displayed quoted text has a "zero false positives" guarantee because it never passed through the model. The LLM selects a reference ID; the system retrieves verbatim text by ID from a non-AI store.

**Evidence Strength:** Practitioner report (Invetech healthcare application). No peer-reviewed evaluation, but the architectural insight is sound: if text never enters the LLM context as generatable output, it cannot be hallucinated.

**Limitation:** Surrounding LLM-generated commentary may still hallucinate. The LLM may select an irrelevant but verbatim quote.

**Applicability to paper synthesis:** HIGH. Store paper text in a database indexed by passage ID. LLM agents select passage IDs; retrieval is deterministic lookup.

**Source:** [Deterministic Quoting: Making LLMs Safer for Healthcare](https://mattyyeung.github.io/deterministic-quoting) (Yeung, 2024)

---

### 1.2 LLMQuoter: Quote-First-Then-Answer (Lavi et al., 2025)

**Technique:** Decouple quote extraction from reasoning. A lightweight model (LLaMA-3B + LoRA) first extracts relevant verbatim quotes from source documents, then passes *only those curated snippets* to a reasoning model for synthesis.

**Key Results:**
- Over 20-point accuracy gains vs. full-context approaches (RAFT baseline)
- LLaMA-1B: 62.2% accuracy with quotes vs. 24.4% with full context
- Reduces cognitive overhead for downstream reasoning models

**Evidence Strength:** STRONG. Peer-reviewed (SCITEPRESS 2025). Evaluated on HotpotQA with 15,000-sample fine-tuning set. Code released.

**Architecture Insight:** By separating extraction (which passages matter?) from reasoning (what do they mean together?), each model operates within a narrower, more constrained problem space. The quote extraction model does not need to reason; the reasoning model does not need to search.

**Applicability to paper synthesis:** VERY HIGH. This is essentially the architecture needed: extract verbatim quotes per paper first, then pass curated quotes to synthesis agents.

**Source:** [LLMQuoter: Enhancing RAG Capabilities Through Efficient Quote Extraction From Large Contexts](https://arxiv.org/abs/2501.05554) (arXiv 2501.05554, Jan 2025)

---

### 1.3 ReClaim: Ground Every Sentence (Peng et al., 2025)

**Technique:** Interleave reference generation and claim generation at the sentence level. Instead of generating a full response then adding citations post-hoc, the model alternates: select a reference passage, then generate a claim grounded in it.

**Key Results:**
- 90% citation accuracy
- 100% consistency and attribution ratios
- 22% reduction in citation length vs. prior methods

**Evidence Strength:** STRONG. Published at NAACL 2025 Findings. Code released on GitHub.

**Architecture Insight:** The interleaving forces the model to ground *before* claiming, not after. This inverts the typical failure mode where the model generates a claim and then searches for supporting evidence (confirmation bias).

**Applicability to paper synthesis:** HIGH. The interleaved pattern could be adapted for synthesis agents: for each claim you want to make, first identify the supporting passage, then formulate the claim constrained to what the passage actually says.

**Source:** [Ground Every Sentence: Improving Retrieval-Augmented LLMs with Interleaved Reference-Claim Generation](https://aclanthology.org/2025.findings-naacl.55/) (NAACL 2025 Findings)

---

## 2. Claim Decomposition and Verification

### 2.1 FActScore: Atomic Fact Decomposition (Min et al., 2023; widely adopted 2024-2025)

**Technique:** Break generated text into atomic facts — the smallest verifiable units — then verify each independently against a knowledge source.

**Pipeline:** Generate text -> Decompose into atomic facts -> Retrieve evidence per fact -> Verify each fact -> Compute percentage supported

**Key Results:**
- ChatGPT achieved only 58% FActScore for biography generation
- Automated estimation within 2% error of human evaluation
- Spawned an entire family of verification tools (VeriScore, MiniCheck, MedScore, VeriFastScore)

**Evidence Strength:** STRONG. EMNLP 2023. Widely replicated. Became the de facto evaluation paradigm for long-form factuality.

**Limitation:** Sensitive to the decomposition method — different strategies produce different atomic fact sets, influencing reliability. This is the core finding of the "Decomposition Dilemmas" and "Alignment Bottleneck" papers (see 2.4).

**Source:** [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation](https://aclanthology.org/2023.emnlp-main.741/) (EMNLP 2023)

---

### 2.2 Claimify: Structured Claim Extraction (Microsoft Research, 2025)

**Technique:** Three-stage pipeline for extracting verifiable claims from LLM outputs: Selection (identify sentences with verifiable information) -> Disambiguation (resolve multiple interpretations, extract only when high confidence) -> Decomposition (convert to precise, context-independent claims).

**Key Results:**
- 99% entailment rate (claims are faithful to source text)
- 87.6% coverage of verifiable content
- 96.7% precision
- First system to handle ambiguous interpretations explicitly

**Evidence Strength:** STRONG. Microsoft Research. Evaluated on BingCheck dataset covering broad topics and complex LLM outputs. The disambiguation step is novel and directly relevant to synthesis where ambiguity is common.

**Applicability to paper synthesis:** HIGH. The disambiguation step is critical — academic papers often contain hedged or conditional claims. Extracting claims only when interpretation confidence is high prevents the most dangerous synthesis errors.

**Source:** [Claimify: Extracting High-Quality Claims from Language Model Outputs](https://www.microsoft.com/en-us/research/blog/claimify-extracting-high-quality-claims-from-language-model-outputs/) (Microsoft Research, 2025); [Paper](https://www.microsoft.com/en-us/research/publication/towards-effective-extraction-and-evaluation-of-factual-claims/)

---

### 2.3 VeriScore: Factuality of Verifiable Claims (2024)

**Technique:** Unlike FActScore which assumes all claims are verifiable, VeriScore distinguishes verifiable from unverifiable claims, then verifies only the former using Google Search + GPT-4.

**Key Results:**
- VeriFastScore (2025 follow-up): unifies decomposition and verification into a single model pass, achieving 30x speedup (< 5 seconds vs. 2 minutes)
- Online RL with VeriScore rewards: +23.1 points factuality precision, +23% more factual statements

**Evidence Strength:** MODERATE-STRONG. Peer-reviewed. The verifiable/unverifiable distinction is important for academic synthesis where many claims are interpretive, not factual.

**Source:** [VeriScore: Evaluating the Factuality of Verifiable Claims in Long-Form Text Generation](https://arxiv.org/abs/2406.19276) (2024)

---

### 2.4 The Decomposition Dilemma (Hu et al., NAACL 2025; Chen et al., 2026)

**Critical Finding:** Claim decomposition does NOT always improve verification. Two complementary papers establish this:

**Decomposition Dilemmas (Hu et al., NAACL 2025):**
- Decomposition helps with complex inputs
- BUT: increasing sub-claims initially improves performance, then the *noise from decomposition itself* offsets gains, leading to performance degradation
- Trade-off between accuracy gains and decomposition-introduced noise

**The Alignment Bottleneck (Chen et al., 2026):**
- Decomposition improves verification ONLY when evidence is granular and strictly aligned to sub-claims
- Standard setups using repeated claim-level evidence (SRE) fail and often degrade performance
- Error propagation: intermediate step errors compound through the pipeline
- Introduced a new dataset with temporally bounded evidence and human-annotated sub-claim evidence spans

**Evidence Strength:** STRONG. Both peer-reviewed (NAACL 2025, arXiv 2026 with datasets). This is essential knowledge for pipeline design.

**Implication for paper synthesis:** Decompose claims, but ALIGN evidence at the sub-claim level. Do not pass the full paper context to verify each sub-claim — pass only the specific passage that supports that specific sub-claim. Without this alignment, decomposition makes things worse, not better.

**Sources:**
- [Decomposition Dilemmas: Does Claim Decomposition Boost or Burden Fact-Checking Performance?](https://arxiv.org/abs/2411.02400) (NAACL 2025)
- [The Alignment Bottleneck in Decomposition-Based Claim Verification](https://arxiv.org/abs/2602.10380) (2026)

---

## 3. Automated Verification Infrastructure

### 3.1 MiniCheck: GPT-4-Level Verification at 400x Lower Cost (Tang et al., EMNLP 2024)

**Technique:** Fine-tune a small model (Flan-T5-Large, 770M parameters) on synthetic factual error data generated by GPT-4, then use it as a cheap, fast fact-checker for grounding verification.

**Key Results:**
- MiniCheck-FT5 (770M) reaches GPT-4 accuracy for grounding checks
- 400x lower cost than GPT-4
- Outperforms all comparable-size systems
- Evaluated on LLM-AggreFact unified benchmark

**Evidence Strength:** STRONG. EMNLP 2024. Open-source models on HuggingFace. Practical for integration into pipelines.

**Applicability to paper synthesis:** HIGH. Use as a cheap verification layer: after synthesis, run MiniCheck on each claim + its supporting passage to flag unsupported claims before human review.

**Source:** [MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents](https://arxiv.org/abs/2404.10774) (EMNLP 2024)

---

### 3.2 Provenance: Lightweight NLI-Based Fact-Checker (Sankararaman et al., EMNLP 2024)

**Technique:** Use compact, open-source NLI models (~300M parameters) to compute a factuality score given a context and putative output. No LLM required for verification.

**Key Properties:**
- Low latency, low cost
- No LLM fine-tuning needed
- Traces hallucinations back to specific context chunks
- High ROC-AUC across diverse datasets

**Evidence Strength:** STRONG. EMNLP 2024 Industry Track.

**Applicability to paper synthesis:** HIGH. Complementary to MiniCheck. Can trace which specific paper chunk a hallucination relates to, enabling targeted correction.

**Source:** [Provenance: A Light-weight Fact-checker for Retrieval Augmented LLM Generation Output](https://aclanthology.org/2024.emnlp-industry.97/) (EMNLP 2024)

---

### 3.3 AGREE: Self-Grounding via Fine-Tuning (Google, NAACL 2024)

**Technique:** Fine-tune LLMs to self-ground their claims and provide accurate citations during generation (not post-hoc). Combines learning-based adaptation with test-time adaptation where the model iteratively seeks additional information based on its own citations.

**Key Results:**
- 30%+ relative improvement in grounding quality vs. prompting-based approaches
- Superior to both prompting and post-hoc citation approaches

**Evidence Strength:** STRONG. NAACL 2024. Google Research. Evaluated across 5 datasets and 2 LLMs.

**Limitation:** Requires fine-tuning, which may not be practical for all deployment scenarios.

**Source:** [Effective Large Language Model Adaptation for Improved Grounding and Citation Generation](https://aclanthology.org/2024.naacl-long.346/) (NAACL 2024)

---

### 3.4 OpenFactCheck: Unified Evaluation Framework (Wang et al., EMNLP 2024)

**Technique:** Three-module framework: Response Evaluator (customize fact-checking systems), LLM Evaluator (assess overall LLM factuality), Fact Checker Evaluator (evaluate fact-checking systems themselves).

**Key Property:** Meta-evaluation — not just checking facts, but evaluating whether your fact-checking pipeline itself is reliable. Dataset: FactQA with 6,480 examples across 7 corpora.

**Evidence Strength:** STRONG. EMNLP 2024 Demo. Open-source Python library + web service.

**Source:** [OpenFactCheck: A Unified Framework for Factuality Evaluation of LLMs](https://aclanthology.org/2024.emnlp-demo.23/) (EMNLP 2024)

---

### 3.5 FACTS Grounding Benchmark (Google DeepMind, 2024-2025)

**Technique:** Benchmark for evaluating LLM ability to generate factually accurate responses grounded in provided documents. 1,719 examples across finance, technology, retail, medicine, law.

**Key Results:**
- Best models achieve ~69% FACTS Score (Gemini 3 Pro)
- Expanded to FACTS Benchmark Suite with parametric and search-augmented evaluation

**Evidence Strength:** STRONG. Google DeepMind. Public leaderboard on Kaggle. Provides ground truth for evaluating grounding quality.

**Source:** [FACTS Grounding: A New Benchmark for Evaluating the Factuality of Large Language Models](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/) (DeepMind, Dec 2024); [Paper](https://arxiv.org/abs/2501.03200)

---

## 4. Metacognitive Scaffolds

### 4.1 Chain-of-Verification (CoVe) (Dhuliawala et al., ACL 2024 Findings)

**Technique:** Four-step self-verification:
1. Draft initial response
2. Plan verification questions to fact-check the draft
3. Answer verification questions *independently* (not biased by the draft)
4. Generate final verified response incorporating corrections

**Key Property:** Step 3 is the critical innovation — answering verification questions independently prevents confirmation bias from the initial draft.

**Key Results:**
- Decreases hallucinations across list-based questions (Wikidata), closed-book MultiSpanQA, and long-form generation
- Outperforms zero-shot, few-shot, and chain-of-thought baselines

**Evidence Strength:** STRONG. ACL 2024 Findings. Meta AI research team. The independent verification step has strong theoretical grounding in debiasing.

**Limitation:** Verification efficacy bounded by verifier capacity. LLM-based verifiers may propagate failures without external knowledge.

**Applicability to paper synthesis:** HIGH. After generating a synthesis claim, plan verification questions ("Does Paper X actually report effect size Y?"), answer them by re-reading the paper independently, then revise.

**Source:** [Chain-of-Verification Reduces Hallucination in Large Language Models](https://aclanthology.org/2024.findings-acl.212/) (ACL 2024 Findings)

---

### 4.2 CRITIC: Tool-Interactive Self-Correction (Gou et al., ICLR 2024)

**Technique:** Generate initial output -> Interact with external tools (search engines, code interpreters, etc.) to verify -> Generate critique -> Correct -> Iterate until stopping condition.

**Key Property:** Self-correction succeeds because verification uses *external tools*, not just internal reasoning. This directly addresses the finding that LLMs cannot reliably self-correct without external feedback.

**Key Results:**
- Consistent performance enhancement across free-form QA, mathematical synthesis, and toxicity reduction
- Practical: requires only text-to-text tool APIs and few-shot demonstrations

**Evidence Strength:** STRONG. ICLR 2024.

**Applicability to paper synthesis:** HIGH. The "tool" is the source paper itself. After generating a synthesis claim, the agent queries the paper (via retrieval) to verify the claim, generates a critique, and corrects. The paper text serves as the external ground truth.

**Source:** [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://arxiv.org/abs/2305.11738) (ICLR 2024)

---

### 4.3 Metacognitive Prompting (MP) (Wang & Zhao, NAACL 2024)

**Technique:** Five-stage prompting that emulates human metacognition:
1. Understand the input text
2. Make a preliminary judgment
3. Critically evaluate the preliminary analysis
4. Reach a final decision with reasoning explanation
5. Evaluate confidence level in the entire process

**Key Results:**
- Outperforms other prompting baselines across majority of tasks
- Forces explicit confidence estimation, which calibrates output reliability

**Evidence Strength:** STRONG. NAACL 2024.

**Applicability to paper synthesis:** MODERATE. Useful as a prompting scaffold for synthesis agents, especially the critical evaluation step (3) and confidence estimation (5). However, the self-correction limitations apply: without external evidence, the critical evaluation may not catch factual errors.

**Source:** [Metacognitive Prompting Improves Understanding in Large Language Models](https://aclanthology.org/2024.naacl-long.106/) (NAACL 2024)

---

### 4.4 The Self-Correction Boundary (Kamoi et al., TACL 2024; Huang et al., ICLR 2024)

**Critical Finding:** LLMs CANNOT reliably self-correct without external feedback.

**What the evidence establishes:**
- No prior work demonstrates successful intrinsic self-correction (i.e., using only the LLM's own prompted feedback) for general tasks
- Performance sometimes *degrades* after self-correction attempts
- The bottleneck is feedback generation, not correction capability
- Self-correction works ONLY with: reliable external feedback, tasks exceptionally suited to self-correction, or large-scale fine-tuning

**Evidence Strength:** VERY STRONG. TACL 2024 survey + ICLR 2024/2025. Replicated finding across multiple research groups.

**Implication for paper synthesis:** ALL metacognitive scaffolds must include external verification. Asking the model "are you sure?" is not verification. Asking the model to re-read the source passage and check its claim against verbatim text IS verification (because the source text is external ground truth).

**Sources:**
- [When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/) (TACL 2024)
- [Large Language Models Cannot Self-Correct Reasoning Yet](https://openreview.net/forum?id=IkmD3fKBPQ) (ICLR 2024)

---

## 5. Multi-Paper Synthesis Integrity

### 5.1 Citation Hallucination Rates (Empirical Baseline)

**What we know about the problem:**

| Finding | Source |
|---------|--------|
| All models hallucinate citations at 14-95% rates across 40 domains | GhostCite (2026) |
| 100+ hallucinated citations in 53 NeurIPS 2025 papers | SPY Lab/arXiv analysis |
| 50 ICLR submissions with hallucinated citations | BetaKit investigation |
| Fabrications are "chimeric" — blending elements of real papers | GhostCite (2026) |
| DOI presence: 71% natural sciences, 38% humanities | ALCE evaluation |
| GPT-4 hallucination rate for systematic reviews: 28.6% | JMIR 2024 |
| Bard hallucination rate for systematic reviews: 91.4% | JMIR 2024 |

**Implication:** Default LLM behavior is fundamentally unreliable for academic citation. Every architectural decision must assume the model WILL hallucinate connections, effect sizes, and attributions unless constrained by design.

**Sources:**
- [GhostCite: A Large-Scale Analysis of Citation Validity in the Age of Large Language Models](https://arxiv.org/abs/2602.06718) (2026)
- [Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic Reviews](https://www.jmir.org/2024/1/e53164) (JMIR 2024)
- [Trends in LLM-Generated Citations on arXiv](https://spylab.ai/blog/hallucinations/) (SPY Lab)

---

### 5.2 The ALCE Attribution Benchmark (Gao et al., EMNLP 2023; extended 2024-2025)

**Technique:** Automatic evaluation of LLM generations with citations across three dimensions: fluency, correctness, and citation quality (recall + precision via NLI verification).

**Key Results:**
- Citation recall accuracy: 66.1%
- Effective at detecting irrelevant citations
- Limited by NLI model inability to detect "partial support"

**Implication for multi-paper synthesis:** Partial support is the most dangerous failure mode in synthesis — a claim that is *mostly* supported by a paper but with a critical detail wrong (e.g., wrong effect size, wrong direction, wrong population). ALCE's limitation here mirrors the real-world difficulty.

**Source:** [Enabling Large Language Models to Generate Text with Citations](https://arxiv.org/abs/2305.14627) (EMNLP 2023)

---

### 5.3 Knowledge Graph Integration (ACL 2025 SRW)

**Technique:** Integrate knowledge graphs into LLM inference to constrain the relational structure of claims. Instead of allowing the model to freely associate findings across papers, structured knowledge representations enforce valid connections.

**Evidence Strength:** MODERATE. Systematic literature review (ACL 2025 Student Research Workshop). The approach is promising but implementation maturity varies.

**Source:** [Mitigating Hallucination by Integrating Knowledge Graphs into LLM Inference](https://aclanthology.org/2025.acl-srw.53/) (ACL 2025)

---

## 6. Integrated Pipeline Design: Synthesis of Findings

Based on the evidence above, the highest-fidelity pipeline for LLM-assisted multi-paper academic synthesis would combine:

### Stage 1: Quote Extraction (per paper)
- **Architecture:** LLMQuoter pattern — lightweight model extracts verbatim quotes
- **Storage:** Deterministic Quoting pattern — quotes stored in a database with passage IDs
- **Output:** A structured set of `{paper_id, passage_id, verbatim_quote, page_ref}` tuples

### Stage 2: Claim Decomposition (per paper)
- **Architecture:** Claimify's three-stage pipeline (Selection -> Disambiguation -> Decomposition)
- **Critical constraint:** From Alignment Bottleneck paper — each sub-claim MUST be aligned to its specific supporting passage, not the whole paper
- **Output:** `{claim, supporting_passage_id, confidence, is_hedged}`

### Stage 3: Cross-Paper Synthesis
- **Architecture:** ReClaim's interleaved reference-claim generation — for each synthesis claim, first identify the supporting quotes from Stage 1, then formulate the claim
- **Verification:** CoVe pattern — after drafting synthesis, generate verification questions, answer them independently by re-reading source passages, revise
- **Constraint:** Never generate a cross-paper connection without verbatim quotes from BOTH papers supporting the connection

### Stage 4: Automated Verification Layer
- **First pass:** MiniCheck (770M, GPT-4-level accuracy, 400x cheaper) — verify each claim against its supporting passage
- **Second pass:** Provenance NLI checker — trace any flagged claims back to specific source chunks
- **Human review:** Focus human attention on claims MiniCheck flags as unsupported, hedged claims from Stage 2, and all cross-paper connections

### Stage 5: Metacognitive Scaffolding (throughout)
- **CoVe** at every synthesis step (not just final output)
- **CRITIC** pattern: source papers as the "external tool" for verification
- **NEVER rely on intrinsic self-correction** — the model asking itself "am I sure?" is not verification
- **Confidence calibration:** Metacognitive Prompting's five-stage process, especially the explicit confidence estimation

### Key Design Principles (evidence-backed)

1. **Decouple extraction from reasoning** (LLMQuoter). The model that identifies relevant passages should not be the model that synthesizes them.
2. **Ground before claiming** (ReClaim). Invert the default: identify evidence first, then formulate claims constrained to what the evidence says.
3. **Align evidence at sub-claim granularity** (Alignment Bottleneck). Do not verify a sub-claim against the full paper — verify against the specific passage.
4. **External verification is non-negotiable** (Self-Correction Survey). Every verification step must involve comparing against source text, not asking the model if it's correct.
5. **Disambiguation before decomposition** (Claimify). Academic papers contain hedged, conditional, and ambiguous claims. Extract only when interpretation confidence is high.
6. **Decomposition has diminishing returns** (Decomposition Dilemmas). More sub-claims is not always better — the noise from over-decomposition eventually degrades verification.

---

## Evidence Strength Key

| Rating | Meaning |
|--------|---------|
| VERY STRONG | Multiple peer-reviewed replications, consistent findings |
| STRONG | Peer-reviewed at top venue, evaluated on standard benchmarks |
| MODERATE | Peer-reviewed but limited evaluation, or preprint with strong methodology |
| WEAK | Practitioner report or opinion without controlled evaluation |
| SPECULATIVE | Theoretical argument without empirical support |

---

## Full Source List

### Peer-Reviewed (Top Venues)

1. Dhuliawala, S., et al. (2024). "Chain-of-Verification Reduces Hallucination in Large Language Models." *ACL 2024 Findings.* [Paper](https://aclanthology.org/2024.findings-acl.212/)
2. Gou, Z., et al. (2024). "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing." *ICLR 2024.* [Paper](https://arxiv.org/abs/2305.11738)
3. Wang, Y. & Zhao, J. (2024). "Metacognitive Prompting Improves Understanding in Large Language Models." *NAACL 2024.* [Paper](https://aclanthology.org/2024.naacl-long.106/)
4. Kamoi, R., et al. (2024). "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs." *TACL 2024.* [Paper](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/)
5. Huang, J., et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet." *ICLR 2024.* [Paper](https://openreview.net/forum?id=IkmD3fKBPQ)
6. Min, S., et al. (2023). "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation." *EMNLP 2023.* [Paper](https://aclanthology.org/2023.emnlp-main.741/)
7. Tang, L., et al. (2024). "MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents." *EMNLP 2024.* [Paper](https://arxiv.org/abs/2404.10774)
8. Sankararaman, H., et al. (2024). "Provenance: A Light-weight Fact-checker for Retrieval Augmented LLM Generation Output." *EMNLP 2024 Industry.* [Paper](https://aclanthology.org/2024.emnlp-industry.97/)
9. Gao, T., et al. (2023). "Enabling Large Language Models to Generate Text with Citations." *EMNLP 2023.* [Paper](https://arxiv.org/abs/2305.14627)
10. Jiang, X., et al. (2024). "Effective Large Language Model Adaptation for Improved Grounding and Citation Generation (AGREE)." *NAACL 2024.* [Paper](https://aclanthology.org/2024.naacl-long.346/)
11. Hu, Q., et al. (2025). "Decomposition Dilemmas: Does Claim Decomposition Boost or Burden Fact-Checking Performance?" *NAACL 2025.* [Paper](https://arxiv.org/abs/2411.02400)
12. Peng, D., et al. (2025). "Ground Every Sentence: Improving Retrieval-Augmented LLMs with Interleaved Reference-Claim Generation." *NAACL 2025 Findings.* [Paper](https://aclanthology.org/2025.findings-naacl.55/)
13. Wang, Y., et al. (2024). "OpenFactCheck: A Unified Framework for Factuality Evaluation of LLMs." *EMNLP 2024 Demo.* [Paper](https://aclanthology.org/2024.emnlp-demo.23/)
14. Google DeepMind. (2024). "FACTS Grounding Leaderboard." [Paper](https://arxiv.org/abs/2501.03200)

### Preprints and Technical Reports

15. Microsoft Research. (2025). "Claimify: Extracting High-Quality Claims from Language Model Outputs." [Blog](https://www.microsoft.com/en-us/research/blog/claimify-extracting-high-quality-claims-from-language-model-outputs/)
16. Lavi, E., et al. (2025). "LLMQuoter: Enhancing RAG Capabilities Through Efficient Quote Extraction From Large Contexts." *arXiv 2501.05554.* [Paper](https://arxiv.org/abs/2501.05554)
17. Chen, Z., et al. (2026). "The Alignment Bottleneck in Decomposition-Based Claim Verification." *arXiv 2602.10380.* [Paper](https://arxiv.org/abs/2602.10380)
18. Song, Y., et al. (2024). "VeriScore: Evaluating the Factuality of Verifiable Claims in Long-Form Text Generation." *arXiv 2406.19276.* [Paper](https://arxiv.org/abs/2406.19276)

### Empirical Studies on Failure Modes

19. GhostCite. (2026). "A Large-Scale Analysis of Citation Validity in the Age of Large Language Models." *arXiv 2602.06718.* [Paper](https://arxiv.org/abs/2602.06718)
20. Alkaissi, H. & McFarlane, S. (2024). "Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic Reviews." *JMIR 2024.* [Paper](https://www.jmir.org/2024/1/e53164)
21. SPY Lab. (2025). "Trends in LLM-Generated Citations on arXiv." [Blog](https://spylab.ai/blog/hallucinations/)

### Practitioner Reports

22. Yeung, M. (2024). "Deterministic Quoting: Making LLMs Safer for Healthcare." [Blog](https://mattyyeung.github.io/deterministic-quoting)
