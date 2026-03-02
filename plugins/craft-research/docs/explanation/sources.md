# Sources and Bibliography

Research informing the craft-research plugin design.

## Platform Reliability

- Nature Communications (2025). LLM citation accuracy study.
  - 50-90% of LLM responses not fully supported by cited sources.

- Fortune (2025). NeurIPS hallucinated citations incident.
  - 100+ hallucinated citations entered NeurIPS 2025 official record.

- Omniscience Index. Gemini Deep Research reliability benchmark.
  - 66% DOI error rate. Study/year often correct, DOI wrong. 88% overall hallucination on supporting details.

- Deakin University. GPT-4o citation fabrication study.
  - 1 in 5 academic citations fabricated.

## Extraction and Verification Techniques

- Dhuliawala, S., Komeili, M., Xu, J., Radev, D., Lewis, M., Riedel, S., & Shmidhuber, J. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. *Meta Research*. arXiv:2309.11495.
  - Independent verification: +23% F1 improvement. The mechanism is independence — answering verification questions without seeing the original claim prevents anchoring.

- Min, S. et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.
  - Atomic fact decomposition for evaluation. Basis for the Claimify pipeline's decomposition stage.

- Claimify Pipeline. Structured claim extraction.
  - 99% claim entailment through Selection → Disambiguation → Decomposition. Most extraction failures trace to compound, ambiguous claims entering verification.

- Dual-LLM Cross-Critique.
  - Two models extract independently. Concordance check: 0.94 accuracy on agreements. Cross-critique resolves 51% of disagreements. Remaining disagreements are genuine ambiguities for human review.

## Synthesis and Multi-Document Reasoning

- LitLLMs. Plan-Based Synthesis.
  - Structured outline before synthesis reduces hallucination vs direct generation. Gap-aware: marks missing coverage rather than filling with fabrication.

- Synthesis hallucination research (2024).
  - 75% of content in multi-document LLM summaries can be hallucinated. Position bias: LLMs weight information by position in prompt, not by importance.

## Prompting and AI Capabilities

- Yao, S. et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *Princeton/DeepMind*.
  - 74% accuracy vs 49% (CoT) vs 33% (standard prompting).

- Sebastian Raschka (2025). State of LLMs 2025.
  - Platform comparison, capability overview.

- Aakash Gupta. Meta-analysis of 1,500 papers on prompt engineering.
  - Role prompting has "little to no effect on correctness." Over-detailed prompts counterproductive with sophisticated models.

- Lenny's Newsletter (2025). Prompt engineering 2025.
  - o1 performs worse with examples. Advanced models need different prompting strategies.

## Systematic Review Methodology

- PRISMA-trAIce (2025). PMC12694947.
  - 14-item extension to PRISMA 2020 for AI-assisted literature reviews. Distinguishes human vs AI exclusions. Mandates human-AI interaction description. Key finding: "Active participation of the researcher throughout the entire process is still crucial."

## Citation Verification Tools

- Scite.ai. Smart Citations.
  - 1.5B citations classified as supporting, opposing, or mentioning. Semantic classification beyond simple citation counting.

- SemanticCite. arXiv:2511.16198.
  - 4-class verification: Supported, Partial, Unsupported, Uncertain.

- Elicit. Academic paper search.
  - 138M+ papers indexed. Semantic search beyond keyword matching.

- Consensus. Research agreement visualization.
  - Visual summary of research consensus on specific questions.

## Evidence Weighting

- Cochrane Collaboration. Evidence hierarchy.
  - Meta-analysis > RCT > Quasi-experimental > Observational > Case study > Expert opinion. Foundation for the evidence weighting protocol in the synthesizing skill.

## Design Principles (from CIX Thesis)

- Blaurock, M. et al. (2025). Human-AI co-production quality. RCT, n=654.
  - Control (β=0.507) > Transparency (β=0.415). Engagement features non-significant (b=0.090, ns). The research plugin itself is designed around these levers: user controls scope, pipeline is transparent, no engagement features.

- Bastani, H. et al. (2025). Generative AI without guardrails can harm learning. *PNAS*.
  - GPT Tutor (hints only): no harm. GPT Base (direct answers): -17% learning. The research plugin provides extraction and verification, not answers — the human synthesizes understanding.
