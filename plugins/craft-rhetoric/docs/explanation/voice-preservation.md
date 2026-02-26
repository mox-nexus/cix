# Voice Preservation in Multi-Agent Writing Pipelines

Why craft-rhetoric treats the author's voice as a first-class architectural constraint, not a style pass at the end.

## The Problem

When content passes through a pipeline of AI agents — discourse, comprehension, structure, style, evaluation — each agent makes changes that individually seem minor but compound into total voice erasure. We call this **cumulative voice drift**: death by a thousand polishes.

Each agent optimizes for its own objective (clarity, structure, engagement, correctness) without awareness of the cumulative effect. The result: output that is well-crafted but sounds like no one. The author's strategic inefficiencies — deliberate detours, characteristic rhythms, domain-specific phrasing, rough edges that signal thinking happening live — are systematically smoothed away.

This is not a hypothetical risk. The research documents it at multiple levels.

## The Evidence

### RLHF Causes Homogenization

Padmakumar & He (ICLR 2024) ran controlled experiments where users wrote essays with GPT-3 (base) and InstructGPT (RLHF-tuned). Key finding: **InstructGPT co-writing produced statistically significant diversity reduction** (key point diversity: Solo 0.792 → InstructGPT 0.738), while base GPT-3 did not. The human-contributed text remained unaffected — homogenization came entirely from model-contributed portions.

The quality-diversity tradeoff is baked into instruction tuning. The same alignment that makes models helpful makes them converge.

### Individual Quality Up, Collective Diversity Down

Doshi & Hauser (Science Advances, 2024, n=300) found that AI-assisted stories scored **8.1% higher for individual novelty** but were **5% more similar to each other** than human-only stories. The effect is strongest for initially less-creative writers and widens with scale. Enhancing GPT's diversity through parameter or prompt modifications did not close the gap.

Individual benefit and collective loss are not a bug. They are a structural consequence of shared generative sources.

### Cross-Model Convergence

Wenger & Kenett (arXiv 2025) administered standardized creativity tests to humans and a broad set of LLMs. LLM responses are much more similar to other LLM responses than human responses are to each other, even after controlling for response structure. Homogenization is not model-specific — it is cross-model. The problem is architectural.

### The Diagnosable LLM Style

Reinhart et al. (PNAS 2025) used Biber's Multi-Dimensional Analysis on parallel corpora of human- and LLM-written texts. Instruction-tuned LLMs have a distinct style that persists even when prompted for informal register:

- Present participial clauses: **2-5x** the rate of human text
- Nominalizations: **1.5-2x** the rate of human text
- Agentless passive voice: **half** the human rate
- Differences are **larger for instruction-tuned models** than base models

These features are concrete, countable, and correctable — but only if you know to look for them.

### Writer-Edited Beats LLM-Edited

Chakrabarty, Laban & Wu (CHI 2025, Best Paper Honorable Mention) had 18 professional writers edit 1,057 LLM-generated paragraphs, producing 8,035 fine-grained edits. The preference ordering was clear: **writer-edited > LLM-edited > LLM-generated** (statistically significant across all model families tested).

They formalized the LAMP taxonomy — 7 categories of LLM writing idiosyncrasies: Cliche, Unnecessary Exposition, Purple Prose, Awkward Word Choice, Poor Sentence Structure, Lack of Specificity, Tense Inconsistency. These are now detection targets in the voicing skill.

### Metacognitive Monitoring Is Underexplored

Reza et al. (CSCW 2025) systematically reviewed 109 HCI papers on co-writing (2018-2024) and interviewed 15 writers. Their central finding: **monitoring — metacognitive self-regulation during writing — is significantly underexplored** in AI writing tool research. Almost all tools focus on generating or editing text. Almost none help the writer see their own patterns.

They also identified two writer profiles:
- **Content-centric writers**: open to AI in translating/reviewing, want control over planning
- **Form-centric writers**: resist AI at the expression layer — because that's where voice lives

The form-centric insight is crucial. Voice is not a surface property you can apply after the fact. It lives in the expression layer — word choice, rhythm, phrasing. When an agent touches that layer, it touches voice.

### The Ghostwriter Effect

Draxler et al. (TOCHI 2024, n=126) documented the **AI Ghostwriter Effect**: users don't feel ownership of AI-generated text but still publicly declare authorship. Higher user influence on texts increased sense of ownership. Personalization did not eliminate the effect.

Ownership perception is a proxy for voice engagement. When users don't feel ownership, they're not actively curating voice — they're accepting the machine's.

### Pragmatists Maintain Voice

Doshi & Li (NeurIPS 2025 Creative AI Track) analyzed a large-scale corpus spanning pre- and post-LLM eras and found three emergent archetypes: **Adopters** (increased AI-style similarity), **Resistors** (decreased similarity), and **Pragmatists** (stable style while engaging AI themes). Pragmatists use AI as a tool for thematic exploration while maintaining their own stylistic identity.

Not all writers converge. Intentional practitioners maintain voice. The question is what separates Pragmatists from Adopters — and whether that separation can be designed into tools.

## Why This Matters for craft-rhetoric

The craft-rhetoric pipeline has nine agents. Content passes through socrates (discourse) → magellan → feynman → orwell → sagan → orwell → vyasa → tufte/jobs → orwell → ebert. Each step is a transformation. Orwell runs after every prose-transforming step to catch drift before it compounds. Without these architectural constraints, each transformation smooths voice.

The CIX thesis — AI should be complementary, not substitutive — applies directly. If the pipeline replaces the author's voice with a generic "well-written" voice, it has substituted, not complemented. The output may be better by some aggregate quality metric, but it is no longer the author's. The generative spark — the thinking, the rough edges, the characteristic phrasings — has been polished away.

## The Architecture

### Voice Anchor (`voice.md`)

Co-created with the author during discourse. Distinguishes **voice features** (protect) from **voice habits** (correct). Only habits the author explicitly flags are correctable. Everything else is preserved by default.

This matters because what looks like a flaw to an optimizer may be a feature to the author. Short fragmented sentences. Technical metaphors from another domain. Dry humor. Thinking happening live. These are voice. An agent trained on millions of documents will smooth them toward the mean.

### Scoped Agent Mandates

No agent has a "make it better" mandate. Each agent changes only what falls within its defined scope:

- Feynman verifies accuracy — does NOT rephrase
- Sagan weaves Three Doors — does NOT replace word choices
- Vyasa arranges sections — does NOT rewrite sentences
- Orwell evaluates voice — does NOT restructure arguments

The boundaries are explicit because the training signal is implicit. Without explicit scope, every agent will drift toward "improve" — which means "converge toward the training distribution's idea of good writing."

### Minimal Transformation

Every agent makes the minimum change for its function. If a sentence is structurally sound but "could be better," leave it. "Better" pulls toward the mean. Voice lives in the divergence from the mean.

### Ground Truth as Immutable Reference

`ground-truth.md` is never modified by any agent. Every agent can read it — not just for content, but for voice signal. The phrasing, rhythm, and rough edges in the author's discourse output are the canonical voice reference. When in doubt about whether a change erases voice, compare against discourse.

### Diff-Against-Source

Every agent produces a structured diff of what it changed and why, mapped to its mandate. If a change touches voice-flagged phrasing, it requires explicit justification. This creates an audit trail — you can trace exactly where voice was lost and which agent did it.

### Voice Regression Testing

After the full pipeline, the final output is compared against ground-truth.md and voice.md across five dimensions: lexical fingerprint, rhythmic variation, voice features, rough edges, and convergence. This is the last gate before shipping.

## The Connection to the Broader Thesis

Voice preservation is the complementary intelligence principle applied to writing craft. The pipeline should amplify the author's thinking — surface connections they missed, organize for audiences they hadn't considered, catch errors they didn't see — without replacing the thing that makes the writing theirs.

The generative step, in writing as in code, is where the human forms understanding. When an agent smooths away "Wait, why would that be a sensor?" and replaces it with "The sensor classification was incorrect; the component functions as a dataset" — the human's thinking has been erased. The content is the same. The voice is gone. The reader can no longer hear someone working through a problem. They hear a document.

That difference is the whole game.

## Sources

- Padmakumar, V. & He, H. (2024). Does Writing with Language Models Reduce Content Diversity? *ICLR 2024*. https://arxiv.org/abs/2309.05196
- Doshi, A.R. & Hauser, O.P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*, 10(28). https://www.science.org/doi/10.1126/sciadv.adn5290
- Wenger, Y. & Kenett, Y.N. (2025). We're Different, We're the Same: Creative Homogeneity Across LLMs. *arXiv*. https://arxiv.org/abs/2501.19361
- Reinhart, A. et al. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *PNAS*. https://www.pnas.org/doi/10.1073/pnas.2422455122
- Chakrabarty, T., Laban, P. & Wu, C.-S. (2025). Can AI writing be salvaged? Mitigating Idiosyncrasies and Improving Human-AI Alignment in the Writing Process through Edits. *CHI 2025* (Best Paper HM). https://dl.acm.org/doi/10.1145/3706598.3713559
- Reza, M. et al. (2025). Co-Writing with AI, on Human Terms: Aligning Research with User Demands Across the Writing Process. *PACM HCI (CSCW)*. https://dl.acm.org/doi/10.1145/3757566
- Draxler, F. et al. (2024). The AI Ghostwriter Effect. *ACM TOCHI*, 31(2). https://dl.acm.org/doi/10.1145/3637875
- Doshi, V. & Li, M. (2025). Writing in Symbiosis: Mapping Human Creative Agency in the AI Era. *NeurIPS 2025 Creative AI Track*. https://arxiv.org/abs/2512.13697
- Zhu, D. & Cong, L. (2025). Divergent LLM Adoption and Heterogeneous Convergence Paths in Research Writing. *arXiv*. https://arxiv.org/abs/2504.13629
- Liang, W. et al. (2024). Monitoring AI-Modified Content at Scale. *ICML 2024*. https://proceedings.mlr.press/v235/liang24b.html
- Wang, Z. et al. (2025). Catch Me If You Can? LLMs Still Struggle to Imitate Implicit Writing Styles. *EMNLP 2025 Findings*. https://aclanthology.org/2025.findings-emnlp.532.pdf
- O'Sullivan, J. (2025). Stylometric comparisons of human versus AI-generated creative writing. *Nature HSSC*. https://www.nature.com/articles/s41599-025-05986-3
- Kobak, D. & Gonzalez-Marquez, R. (2025). Delving into ChatGPT usage in academic writing. *Science Advances*. (379 excess words from 14M PubMed abstracts)
- Shaib, C. et al. (2025). Measuring AI "Slop" in Text. *arXiv*. https://arxiv.org/abs/2509.19163
