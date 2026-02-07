# The Evidence

Research accumulating across disciplines points toward the same pattern: AI improves output while degrading capability.

---

## Sources

**Skill Formation & Learning**
- [Shen & Tamkin (2026). How AI Impacts Skill Formation. Anthropic.](https://arxiv.org/pdf/2601.20245)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2413913122)

**Cognitive Effects**
- [Lee et al. (2025). Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/10.1145/3613904.3641913)
- [Kosmyna et al. (2025). AI-Assisted Writing and Memory. MIT Media Lab.](https://www.media.mit.edu/)
- [Gerlich (2025). AI Tools and Cognitive Offloading. MDPI Societies.](https://www.mdpi.com/2075-4698/15/1/6)
- [Budzyń et al. (2025). AI-Assisted Colonoscopy. Lancet.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)

**Productivity & Perception**
- [METR (2025). AI Impact on Developer Productivity. RCT.](https://arxiv.org/abs/2507.09089)
- [Cui/Demirer et al. (2024). Effects on High Skilled Work. RCTs.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4671691)
- [Stack Overflow Developer Survey (2024-2025).](https://survey.stackoverflow.co/2024/)

**Collaboration Design**
- [Blaurock et al. (2024). AI-Based Service Contingencies. Journal of Service Research.](https://journals.sagepub.com/doi/10.1177/10946705241253322)
- [Bansal et al. (2021). AI Explanations and Trust. CHI.](https://dl.acm.org/doi/10.1145/3411764.3445717)

**Homogenization & Diversity**
- [Jiang et al. (2025). Artificial Hivemind. NeurIPS Best Paper.](https://arxiv.org/abs/2510.22954)
- [Doshi & Hauser (2024). Individual Creativity vs Collective Diversity. Science Advances.](https://www.science.org/doi/10.1126/sciadv.adn5290)
- [Meta-analysis (2025). Generative AI and Creativity. arXiv.](https://arxiv.org/abs/2505.17241)
- [Hintze et al. (2026). Visual Elevator Music. Patterns/Cell.](https://www.cell.com/patterns/fulltext/S2666-3899(25)00299-5)
- [Xu et al. (2025). Echoes in AI: LLM Homogenization. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2504966122)
- [Zhang et al. (2025). AI and Survey Homogenization. Sociological Methods & Research.](https://journals.sagepub.com/doi/10.1177/00491241251327130)

**Disempowerment**
- [Sharma et al. (2026). Who's in Charge? Disempowerment Patterns. Anthropic.](https://arxiv.org/abs/2601.19062)

**Longitudinal**
- [Zhou et al. (2025). Creative Scar. Technology in Society.](https://www.sciencedirect.com/science/article/abs/pii/S0160791X25002775)

---

## Abstract

The evidence clusters into five hypotheses, each supported by multiple independent studies:

| Hypothesis | Key Effect | Sources |
|------------|-----------|---------|
| **Engagement model determines outcome** | 86% vs 24% mastery from same AI | Shen & Tamkin, Bastani |
| **Cognitive degradation is measurable** | β = -0.69 (AI confidence → less thinking) | Lee, Kosmyna, Gerlich, Budzyń |
| **Perception gap hides harm** | 43-point gap (predicted vs actual) | METR, Stack Overflow |
| **Control and transparency work** | β = 0.507 (control), β = 0.415 (transparency) | Blaurock |
| **Homogenization threatens diversity** | g = -0.863 diversity reduction | Meta-analysis, Jiang (NeurIPS Best Paper), Doshi |
| **Users misjudge what helps them** | Harmful interactions rated favorably | Sharma (Anthropic) |

---

## Explanation

### Engagement model determines outcome

Shen & Tamkin (Anthropic, 2026) ran an RCT with 52 engineers learning a new library. Six interaction patterns emerged from identical AI access:

| Pattern | Mastery | Behavior |
|---------|---------|----------|
| Generation-Then-Comprehension | 86% | Generated code, asked follow-up questions |
| Hybrid Code-Explanation | 68% | Requested explanations with code |
| Conceptual Inquiry | 65% | Conceptual questions only, wrote code themselves |
| AI Delegation | 39% | Paste and move on |
| Progressive Reliance | 35% | Started manual, ended delegating |
| Iterative Debugging | 24% | AI fixes errors repeatedly |

Same tool. Mastery ranging from 24% to 86%. The interaction pattern, not the technology, determined learning.

Bastani's PNAS study (n=1,000 students) confirmed this in education. Unrestricted ChatGPT caused 17% worse exam performance. Scaffolded ChatGPT with guardrails showed no significant difference from control. Design shapes outcome.

### Cognitive degradation is measurable

Lee et al. (CHI 2025, n=319 knowledge workers) found confidence in AI negatively correlated with critical thinking enacted (β = -0.69). Workers shift from execution to oversight without maintaining verification rigor.

Kosmyna (MIT Media Lab) measured this neurologically. EEG during AI-assisted writing showed reduced memory encoding. 83% couldn't recall content from their own work — they never learned it.

Budzyń (Lancet, crossover RCT) showed skill atrophy directly. After 3 months with AI-assisted polyp detection, endoscopists' unaided detection rate dropped from 28.4% to 22.4%. A 20% decline in 12 weeks.

Gerlich (n=666) found AI use negatively predicts critical thinking (β = -1.76) with younger users most affected.

### Perception gap hides harm

METR's RCT (16 experienced developers, 246 real tasks) showed a 43-point perception gap: predicted 24% speedup, actual 19% slowdown.

Stack Overflow surveys show the paradox at scale: trust in AI accuracy dropped 10 points (43% → 33%) while adoption rose 8 points (76% → 84%). People use tools they don't trust, perceive benefits they don't get.

The gap prevents correction. You can't fix what you don't notice.

### Control and transparency work

Blaurock's meta-analysis (106 studies, 654 professionals) identified what predicts good outcomes:

| Factor | Effect Size |
|--------|-------------|
| Process control | β = 0.507 |
| Transparency | β = 0.415 |
| Outcome control | Significant positive |
| Engagement features | b = -0.555 (negative) |

Control is the strongest lever. Transparency is second. Engagement features (AI asking questions) actually hurt frequent users.

Bansal (CHI 2021) explained why explanations alone fail: they increased acceptance regardless of correctness. When AI was right, small improvement. When wrong, performance degraded. Explanations build trust without calibrating it.

### Homogenization threatens diversity

**The Artificial Hivemind (NeurIPS 2025 Best Paper):** Jiang et al. tested 70+ LLMs on 26,000 open-ended queries. When 25 different models wrote "a metaphor about time," only 2 dominant clusters emerged. Temperature and ensembling don't help — RLHF over-fits to consensus, penalizing valid but idiosyncratic responses.

**Meta-analysis (28 studies, n=8,214):** Pooled effect size for diversity reduction: **g = -0.863** (CI: -1.328 to -0.398, p&lt;0.001). Large negative effect. Individual creative performance goes up (+0.27), but collective diversity goes down hard.

**Visual convergence:** Hintze et al. (Patterns/Cell, Jan 2026) ran 700 iterative AI image generation loops. ALL converged to just 12 motifs (lighthouses, Gothic cathedrals, rustic buildings...) regardless of starting prompt. "What they generated is bland, pop culture, generic."

Doshi & Hauser (Science Advances) quantified the social dilemma: individual novelty +8.1%, story similarity +10.7%. Individually better off, collectively homogenized.

**Cultural homogenization:** Agarwal et al. (CHI 2025) found AI pushes writing toward Western norms. Cultural classification accuracy dropped from 90.6% to 83.5% with AI assistance.

When everyone uses the same AI, outputs converge. The diversity that enables collective intelligence — Hong & Page showed diverse groups outperform best-ability groups — disappears.

**Mitigation evidence:** Wan & Kalman (2025) showed that using 10 diverse AI "personas" eliminated the homogenization effect. Within-persona similarity: 0.92, across-persona: 0.20. Diversity can be preserved through design.

### Users misjudge what helps them

Sharma et al. (Anthropic, Jan 2026) analyzed ~1.5 million Claude.ai conversations. The finding: **users rate disempowering interactions MORE favorably** in the moment. Interactions that distorted reality, value judgments, or actions felt good.

But when users actually **acted on AI outputs**, satisfaction dropped **below baseline**. Users expressed regret: "I should have listened to my own intuition."

This explains why the perception gap (METR: predicted 24% speedup, actual 19% slowdown) persists. Short-term satisfaction ≠ long-term benefit. Users can't self-correct because the feedback loop is broken — the harm feels helpful.

**Implication:** Design must compensate for miscalibrated user preferences. Transparency and control aren't just nice-to-have — they're necessary because users can't reliably judge what's good for them in the moment.

### The creative scar

Zhou et al. (Technology in Society, 2025) ran a 7-day lab experiment with 2-month follow-up. 61 participants, 3,593 ideas.

Key finding: **creativity drops remarkably when AI is withdrawn, and homogeneity keeps climbing even months later.** The "creative scar" persists.

> "Users do not truly acquire the ability to create but easily lose it once generative AI is no longer available."

This is the longitudinal evidence that was missing. Not just correlation — capability degradation over time, persisting after AI removal.

### The pattern across hypotheses

Each hypothesis has independent support from multiple studies, multiple methods, multiple domains. The convergence isn't coincidental. These aren't separate problems. They're facets of the same dynamic: AI that substitutes for human cognition improves immediate output while degrading the foundation.

The research doesn't say AI is harmful. It says *substitutive* use is harmful. The same tools, used complementarily — with transparency, control, and active engagement — show neutral or positive effects on capability.

Design determines outcome. The question is whether the collaboration is structured for complementarity or substitution.
