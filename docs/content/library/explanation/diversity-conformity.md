# Diversity & Conformity

AI increases individual quality while systematically reducing collective diversity — creating intellectual monocultures that threaten systemic resilience.

---

## Sources

**Homogenization Evidence**
- [Jiang et al. (2025). Artificial Hivemind. NeurIPS Best Paper.](https://arxiv.org/abs/2510.22954)
- [Meta-analysis (2025). Generative AI and Creativity. arXiv.](https://arxiv.org/abs/2505.17241)
- [Doshi & Hauser (2024). Individual Creativity vs Collective Diversity. Science Advances.](https://www.science.org/doi/10.1126/sciadv.adn5290)
- [Xu et al. (2025). Echoes in AI: LLM Homogenization. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2504966122)
- [Zhang et al. (2025). AI and Survey Homogenization. Sociological Methods & Research.](https://journals.sagepub.com/doi/10.1177/00491241251327130)
- [Hintze et al. (2026). Visual Elevator Music. Patterns/Cell.](https://www.cell.com/patterns/fulltext/S2666-3899(25)00299-5)
- [Agarwal et al. (2025). Cultural Homogenization in AI-Assisted Writing. CHI.](https://dl.acm.org/doi/10.1145/3613904.3642215)

**Theoretical Foundations**
- [Hong & Page (2004). Groups of Diverse Problem Solvers. PNAS.](https://www.pnas.org/doi/10.1073/pnas.0403723101)
- [Ashby (1956). Law of Requisite Variety. An Introduction to Cybernetics.](https://archive.org/details/introductiontocy0000ashb)

**Analogous Domains**
- [Haldane (2009, 2016). Financial Monoculture. Bank of England.](https://www.bankofengland.co.uk/speech/2009/rethinking-the-financial-network)
- [Taleb (2007). The Black Swan.](https://www.penguinrandomhouse.com/books/176226/the-black-swan-second-edition-by-nassim-nicholas-taleb/)

**Mitigation**
- [Wan & Kalman (2025). Diverse AI Personas Prevent Homogenization.](https://arxiv.org/abs/2505.09222)

---

## Abstract

When 25 different language models write "a metaphor about time," only 2 dominant response clusters emerge. <span class="ev ev-strong" title="NeurIPS Best Paper, 70+ models, 26,000 queries">●</span> This isn't an edge case. It's the central finding of Jiang et al.'s "Artificial Hivemind" — the 2025 NeurIPS Best Paper: large language models trained on the same data converge toward the same outputs, collapsing the solution space despite apparent diversity.

Meta-analysis across 28 studies (n=8,214) quantifies the effect: **g = -0.863 diversity reduction** — the largest negative effect size in the creativity literature. <span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214, p&lt;0.001">●</span> Individual novelty increases (+0.27). Collective diversity collapses (-0.863). Everyone becomes better. Everyone becomes the same.

The consequences are systemic. Hong & Page proved formally that diverse groups outperform best-ability homogeneous groups. <span class="ev ev-strong" title="PNAS, formal mathematical proof + simulation">●</span> Ashby's Law of Requisite Variety states that control systems need at least as much variety as the disturbances they encounter. When outputs converge while problems remain varied, the system loses its ability to cope. Haldane documented this in finance: by 2008, hedge fund strategies showed average correlation of 0.35; when the market turned, they failed together. <span class="ev ev-weak" title="Expert analysis, historical case study">○</span>

AI homogenization creates the same risk at scale — intellectual monoculture where individual capability rises but collective resilience collapses.

---

## Explanation

### The empirical evidence is unambiguous

Jiang et al. tested 70+ language models on 26,000 open-ended queries. <span class="ev ev-strong" title="NeurIPS Best Paper, 70+ models, 26,000 queries">●</span> The finding: **convergence regardless of model architecture or temperature settings.** Models as different as GPT-4, Claude, Llama, and Gemini produce statistically indistinguishable response clusters on creative tasks.

The mechanism is RLHF (Reinforcement Learning from Human Feedback). Training optimizes for consensus — penalizing valid but idiosyncratic responses. Temperature and ensembling don't help. The convergence happens during training, not generation.

Doshi & Hauser (Science Advances) quantified the social dilemma precisely: individual novelty **+8.1%**, story similarity **+10.7%**. <span class="ev ev-strong" title="Science Advances peer-reviewed, controlled experiment">●</span> Each person is better off using AI. Collectively, the diversity that enables innovation disappears.

The meta-analysis (28 studies, n=8,214) confirms this isn't limited to writing. <span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214, p&lt;0.001">●</span> Pooled effect size for diversity reduction: **g = -0.863** (95% CI: -1.328 to -0.398, p&lt;0.001). This is a large negative effect by Cohen's standards. One of the largest observed in the creativity literature.

### Visual convergence: "elevator music" aesthetics

Hintze et al. (Patterns/Cell, January 2026) documented this in image generation. <span class="ev ev-moderate" title="Single study, 700 trials, Patterns/Cell">◐</span> They ran 700 iterative AI generation loops with varied starting prompts. The result: ALL converged to just 12 visual motifs — lighthouses, Gothic cathedrals, rustic buildings with warm lighting.

From their paper: "What they generated is bland, pop culture, generic... visual elevator music."

Initial diversity collapsed into aesthetic homogeneity within 15-20 iterations regardless of starting prompt. The "elevator music" analogy is precise — technically competent, individually pleasant, collectively indistinguishable.

### Cultural erosion

Agarwal et al. (CHI 2025) showed AI pushes writing toward Western cultural norms. <span class="ev ev-strong" title="CHI peer-reviewed, classification study">●</span> They trained classifiers to distinguish cultural origin in writing. Baseline accuracy: 90.6%. With AI assistance: 83.5%. A 7-point drop in cultural distinguishability.

Non-Western writers using AI sound more Western. Not because they intend to — because AI training data over-represents Western perspectives and RLHF reinforces dominant patterns.

This isn't preference. It's erasure. The quiet kind — where everyone becomes individually better at communicating while collectively losing distinct voices.

### Text convergence across contexts

Xu et al. (PNAS 2025) found "echoes" — idiosyncratic plot elements recurring across different LLMs. <span class="ev ev-moderate" title="PNAS peer-reviewed, single study">◐</span> Specific character names, plot devices, and narrative structures appear with implausible frequency. Not plagiarism — convergent outputs from shared training distributions.

Zhang et al. (Sociological Methods & Research 2025) analyzed survey responses with AI assistance. <span class="ev ev-moderate" title="Single study, social science domain">◐</span> Content overlap between different respondents: **67-75%** with AI assistance, compared to baseline. Open-ended responses — supposedly the most personal form of data — became statistically similar.

This has methodological implications. Social science relies on diverse perspectives. If AI assistance homogenizes responses, what are we actually measuring?

### Why diversity matters: the formal proof

Hong & Page (PNAS 2004) proved this mathematically and validated with simulation. <span class="ev ev-strong" title="PNAS, formal mathematical proof + simulation">●</span> The theorem: **randomly selected diverse groups outperform best-ability homogeneous groups** on complex problem-solving tasks.

The mechanism is not about individual skill. It's about coverage of the solution space. Diverse perspectives explore different paths. Homogeneous groups — even if individually superior — search the same regions repeatedly.

From their proof: "Diversity trumps ability." Not always. But in complex domains with large solution spaces — which describes most interesting problems — diverse search beats focused excellence.

This has direct implications for software engineering. If everyone using AI converges toward similar architectural patterns, problem-solving approaches, and code structures, the collective capacity to handle novel challenges degrades even as individual code quality improves.

### Ashby's Law: variety absorbs variety

W. Ross Ashby's Law of Requisite Variety (1956): **only variety can destroy variety.** A control system must possess at least as much internal variety as the disturbances it encounters.

Applied to cognition: if problems are varied but solutions are homogeneous, the system cannot adapt. You need diverse problem-solving capacity to handle diverse problems.

AI homogenization violates this principle. Problems remain varied — new technologies, novel requirements, emergent failures. But if everyone's approach converges, the system loses requisite variety. When a disturbance hits outside the common solution space, everyone fails simultaneously.

### The financial analogy: 2008 as a monoculture collapse

Andy Haldane (Bank of England, 2009) analyzed the 2008 financial crisis through the lens of monoculture. <span class="ev ev-weak" title="Expert analysis, historical case study">○</span> By 2008, hedge fund strategies showed average pairwise correlation of ~0.35. Everyone was optimizing for the same signals — subprime risk was mispriced, leverage was cheap, housing would rise.

When the disturbance came (housing prices fell), strategies that worked independently failed simultaneously. Correlation during crisis approached 1.0. No diversity to absorb the shock.

Haldane: "Finance has a natural tendency toward monoculture. And monoculture, in finance as in agriculture, creates vulnerability to catastrophic risk."

The parallel to AI is not precise — software doesn't crash globally like markets. <span class="ev ev-speculative" title="Analogy from different domain, no direct evidence">◌</span> But the principle holds. If everyone uses the same AI, trains on the same data, converges toward the same patterns, then shared vulnerabilities propagate. A pathogen that exploits common patterns affects everyone simultaneously.

### The biological analogy: monoculture efficiency until the pathogen

Monocultures are efficient. Single-variety farming maximizes short-term yield. But when a pathogen emerges that exploits that variety, the entire crop fails at once. Diversity isn't redundancy — it's antifragility. <span class="ev ev-weak" title="General biological principle, applied by analogy">○</span>

The Irish Potato Famine is the canonical case: Phytophthora infestans encountered a genetically uniform crop. One variety, one vulnerability, one million dead. Not because potatoes were bad. Because uniformity created systemic fragility.

AI homogenization creates similar dynamics in cognition and culture. Not literally famine. But the loss of diverse approaches, diverse aesthetics, diverse ways of thinking about problems. When the disturbance comes — a novel challenge, a paradigm shift, a requirement that doesn't fit the common template — everyone using the same AI lacks the variety to respond.

Nassim Taleb's phrasing: systems are antifragile when they gain from disorder. Diversity enables that. Monoculture prevents it.

### Software engineering implications

Code patterns converge. If everyone uses AI trained on the same repositories, the same architectural patterns propagate. Not because they're optimal for every context — because they're statistically dominant in training data.

Examples of potential convergence:
- **Architecture**: Microservices become default even when monoliths would suffice, because microservices appear more frequently in modern training corpora.
- **Error handling**: Common patterns (try/catch, error propagation) dominate even where domain-specific handling would be better.
- **Security**: Shared defensive patterns create shared attack surfaces. If everyone implements auth the same way, exploits that target that pattern affect everyone.
- **Problem-solving**: Novel solutions become rarer. If AI suggests the statistically common approach, users anchor to it. Over time, idiosyncratic but effective approaches disappear from practice.

This isn't deterministic. <span class="ev ev-speculative" title="Projection from observed trends, not direct measurement">◌</span> It's a plausible trajectory based on observed homogenization in other domains. The mechanism — AI trained on shared data produces convergent outputs — is established. The extrapolation to software practice is reasonable but unproven.

### Why the mechanism is structural

AI doesn't cause homogenization through malice or poor design. It's a natural consequence of how the technology works.

**Training on consensus.** Language models are trained on what people wrote. RLHF optimizes for what human raters prefer. Both sources favor consensus over idiosyncrasy. The model learns "write something typical" not "write something distinctive."

**Anchoring effects.** When AI suggests an answer, users anchor to it (Tversky & Kahneman). Even if the user modifies the output, the starting point shapes the final result. Over millions of interactions, outputs cluster around AI suggestions.

**Iterative reinforcement.** As more AI-generated content enters training data (the "model collapse" problem), future models train on homogenized outputs, further reinforcing convergence. Shumailov et al. (2023) showed iterative training on model outputs leads to "irreversible defects" — diversity collapse that worsens each generation.

This isn't a bug to fix. It's a property of statistical learning from shared distributions.

### The compounding risk

Individual use compounds to collective effect. One person using AI doesn't threaten diversity. A billion people using the same AI, anchoring to the same suggestions, internalizing the same patterns — that changes the distribution of human thought.

The first-order effect is measurable now: g = -0.863 diversity reduction. <span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214">●</span>

The second-order effect is speculative but plausible: <span class="ev ev-speculative" title="Projection, not yet measured">◌</span> as AI-homogenized content becomes training data for future models, the convergence accelerates. Users trained in an AI-saturated environment learn AI patterns as baseline. Defaults shift. What was once idiosyncratic becomes incomprehensible. The center of gravity moves, and diversity relative to that center shrinks.

Analogous to linguistic drift — but faster, because AI accelerates the feedback loop.

### Not inevitable: mitigation exists

Wan & Kalman (2025) showed that using 10 diverse AI "personas" eliminated the homogenization effect. <span class="ev ev-moderate" title="Single study, promising but needs replication">◐</span> They created personas with different training biases, temperature settings, and RLHF targets. Within-persona output similarity: 0.92. Across-persona similarity: 0.20.

Users exposed to multiple personas maintained diversity comparable to no-AI baseline. The mechanism: diverse starting points prevent anchoring to a single mode. Users synthesize across suggestions rather than accepting one.

This demonstrates homogenization is design-dependent, not inherent. The problem is using the same AI the same way at scale. The solution is structural variety — either multiple models or deliberate diversification of outputs.

Jiang et al. proposed "divergent thinking prompts" as another mitigation: explicitly instruct models to produce unusual responses. Early results suggest this helps but doesn't eliminate convergence. <span class="ev ev-weak" title="Proposed intervention, limited validation">○</span> The training distribution still constrains outputs. Prompting can shift the mode but can't create variety that wasn't learned.

### The timeline

Current adoption patterns suggest homogenization is accelerating. GitHub Copilot has 150M+ users (2025). ChatGPT reached 100M monthly active users in two months. These aren't separate tools — they're trained on overlapping data, optimized toward similar targets.

The research showing diversity reduction (g = -0.863) comes from studies conducted in 2023-2024. <span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214">●</span> Adoption has increased since then. The effect is plausibly larger now. We don't have 2026 data yet.

The tipping point isn't clear. At what adoption rate does collective diversity degrade enough to threaten systemic resilience? Unknown. <span class="ev ev-speculative" title="No threshold studies exist">◌</span> Hong & Page's theorem doesn't quantify how much diversity is "enough" — only that more is better for complex problems.

But the trajectory is observable. Individual quality rising. Collective diversity falling. The question is whether interventions can reverse the trend before systemic effects become irreversible.

### What this means for collaborative intelligence

The thesis of collaborative intelligence is that AI should amplify human capability while preserving what makes humans valuable. Diversity is one of those things.

If AI homogenizes outputs, it's not collaborative — it's substitutive. The human contribution becomes "accept or modify AI suggestion" rather than "generate from diverse perspectives."

The research suggests design principles that preserve diversity:

| Principle | Mechanism | Evidence |
|-----------|-----------|----------|
| **Multiple models** | Expose users to diverse starting points | Wan & Kalman (2025) <span class="ev ev-moderate" title="Single study">◐</span> |
| **Attempt-first** | Generate before consulting AI | Prevents anchoring to AI mode |
| **Divergent prompting** | Explicitly request unusual responses | Jiang et al. (2025) <span class="ev ev-weak" title="Proposed, limited validation">○</span> |
| **Source diversity** | Train on underrepresented data | Reduces Western bias (Agarwal) <span class="ev ev-strong" title="CHI peer-reviewed">●</span> |

None of these are expensive. They require intentionality. The question is whether the industry implements them or optimizes for engagement and immediate output quality — which the research shows drives homogenization.

### The ethical dimension

Homogenization isn't just an efficiency problem. It's an equity problem. When AI pushes outputs toward dominant patterns, it erases minority voices. Not through explicit censorship — through statistical convergence toward the majority.

Agarwal et al. showed this empirically: non-Western writers sound more Western with AI assistance. <span class="ev ev-strong" title="CHI peer-reviewed">●</span> Cultural distinguishability dropped 7 percentage points. That's not users choosing to conform. It's AI nudging outputs toward the training distribution center.

At scale, this means:
- **Cultural erosion** — minority languages, perspectives, aesthetics become statistically rarer, harder to preserve
- **Epistemological narrowing** — ways of knowing outside the Western analytical tradition get filtered out
- **Creative stagnation** — novel ideas that don't fit existing patterns are less likely to emerge

This compounds existing inequities. Dominant groups already have more representation in training data. AI reinforces that dominance. The feedback loop is self-reinforcing.

Mitigation requires deliberate counter-pressure: training on underrepresented data, rewarding divergence, designing for pluralism rather than consensus.

### The unanswered questions

The research establishes homogenization is real and large (g = -0.863). <span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214">●</span> It doesn't yet establish:

**Threshold effects.** At what level of homogenization does collective problem-solving degrade? Hong & Page show diversity helps, but don't quantify "how much is enough." <span class="ev ev-speculative" title="Unknown threshold">◌</span>

**Longitudinal persistence.** Does homogenization reverse when AI use stops? Zhou et al. showed creativity deficits persist for months after AI withdrawal. <span class="ev ev-moderate" title="Single study, n=61">◐</span> Does diversity recover or is the effect permanent?

**Domain specificity.** Is the effect uniform across domains? Creativity tasks show g = -0.863. <span class="ev ev-strong" title="Meta-analysis">●</span> Is software engineering equally affected? Plausible but unmeasured. <span class="ev ev-speculative" title="Inference from adjacent domain">◌</span>

**Intervention effectiveness.** Wan & Kalman showed diverse personas help. <span class="ev ev-moderate" title="Single study">◐</span> Does this scale? Do other interventions work? Divergent prompting is theoretically promising but minimally tested. <span class="ev ev-weak" title="Limited validation">○</span>

**Second-order effects.** When homogenized outputs become training data, does convergence accelerate? Model collapse theory says yes. <span class="ev ev-moderate" title="Theoretical prediction with some empirical support">◐</span> Empirical measurement at scale doesn't exist yet.

These are knowable. They require longitudinal studies, domain-specific analysis, and intervention trials. The absence of data isn't evidence of absence. It's a call for research.

### The stakes

Diversity isn't aesthetic preference. It's systemic requirement. Complex systems need variety to handle disturbances (Ashby). <span class="ev ev-strong" title="Formal cybernetic principle">●</span> Collective intelligence requires diverse perspectives (Hong & Page). <span class="ev ev-strong" title="Mathematical proof + simulation">●</span> Monocultures are fragile (biology, finance, demonstrated historically). <span class="ev ev-weak" title="Multiple historical cases, analogy">○</span>

AI homogenization threatens this at scale. Individual quality rising while collective diversity collapses. The effect size (g = -0.863) is among the largest observed in the creativity literature. <span class="ev ev-strong" title="Meta-analysis, 28 studies">●</span> Adoption is accelerating. Mitigation exists but isn't deployed at scale.

The trajectory is measurable. The question is whether design changes in time to preserve what makes collective intelligence work: the variety, the idiosyncrasy, the perspectives that don't fit the statistical mode but turn out to be exactly what's needed when the disturbance comes.

If AI makes everyone better while making everyone the same, we gain individual capability while losing collective resilience. That's not progress. That's trading the foundation for the scaffolding.
