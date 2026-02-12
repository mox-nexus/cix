# Skill Formation Evidence

Research synthesis on how AI assistance affects learning, mastery development, and skill atrophy.

---

## Sources

- [Shen & Tamkin (2026). How AI Impacts Skill Formation. Anthropic.](https://arxiv.org/pdf/2601.20245)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2422633122)
- [Budzyń et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)
- [Zhou et al. (2025). Creative Scar. Technology in Society.](https://www.sciencedirect.com/science/article/abs/pii/S0160791X25002775)
- [Pallant et al. (2025). Mastery Orientation. ACU Research Bank.](https://doi.org/10.3316/informit.106046894747026)
- [Freise et al. (2025). Job Crafting with AI. HICSS.](https://hdl.handle.net/10125/107542)

---

## Six Interaction Patterns

### Shen & Tamkin (Anthropic, 2026) <span class="ev ev-moderate" title="RCT, n=52, single library, 70-minute session">◐</span>

**Design:** Randomized controlled trial. 52 software engineers learning a new Python library (Trio async). AI group had Claude access. Control group had documentation only.

**Key finding:** Six distinct interaction patterns emerged from identical AI access, producing mastery scores from 24% to 86%.

| Pattern | Mastery | Behavior |
|---------|---------|----------|
| Generation-Then-Comprehension | 86% | AI generated code → human asked follow-up questions |
| Hybrid Code-Explanation | 68% | Requested explanations alongside code |
| Conceptual Inquiry | 65% | Conceptual questions only, wrote code themselves |
| AI Delegation | 39% | Paste and move on |
| Progressive Reliance | 35% | Started manual, ended delegating |
| Iterative Debugging | 24% | AI fixes errors repeatedly |

**The error mechanism:** Control group encountered median 3 errors during the learning task. AI users who delegated encountered 1 error. The errors — especially Trio-specific TypeError and RuntimeWarning — forced understanding of how the library actually worked. AI users who delegated never hit those errors. They finished faster and learned nothing.

**Participant self-awareness:** AI users recognized the gap:
- "I feel like I got lazy"
- "There are still a lot of gaps in my understanding"
- "I wish I'd taken the time to understand the explanations more"

**Speed vs learning tradeoff:** Fastest completion (AI Delegation, 19.5 min) produced worst learning (39%). Best learning (Generation-Then-Comprehension, 24 min) was only slightly slower while building actual capability.

**Experience-level differences:** Junior developers showed largest productivity gains (27-39%) and largest learning deficits. Seniors showed smaller gains (7-16%) but maintained capability.

**Limitations:** n=52. Single library (Trio async). 70-minute session — no measurement of long-term retention. Needs replication across different domains and timeframes.

---

## Scaffolded vs Direct AI

### Bastani et al. (PNAS, 2025) <span class="ev ev-strong" title="RCT, n=1,000, PNAS peer-reviewed">●</span>

**Design:** Randomized controlled trial with 1,000 students in mathematics education.

**Key finding:** Two versions of ChatGPT, same underlying model, opposite learning outcomes.

| Condition | Learning Outcome |
|-----------|-----------------|
| No AI (control) | Baseline |
| GPT Tutor (hints only) | No harm to learning |
| GPT Base (direct answers) | **17% worse** on unassisted assessment |

**Mechanism:** Direct answers bypass desirable difficulties — the productive struggle that builds understanding. Hints preserve the generative step where learning occurs.

**Implication:** Same technology, different interaction design, opposite trajectories. The variable is whether the tool substitutes for thinking or supports it.

**Limitations:** Mathematics education — transfer to software development is plausible but not directly measured. Single academic domain.

---

## Skill Atrophy Over Time

### Budzyń et al. (Lancet, 2025) <span class="ev ev-moderate" title="Lancet crossover RCT, medical domain">◐</span>

**Design:** Crossover randomized controlled trial. Endoscopists used AI-assisted polyp detection for 3 months, then worked without it.

**Key finding:** Unaided detection rate dropped from 28.4% to 22.4% after AI removal — a **20% decline in 12 weeks**.

**Mechanism:** Procedural skills require practice. AI-assisted work reduces practice of the underlying skill. Remove the AI, and the unpracticed skill has degraded.

**The Savings Effect:** Relearning takes less than 50% of original training time (established cognitive science finding). Skills are dormant, not destroyed.

**Limitations:** Medical domain — transfer to software development involves different skill types (cognitive vs perceptual). No equivalent study exists for developers.

### Longitudinal Evidence

**Medical parallel:** Endoscopists using AI-assisted detection for 12 weeks showed 20% decline in unaided detection when AI was removed. <span class="ev ev-strong" title="Budzyń et al. Lancet 2025, crossover RCT">●</span> Software development involves more abstract reasoning than perceptual skills — whether cognitive skills atrophy faster or slower is unknown. <span class="ev ev-speculative" title="Cross-domain inference">◌</span>

---

## The Creative Scar

### Zhou et al. (Technology in Society, 2025) <span class="ev ev-moderate" title="Longitudinal experiment, n=61, 2-month follow-up">◐</span>

**Design:** 7-day lab experiment with 2-month follow-up. 61 participants, 3,593 ideas generated.

**Key finding:** Creativity drops remarkably when AI is withdrawn, and homogeneity keeps climbing even months later. The "creative scar" persists.

> "Users do not truly acquire the ability to create but easily lose it once generative AI is no longer available."

This is the longitudinal evidence showing capability degradation persisting after AI removal — not just correlation, but measured trajectory over time.

**Limitations:** n=61. Creativity tasks, not software. 2-month follow-up may not capture full recovery timeline.

---

## Mastery vs Performance Orientation

### Pallant et al. (2025) <span class="ev ev-moderate" title="Single study, odds ratio">◐</span>

**Key finding:** The largest effect size in the collaborative AI literature.

| Orientation | Critical Thinking Maintenance |
|------------|------------------------------|
| Mastery (focused on learning) | **OR = 35.7** |
| Performance (focused on output) | Baseline |

Users who framed AI interactions as learning opportunities maintained critical thinking at 35.7x the odds of users who framed interactions as task completion.

This dominates control (β = 0.507) and transparency (β = 0.415) from [collaboration design evidence →](collaboration-design-evidence).

**Limitations:** Single study. Odds ratio from observational data. Needs replication.

---

## Job Crafting Patterns

### Freise et al. (HICSS, 2025) <span class="ev ev-moderate" title="HICSS 2025, qualitative study">◐</span>

Two task allocation patterns produce opposite outcomes:

**Approach Crafting** — Assign AI to mundane work, reserve hard problems for yourself:
- AI handles: Boilerplate, CRUD, formatting, test scaffolding
- Human handles: Architecture, domain models, edge cases, design
- Result: Human practices hard skills more. Skills compound.

**Avoidance Crafting** — Use AI to avoid cognitively demanding tasks:
- AI handles: Complex algorithms, architecture, debugging
- Human handles: Review, simple implementations, routine changes
- Result: Human stops practicing skills that matter most. Capability erodes.

**The differentiator:** Not usage frequency. Not AI capability. What the human reserves for themselves.

**Limitations:** Qualitative study. Observational patterns, not controlled experiment.

---

## Recovery Protocols

Based on the atrophy evidence, three evidence-based recovery approaches:

**Switch-Off Protocol** — Periodic work without AI assistance:

| Frequency | Duration | Purpose |
|-----------|----------|---------|
| Weekly | 2-4 hours | Maintain baseline capability |
| Monthly | Full day | Test independent function |
| Quarterly | Complex task end-to-end | Deep capability assessment |

**Simulator Protocol** — Attempt-first before AI consultation. 15-30 minutes of independent effort preserves problem-solving practice while still leveraging AI. <span class="ev ev-speculative" title="Aviation training analogy + Bastani PNAS findings">◌</span>

**Hybrid Protocol** — Generation-Then-Comprehension as daily practice. AI generates, human comprehends through questioning. Speed preserved, understanding compounds.

---

## Evidence Summary

| Finding | Effect Size | Evidence Level | Source |
|---------|------------|----------------|--------|
| 6 interaction patterns, 24-86% mastery | d = 0.738 skill gap | <span class="ev ev-moderate">◐</span> Moderate | Shen & Tamkin 2026 |
| Direct AI answers harm learning | -17% exam performance | <span class="ev ev-strong">●</span> Strong | Bastani PNAS 2025 |
| Scaffolded AI preserves learning | No significant difference | <span class="ev ev-strong">●</span> Strong | Bastani PNAS 2025 |
| 3-month skill atrophy | -20% detection rate | <span class="ev ev-moderate">◐</span> Moderate | Budzyń, Lancet 2025 |
| Creative scar persists months | Measured decline | <span class="ev ev-moderate">◐</span> Moderate | Zhou 2025 |
| Mastery orientation protective | OR = 35.7 | <span class="ev ev-moderate">◐</span> Moderate | Pallant 2025 |
| Job crafting determines trajectory | Qualitative patterns | <span class="ev ev-moderate">◐</span> Moderate | Freise, HICSS 2025 |
| Long-term developer trajectory | Unknown | <span class="ev ev-speculative">◌</span> Speculative | No direct study |

---

*Full citations in [bibliography](bibliography)*
