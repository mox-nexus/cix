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

**Homogenization**
- [Xu et al. (2025). Echoes in AI: LLM Homogenization. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2504966122)
- [Zhang et al. (2025). AI and Survey Homogenization. Sociological Methods & Research.](https://journals.sagepub.com/doi/10.1177/00491241251327130)

---

## Abstract

The evidence clusters into five hypotheses, each supported by multiple independent studies:

| Hypothesis | Key Effect | Sources |
|------------|-----------|---------|
| **Engagement model determines outcome** | 86% vs 24% mastery from same AI | Shen & Tamkin, Bastani |
| **Cognitive degradation is measurable** | β = -0.69 (AI confidence → less thinking) | Lee, Kosmyna, Gerlich, Budzyń |
| **Perception gap hides harm** | 43-point gap (predicted vs actual) | METR, Stack Overflow |
| **Control and transparency work** | β = 0.507 (control), β = 0.415 (transparency) | Blaurock |
| **Homogenization threatens diversity** | 67-75% vs 30-45% content overlap | Xu, Zhang |

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

Xu et al. (PNAS 2025) analyzed LLM story generation. Idiosyncratic plot elements echoed across generations and across different models. 50/100 GPT-4 Kafka continuations had the policeman give directions to take the "second left."

Zhang et al. found AI-assisted survey responses showed 67-75% content overlap versus 30-45% human baseline. The responses were also systematically more positive, masking underlying variation.

When everyone uses the same AI, outputs converge. The diversity that enables collective intelligence — Hong & Page showed diverse groups outperform best-ability groups — disappears.

### The pattern across hypotheses

Each hypothesis has independent support from multiple studies, multiple methods, multiple domains. The convergence isn't coincidental. These aren't separate problems. They're facets of the same dynamic: AI that substitutes for human cognition improves immediate output while degrading the foundation.

The research doesn't say AI is harmful. It says *substitutive* use is harmful. The same tools, used complementarily — with transparency, control, and active engagement — show neutral or positive effects on capability.

Design determines outcome. The question is whether the collaboration is structured for complementarity or substitution.
