# Cartography Agent Design Patterns

Research synthesis for survey/mapping agents in multi-agent content pipelines.

Date: 2026-02-24

---

## 1. Survey-Then-Verify Patterns

Techniques for structuring an agent that skims broadly, then verifies key extractions before passing the map downstream.

### 1.1 Chain-of-Verification (CoVe) — Factored Execution

**Source**: Dhuliawala et al., "Chain-of-Verification Reduces Hallucination in Large Language Models" (ACL Findings 2024)

**Technique**: Four-step pipeline where the model (1) drafts an initial response, (2) plans verification questions to fact-check the draft, (3) answers those questions *independently* (factored execution — no access to original draft or other verification answers), (4) synthesizes a final verified response.

**Key finding**: Fully factored execution (each verification question answered in isolation) produces the strongest results because it prevents bias propagation between verification steps. Reduces factual hallucinations by 50-70% on QA and long-form generation benchmarks.

**Implementation for cartography**: After the survey pass produces a source inventory with key claims, generate verification questions per claim ("Does source X actually say Y?", "Does this paper's methodology support this scope classification?"). Answer each verification question by re-reading the relevant source passage — critically, without access to the initial survey output. Only claims that survive verification enter the cartography.

**Practical note**: The "factored" part is the critical design choice. If the verifier can see the original extraction, it tends to confirm rather than independently check. Architect the verification as a separate agent call or at minimum a separate context window.

### 1.2 FActScore Decompose-Then-Verify

**Source**: Min et al., "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation" (EMNLP 2023, widely adopted 2024-2025)

**Technique**: Break generated text into atomic facts, then verify each atomic fact independently against a knowledge source. The proportion of supported atomic facts is the score.

**Implementation for cartography**: After producing the source inventory, decompose each "key claims" entry into atomic facts. Verify each atom against the original source. Score the cartography's factual precision before passing it downstream. This catches compound claims where part is accurate and part is hallucinated.

**Practical note**: Atomic decomposition is itself error-prone — Claimify (below) addresses this with a more robust pipeline.

### 1.3 Plan-and-Act: Survey as Planning Phase

**Source**: "Plan-and-Act: Improving Planning of Agents for Long-Horizon Tasks" (arXiv 2025, 2503.09572)

**Technique**: Separate the planning phase (survey, landscape mapping, task decomposition) from the execution phase (deep work). The planning agent produces a structured plan that constrains execution agents. Key insight: the plan is a *contract* — execution agents work within its bounds, not beyond them.

**Implementation for cartography**: Magellan's cartography IS the plan phase. The cartography constrains what feynman reads deeply, what vyasa organizes, what planner schedules. Formalizing this as a contract (typed schema, not prose) prevents downstream agents from inventing sources or claims the cartography didn't surface.

### 1.4 MetaGPT SOP-Based Verification

**Source**: Hong et al., "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework" (ICLR 2024, Oral — top 1.2%)

**Technique**: Encode Standard Operating Procedures (SOPs) as structured prompts. Each agent produces typed, schema-conforming outputs. Downstream agents verify intermediate results against the schema before proceeding. Cascading hallucinations are suppressed by requiring modular, inspectable outputs at each step.

**Key finding**: Structured intermediate outputs significantly increase downstream success rates because they maintain consistency and minimize ambiguity during collaboration.

**Implementation for cartography**: Define map/MOC.md not as free-form prose but as a schema with required fields (source inventory table, cluster definitions, gap types). Downstream agents validate the schema before consuming it. Missing fields or malformed entries get rejected back to magellan rather than silently propagated.

---

## 2. Quote-Anchored Inventories

Methods where each claim in an inventory includes a direct quote from the source as provenance.

### 2.1 ReClaim: Interleaved Reference-Claim Generation

**Source**: "Ground Every Sentence: Improving Retrieval-Augmented LLMs with Interleaved Reference-Claim Generation" (NAACL Findings 2025)

**Technique**: Generate output as an alternating sequence of references and claims: `{r1, c1, r2, c2, ..., rn, cn}` where each reference is a sentence-level citation directly supporting the subsequent claim. Two variants:
- **ReClaim Unified**: Single model generates the full attributed sequence in one pass
- **ReClaim w/IG**: Two specialized models (ReferModel generates the reference, ClaimModel generates the claim using only the reference as context, filtering extraneous information)

**Performance**: 86% citation accuracy (vs 66.2% for ALCE baseline). Citations are ~20% the length of passage-level citations, reducing verification burden. 100% consistency ratio with constrained decoding.

**Implementation for cartography**: For each key claim in the evidence clusters, require the format:

```
QUOTE: "exact text from source" (Source #, page/section)
CLAIM: [what this establishes for the project]
```

The quote anchors the claim to a specific passage. Downstream agents (feynman, planner) can verify by checking the quote against the source — they don't need to re-read the whole paper. The interleaved format makes ungrounded claims structurally visible (a claim without a preceding quote is malformed).

### 2.2 Claimify: Four-Stage Extraction Pipeline

**Source**: Metropolitansky & Larson, "Towards Effective Extraction and Evaluation of Factual Claims" (ACL 2025 Main Conference), Microsoft Research

**Technique**: Four-stage pipeline for extracting verifiable claims:
1. **Sentence Splitting + Context**: Split into sentences, preserve neighboring context
2. **Selection**: Keep only sentences with verifiable propositions. Sentences with no verifiable content are labeled "No verifiable claims"
3. **Disambiguation**: Detect ambiguity, attempt resolution using local context. Unresolvable ambiguity → "Cannot be disambiguated" (excluded rather than guessed)
4. **Decomposition**: Convert each disambiguated sentence into standalone, decontextualized claims

**Performance**: 99% entailment rate (claims are supported by source), 87.6% recall of verifiable content, 96.7% precision.

**Key design choice**: Claimify explicitly handles ambiguity by *excluding* rather than guessing. When a passage could mean two things and context doesn't resolve it, the claim is flagged rather than decomposed. This is the opposite of most extraction systems that force an interpretation.

**Implementation for cartography**: Apply the Claimify pipeline to the "key claims" field in each evidence cluster. Each claim must be:
- **Verifiable**: not opinion or vague assertion
- **Decontextualized**: understandable without reading the surrounding text
- **Disambiguated**: only one interpretation, or flagged as ambiguous

Claims that fail disambiguation get flagged in the cartography as "AMBIGUOUS — requires feynman's deep reading to resolve."

### 2.3 FRONT: Fine-grained Quote Supervision

**Source**: Referenced in "Attribution, Citation, and Quotation: A Survey of Evidence-based Text Generation with Large Language Models" (arXiv, August 2025)

**Technique**: Supervise LLMs with fine-grained supporting quotes to guide and improve citation generation. The model learns to extract and present the specific text passage that supports each claim, not just point to a document.

**The quotation gap**: The survey finds that only 13% of evidence-based text generation papers address quotation (vs 75% citation, 62% attribution). Quotation — embedding verbatim source text — remains significantly under-researched despite being the strongest provenance signal.

**Implementation for cartography**: This validates the quote-anchored approach as a design choice. The cartography should use direct quotes (verbatim source text) rather than citations (document references) or attributions (loose connections). Quotes are verifiable by string matching; citations require re-reading; attributions require judgment.

---

## 3. Confidence Calibration

Techniques for an agent to express meaningful uncertainty about its own extractions.

### 3.1 Structural Confidence over Verbalized Confidence

**Source**: Xiong et al., "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs" (ICLR 2024)

**Key finding**: LLMs are systematically overconfident when verbalizing their confidence, imitating human patterns of expressing certainty. Verbalized confidence ("I am confident that...") is unreliable as a signal. As model capability scales up, calibration improves but remains far from ideal.

**Mitigation strategies**: Chain-of-thought prompting and self-probing reduce overconfidence somewhat, but structural checks outperform verbalized confidence in all tested conditions.

**Implementation for cartography**: Never rely on magellan saying "I'm confident this paper says X." Instead, require structural evidence of confidence:
- Can the claim be grounded in a direct quote? (structural)
- Does the claim survive factored verification? (structural)
- Do multiple sources converge on the same claim? (structural)

### 3.2 Cycles of Thought: Explanation Stability as Confidence Proxy

**Source**: "Cycles of Thought: Measuring LLM Confidence through Stable Explanations" (arXiv 2024, 2406.03441)

**Technique**: Generate N explanations for a claim. Measure how consistently those explanations support the same conclusion. Stable explanations (all converging on same answer) indicate high confidence. Divergent explanations indicate low confidence. Uses entailment probability to filter logically incoherent explanations, preventing the model from trusting plausible-sounding but unsound reasoning.

**Key insight**: Raw explanation likelihood poorly distinguishes correct from incorrect answers — the distributions overlap. Entailment probability creates clear separation by filtering logically incoherent explanations.

**Implementation for cartography**: For critical claims in the cartography (especially gap identifications and cluster assignments), generate 3 alternative framings of the same claim. If all three converge, mark as SOLID. If they diverge, mark as UNCERTAIN. This is computationally expensive — use selectively on high-impact claims, not every inventory entry.

### 3.3 Confidence-Improved Self-Consistency (CISC)

**Source**: "Confidence Improves Self-Consistency in LLMs" (ACL Findings 2025)

**Technique**: Extends self-consistency sampling by adding a self-assessment step: each reasoning path gets a confidence score, then weighted majority vote selects the answer. Outperforms standard self-consistency in both efficiency and accuracy.

**Related**: Reasoning-Aware Self-Consistency (RASC) reduces sample usage by ~70% while maintaining accuracy by assessing reasoning quality alongside answer consistency.

**Implementation for cartography**: When magellan classifies a source's scope or strength, sample 3 classifications with self-assessed confidence scores. If all 3 agree with high confidence, accept. If they disagree, flag for manual review. The weighted vote catches cases where 2/3 paths are confidently wrong and 1/3 is correctly uncertain.

### 3.4 Four-Tier Structural Confidence (from Discovering Skill)

**Source**: Already in the codebase — `plugins/craft-rhetoric/skills/discovering/SKILL.md`

**Technique**: Four categories based on structural signals, not verbalized confidence:

| Category | Meaning | Signal |
|----------|---------|--------|
| **Solid** | Multiple verification paths converge | Proceed |
| **Probable** | Most paths converge, minor uncertainty | Proceed with caveats |
| **Uncertain** | Paths diverge, comprehension gaps | Flag in output |
| **Unknown** | Cannot verify, insufficient material | Flag or ask human |

**Implementation for cartography**: Apply these categories to each entry in the source inventory. A source classified as "Solid" has been verified (quote + factored check). "Probable" has a quote but no independent verification. "Uncertain" has no quote — scope/strength are inferred from title/abstract only. "Unknown" means the source couldn't be read or parsed.

---

## 4. Error Propagation Prevention

How survey/mapping agents prevent their errors from compounding in downstream agents that trust the map.

### 4.1 The 0.95^N Problem (Compound Error Rates)

**Source**: "Towards a Science of Scaling Agent Systems" (Google DeepMind, arXiv late 2025); analyzed in "Why Your Multi-Agent System is Failing: Escaping the 17x Error Trap of the Bag of Agents" (Towards Data Science, Jan 2026)

**Key finding**: If each agent step has 95% accuracy, a 10-step pipeline has 0.95^10 = 60% accuracy. A 20-step pipeline: 36%. Error compounds multiplicatively, not additively. The "coordination tax" shows accuracy gains saturate beyond 4 agents without structured topology.

**Mitigation**: Structured coordination topologies (not "bags of agents"), closed-loop feedback, and verification gates between pipeline stages. The critical architectural choice is whether adding an agent *multiplies* error or *divides* it (verifiers divide, generators multiply).

**Implementation for cartography**: Magellan is step 1 in the pipeline. Every error in the cartography multiplies through feynman, vyasa, orwell, etc. This means:
- The cartography must be the most heavily verified artifact in the pipeline
- Verification gates before downstream consumption are essential
- A wrong source classification or fabricated claim in the cartography creates a 0.95^N cascade
- Socrates (the evaluator gate) should validate the cartography BEFORE planner runs

### 4.2 Typed Schema Contracts Between Agents

**Source**: Multi-agent pipeline architecture patterns (2024-2025); MetaGPT SOPs; agent-driven pipeline DAG patterns

**Technique**: Define explicit input/output contracts between agents using typed schemas. Each agent's output must conform to a schema that the downstream agent validates before consuming. Malformed outputs are rejected, not silently interpreted.

**Key insight from agent-driven pipelines**: "Control passes as structured artifacts or messages between agents, with results verified (often by downstream agents) before further advancing the pipeline, enforcing strong correctness and robustness properties."

**Implementation for cartography**:

```
CartographySchema:
  source_inventory: list[SourceEntry]  # Required
  evidence_clusters: list[Cluster]     # Required
  connection_map: ConnectionMap        # Required
  gaps: list[Gap]                      # Required
  landscape_summary: str               # Required

SourceEntry:
  id: int                              # Required
  name: str                            # Required
  type: enum[paper, code, docs, ...]   # Required, validated
  location: str                        # Required, must resolve
  scope: str                           # Required
  strength: enum[primary, secondary, tertiary, anecdotal]  # Required, validated
  confidence: enum[solid, probable, uncertain, unknown]     # Required

Cluster:
  name: str                            # Required
  source_ids: list[int]                # Required, must reference valid source IDs
  coverage: enum[dense, adequate, thin, gap]  # Required
  key_claims: list[AnchoredClaim]      # Required

AnchoredClaim:
  quote: str                           # Required — verbatim from source
  source_id: int                       # Required — which source
  location_in_source: str              # Required — section/page
  claim: str                           # Required — what this establishes
  confidence: enum[solid, probable, uncertain, unknown]
  disambiguation_status: enum[resolved, ambiguous, not_applicable]
```

Downstream agents validate this schema. A claim without a quote is malformed. A source_id that doesn't exist in the inventory is malformed. An enum value outside the allowed set is malformed. Malformed entries don't silently pass — they error.

### 4.3 ChatDev's Failure Mode: Mutual Validation Loops

**Source**: Referenced in "The Trust Paradox in LLM-Based Multi-Agent Systems" (arXiv 2024, 2510.18563)

**Anti-pattern**: In ChatDev, an error in a shared planning module propagated downstream because all agents validated each other's outputs without external ground truth. This created a "feedback loop of erroneous confirmations" — each agent confirmed the previous agent's error because it had no independent basis for disagreement.

**Design lesson**: Verification must use an independent signal, not just another agent's agreement. In a multi-agent pipeline, agents that consume the cartography should verify claims against the *source material*, not against the cartography's own internal consistency. Internal consistency is necessary but not sufficient.

**Implementation for cartography**: When socrates gates the cartography, the gate check must include:
1. **Schema validation**: Does the cartography conform to the typed schema? (structural)
2. **Sample verification**: Pick N claims at random, re-read the quoted source passages, check that the quotes are accurate and the claims follow (external ground truth)
3. **Coverage check**: Does the cartography address all ground truth claims from discourse? (completeness against human intent)

Do NOT rely solely on: "Does the cartography seem internally consistent?" That's the ChatDev failure mode.

### 4.4 Confidence-as-Downstream-Instruction

**Source**: Synthesized from confidence calibration research + multi-agent contract patterns

**Technique**: The cartography doesn't just express confidence for its own sake — it instructs downstream agents on how to treat each entry. Confidence categories map to downstream behaviors:

| Cartography confidence | Downstream instruction |
|------------------------|----------------------|
| **Solid** (quote + verified) | Feynman can use directly, no re-verification needed |
| **Probable** (quote, not independently verified) | Feynman should verify quote accuracy during deep read |
| **Uncertain** (no quote, inferred from skim) | Feynman MUST deep-read and may reclassify |
| **Unknown** (couldn't read/access) | Planner must decide: acquire source or work without it |

This prevents the most dangerous error mode: a downstream agent treating an uncertain extraction as established fact. The confidence category is not metadata — it's a behavioral instruction.

### 4.5 Adversarial Redundancy

**Source**: Multi-agent trust/risk patterns; "Enhancing Robustness of LLM-Driven Multi-Agent Systems" (arXiv 2025, 2507.04105)

**Technique**: Incorporate diverse information sources and adversarial checks within agent loops to prevent collusive failures. Don't rely on a single agent's survey — use redundant, independent checks.

**Implementation for cartography**: For the highest-stakes claims (those that will anchor entire articles), have a second independent extraction. Not a second pass by magellan (same agent, same biases) — but feynman's deep read as an independent check that can override the cartography's surface classification. If feynman's deep reading contradicts magellan's survey classification, feynman wins (deeper signal beats broader signal).

---

## 5. Synthesis: Design Recommendations for Magellan

Based on the research above, here are concrete patterns for the cartography agent:

### Output Contract
- Typed schema with required fields (not free-form prose)
- Every key claim must be quote-anchored (verbatim text + source location)
- Confidence is structural (solid/probable/uncertain/unknown), never verbalized
- Confidence maps to downstream behavioral instructions

### Verification Protocol
- After initial survey: generate factored verification questions per claim
- Answer each verification question independently (no access to survey output)
- Apply Claimify's disambiguation rule: exclude rather than guess on ambiguous passages
- Score the cartography's factual precision before release

### Error Prevention
- Socrates gates the cartography before planner consumes it
- Gate check includes sample verification against source material (not just internal consistency)
- Schema validation catches structural errors (missing quotes, invalid references)
- Downstream agents know how to treat each confidence level (behavioral instructions)

### What Not To Do
- Don't rely on verbalized confidence ("I'm confident this paper says X")
- Don't let downstream agents validate the cartography by internal consistency alone (ChatDev anti-pattern)
- Don't treat the cartography as ground truth — it's a map, and maps have errors. The confidence tiers communicate which parts of the map to trust and which to re-survey.

---

## Sources

### Survey-Then-Verify
- [Chain-of-Verification Reduces Hallucination in LLMs](https://aclanthology.org/2024.findings-acl.212/) — Dhuliawala et al., ACL Findings 2024
- [FActScore: Fine-grained Atomic Evaluation](https://arxiv.org/abs/2305.14251) — Min et al., EMNLP 2023
- [MetaGPT: Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) — Hong et al., ICLR 2024
- [Plan-and-Act: Improving Planning of Agents](https://arxiv.org/html/2503.09572v3) — arXiv 2025

### Quote-Anchored Inventories
- [Ground Every Sentence: Interleaved Reference-Claim Generation](https://aclanthology.org/2025.findings-naacl.55/) — NAACL Findings 2025
- [Claimify: Extracting High-Quality Claims from LLM Outputs](https://www.microsoft.com/en-us/research/blog/claimify-extracting-high-quality-claims-from-language-model-outputs/) — Metropolitansky & Larson, ACL 2025
- [Attribution, Citation, and Quotation: A Survey](https://arxiv.org/html/2508.15396) — arXiv August 2025

### Confidence Calibration
- [Can LLMs Express Their Uncertainty?](https://arxiv.org/abs/2306.13063) — Xiong et al., ICLR 2024
- [Cycles of Thought: Measuring LLM Confidence through Stable Explanations](https://arxiv.org/html/2406.03441v1) — arXiv 2024
- [Confidence Improves Self-Consistency in LLMs](https://arxiv.org/pdf/2502.06233) — ACL Findings 2025
- [Uncertainty Quantification and Confidence Calibration in LLMs: A Survey](https://arxiv.org/html/2503.15850) — arXiv 2025

### Error Propagation Prevention
- [Towards a Science of Scaling Agent Systems](https://towardsdatascience.com/why-your-multi-agent-system-is-failing-escaping-the-17x-error-trap-of-the-bag-of-agents/) — Google DeepMind (via TDS analysis), 2025-2026
- [The Trust Paradox in LLM-Based Multi-Agent Systems](https://arxiv.org/html/2510.18563v1) — arXiv 2025
- [MetaGPT SOPs](https://proceedings.iclr.cc/paper_files/paper/2024/file/6507b115562bb0a305f1958ccc87355a-Paper-Conference.pdf) — ICLR 2024
- [Why Multi-Agent LLM Systems Fail](https://arxiv.org/html/2503.13657v1) — arXiv 2025
- [Enhancing Robustness of LLM-Driven Multi-Agent Systems](https://arxiv.org/pdf/2507.04105) — arXiv 2025

### Systematic Review / Literature Mapping
- [AI Tools for Automating Systematic Literature Reviews](https://dl.acm.org/doi/10.1145/3747912.3747962) — ACM 2025
- [Analysis of Article Screening and Data Extraction by AI SLR Platform](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1662202/full) — Frontiers 2025

### Multi-Agent Architecture
- [Google's Multi-Agent Design Patterns](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/) — InfoQ 2026
- [Designing Effective Multi-Agent Architectures](https://www.oreilly.com/radar/designing-effective-multi-agent-architectures/) — O'Reilly 2025
- [ALCE: Enabling LLMs to Generate Text with Citations](https://arxiv.org/abs/2305.14627) — EMNLP 2023
