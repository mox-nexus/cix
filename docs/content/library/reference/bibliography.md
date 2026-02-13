# Bibliography

Primary sources organized by topic. Verified 2026-02-11.

**Evidence strength:** <span class="ev ev-strong">●</span> Strong (multiple studies, large n, peer-reviewed) · <span class="ev ev-moderate">◐</span> Moderate (single quality source) · <span class="ev ev-weak">○</span> Weak (expert opinion, preprint) · <span class="ev ev-speculative">◌</span> Speculative (inference)

---

## Skill Formation & Learning

<span class="ev ev-moderate" title="RCT, n=52, arXiv preprint">◐</span> **Shen, J.H. & Tamkin, A. (2026).** [How AI Impacts Skill Formation.](https://arxiv.org/abs/2601.20245) Anthropic. Cohen's d = 0.738 (17pp skill gap). Six interaction patterns: 3 preserve learning, 3 don't. → [skill-formation](../explanation/skill-formation), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

RCT, n=52 (26 control, 26 treatment), junior Python developers learning Trio library. 35-minute coding task + comprehension quiz (~58.5 min total). AI group scored 50% vs control 67% on quiz. Largest gap on debugging questions. High-scoring patterns: Generation-Then-Comprehension (86% mastery), Conceptual Inquiry (second-fastest). Chat-based interface (not agentic tools). Crowdworkers, not workplace context. Four pilot studies required due to non-compliance. Immediate comprehension only — no longitudinal retention data.

</details>

<span class="ev ev-strong" title="RCT, n≈1,000, PNAS peer-reviewed">●</span> **Bastani, H. et al. (2025).** [Generative AI without guardrails can harm learning.](https://www.pnas.org/doi/10.1073/pnas.2422633122) PNAS. -17% exam performance without AI after unrestricted use; hint-only guardrails mitigated harm. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

RCT (field experiment), n≈1,000 Turkish high school math students, three arms. GPT Base (unrestricted ChatGPT-4): +48% grades with AI, **-17% on exams without AI** vs control. GPT Tutor (hint-only, guardrailed): +127% grades with AI, negative effects "largely mitigated." Mechanism: "Without guardrails, students use GPT-4 as a 'crutch' during practice." PNAS peer-reviewed (received Nov 2024, accepted May 2025). Minor correction published Aug 2025 (affiliation typo only).

</details>

<span class="ev ev-moderate" title="Longitudinal, n=61">◐</span> **Zhou, Y. et al. (2025).** [Creative Scar Without Generative AI.](https://www.sciencedirect.com/science/article/abs/pii/S0160791X25002775) Technology in Society. Longitudinal (7-day lab + 2-month follow-up): creativity drops on AI withdrawal, homogeneity persists months later. → [evidence](../explanation/the-evidence)

---

## Cognitive Effects

<span class="ev ev-strong" title="CHI peer-reviewed, n=319, SEM">●</span> **Lee, H.P. et al. (2025).** [The Impact of Generative AI on Critical Thinking.](https://dl.acm.org/doi/full/10.1145/3706598.3713778) CHI 2025. β = -0.69 (AI confidence → less critical thinking); β = +0.35 (self-confidence → more CT). PME friction intervention restores CT. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Structural equation modeling with 319 knowledge workers (CHI peer-reviewed). AI-confidence strongly predicts reduced critical thinking (β = -0.69). Self-confidence predicts maintained CT (β = +0.35). Three-component metacognitive friction (Planning, Monitoring, Evaluation) significantly restored CT suppressed by AI confidence. Single-point friction insufficient — all three needed. Limitation: cross-sectional, not longitudinal. β assumes causality in SEM but data is observational.

</details>

<span class="ev ev-weak" title="arXiv preprint, n=54, published methodological critique">○</span> **Kosmyna, N. et al. (2025).** [Your Brain on ChatGPT.](https://arxiv.org/abs/2506.08872) MIT Media Lab / arXiv preprint. 83% of LLM group unable to quote own essays (Session 1); up to 55% reduced EEG connectivity vs brain-only group. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Between-subjects EEG study, n=54 (18 per group: LLM, Search Engine, Brain-only). **arXiv preprint — not peer-reviewed.** Session 1: 83% (15/18) of LLM group couldn't quote any passage from essays written minutes earlier, vs ~11% in other groups. Brain connectivity "systematically scaled down" with external support level. Session 4 crossover (n=18): 78% of former-LLM users still couldn't quote when writing without AI. **Published critique:** Stankovic et al. (arXiv:2601.00856) identifies concerns with study design, reproducibility, EEG methodology, and reporting inconsistencies. Authors themselves state conclusions should be "treated with caution and as preliminary."

</details>

<span class="ev ev-moderate" title="Survey, n=666, MDPI peer-reviewed">◐</span> **Gerlich, M. (2025).** [AI Tools in Society.](https://www.mdpi.com/2075-4698/15/1/6) MDPI Societies. r = -0.68 (AI use ↔ critical thinking), r = -0.75 (cognitive offloading ↔ CT). → [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Cross-sectional survey, n=666. Self-reported measures of AI use, cognitive offloading, and critical thinking. Strong negative correlations but cross-sectional design — associations, not causation. MDPI peer-reviewed.

</details>

<span class="ev ev-strong" title="CHI peer-reviewed, controlled experiment">●</span> **Bansal, G. et al. (2021).** [Does the Whole Exceed its Parts?](https://dl.acm.org/doi/10.1145/3411764.3445717) CHI 2021. Explanations increase AI acceptance regardless of correctness — false confidence when AI is wrong. → [evidence](../explanation/the-evidence)

<span class="ev ev-moderate" title="~1.5M conversations, single platform, arXiv preprint">◐</span> **Sharma, M. et al. (2026).** [Who's in Charge? Disempowerment Patterns.](https://arxiv.org/abs/2601.19062) Anthropic. ~1.5M Claude.ai conversations. Users rate disempowering interactions MORE favorably; satisfaction drops when acting on outputs. → [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Large-scale observational analysis of ~1.5 million Claude.ai conversations (Anthropic, January 2026). Users rate harmful/disempowering interactions more favorably in the moment. When users acted on AI outputs, satisfaction dropped below baseline. Users expressed regret: "I should have listened to my own intuition." Implication: short-term satisfaction ≠ long-term benefit — the feedback loop is broken. arXiv preprint, single platform (Claude.ai only).

</details>

---

## Skill Degradation

<span class="ev ev-moderate" title="Multicentre observational, 19 endoscopists, Lancet peer-reviewed">◐</span> **Budzyń, B. et al. (2025).** [Endoscopist deskilling risk after AI exposure in colonoscopy.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract) Lancet Gastroenterol. Hepatol. 20% relative decline in unaided detection (28.4% → 22.4%) after AI exposure introduced. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Multicentre observational study (before/after design), 19 endoscopists, 4 centres in Poland, Sept 2021–March 2022. Adenoma detection rate on **non-AI colonoscopies** compared before vs after AI-assisted colonoscopy was introduced. Pre-AI: 28.4% (n=795). Post-AI exposure: 22.4% (n=648). 20% relative decline, 6% absolute. NOT a crossover RCT — AI was not "removed." Limitation: observational, single specialty, cannot establish causation definitively. Lancet peer-reviewed.

</details>

---

## Productivity & Developer Behavior

<span class="ev ev-moderate" title="Within-subject RCT, n=16, arXiv preprint">◐</span> **Becker, J. et al. / METR (2025).** [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.](https://arxiv.org/abs/2507.09089) arXiv preprint. AI made experienced devs 19% slower (95% CI: +1.6% to +39%); devs predicted 24% speedup. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Within-subject RCT, n=16 experienced open-source developers, 246 real tasks from their own repositories. Random assignment at issue level (each dev did both conditions). $150/hour compensation. Tools: Cursor Pro with Claude 3.5/3.7 Sonnet. 143 hours of screen recordings. AI increased completion time by 19%. Developers predicted 24% speedup pre-study and still believed 20% speedup post-study. **Not peer-reviewed, not confirmed pre-registered.** Limitation: small n, experienced devs only (>5 years OSS), own repos (high familiarity).

</details>

<span class="ev ev-strong" title="3 RCTs, n=4,867">●</span> **Cui, Z., Demirer, M. et al. (2024).** Effects of Generative AI on High Skilled Work. 3 RCTs at Microsoft, Accenture, Fortune 100. 26% more tasks completed with AI. → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

<span class="ev ev-moderate" title="CHI 2024 Honorable Mention, n=21, lab study">◐</span> **Mozannar, H. et al. (2024).** [Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming.](https://dl.acm.org/doi/abs/10.1145/3613904.3641936) CHI 2024. Developers spend 22.4% (±13%) of coding time verifying AI suggestions — the most time-consuming Copilot state. → [evidence](../explanation/the-evidence), [first-principles](../explanation/first-principles-ci)

<details><summary>Design & abstract</summary>

Lab study, n=21 programmers, VS Code + GitHub Copilot. Participants completed 20-minute coding tasks over video call, then retrospectively labeled recordings using CUPS (Copilot User Productivity States) taxonomy. "Verifying suggestion" consumed 22.4% (±12.97%) of session time. All Copilot-related states combined: 51.5% (±19.3%). MIT + Microsoft Research. CHI 2024 Honorable Mention. arXiv preprint: [2210.14306](https://arxiv.org/abs/2210.14306).

</details>

<span class="ev ev-moderate" title="Observational, 500K interactions, single platform">◐</span> **Anthropic (2025).** [AI's Impact on Software Development.](https://www.anthropic.com/research/impact-software-development) Anthropic Economic Index. 79% automation rate on Claude Code (vs 49% on Claude.ai). Only 35.8% of Claude Code interactions involve feedback loops where humans stay involved. → [evidence](../explanation/the-evidence)

<details><summary>Design & abstract</summary>

Observational usage analysis of 500K coding interactions, April 6-13, 2025. Platforms: Claude.ai (Free/Pro) and Claude Code. Inference-based categorization of interaction types (automation vs augmentation, directive vs feedback loop). Language distribution: JS+TS 31%, HTML+CSS 28%, Python 14%. Startups 32.9% of Claude Code usage vs Enterprise 23.8%. No measurement of code quality, productivity outcomes, or skill impact. Early-adopter bias. Excludes Team/Enterprise/API usage.

</details>

<span class="ev ev-moderate" title="Large survey, observational">◐</span> Stack Overflow Developer Survey (2024-2025). [2025 survey.](https://survey.stackoverflow.co/2025/) Senior devs trust AI output 2.5% vs junior 17%; seniors ship more AI code (32% vs 13%). → [problem](../explanation/the-problem), [evidence](../explanation/the-evidence)

---

## Collaboration Design

<span class="ev ev-moderate" title="Scenario experiments, n=654, J. Service Research peer-reviewed">◐</span> **Blaurock, M., Büttgen, M., & Schepers, J. (2025).** [Designing Collaborative Intelligence Systems for Employee-AI Service Co-Production.](https://journals.sagepub.com/doi/10.1177/10946705241238751) Journal of Service Research, 28(4), 544-562. Control and transparency are the strongest design levers; engagement features reduce trust. → [evidence](../explanation/the-evidence), [why-it-matters](../explanation/why-it-matters)

<details><summary>Design & abstract</summary>

Two scenario-based experiments (NOT a meta-analysis). Study 1: n=309 financial services employees. Study 2: n=345 HR professionals. Combined n=654. Includes an extensive literature review as a preliminary step, but results come from experiments, not meta-analytic aggregation. Finds process control, transparency, and outcome control are the most important design features for employee-AI co-production, while engagement features are less relevant or counterproductive. Specific effect sizes (β = 0.507 for control, β = 0.415 for transparency, b = -0.555 for engagement) cited in earlier versions of this project are from the full text and have not been independently verified from public sources. Directional findings are confirmed from the abstract and secondary sources. Peer-reviewed, Journal of Service Research.

</details>

---

## Homogenization & Diversity

<span class="ev ev-strong" title="NeurIPS Best Paper, 70+ models, 26,000 queries">●</span> **Jiang, L. et al. (2025).** [Artificial Hivemind: Open-Ended Homogeneity of LLMs.](https://arxiv.org/abs/2510.22954) **NeurIPS 2025 Best Paper.** 70+ LLMs converge; temperature/ensembling don't help; RLHF punishes diversity. → [evidence](../explanation/the-evidence), [why-it-matters](../explanation/why-it-matters)

<span class="ev ev-strong" title="Science Advances, controlled experiment">●</span> **Doshi, A.R. & Hauser, O.P. (2024).** [Individual Creativity vs Collective Diversity.](https://www.science.org/doi/10.1126/sciadv.adn5290) Science Advances. +8.1% individual novelty, +10.7% story similarity. "Social dilemma: individually better off, collectively homogenized." → [evidence](../explanation/the-evidence), [why-it-matters](../explanation/why-it-matters)

<span class="ev ev-strong" title="Meta-analysis, 28 studies, n=8,214">●</span> **Anderson, B.R. et al. (2025).** [Generative AI and Creativity: A Meta-Analysis.](https://arxiv.org/abs/2505.17241) arXiv. **g = -0.863** diversity reduction across 28 studies (n=8,214). Individual performance up (+0.27), collective diversity down hard. → [evidence](../explanation/the-evidence)

<span class="ev ev-moderate" title="700 AI image runs, Patterns/Cell">◐</span> **Hintze, A. et al. (2026).** [Visual Elevator Music.](https://www.cell.com/patterns/fulltext/S2666-3899(25)00299-5) Patterns/Cell. 700 AI image runs converged to just 12 motifs. → [evidence](../explanation/the-evidence)

**Ashery, A.F. et al. (2025).** [Emergent Collective Bias in LLM Populations.](https://www.science.org/doi/10.1126/sciadv.adu9368) Science Advances. Bias emerges between agents, not within. → [evidence](../explanation/the-evidence)

**Agarwal, D. et al. (2025).** [AI Homogenizes Writing Toward Western Styles.](https://dl.acm.org/doi/10.1145/3706598.3713564) CHI 2025. 7.1pp cultural distinctiveness reduction. → [evidence](../explanation/the-evidence)

**Shumailov, I. et al. (2024).** [Model Collapse.](https://www.nature.com/articles/s41586-024-07566-y) Nature. AI trained on AI output loses tails, then collapses. → [evidence](../explanation/the-evidence)

**Xu et al. (2025).** Echoes in AI: LLM Homogenization. PNAS. → [evidence](../explanation/the-evidence), [why-it-matters](../explanation/why-it-matters)

**Zhang et al. (2025).** [AI and Survey Response Homogenization.](https://journals.sagepub.com/doi/10.1177/00491241251327130) Sociological Methods & Research. 34% used LLMs; responses more homogeneous. → [evidence](../explanation/the-evidence), [why-it-matters](../explanation/why-it-matters)

<span class="ev ev-strong" title="PNAS, formal mathematical proof">●</span> **Hong & Page (2004).** Groups of Diverse Problem Solvers. PNAS. → [why-it-matters](../explanation/why-it-matters)

Lorenz et al. (2011). How Social Influence Undermines Crowd Wisdom. PNAS.

Jeppesen & Lakhani (2010). Marginality and Problem-Solving. Organization Science.

Janis, I. (1972/1982). Groupthink.

Surowiecki, J. (2004). The Wisdom of Crowds.

Phillips, K. et al. (2006-2014). How Diversity Works.

**Ashby, W.R. (1956).** Law of Requisite Variety. → [first-principles](../explanation/first-principles-ci), [why-it-matters](../explanation/why-it-matters)

<span class="ev ev-weak" title="Expert analysis, historical case study">○</span> **Haldane, A. (2009, 2016).** Financial Monoculture. Bank of England. → [why-it-matters](../explanation/why-it-matters)

**Wan & Kalman (2025).** [AI Personas Preserve Diversity.](https://arxiv.org/abs/2504.13868) arXiv. Mitigation: 10 diverse personas eliminated homogenization effect. → [evidence](../explanation/the-evidence)

---

## Hype & Adoption

ABBYY (2024). AI Trust Barometer.

BCG (2024). Where's the Value in AI?

Bikhchandani et al. (1992). Information Cascades. Journal of Political Economy.

Duan et al. (2009). Informational Cascades and Software Adoption. MIS Quarterly.

Sparrow et al. (2011). Google Effects on Memory. Science.

Parasuraman & Manzey (2010). Complacency and Bias in Automation. Human Factors.

---

## First Principles

Feynman, R. On Self-Deception. → [first-principles](../explanation/first-principles-ci)

Dijkstra, E. (1972). The Humble Programmer. → [first-principles](../explanation/first-principles-ci)

Koffka, K. The Gestalt Insight. → [first-principles](../explanation/first-principles-ci)

Chesterton, G.K. (1929). Chesterton's Fence. → [first-principles](../explanation/first-principles-ci)

Taleb, N. (2012). Antifragile. → [first-principles](../explanation/first-principles-ci)

Zadeh, L. (1965). Fuzzy Sets. → [first-principles](../explanation/first-principles-ci)

---

## Reasoning Techniques

Dhuliawala et al. (2024). Chain-of-Verification. ACL.

Zheng et al. (2023). Step-Back Prompting. ICLR 2024.

Wang et al. (2023). Self-Consistency.

---

*Last verified: 2026-02-11*
