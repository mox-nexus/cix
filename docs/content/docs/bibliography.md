# Bibliography

Primary sources for the v3 library, organized by argument arc. Every entry is cited in at least one article; every citation in the articles appears here.

**Evidence strength:** <span class="ev ev-strong">●</span> Strong (multiple studies, large n, peer-reviewed) · <span class="ev ev-moderate">◐</span> Moderate (single quality source) · <span class="ev ev-weak">○</span> Weak (expert opinion, preprint) · <span class="ev ev-speculative">◌</span> Speculative (inference)

---

## The Paradox

Productivity gains and learning harm — coexisting, documented, and invisible from inside.

<span class="ev ev-moderate" title="Within-subject RCT, n=16, arXiv preprint">◐</span> **Becker, J. et al. / METR (2025).** [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.](https://arxiv.org/abs/2507.09089) arXiv preprint. AI made experienced devs 19% slower (95% CI: +1.6% to +39%); devs predicted 24% speedup. 43-percentage-point perception gap.
→ [The Paradox](../explanation/the-paradox), [Honest Limits](../explanation/honest-limits)

<details><summary>Design & abstract</summary>

Within-subject RCT, n=16 experienced open-source developers, 246 real tasks from their own repositories. Random assignment at issue level (each dev did both conditions). $150/hour compensation. Tools: Cursor Pro with Claude 3.5/3.7 Sonnet. 143 hours of screen recordings. AI increased completion time by 19%. Developers predicted 24% speedup pre-study and still believed 20% speedup post-study. **Not peer-reviewed, not confirmed pre-registered.** Limitation: small n, experienced devs only (>5 years OSS), own repos (high familiarity).

</details>

<span class="ev ev-strong" title="3 RCTs, n=4,867">●</span> **Cui, Z., Demirer, M. et al. (2024).** Effects of Generative AI on High Skilled Work. SSRN working paper. 3 RCTs at Microsoft, Accenture, Fortune 100. 26% more tasks completed with AI (LATE for adopters). Less experienced developers benefited more.
→ [The Paradox](../explanation/the-paradox), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-moderate" title="RCT, n=52, arXiv preprint">◐</span> **Shen, J.H. & Tamkin, A. (2026).** [How AI Impacts Skill Formation.](https://arxiv.org/abs/2601.20245) Anthropic. arXiv preprint. Cohen's d = 0.738 (17pp skill gap). Six interaction patterns: 3 preserve learning, 3 don't. Generation-Then-Comprehension (86%) vs AI Delegation (39%).
→ [The Paradox](../explanation/the-paradox), [The Mechanism](../explanation/the-mechanism), [The Design Lever](../explanation/the-design-lever), [Honest Limits](../explanation/honest-limits)

<details><summary>Design & abstract</summary>

RCT, n=52 (26 control, 26 treatment), junior Python developers learning Trio library. 35-minute coding task + comprehension quiz (~58.5 min total). AI group scored 50% vs control 67% on quiz. Largest gap on debugging questions. High-scoring patterns: Generation-Then-Comprehension (86% mastery), Conceptual Inquiry (second-fastest). Chat-based interface (not agentic tools). Crowdworkers, not workplace context. Four pilot studies required due to non-compliance. Immediate comprehension only — no longitudinal retention data.

</details>

<span class="ev ev-strong" title="RCT, n~1,000, PNAS peer-reviewed">●</span> **Bastani, H. et al. (2025).** [Generative AI without guardrails can harm learning.](https://www.pnas.org/doi/10.1073/pnas.2422633122) PNAS. GPT Base: +48% during, -17% on unassisted exam. GPT Tutor (hints): +127% during, harm largely mitigated. Same model, different design, different trajectory.
→ [The Paradox](../explanation/the-paradox), [The Design Lever](../explanation/the-design-lever), [Honest Limits](../explanation/honest-limits)

<details><summary>Design & abstract</summary>

RCT (field experiment), n≈1,000 Turkish high school math students, three arms. GPT Base (unrestricted ChatGPT-4): +48% grades with AI, **-17% on exams without AI** vs control. GPT Tutor (hint-only, guardrailed): +127% grades with AI, negative effects "largely mitigated." Mechanism: "Without guardrails, students use GPT-4 as a 'crutch' during practice." PNAS peer-reviewed (received Nov 2024, accepted May 2025). Minor correction published Aug 2025 (affiliation typo only).

</details>

<span class="ev ev-moderate" title="Multicentre observational, 19 endoscopists, Lancet peer-reviewed">◐</span> **Budzyń, B. et al. (2025).** [Endoscopist deskilling risk after AI exposure in colonoscopy.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract) Lancet Gastroenterol. Hepatol. 21% relative decline in unaided adenoma detection (28.4% → 22.4%) after AI exposure. Observational, n=1,443.
→ [The Paradox](../explanation/the-paradox), [Honest Limits](../explanation/honest-limits)

<details><summary>Design & abstract</summary>

Multicentre observational study (before/after design), 19 endoscopists, 4 centres in Poland, Sept 2021–March 2022. Adenoma detection rate on **non-AI colonoscopies** compared before vs after AI-assisted colonoscopy was introduced. Pre-AI: 28.4% (n=795). Post-AI exposure: 22.4% (n=648). 21% relative decline, 6pp absolute. NOT a crossover RCT — AI was not "removed." Limitation: observational, single specialty, cannot establish causation definitively. Lancet peer-reviewed.

</details>

<span class="ev ev-moderate" title="Mixed review, conceptual distinction">◐</span> **Natali, L. et al. (2025).** Deskilling and upskilling inhibition in medicine after AI adoption. Distinguishes deskilling (experts lose what they have) from "upskilling inhibition" (novices never develop skills when AI provides answers first).
→ [The Paradox](../explanation/the-paradox)

<span class="ev ev-moderate" title="Large survey, ICSE peer-reviewed, n=410">◐</span> **Liang, J.T. et al. (2024).** Usability of AI Programming Assistants. ICSE 2024. n=410 developers. Primary uses: reducing keystrokes, recalling syntax, finishing fast. Primary barrier: control — can't get tool to generate what they want.
→ [The Paradox](../explanation/the-paradox)

---

## The Mechanism

How cognitive offloading works — trust, explanations, the generative step, encoding.

<span class="ev ev-moderate" title="Within-subject, n=30, PACMHCI">◐</span> **Chen, Z. et al. (2025).** AI-Assisted Note-Taking. PACMHCI. n=30, within-subject design. Full automation → lowest post-test scores; intermediate AI → highest; manual → most effortful but strong comprehension. Preferred ≠ effective.
→ [The Mechanism](../explanation/the-mechanism)

<span class="ev ev-strong" title="CHI peer-reviewed, n=319, mixed-effects regression">●</span> **Lee, H.P. et al. (2025).** [The Impact of Generative AI on Critical Thinking.](https://dl.acm.org/doi/full/10.1145/3706598.3713778) CHI 2025. β=-0.69 (AI confidence → less critical thinking, p<0.001). Self-confidence effects (β=+0.26, p=0.026; β=+0.31, p=0.046) do not survive Benjamini-Hochberg correction (threshold p<0.007). Uses mixed-effects regression, n=319 workers, 936 task examples.
→ [The Mechanism](../explanation/the-mechanism), [The Design Lever](../explanation/the-design-lever)

<details><summary>Design & abstract</summary>

Cross-sectional survey with mixed-effects regression modeling, 319 knowledge workers across 936 task examples (CHI peer-reviewed). AI-confidence strongly predicts reduced critical thinking (β=-0.69). Self-confidence effects show correct direction but do not survive the paper's own multiple comparisons correction (Benjamini-Hochberg threshold p<0.007). Limitation: cross-sectional, not longitudinal — correlation direction is assumed, not experimentally established. Reverse causation is possible.

</details>

<span class="ev ev-moderate" title="~1.5M conversations, single platform, arXiv preprint">◐</span> **Sharma, M. et al. (2026).** [Who's in Charge? Disempowerment Patterns.](https://arxiv.org/abs/2601.19062) Anthropic. arXiv preprint. ~1.5M Claude.ai conversations. Severe disempowerment potential: <1 in 1,000 conversations. Disempowering interactions receive higher approval ratings.
→ [The Mechanism](../explanation/the-mechanism)

<details><summary>Design & abstract</summary>

Large-scale observational analysis of ~1.5 million Claude.ai conversations (Anthropic, January 2026). Conversations flagged as moderate-or-severe disempowerment potential show positivity rates above the baseline across all categories. Causal mechanism is uncertain; several explanations possible; paper acknowledges this explicitly. Implication for training: approval ratings feed preference models, so systems trained on approval data may drift toward disempowerment. arXiv preprint, single platform (Claude.ai only).

</details>

<span class="ev ev-strong" title="CHI peer-reviewed, controlled experiment, 378 citations">●</span> **Bansal, G. et al. (2021).** [Does the Whole Exceed its Parts?](https://dl.acm.org/doi/10.1145/3411764.3445717) CHI 2021. AI explanations increase acceptance regardless of correctness. Complementary performance gains NOT increased by explanations. A wrong AI that explains itself confidently is more dangerous than one that doesn't.
→ [The Mechanism](../explanation/the-mechanism), [The Design Lever](../explanation/the-design-lever), [What cix Does](../explanation/what-cix-does), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-weak" title="arXiv preprint, n=54, published methodological critique">○</span> **Kosmyna, N. et al. (2025).** [Your Brain on ChatGPT.](https://arxiv.org/abs/2506.08872) MIT Media Lab. arXiv preprint. 83% of LLM group unable to quote own essays (Session 1 behavioral finding); EEG methodology disputed (published critique by Stankovic et al.).
→ [The Mechanism](../explanation/the-mechanism)

<details><summary>Design & abstract</summary>

Between-subjects EEG study, n=54 (18 per group: LLM, Search Engine, Brain-only). **arXiv preprint — not peer-reviewed.** Session 1: 83% (15/18) of LLM group couldn't quote any passage from essays written minutes earlier, vs ~11% in other groups. **Published critique:** Stankovic et al. (arXiv:2601.00856) identifies concerns with study design, reproducibility, EEG methodology, and reporting inconsistencies. Authors themselves state conclusions should be "treated with caution and as preliminary." The behavioral recall finding (83% failure) does not depend on the disputed EEG interpretation.

</details>

<span class="ev ev-moderate" title="RCT, n=30 per condition, AIED, arXiv preprint">◐</span> **Siddiqui, T. et al. (2025).** [AI-Supported Writing Process.](https://arxiv.org/abs/) AIED. RCT, n=30 per condition. Correlation between integrated writing tool use and knowledge transformation: r=0.608 (p=0.001). Correlation between chat-based LLM use and knowledge transformation: r≈0.
→ [The Mechanism](../explanation/the-mechanism), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-moderate" title="IUI peer-reviewed, N=124 total">◐</span> **Kazemitabaar, S. et al. (2025).** Cognitive Engagement Techniques for AI-Assisted Code Learning. IUI 2025. N=82 + N=42 = 124 total. Seven friction techniques tested; Lead-and-Reveal most effective. Population: novice undergrads (18-23), data structures course.
→ [The Mechanism](../explanation/the-mechanism), [The Design Lever](../explanation/the-design-lever), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-weak" title="Qualitative case study, Cornell">○</span> **Umarova, Z. et al. (2025).** Writer-AI Interactions in Writing Process. Cornell. Qualitative case study. Proactive idea exploration produced new ideas regardless of tool type; prolonged mindless copyediting produced few ideas even with Socratic AI.
→ [The Mechanism](../explanation/the-mechanism), [The Design Lever](../explanation/the-design-lever), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-moderate" title="Foundational, replicated across decades">◐</span> **Slamecka, N.J. & Graf, P. (1978).** The Generation Effect: Delineation of a Phenomenon. Journal of Experimental Psychology: Human Learning and Memory. Self-generated information retained ~22% better than passively received information. Replicated across decades of cognitive psychology.
→ [The Paradox](../explanation/the-paradox), [The Mechanism](../explanation/the-mechanism)

<span class="ev ev-moderate" title="Foundational, theoretical framework">◐</span> **Bereiter, C. & Scardamalia, M. (1987).** The Psychology of Written Composition. Knowledge telling vs knowledge transforming — expert writing as a recursive process that generates new understanding through the act of composition. Theoretical basis used in Siddiqui et al. 2025.
→ [The Paradox](../explanation/the-paradox), [The Mechanism](../explanation/the-mechanism)

<span class="ev ev-moderate" title="QCA, n=192, Studies in Higher Education peer-reviewed">◐</span> **Pallant, J.I. et al. (2025).** Mastering Knowledge with GenAI. Studies in Higher Education. QCA of 192 student reflections. Mastery-oriented GenAI use: OR=35.782 (p<0.001) for critical thinking. Not RCT — self-selection possible.
→ [The Paradox](../explanation/the-paradox), [The Design Lever](../explanation/the-design-lever), [Honest Limits](../explanation/honest-limits)

---

## The Design Lever

Which design features move outcomes — process control, transparency, engagement, orientation.

<span class="ev ev-moderate" title="Scenario experiments, n=654, J. Service Research peer-reviewed">◐</span> **Blaurock, M., Büttgen, M., & Schepers, J. (2025).** [Designing Collaborative Intelligence Systems for Employee-AI Service Co-Production.](https://journals.sagepub.com/doi/10.1177/10946705241238751) Journal of Service Research, 28(4), 544-562. Study 2 on perceived outcome responsibility: process control b=0.715 (p<.001), outcome control b=0.524 (p<.011), transparency b=0.511 (p<.001), engagement b=0.090 (ns). All four engagement hypotheses rejected. Expertise reversal: control features significant only for AI novices.
→ [The Design Lever](../explanation/the-design-lever), [What cix Does](../explanation/what-cix-does), [Honest Limits](../explanation/honest-limits)

<details><summary>Design & abstract</summary>

Two scenario-based experiments (NOT a meta-analysis). Study 1: n=309 financial services employees. Study 2: n=345 HR professionals. Combined n=654. Finds process control, transparency, and outcome control are the most important design features for employee-AI co-production; engagement features are not significant or counterproductive. Exploratory post-hoc: AI-experienced subgroup (n=42) showed no significant positive effects for control features; engagement showed what authors call "significant negative effect" on perceived service improvement (b=0.555, p<.05, statistical twin sample — note: source reports positive coefficient but describes as negative effect, a reporting inconsistency). Peer-reviewed, Journal of Service Research.

</details>

---

## The Stakes

Homogenization, model collapse, and what happens at the systemic level.

<span class="ev ev-moderate" title="PNAS, Microsoft Research, 100 generations">◐</span> **Xu, Y. et al. (2025).** Echoes in AI: LLM Homogenization. PNAS, Microsoft Research. 100 GPT-4 completions of a Kafka story: 50/100 had the policeman give directions (second left), 16/100 featured the same bakery. Human-written stories stayed unique.
→ [The Stakes](../explanation/the-stakes)

<span class="ev ev-strong" title="NeurIPS 2025, 70+ models, 26,000 queries">●</span> **Jiang, L. et al. (2025).** [Artificial Hivemind: Open-Ended Homogeneity of LLMs.](https://arxiv.org/abs/2510.22954) NeurIPS 2025. 70+ LLMs converge on the same outputs across model families. Sentence embedding similarity 71-82%. RLHF reward models miscalibrated to idiosyncratic preferences — penalize diversity.
→ [The Stakes](../explanation/the-stakes), [What cix Does](../explanation/what-cix-does), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-strong" title="Science Advances, preregistered experiment, n=893">●</span> **Doshi, A.R. & Hauser, O.P. (2024).** [Individual Creativity vs Collective Diversity.](https://www.science.org/doi/10.1126/sciadv.adn5290) Science Advances. Preregistered, n=893. +8.1% individual novelty (b=0.311, p<0.001), +10.7% collective similarity. "Social dilemma: individually better off, collectively homogenized."
→ [The Stakes](../explanation/the-stakes), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-weak" title="Meta-analysis, arXiv preprint, submitted to CHI, not yet peer-reviewed">○</span> **Holzner, M., Maier, C.D., & Feuerriegel, S. (2025).** [Generative AI and Creativity: A Meta-Analysis.](https://arxiv.org/abs/2505.17241) arXiv (submitted to ACM CHI, not yet peer-reviewed). 28 studies, n=8,214. Individual performance: g=+0.273. Idea diversity: **g=-0.863** (95% CI: [-1.328, -0.398], p<0.001). Leave-one-out: g=-0.655 to g=-0.952, all CIs exclude zero.
→ [The Stakes](../explanation/the-stakes), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-strong" title="Science Advances, computational experiment, N=24-200 agents">●</span> **Ashery, A.F., Aiello, L.M., & Baronchelli, A. (2025).** [Emergent Social Conventions and Collective Bias in LLM Populations.](https://www.science.org/doi/10.1126/sciadv.adu9368) Science Advances. Populations of LLM agents spontaneously develop social conventions. Strong collective biases emerge even when individual agents show no bias — bias is a property of the interaction, not the components.
→ [The Stakes](../explanation/the-stakes)

<span class="ev ev-moderate" title="arXiv, 27 LLMs, 70M claims">◐</span> **Masud, S. et al. (2025).** Epistemic Diversity of LLM Outputs. arXiv:2510.04226. 27 language models, 155 topics, 70 million claims. Every model produced outputs less epistemically diverse than a basic web search. Larger models less diverse than smaller ones.
→ [The Stakes](../explanation/the-stakes)

<span class="ev ev-weak" title="arXiv preprint, modified replication, proof-of-concept">○</span> **Wan, Y. & Kalman, Y.M. (2025).** [AI Personas Preserve Diversity.](https://arxiv.org/abs/2504.13868) arXiv preprint. Modified replication of Doshi & Hauser. 10 distinct AI personas: intra-persona similarity 0.92, inter-persona similarity 0.20. Homogenization effect eliminated. Proof-of-concept; not independently replicated.
→ [The Stakes](../explanation/the-stakes), [What cix Does](../explanation/what-cix-does), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-strong" title="Nature, Vol 631, demonstrated on multiple architectures">●</span> **Shumailov, I. et al. (2024).** [Model Collapse.](https://www.nature.com/articles/s41586-024-07566-y) Nature, Vol 631. Training generative models on model-generated content causes progressive loss of distribution tails. Early collapse: rare content disappears. Late collapse: convergence to very small variance. "Irreversible defects." Demonstrated on LLMs, VAEs, and Gaussian mixture models.
→ [The Stakes](../explanation/the-stakes), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-moderate" title="ICLR 2025, FAIR/Meta">◐</span> **Dohmatob, E. et al. (2025).** Strong Model Collapse. ICLR 2025, FAIR/Meta. Even 1% synthetic data fraction can lead to model collapse; larger models amplify collapse. IMPORTANT: 1% figure derived from supervised linear regression theoretical setting, not production LLM training.
→ [The Stakes](../explanation/the-stakes), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-moderate" title="arXiv, Stanford/MIT/Maryland/Harvard, not peer-reviewed">◐</span> **Gerstgrasser, M. et al. (2024).** [Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413) arXiv. Stanford/MIT/Maryland/Harvard. Replacing real data with synthetic → inevitable collapse (unbounded test error). Accumulating synthetic alongside real data → bounded error. Escape condition requires continuing human data generation.
→ [The Stakes](../explanation/the-stakes), [Honest Limits](../explanation/honest-limits)

<span class="ev ev-strong" title="PNAS, formal mathematical proof">●</span> **Hong, L. & Page, S.E. (2004).** Groups of Diverse Problem Solvers Can Outperform Groups of High-Ability Problem Solvers. PNAS. Formal mathematical proof: diversity of perspective can trump individual ability in collective problem-solving.
→ [The Stakes](../explanation/the-stakes)

<span class="ev ev-weak" title="Expert analysis, historical case study">○</span> **Haldane, A. (2009, 2016).** Financial Monoculture. Bank of England. When system components become highly correlated, aggregate risk approaches any single component's risk. Diversification becomes illusory.
→ [The Stakes](../explanation/the-stakes)

---

*Sources verified against text files in scratch/papers/ where available.*
