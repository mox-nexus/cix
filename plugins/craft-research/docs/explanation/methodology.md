# Research Methodology: Design Rationale

This document explains WHY the craft-research plugin is designed the way it is — the decomposition into four agents, the provenance chain as the central abstraction, and the specific choices at each pipeline stage.

## The Core Problem: Research Hallucination

AI-assisted research has a provenance problem. The numbers are damning:

- **50-90%** of LLM responses are not fully supported by their cited sources (Nature Communications, 2025)
- **1 in 5** academic citations fabricated by GPT-4o (Deakin University)
- **100+** hallucinated citations entered NeurIPS 2025's official record (Fortune)
- **66%** DOI error rate in Gemini Deep Research outputs (Omniscience Index benchmark)
- **75%** of content in multi-document LLM summaries can be hallucinated (synthesis research, 2024)

No single AI platform is reliable for academic-quality research. The failure mode isn't incompetence — it's structural. LLMs are trained to produce plausible text, not verifiable claims. When asked to synthesize across sources, they fill gaps between what sources actually say with plausible-sounding bridges. The bridges are fabrications.

The solution isn't better models. It's better pipeline design — decomposing research into stages where each stage is independently verifiable.

## Why Four Agents

### The Monolith Problem

The original craft-research had two skills: `deep-research` and `synthesize-papers`. Both were comprehensive prompt templates — rich in methodology, but nothing that *executed* the methodology. A single agent asked to "research X" would extract, verify, and synthesize in one pass, with no checkpoint between stages and no independence between extraction and verification.

This mirrors how humans do sloppy research: read a paper, form an impression, "verify" by re-reading through the lens of the impression you already formed. Confirmation bias is the default mode.

### The Decomposition

The four-agent pipeline addresses this by separating concerns:

| Agent | Concern | Independence |
|-------|---------|-------------|
| **elicit** | What does the source say? | Reads source, no synthesis context |
| **scrutiny** | Did the extractor get it right? | Re-reads source independently |
| **synthesis** | What do verified claims collectively say? | Works only from verified claims |
| **audit** | Is the chain intact end-to-end? | Walks chains, doesn't transform |

The key architectural choice: **scrutiny doesn't see elicit's output before re-reading the source.** This independence is the mechanism behind CoVE's +23% F1 improvement. Without it, verification degrades to confirmation.

### Why Not More Agents?

Each agent adds coordination cost. Four is the minimum for independent extraction, verification, synthesis, and quality gating. Fewer collapses independence (extraction + verification in one agent defeats CoVE). More adds overhead without clear benefit.

The rhetoric plugin has 9 agents because prose transformation has more distinct concerns (comprehension, memory, arrangement, voice, visuals, staging, critique). Research has fewer: you extract, verify, integrate, and audit. The domain determines the decomposition.

## Why Evidentiary Provenance

### The Chain

```
Source text → Source quote → Extracted claim → Verified claim → Finding → Audit trace
```

Every link in this chain is verifiable by a human. That's the design constraint. A reader can:

1. Read a finding
2. See which verified claims support it
3. Check that verification was independent
4. Read the extracted quotes
5. Find those quotes in the original papers

If any link breaks, the finding is ungrounded. The audit agent exists specifically to walk these chains and catch breaks before shipping.

### Why Claim IDs

Claims get persistent IDs at extraction (`[blaurock2025:c1]`) that follow them through the entire pipeline. This seems like overhead, but it solves a critical problem: when a synthesis finding says "evidence shows X," you need to trace *which specific claims* support that finding, not just "Blaurock 2025 found something related."

Without IDs, provenance degrades to bibliography — you know which papers were cited, but not which specific findings were drawn from them, or whether those findings were independently verified.

### Why Confidence Only Decreases

A claim extracted with MEDIUM confidence (single Tier 1 source) cannot be upgraded to HIGH through reasoning alone. "This makes sense" or "this is consistent with theory" are not evidence. Only new verified claims from independent sources can increase confidence.

This is a deliberate constraint against the LLM's natural tendency to generate plausible justifications. Without it, every claim gravitates toward HIGH confidence because the model can always construct a coherent argument for why it should be true.

## Why the Claimify Pipeline

### The Three Stages

**Selection** filters non-factual content before it enters the pipeline. Opinions ("We believe..."), hedges ("might suggest..."), and meta-commentary ("As discussed above...") can't be verified. Including them pollutes the extraction with unverifiable assertions that downstream agents can't distinguish from findings.

**Disambiguation** resolves references to specific entities. "It improved accuracy" is ambiguous — what is "it"? What kind of accuracy? Disambiguation turns this into "The CoVE protocol improved F1 accuracy" — a claim that can be independently verified against the source.

**Decomposition** splits compound claims into atoms. "CoVE improves accuracy and reduces hallucination" hides partial truth — maybe it improves accuracy but the hallucination claim is unsupported. Splitting into two claims lets verification operate on each independently.

The pipeline achieves 99% claim entailment (the extracted claim is entailed by the source text). The key insight from the original Claimify research: most extraction failures happen because compound, ambiguous claims enter verification. Fix the input shape, and downstream accuracy follows.

### Why Not Just "Extract Key Findings"?

Because "key findings" is an instruction to summarize, and summarization is where hallucination happens. The model fills gaps, rounds numbers, and overgeneralizes scope. The Claimify pipeline forces atomic extraction — one verifiable fact per claim, with a verbatim quote — which prevents the model from editorializing.

## Why CoVE for Verification

### The Independence Mechanism

Chain-of-Verification (Dhuliawala et al., 2023) works because of a simple insight: when a model generates a claim and then verifies it in the same context, it anchors to its own output. The model "sees" its original claim and pattern-matches confirmation.

CoVE breaks this by having the verifier answer questions about the source *without seeing the original claim first*. The verifier forms their own understanding, then compares. Disagreements between the extraction and the independent reading surface errors that same-context verification would miss.

### The Four Verdicts

VERIFIED, CORRECTED, REFUTED, INSUFFICIENT — not a binary. The distinction between CORRECTED (finding exists, number wrong) and REFUTED (finding misrepresented) matters for downstream synthesis. A CORRECTED claim can still support a finding; a REFUTED claim cannot.

INSUFFICIENT is the honest verdict when the source is ambiguous or the quote can't be located. The alternative — guessing — is the root cause of most research hallucination. Granting explicit permission to say "I can't verify this" reduces the pressure to fabricate verification.

## Why Four-Layer Gap Analysis

Gaps in research are as important as findings, but models rarely report them voluntarily. The four-layer framework (theoretical, methodological, empirical, practical) forces systematic gap identification:

| Layer | What it catches |
|-------|----------------|
| **Theoretical** | Missing formal models, undefined constructs |
| **Methodological** | Missing study designs (no longitudinal, no RCT) |
| **Empirical** | Missing populations, contexts, datasets |
| **Practical** | Missing implementations, deployments |

Without explicit gap analysis, synthesis presents what was found and silently omits what wasn't. The reader sees a coherent narrative and assumes it's complete. The gaps — which often point to the most important future work — are invisible.

## Why a Workspace

The `.research/` workspace serves the same function as `.rhet/` in craft-rhetoric: it's the shared state that all agents read from and write to, with clear ownership per directory.

```
.research/
├── scope.md              # Human-authored (immutable)
├── extraction/           # elicit writes
├── verification/         # scrutiny writes
├── synthesis/            # synthesis writes
└── audit/                # audit writes
```

The workspace makes the pipeline inspectable. A human can open `verification/blaurock2025.md` and see exactly which claims were verified, corrected, or refuted. They can open `synthesis/control-effects.md` and see which verified claims support each finding. The workspace is the audit trail.

### Why scope.md Is Immutable

`scope.md` is the human's generative step — defining what questions matter and what boundaries apply. No agent modifies it. This is the research equivalent of rhetoric's `ground-truth.md`.

The constraint prevents scope creep, where agents expand the research to answer questions the human didn't ask. A finding that answers an unasked question is noise, not signal. The scope constrains what counts as relevant.

## The Relationship to craft-rhetoric

craft-research and craft-rhetoric share architectural DNA:

| Pattern | craft-rhetoric | craft-research |
|---------|---------------|----------------|
| Hub + spokes | rhetoric + 8 spokes | research + 4 spokes |
| Human input | ground-truth.md | scope.md |
| Workspace | .rhet/ | .research/ |
| Quality gate | ebert (ship/return) | audit (ship/return) |
| Recurring evaluator | orwell (voice after each step) | — (not needed) |
| Central constraint | Voice preservation | Evidentiary provenance |
| Pipeline direction | Understanding → delivery | Evidence → findings |

The key difference: rhetoric needs voice preservation (orwell running after every prose step) because each agent transforms prose. Research doesn't have prose transformation — extraction, verification, and synthesis produce structured output, not narrative. So there's no equivalent to orwell.

## Sources

### Platform Reliability
- Nature Communications (2025). LLM citation accuracy study.
- Fortune. NeurIPS hallucinated citations.
- Omniscience Index. Gemini reliability benchmark.
- Deakin University. GPT-4o citation fabrication study.

### Techniques
- Dhuliawala, S. et al. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. *Meta Research*. arXiv:2309.11495. (+23% F1)
- Min, S. et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.
- Princeton/DeepMind. Tree-of-Thought study. (74% vs 49% CoT vs 33% standard)

### Synthesis
- LitLLMs. Plan-based synthesis reduces hallucination vs direct generation.
- Claimify pipeline. 99% claim entailment through structured decomposition.
- Dual-LLM cross-critique. 0.94 accuracy, 51% discordance resolution.

### Systematic Review
- PRISMA-trAIce (2025). PMC12694947. 14-item extension for AI-assisted literature reviews.

### Meta-Analysis
- Gupta, A. Analysis of 1,500 papers on prompt engineering.
