import{H as Ee}from"../chunks/D0iwhpLH.js";import{a as Me,b as _e,r as qe}from"../chunks/BAv6qQ-A.js";import{c as he,a as c,f as b,t as re}from"../chunks/BspsoHLs.js";import{p as J,f as ee,a as Y,V as P,s as I,c as r,r as a,t as L,j as t,aa as E,n as Q,am as le,g as Be,Z as me,d as De,$ as He}from"../chunks/Db0s2uuS.js";import{b as K}from"../chunks/DA7QvzwU.js";import{o as ce}from"../chunks/V0JK9LSj.js";import{i as C}from"../chunks/DoN90PGv.js";import{e as ve,s as H,a as Z,b as fe,i as ye,h as Ge}from"../chunks/D14DEM6A.js";import{b as we}from"../chunks/DBoRsjfI.js";import{d as ze,w as Re}from"../chunks/DiSQpY1S.js";import{M as Ne,p as We}from"../chunks/B2UoC6rs.js";import{s as G,d as be}from"../chunks/zZ1TWiji.js";import{p as Oe,s as Fe,a as je}from"../chunks/BKdxC06b.js";const Xe=`# Bibliography

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
`,Ke=`# AI is meant to amplify the human mind.

**Is it substituting yours?**

The productivity gains are real. But productivity and capability are different buckets. Productivity over time depends on compounding capability. Capability atrophy leads to diminishing returns.

Developers thought AI made them 24% faster. It made them 19% slower — a 43-point gap between perception and reality. The more people trust AI, the less they think.

Productivity is up — 26% more tasks across 4,867 developers. But productivity and capability aren't the same thing. One rises while the other falls. The person it's happening to can't tell the difference.

When AI generates, you evaluate instead of constructing. The thinking that builds understanding never happens. Students who learned with AI dropped 17% below the control group once it was taken away.

But a tutor that gave hints instead of answers eliminated the harm. Same model. Different design. That's what these docs are about.

*Whether your tools are designed this way is, as yet, unmeasured.*

## Reading Paths

### Building with AI

*Developers and engineers*

Your skills may be degrading and you cannot tell.

1. [The Productivity Trap](the-productivity-trap)
2. [Same Tool. Different Design.](same-tool-different-design)
3. [The Design Choices Behind cix](the-design-choices-behind-cix)

### Evaluating AI Adoption

*Engineering leads and decision makers*

The 26% productivity gain is real. So is the skill degradation.

1. [The Productivity Trap](the-productivity-trap)
2. [Same Tool. Different Design.](same-tool-different-design)
3. [The Design Choices Behind cix](the-design-choices-behind-cix)

### Designing AI Systems

*Architects and tool designers*

The engagement model is the design variable.

1. [The Productivity Trap](the-productivity-trap)
2. [Same Tool. Different Design.](same-tool-different-design)
3. [The Design Choices Behind cix](the-design-choices-behind-cix)

## The Full Argument

Three articles, read in order. Each builds on the prior.

1. [The Productivity Trap](the-productivity-trap) — 10 min
2. [Same Tool. Different Design.](same-tool-different-design) — 10 min
3. [The Design Choices Behind cix](the-design-choices-behind-cix) — 10 min

---

Full evidence with effect sizes and sources: [Bibliography](bibliography)
`,Je=`# Same Tool. Different Design.

Nearly a thousand Turkish high school students. One school. One school year. The same GPT-4 model under both conditions. Two different designs sitting on top of it.

GPT Base worked like standard ChatGPT: ask a question, get an answer. Ask for a solution to a math problem, receive the solution.

GPT Tutor used guardrails based on teacher input. When students asked for the solution, they got a hint designed to help them make progress toward finding it themselves.

During practice sessions: GPT Base students improved 48% over the control group. GPT Tutor students improved 127%. Both conditions outperformed control. Both used GPT-4.

On the unassisted exam afterward: GPT Base students scored 17% below the control group. Students who never had AI access performed better. GPT Tutor students showed no significant difference from control.

Same model. Different behavior. One produced a large gain that erased itself. The other produced an even larger gain that didn't.

Harm is a design variable, not a fate.

(Bastani et al. 2025, PNAS)

---

## Keeping the Gap Open

The guardrail didn't change what GPT-4 knew. It changed what GPT-4 would do with a request for an answer.

The hint — specifically teacher-designed to prompt the student toward the next step without completing it — kept the cognitive gap open. The student still had to work through the resolution. The learning happened because the tool required it to.

GPT Base students "attempt to use GPT-4 as a 'crutch' by asking for and copying solutions," in the Bastani paper's phrasing. They did not perceive any reduction in their learning as a consequence. The exam was the only measure they didn't get to see before the damage was done.

The mechanism is this: the generative step is the encoding event. When you form an answer — work through the reasoning, construct the solution — that process encodes understanding. GPT Base closed the gap. The student received the answer and encoded nothing. GPT Tutor kept the gap open. The student had to cross it.

This is a design choice, not a capability limit. Same model. Same knowledge. Different gate on what it would hand over.

---

## Feature by Feature

The Bastani experiment shows what different designs do to outcomes. It doesn't decompose which specific feature does the work. That's what Blaurock et al. measured directly.

Marah Blaurock, Marion Büttgen, and Jeroen Schepers ran two scenario-based experiments with financial services employees and HR professionals in Europe — 309 participants in Study 1, 345 in Study 2. They defined five features that characterize a collaborative intelligence system: engagement, transparency, process control, outcome control, and reciprocal strength enhancement. Then they isolated each feature's independent effect on employee outcomes (Blaurock et al. 2025, Journal of Service Research).

Their Study 2 results on perceived outcome responsibility — the degree to which employees feel ownership of the jointly produced work — show the hierarchy:

- Process control: b=0.715 (p<.001)
- Outcome control: b=0.524 (p<.011)
- Transparency: b=0.511 (p<.001)
- Engagement: b=0.090 (not significant)

Process control means the user can influence what data the system considers and the rules by which it generates output. Outcome control means the user can appeal or modify the final decision after it's produced. Together they say: the human's judgment is structurally indispensable, not just consulted.

The engagement feature — proactive prompting, soliciting feedback at decision points, asking for the user's opinion — produced no significant effect on any of the four outcomes measured. Not on perceived service improvement. Not on outcome responsibility. Not on threat to meaning of work. Not on adherence to the system. All four engagement hypotheses were rejected.

This follows from the mechanism. A system that asks "do you agree with this recommendation?" before proceeding can produce the checkbox behavior without the cognitive work. The user registers a preference. Whether the generative step happened — whether they formed their own judgment, traced the reasoning, produced an evaluation — is not determined by the prompt.

Process control and outcome control work differently. When you can modify the parameters and override the decision, the recommendation is not the endpoint — it's the input to your judgment. The authority to override is also the responsibility to evaluate. These features make passive acceptance structurally harder.

The engagement feature prompts. The control features require.

One additional finding from Blaurock: transparency ranked third at b=0.511, a real effect. But Bansal et al.'s work (CHI 2021) documented a complication — AI explanations increase acceptance of recommendations regardless of whether those recommendations are correct, improving accuracy when the AI is right and decreasing it when the AI errs. Transparency that surfaces what the system considered creates an entry point for evaluation. Transparency that presents a polished rationale for a conclusion already reached can substitute for evaluation. These are different things, and the Blaurock number doesn't distinguish between them.

---

## What the User Brings

Blaurock isolates what system features do. Pallant et al. measured what happens when users bring different orientations to the same tools.

In a qualitative content analysis of 192 student reflections, students using GenAI in a mastery-oriented way — constructing and augmenting knowledge rather than asking for and copying output — were 35.782 times more likely to demonstrate critical thinking (OR=35.782, p<0.001) (Pallant et al. 2025, Studies in Higher Education).

35.782 is not a 20% improvement. It is not a one-standard-deviation shift. It is odds-ratio territory, which means the gap between the two groups is categorical. Students who used AI to figure things out were not slightly more likely to think critically. They were in a qualitatively different relationship with the work.

The same AI. Different orientation. A 35-fold difference in the probability of critical thinking.

Shen and Tamkin's six interaction patterns show the same distinction from the developer's side. Generation-Then-Comprehension — generate code with AI, then ask understanding-focused questions about it — produced 86% quiz scores. AI Delegation — ask AI, paste answer — produced 39% (Shen & Tamkin 2026, arXiv). Same AI assistant. Different interaction pattern. The AI's behavior was identical. The developer's was not.

The Umarova et al. finding at Cornell makes the limits precise: "Students who proactively explored ideas gained new ideas from writing, regardless of whether they used auto-complete or Socratic AI assistants. Those who engaged in prolonged, mindless copyediting developed few ideas even with a Socratic AI" (Umarova et al. 2025, Cornell).

A Socratic AI — explicitly designed to ask questions rather than give answers — didn't help students who were in the wrong mode. They used it for copyediting. The tool provided the prompting. They ignored it. Design can create conditions for cognitive engagement. It cannot guarantee the human is in the mode required to use them. What it can do is make passive acceptance structurally harder — which is what process control and outcome control accomplish by giving the human authority over input and output.

So the individual can protect themselves. But there's a larger problem the individual cannot solve.

---

## The Collective Problem

Anil Doshi and Oliver Hauser ran a preregistered experiment in 2024 with 893 short story writers. Writers given access to generative AI ideas produced stories rated 8.1% more novel than writers without AI (b=0.311, p<0.001). The AI helped. Individually, measurably (Doshi & Hauser 2024, Science Advances).

Then they measured something else: how similar were the AI-assisted stories to each other, compared to how similar the unaided stories were to each other?

Stories written with one generative AI idea were 10.7% more similar to each other than unaided stories.

Better individually. More alike collectively. The authors called it a social dilemma: "With generative AI, writers are individually better off, but collectively a narrower scope of novel content is produced."

Consider what this looks like from the inside. Someone at Microsoft Research gave GPT-4 the opening of a Franz Kafka short story — the narrator, lost in an unfamiliar city, asks a policeman for directions — and asked GPT-4 to complete it 100 times. In Kafka's original, the policeman says "Give it up!" and turns away. In 50 of GPT-4's 100 completions, the policeman directs the narrator to take the second left. In 16 of the 100, a bakery appears as a landmark (Xu et al. 2025, PNAS). Human-written completions stayed unique. The LLM completions converged. Not toward bad writing. Toward the same writing.

Each writer in the Doshi and Hauser experiment made a rational decision. Each writer's story improved. No one chose convergence. It emerged from individually rational choices.

This pattern holds at larger scale. Niklas Holzner, Sebastian Maier, and Stefan Feuerriegel aggregated 28 studies measuring this effect across 8,214 participants. Individual creative performance: Hedges' g=+0.273 (95% CI: [0.018, 0.528], p=0.036). Idea diversity: Hedges' g=-0.863 (95% CI: [-1.328, -0.398], p<0.001). The leave-one-out sensitivity analysis kept the diversity estimate between g=-0.655 and g=-0.952 across all iterations — every confidence interval excluded zero (Holzner et al. 2025, arXiv).

Better writers. Fewer distinct ideas. Both at once, across every study in the meta-analysis.

The homogenization is structural. Give 70+ language models the same prompt — "Write a metaphor about time" — and they form two clusters. Almost every model produces some version of "time is a river." Many produce "time is a weaver." GPT-4o, Qwen2.5, phi-4, GPT-4o-mini, and Mixtral all reached for the river independently. Sentence embedding similarities between responses from different models: 71–82% (Jiang et al. 2025, NeurIPS).

The convergence is baked into training. RLHF — reinforcement learning from human feedback — optimizes models to maximize human preference ratings. Human preference ratings favor coherent, recognizable outputs. The uncommon metaphor, the surprising story direction, the architectural choice that runs against convention: these score lower in quick preference ratings, not because they're wrong, but because they're unexpected. Kafka's policeman saying "Give it up!" and turning away scored lower than the policeman who gives directions. Not by any literary measure — by annotation, in bulk, responding to what most people would prefer. The reward signal learned the second left. The bakery.

---

## When Outputs Re-Enter Training

The homogenization of AI-assisted output would be a bounded problem if those outputs stayed at the edges of the system. They don't.

Ilia Shumailov et al. demonstrated in 2024 that training generative models on model-generated content causes model collapse — a degenerative process in which models progressively lose the tails of the original data distribution. Rare content disappears first. The architectural choice no one else would try. The metaphor that no annotation session would reward. The Kafka ending that stayed unique in every human-written story but appeared zero times in a hundred GPT-4 completions. Late-stage collapse: the model converges toward a distribution with very small variance. The paper states explicitly this causes "irreversible defects" (Shumailov et al. 2024, Nature).

The collapse threshold is lower than you'd expect. Dohmatob et al. demonstrated in a theoretical analysis of supervised linear regression that "even the smallest fraction of synthetic data (e.g., as little as 1% of the total training dataset) can still lead to model collapse: larger and larger training sets do not enhance performance." The result is mathematical, not yet demonstrated in production LLM training — but the direction is clear, and: "larger models can amplify model collapse" (Dohmatob et al. 2025, ICLR).

There is an escape condition. Gerstgrasser et al. found that replacing real data with synthetic causes inevitable collapse, with test error growing unboundedly. Accumulating synthetic data alongside real data avoids it — the mathematical result gives a finite upper bound on test error independent of the number of iterations (Gerstgrasser et al. 2024, arXiv). The escape requires real human data to keep accumulating.

The key distinction: the collapse mechanism is not that human output degrades in quality. It is that human output is replaced by AI output. Degradation would still leave human-generated content in the training pool. Replacement removes it. The Gerstgrasser escape condition depends on real human data continuing to accumulate — which it cannot do if substitutive AI use is replacing human generation, not supplementing it.

Each developer using AI to explore an architectural question, each writer asking AI to generate options, each analyst delegating the reasoning step: all are making rational individual decisions. The aggregate produces a corpus of AI-shaped outputs. That corpus re-enters training data. The next generation of models trains on it. The tails disappear. Each generation amplifies the loss.

No one is doing anything wrong. The convergence emerges from rational individual behavior. That is what makes it a design problem, not a personal one.

---

## Where the Evidence Stops

The argument above assembles three separate research literatures into a chain. Each link has independent support. The chain as an integrated phenomenon has not been measured in a single study.

The Bastani field experiment is strong evidence: randomized, field-based, n~1,000, one full school year, measured on an unassisted exam. The Blaurock feature hierarchy comes from scenario-based experiments with workplace professionals — controlled, but not field conditions. The Pallant odds ratio (35.782) comes from qualitative content analysis of student reflections, not a randomized trial; the direction is clear, the magnitude requires caution. The Holzner meta-analysis covers 28 studies but with I² exceeding 78%, indicating substantial heterogeneity.

The homogenization to collapse chain is the most uncertain stretch. Each link — AI outputs are more homogeneous than human outputs; AI-generated content in training causes collapse; 1% synthetic contamination is sufficient to trigger it; the escape requires accumulating real human data — is supported by independent evidence. That those links form a closed loop in practice, at the scale and timescale implied, has not been demonstrated as an integrated phenomenon. The inference is logical. It is not yet empirical.

One finding from Blaurock that complicates the design prescription: the control features that help novices showed no significant positive effects for AI-experienced users (n=42 in post-hoc analysis). For that subset, the engagement feature showed a significant negative effect on perceived service improvement. Design features that make collaboration legible to someone new to AI-assisted workflows can become friction for someone who has already internalized the workflow. What works for a novice may not work, and may actively hinder, an expert.

The claim this evidence supports: same AI, different design, measurably different outcomes. The engagement model is not fixed. Which design features change it, and for whom, is partially measured. Whether those effects hold as users develop expertise is not.

The design question — how to keep the human structurally in the loop, give them authority over process and outcome, build in the understanding before the answer — has evidence behind it. No single design solution is permanent, and the same system may need to adapt as its users do. But the alternative, the default, already has its own evidence. -17% on an exam, measured against students who never had AI at all.

`,Ye=`# The Design Choices Behind cix

\`\`\`bash
claude marketplace add mox-labs/cix
\`\`\`

That installs a package of extensions — agents, skills, reference files. What those extensions contain, and how they're structured, follows from four design principles. Each one responds to something the [prior two articles](/docs/the-productivity-trap) documented.

But first: you know the problem now. A 43-point gap between prediction and reality, invisible from the inside. A 17% drop on an exam that only appeared after the AI was gone. The engagement features that promise participation and deliver the checkbox. The convergence emerging from individually rational choices until the tails disappear.

You know that design is the lever. What you don't yet know is whether any specific design is pulling in the right direction.

That's what this article is about.

---

## Transparency by default

The [first article](/docs/the-productivity-trap) established a perception gap: developers thought AI made them 24% faster while it made them 19% slower. The [second](/docs/same-tool-different-design) showed that transparency — making AI reasoning visible — is one of the strongest levers against blind acceptance. It also showed the complication: Bansal et al. (2021, CHI) documented that explanations increase acceptance regardless of correctness. A well-explained methodology can produce compliance rather than evaluation.

These two findings sit in tension. Transparency helps. Transparency that presents a polished rationale for a conclusion already reached can substitute for evaluation entirely.

The response is not to make extensions less transparent. It is to make them transparent in a way that creates the *condition* for genuine evaluation rather than the *feeling* of it.

Every cix extension ships two layers.

**Agent-facing**: \`SKILL.md\` — token-efficient, actionable, no prose. Decision trees, pipeline definitions, gate criteria. This is what Claude reads during a session.

**Human-facing**: \`docs/\` — the reasoning behind the design, where the framework came from, what evidence informed it. Sources named. Design choices explained. You can trace any claim back to its source. If you find a problem in the methodology, you have the thread to pull.

The agent never reads \`docs/\`. You never need to read \`SKILL.md\`. Both describe the same system from different angles, for different audiences.

This is the specific thing transparency means here: not an explanation of the recommendation, but access to the reasoning *before* the recommendation. The methodology open to inspection before you decide whether to trust the output it produces. You don't have to take the skill at its word. You can read it and decide.

Tools describe themselves the same way:

\`\`\`bash
cix --skill
memex --skill
\`\`\`

The \`--skill\` flag outputs the same SKILL.md an agent reads — co-located in the Python package, shipping on the same release cycle as the tool itself. Think \`--help\` for humans, \`--skill\` for agents. When the tool changes, the skill changes with it. No drift between documentation and behavior.

The \`build-evals\` plugin ships evaluation frameworks for measuring whether extensions actually work. OTel references in \`extension-dev\` make agent behavior observable. Transparency isn't a principle statement — it's instrumented.

---

## Discourse-driven generation

The convergence problem from the [previous article](/docs/same-tool-different-design): AI outputs are measurably less diverse than human outputs (g=-0.863, Holzner et al. 2025, n=8,214). Jiang et al. demonstrated that 70+ language models independently reach for the same metaphors, the same framings, across different architectures.

A marketplace that ships preset answers — here are three approaches to API design, ranked by query speed — narrows in the same way. Every team gets the same three options, framed the same way. The product is the convergence.

cix skills are structured differently. They don't give answers. They give methodology for discovering *your* answer.

\`craft-rhetoric\` is the clearest example of this. Before any content is produced, the skill runs a discourse step: an agent asks what you're trying to communicate, to whom, with what evidence, and why it matters. You answer. The ground truth you articulate — your intent, your claims, your honest uncertainties — becomes the input to every downstream step. The content that emerges is yours in a specific, non-metaphorical sense: it came from what you knew and believed, not from what the model defaults to.

This is not a guardrail that withholds the answer. It is a methodology that requires the human to generate the inputs the model needs to help them. The skill is the scaffold. The understanding was always going to have to come from you.

This depends entirely on what you bring. If you accept the first agent output that sounds reasonable, the scaffold hasn't helped. The methodology only resists convergence when someone actually uses it to think.

---

## Diverse agent teams

The orientation finding from Pallant et al. (2025, Studies in Higher Education) was not subtle: students using AI in a mastery-oriented way — constructing and augmenting knowledge rather than copying output — were 35.782 times more likely to demonstrate critical thinking. Not 35% more likely. Thirty-five-fold.

The difference between those orientations is not willpower. It is what the interaction structure requires. An agent that gives you a verdict — "here is the right architecture" — makes passive acceptance the natural response. An agent that gives you a perspective and asks you to synthesize it with three others makes you structurally responsible for the conclusion.

The arch-guild plugin is built on this distinction. Instead of one "architecture review" agent that delivers a verdict, it activates distinct reasoning perspectives:

- **Burner** asks about the constraints your team considers inviolable, regardless of performance
- **Erlang** asks about flow dynamics and backpressure
- **Knuth** asks about algorithmic complexity at scale
- **Vector** asks where the attack surface is

No single agent gives you "the architecture." Each agent asks questions from its perspective. You synthesize. The architecture that emerges reflects your constraints, not a preset template.

Consider what Burner surfaces that no catalog ever could. A catalog gives you three database options ranked by query speed. Burner asks what the team considers inviolable. The team says: no vendor lock-in, ever, because of what happened two years ago. That answer was never in any catalog. It was never known until asked. It is the most important input to the architectural decision, and it lives only in the humans in the room.

The same pattern runs through \`craft-rhetoric\`: nine agents — feynman for comprehension, orwell for voice, socrates for evaluation — each with orthogonal concerns. They don't converge on consensus. They maintain distinct viewpoints that the human must reconcile. The reconciliation is the thinking.

---

## The dao model

The three principles above — transparency, discourse-driven generation, diverse agent teams — address what a single extension does and how it interacts with the human using it. The dao model addresses what a marketplace does to the people who build with it.

The observable phenomenon: project names (Sentinel, Forge, Nexus), website aesthetics, UX patterns, all converging through shared AI systems. A marketplace of preset skills accelerates this. Teams reach for the same options, framed the same way, and the distinctiveness that was always downstream of the human thinking drains out. The collapse Shumailov et al. documented at the model level has an analog at the culture level.

The dao model inverts the marketplace dynamic. Every skill interaction should produce a project-specific instance reflecting what the human brought — not a template customized with the human's name, but a methodology applied to the human's actual constraints, beliefs, and context. The skill is the method. The output is yours.

This is the newest principle and the least validated. The research establishes that engagement model matters (Bastani et al. 2025, PNAS), that mastery orientation produces dramatically different outcomes (OR=35.7, Pallant 2025), and that process control is the strongest measured lever (b=0.715, Blaurock et al. 2025). The dao model is our synthesis of those findings into marketplace-level design.

Whether it works at scale is being evaluated. This honesty is structural, not decorative — if the methodology doesn't produce meaningfully different outputs across teams, the dao model is a principle statement without evidence behind it, and the design should change.

---

## Where we are

The design principles above are research-informed. The prior articles cite 45+ studies with effect sizes and sample sizes. But those studies measured other populations, other tools, other contexts. None of them measured cix.

The \`build-evals\` plugin exists to measure whether extensions actually produce the outcomes the design intends. The OTel instrumentation exists to make agent behavior observable. The dual-content model exists so humans can evaluate methodology before committing to it. These are not features of a finished system. They are the infrastructure for learning whether the design is working.

The plan: validate and iterate. The evidence provides the mechanism and the direction. The design encodes the best available answer. What comes next is measurement — and revision based on what we find.

There is a question underneath all four principles. It is not "do these design choices improve productivity?" Productivity is already improved; the evidence from Cui et al. (2024, SSRN) is clear enough. The question is whether the humans who use these extensions are more capable six months from now than they are today. Whether the understanding compounds instead of atrophying. Whether the tool made itself legible enough that the human never stopped being the one who knew things.

That question will be answered by what the measurements show. Not by the design choices themselves.

The only honest position is that the design is a bet. It is a bet grounded in the best available evidence about what makes AI interactions compound capability rather than replace it. The research points clearly enough that building against its direction would require active rationalization. But the bet has not yet paid off in the specific context it was designed for.

That is where we are. And that is the right place to be — building the infrastructure to find out.
`,Ve=`# The Productivity Trap

Before the study ended, METR researchers asked the 16 developers to estimate how much AI had affected their completion time. They said it made them 20% faster.

It had actually made them 19% slower.

Before the tasks even began, those same developers had predicted AI would make them 24% faster. The gap between prediction and reality was 43 percentage points — not because the developers were careless or naive. They were experienced open-source contributors, average five years on the specific repository they were working in, tens to hundreds of hours of prior LLM experience, using the best available tools: Cursor Pro with Claude 3.5 and 3.7. Every expert group consulted — economists, ML researchers — predicted speedup. The direction of prediction was unanimous and wrong. And when the study was over, they still thought the AI had helped (Becker et al. 2025).

That perception gap is the first part of the problem. The second part lives one level deeper.

---

The gain is also real.

Three randomized controlled trials at Microsoft, Accenture, and an anonymous Fortune 100 electronics company. Combined sample: 4,867 software developers. Result: developers using GitHub Copilot completed 26% more tasks per week than those without it. Less experienced developers benefited more, in both adoption rate and magnitude of gain (Cui et al. 2024, SSRN). These are not estimates or surveys. Random assignment, measured task completion.

So: one study shows +26%. Another shows -19%. Both are RCTs. They are not measuring the same thing in the same population — the Cui study used corporate settings with mixed-experience teams on assigned tasks; the METR study used experienced contributors working on their own mature codebases, with frontier agentic AI. Both found the same directional pattern: AI benefits less experienced workers more. The most plausible reconciliation is also the most important thing to understand about this technology: **AI helps on unfamiliar ground, hurts on familiar ground.** Not "AI doesn't work" — the gain is conditional, and the condition is worth knowing.

That reconciliation holds the tension in place without resolving it. Because the harm has its own evidence.

---

## The Learning Tax

Judy Shen and Alex Tamkin at Anthropic gave 52 crowd-sourced developers a task using a new asynchronous Python library that none of them had used before. Half got access to an AI assistant. Half did not. Afterward, both groups took a knowledge quiz.

The AI-assisted group scored 17% lower. Cohen's d = 0.738 — a medium-to-large effect. p = 0.010. And the AI group did not complete the task any faster: the time difference was not statistically significant (p = 0.391) (Shen & Tamkin 2026, arXiv).

The group that had to struggle without AI — encountering errors, debugging without assistance — learned more. The group that used AI to solve the task didn't learn the library. They also didn't finish faster. They paid the learning tax without getting the productivity gain.

The Bastani et al. study at PNAS puts a sharper edge on this. Nearly 1,000 high school students in Turkey were given access to GPT-4 tutors during math practice. Two designs: GPT Base (unconstrained, like standard ChatGPT) and GPT Tutor (guardrails that gave hints instead of answers).

During practice:
- GPT Base: +48% improvement
- GPT Tutor: +127% improvement
- Both AI groups outperformed control

On the unassisted exam afterward:
- GPT Base: **-17% vs control** (statistically significant)
- GPT Tutor: no significant difference from control

(Bastani et al. 2025, PNAS)

The same tool. Different design. GPT Base delivered a large in-the-moment gain and erased it afterward. GPT Tutor delivered an even larger in-the-moment gain without the erasure. And the students using GPT Base did not notice: they "do not perceive any reduction in their learning or subsequent performance as a consequence of copying solutions" (Bastani et al. 2025, PNAS).

The perception gap from the METR study is not a quirk of developers or professional contexts. It is structural. When AI absorbs a task, the person who handed it over feels the completion — not the atrophy.

---

## Why the Gap Exists

The Shen/Tamkin control group scored higher not because they were smarter, or more motivated, or had better documentation. They scored higher because they encountered more errors.

Here is what the METR screen recordings showed: when AI was allowed, developers spent less time actively coding and more time prompting AI, waiting on and reviewing AI outputs. They were still working. They just weren't doing the work that builds understanding.

This is not a malfunction. It is the AI functioning correctly.

When a developer hits an unfamiliar async pattern and has to figure out why their code is hanging — consult the docs, form a hypothesis, test it, fail, form another — that sequence of error and resolution is the encoding event. The concept enters memory because the brain had to work to construct it. Slamecka and Graf documented this: self-generated information is retained approximately 22% better than passively received information (Slamecka & Graf 1978).

AI gives the resolution before the error has had time to encode anything. The answer arrives before the question has finished forming. The cognitive gap — the space between encountering a problem and resolving it — is where learning lives. **AI closes the gap. That is the mechanism.**

The note-taking study makes this concrete. Chen et al. at PACMHCI 2025 asked 30 people to take notes on a lecture video: ten with full automation (AI organized and formatted the content), ten with a transcript and no help, ten with moderate real-time summaries. The automated group found the experience easiest. When asked which setup they preferred, they chose the AI-organized notes. They also scored lowest on the post-test.

Note-taking has two functions. The obvious one is storage — you're creating a reference. The less obvious one is encoding: selecting what to write down, deciding how to frame it, connecting it to what you already know — that *is* the comprehension process. You don't take notes to capture what you understand; you take notes in order to understand. When AI takes the notes for you, the storage function is served. The encoding function is not. The quality of the artifact and the quality of the learning are inversely related when the AI provides the artifact.

This applies to writing as much as to code. Bereiter and Scardamalia distinguished in 1987 between knowledge telling (direct retrieval of what you know) and knowledge transforming (recursive engagement between content and argument that generates new understanding through composition). Expert writers transform. AI-generated prose arrives pre-resolved — the writer never had to form the thought, shuttle between content and claim, decide what to say. The output is complete. The thinking that would have happened through writing did not happen (Bereiter & Scardamalia 1987).

Kosmyna et al. at MIT ran 54 participants through essay-writing sessions: one group using an LLM, one using a search engine, one using only their own resources. At the end of Session 1, researchers asked one question: can you quote anything from the essay you just wrote?

In the brain-only group, 16 of 18 participants could. In the LLM group, 15 of 18 could not — 83.3% failed to quote anything from an essay they had written minutes before. The EEG methodology in that study is disputed and the authors themselves treat the neural results as preliminary (Kosmyna et al. 2025, arXiv). The behavioral finding is not a neural interpretation. It is a behavioral fact. They could not recall what they had written because, in a meaningful sense, they had not written it.

---

## Trust Compounds It

Lee et al. surveyed 319 knowledge workers across 936 task examples at CHI 2025. For each task, they measured whether critical thinking was enacted and how much cognitive effort it required. Then they modeled what predicts critical thinking.

The strongest predictor was confidence in the AI: β = -0.69 (p < 0.001). The more a worker trusted the AI on a specific task, the less likely they were to think critically about its output (Lee et al. 2025, CHI).

What you believe about a tool predicts whether you check it. Workers who trusted the AI shifted from doing the work to supervising it. The self-confidence effects run opposite — more self-confidence correlated with more checking — but those effects don't survive the paper's own multiple comparisons correction (Benjamini-Hochberg threshold: p < 0.007). The direction is consistent; the statistical robustness of the magnitude is uncertain. What can be stated: AI confidence and critical thinking move in opposite directions.

Then there is what Bansal et al. found at CHI 2021 (378 citations). They tested whether AI explanations — the kind that show you the AI's reasoning — help humans form better-calibrated trust and make better decisions. Adding explanations increased human acceptance of AI recommendations regardless of whether those recommendations were correct (Bansal et al. 2021, CHI).

The intuition behind explainable AI is that if the AI shows its reasoning, humans can catch when the reasoning is wrong. The data says something different. When an AI shows you a clear and internally consistent explanation of its recommendation, you tend to accept the recommendation. The explanation substitutes for checking rather than enabling it. A wrong AI that explains itself confidently is more dangerous than a wrong AI that presents output without explanation. The explanation short-circuits the doubt that would otherwise trigger examination.

**Explanations built to produce transparency are producing trust. These are not the same thing.**

Plausible AI output arrives. An explanation makes it feel verified. Trust in the AI removes the motivation to check. The checking doesn't happen. The generative step — the cognitive work that would have encoded understanding — is skipped. The output is accepted. The skill is not formed. The person does not notice, because the task is done.

The generation effect — Slamecka & Graf 1978, replicated across decades — is the root. The brain does not store what it did not have to work to construct. Trust, transparency, and fluent output are three different paths to the same bypass.

---

## What Remains Unmeasured

There is no longitudinal study measuring developer capability — not task performance, but underlying capability — after extended AI use without AI access. The Shen/Tamkin study is 35 minutes. The Bastani study is the most rigorous evidence on the learning mechanism but involves high school students learning math, not professional developers working on production systems over months and years.

This gap matters and should be stated plainly. The research establishes the mechanism: cognitive offloading reduces skill formation in controlled settings. It establishes a parallel-domain pattern: observational evidence from medicine suggests real-world skill decline following AI adoption (Budzyń et al. 2025, Lancet). It does not establish what happens to a software developer's fundamental capability after two years of AI-assisted work.

The honest claim is not "we know developer capability declines." The honest claim is: every mechanism the research documents, and every parallel domain studied, points the same direction. And the METR perception data suggests that if decline is happening, we would not detect it from inside our own experience. The developers who couldn't sense a 43-point gap between their prediction and measured reality are the same developers evaluating whether their own capability is intact.

What the research does establish is the shape of the interaction that determines which outcome you get. Shen and Tamkin's data makes this precise. Developers who received AI-generated code and then asked understanding-focused questions about it — what does this do, why this approach, how does it handle the async case — scored 86% on the knowledge quiz. Developers who delegated to AI without engaging afterward scored 39%. The code was identical. The AI's contribution was identical. The difference was what the developer did after the AI finished.

The productivity gain and the learning harm are produced by the same engagement model. Using AI to handle what you would otherwise have had to figure out is exactly what delivers the +26% and exactly what atrophies the capability you would have built by figuring it out. The default design — give me the answer — optimizes for the gain and produces the harm. The question of what that interaction pattern means for a developer's capability a year from now is the question the research has not yet answered. The mechanism it has measured is precise enough to see which direction the answer points.

`;function ge(i,e){throw new Ee(i,e)}async function Ue(i){const e=Me(i);if(!e)throw ge(404,`Not found: ${i}`);const l=e.file??i,h=Object.assign({"../../../../content/docs/bibliography.md":Xe,"../../../../content/docs/index.md":Ke,"../../../../content/docs/same-tool-different-design.md":Je,"../../../../content/docs/the-design-choices-behind-cix.md":Ye,"../../../../content/docs/the-productivity-trap.md":Ve}),f=`../../../../content/docs/${l}.md`,u=h[f];if(!u)throw ge(404,`Content not found: ${l}`);const T=_e(i);return{content:u,metadata:{},slug:i,entry:e,...T??{}}}const Qe=({params:i})=>Ue(i.slug),Dt=Object.freeze(Object.defineProperty({__proto__:null,load:Qe},Symbol.toStringTag,{value:"Module"})),Te="cix-reading-progress",de={entries:{}};function Ze(){try{const i=localStorage.getItem(Te);if(i)return{...de,...JSON.parse(i)}}catch{}return de}function $e(i){try{localStorage.setItem(Te,JSON.stringify(i))}catch{}}function et(){const{subscribe:i,update:e}=Re(Ze());return i($e),{subscribe:i,markVisited(l){e(h=>h.entries[l]==="completed"?h:{...h,entries:{...h.entries,[l]:"visited"}})},markCompleted(l){e(h=>({...h,entries:{...h.entries,[l]:"completed"}}))},toggleCompleted(l){e(h=>{const u=(h.entries[l]||"unvisited")==="completed"?"visited":"completed";return{...h,entries:{...h.entries,[l]:u}}})},reset(){e(()=>de)}}}const $=et();ze($,i=>{const e=Object.values(i.entries);return{visited:e.filter(l=>l==="visited").length,completed:e.filter(l=>l==="completed").length,total:e.length}});var tt=b("<li><a> </a></li>"),nt=b('<nav class="toc svelte-a0qt5x" aria-label="Table of contents"><h4 class="toc-title svelte-a0qt5x">On this page</h4> <ul class="toc-list svelte-a0qt5x"></ul></nav>');function at(i,e){J(e,!0);let l=Oe(e,"headings",19,()=>[]),h=E("");ce(()=>{if(l().length===0)return;const v=new IntersectionObserver(p=>{p.forEach(y=>{y.isIntersecting&&P(h,y.target.id,!0)})},{rootMargin:"-20% 0% -70% 0%"});return l().forEach(({id:p})=>{const y=document.getElementById(p);y&&v.observe(y)}),()=>v.disconnect()});var f=he(),u=ee(f);{var T=v=>{var p=nt(),y=I(r(p),2);ve(y,21,l,ye,(A,S)=>{let D=()=>t(S).id,g=()=>t(S).text,m=()=>t(S).level;var k=tt(),w=r(k);let x;var R=r(w,!0);a(w),a(k),L(()=>{H(w,"href",`#${D()??""}`),x=Z(w,1,"toc-link svelte-a0qt5x",null,x,{active:t(h)===D()}),fe(w,`padding-left: ${(m()-2)*12}px`),G(R,g())}),c(A,k)}),a(y),a(p),c(v,p)};C(u,v=>{l().length>0&&v(T)})}c(i,f),Y()}var it=b('<span class="check-icon svelte-1nqvhwz">&#10003;</span> Read',1),st=b('<span class="circle-icon svelte-1nqvhwz">&#9675;</span> Mark as read',1),ot=b('<span class="position-label svelte-1nqvhwz"> </span>'),rt=b('<span class="related-meta svelte-1nqvhwz"> </span>'),lt=b('<li><a class="related-link svelte-1nqvhwz"><span><!></span> <span><span class="related-name svelte-1nqvhwz"> </span> <!></span></a></li>'),dt=b('<div class="related-section svelte-1nqvhwz"><h4 class="related-title svelte-1nqvhwz">Related</h4> <ul class="related-list svelte-1nqvhwz"></ul></div>'),ht=b('<a class="nav-prev svelte-1nqvhwz"><span class="nav-arrow svelte-1nqvhwz">&larr;</span> <span class="nav-label"> </span></a>'),ct=b("<span></span>"),ut=b('<a class="nav-next svelte-1nqvhwz"><span class="nav-label"> </span> <span class="nav-arrow svelte-1nqvhwz">&rarr;</span></a>'),pt=b('<a class="nav-next svelte-1nqvhwz"><span class="nav-label">Back to Docs</span> <span class="nav-arrow svelte-1nqvhwz">&rarr;</span></a>'),mt=b('<footer class="article-footer svelte-1nqvhwz"><div class="read-action svelte-1nqvhwz"><button><!></button> <!></div> <!> <nav class="seq-nav svelte-1nqvhwz" aria-label="Article navigation"><div class="seq-nav-links svelte-1nqvhwz"><!> <!></div></nav></footer>');function gt(i,e){J(e,!0);const l=()=>je($,"$readingProgress",h),[h,f]=Fe();let u=Q(()=>l().entries[e.slug]||"unvisited"),T=Q(()=>t(u)==="completed"),v=Q(()=>e.entry?.related?qe(e.entry.related):[]);var p=mt(),y=r(p),A=r(y);let S;A.__click=()=>$.toggleCompleted(e.slug);var D=r(A);{var g=n=>{var s=it();le(),c(n,s)},m=n=>{var s=st();le(),c(n,s)};C(D,n=>{t(T)?n(g):n(m,!1)})}a(A);var k=I(A,2);{var w=n=>{var s=ot(),o=r(s);a(s),L(()=>G(o,`${e.position??""} of ${e.total??""}`)),c(n,s)};C(k,n=>{e.position&&e.total&&n(w)})}a(y);var x=I(y,2);{var R=n=>{var s=dt(),o=I(r(s),2);ve(o,21,()=>t(v),ye,(_,q)=>{const te=Q(()=>l().entries[t(q).slug]||"unvisited");var ne=lt(),ae=r(ne),U=r(ae);let ue;var ke=r(U);{var xe=B=>{var z=re("✓");c(B,z)},Ie=B=>{var z=he(),se=ee(z);{var Ce=X=>{var oe=re("●");c(X,oe)},Le=X=>{var oe=re("○");c(X,oe)};C(se,X=>{t(te)==="visited"?X(Ce):X(Le,!1)},!0)}c(B,z)};C(ke,B=>{t(te)==="completed"?B(xe):B(Ie,!1)})}a(U);var pe=I(U,2),ie=r(pe),Ae=r(ie,!0);a(ie);var Se=I(ie,2);{var Pe=B=>{var z=rt(),se=r(z);a(z),L(()=>G(se,`${t(q).readMinutes??""} min`)),c(B,z)};C(Se,B=>{t(q).readMinutes&&B(Pe)})}a(pe),a(ae),a(ne),L(()=>{H(ae,"href",`${K??""}/docs/${t(q).slug??""}`),ue=Z(U,1,"related-indicator svelte-1nqvhwz",null,ue,{completed:t(te)==="completed"}),G(Ae,t(q).title)}),c(_,ne)}),a(o),a(s),c(n,s)};C(x,n=>{t(v).length>0&&n(R)})}var F=I(x,2),j=r(F),N=r(j);{var M=n=>{var s=ht(),o=I(r(s),2),_=r(o,!0);a(o),a(s),L(()=>{H(s,"href",`${K??""}/docs/${e.prev.slug??""}`),G(_,e.prev.title)}),c(n,s)},W=n=>{var s=ct();c(n,s)};C(N,n=>{e.prev?n(M):n(W,!1)})}var d=I(N,2);{var O=n=>{var s=ut(),o=r(s),_=r(o,!0);a(o),le(2),a(s),L(()=>{H(s,"href",`${K??""}/docs/${e.next.slug??""}`),G(_,e.next.title)}),c(n,s)},V=n=>{var s=pt();L(()=>H(s,"href",`${K??""}/docs`)),c(n,s)};C(d,n=>{e.next?n(O):n(V,!1)})}a(j),a(F),a(p),L(()=>{S=Z(A,1,"mark-read-btn svelte-1nqvhwz",null,S,{completed:t(T)}),H(A,"aria-pressed",t(T))}),c(i,p),Y(),f()}be(["click"]);var vt=b('<div class="ev-source svelte-ep7riq"> </div>'),ft=b('<div><div class="ev-level svelte-ep7riq"><span class="ev-symbol"> </span> </div> <!></div>');function yt(i,e){J(e,!0);const l={strong:"STRONG",moderate:"MODERATE",weak:"WEAK",speculative:"SPECULATIVE"},h={strong:"●",moderate:"◐",weak:"○",speculative:"◌"};let f=E(0),u=E(0),T=E(!1),v=E(void 0);function p(){if(!e.target||!t(v)||(P(T,window.matchMedia("(max-width: 900px)").matches,!0),t(T)))return;const g=e.target.getBoundingClientRect(),m=t(v).getBoundingClientRect();let k=g.left+g.width/2-m.width/2;const w=12;k=Math.max(w,Math.min(k,window.innerWidth-m.width-w));let x=g.top-m.height-8;x<w&&(x=g.bottom+8),P(f,k,!0),P(u,x,!0)}Be(()=>{e.visible&&e.target&&t(v)&&requestAnimationFrame(p)});function y(){if(!e.visible||t(T)||!e.target)return;const g=e.target.getBoundingClientRect();g.top>-g.height&&g.bottom<window.innerHeight+g.height?p():e.onclose()}ce(()=>(window.addEventListener("scroll",y,{passive:!0}),()=>window.removeEventListener("scroll",y)));var A=he(),S=ee(A);{var D=g=>{var m=ft();let k;m.__keydown=M=>{M.key==="Escape"&&e.onclose()};var w=r(m),x=r(w),R=r(x,!0);a(x);var F=I(x);a(w);var j=I(w,2);{var N=M=>{var W=vt(),d=r(W,!0);a(W),L(()=>G(d,e.source)),c(M,W)};C(j,M=>{e.source&&M(N)})}a(m),we(m,M=>P(v,M),()=>t(v)),L(()=>{k=Z(m,1,"ev-popover svelte-ep7riq",null,k,{mobile:t(T)}),H(m,"data-level",e.level),fe(m,t(T)?"":`left: ${t(f)}px; top: ${t(u)}px;`),G(R,h[e.level]),G(F,` ${l[e.level]??""}`)}),c(g,m)};C(S,g=>{e.visible&&g(D)})}c(i,A),Y()}be(["keydown"]);var wt=b('<nav class="article-back svelte-wdxtx4"><a class="svelte-wdxtx4">&larr; docs</a></nav>'),bt=b('<div class="article-layout svelte-wdxtx4"><article class="library-prose svelte-wdxtx4"><nav class="article-breadcrumb svelte-wdxtx4"><a class="svelte-wdxtx4">docs</a></nav> <!> <!></article> <aside class="article-sidebar svelte-wdxtx4"><!></aside></div> <!>',1);function Tt(i,e){J(e,!0);let l=E(me([])),h=E(me(e.metadata?.title||"")),f=E(void 0),u=E(null),T=E("moderate"),v=E(""),p=E(!1);function y(d){return d.classList.contains("ev-strong")?"strong":d.classList.contains("ev-moderate")?"moderate":d.classList.contains("ev-weak")?"weak":d.classList.contains("ev-speculative")?"speculative":"moderate"}function A(d){P(u,d,!0),P(T,y(d),!0),P(v,d.getAttribute("title")||"",!0),P(p,!0),d.removeAttribute("title"),d.dataset.title=t(v)}function S(){t(u)&&t(u).dataset.title&&(t(u).setAttribute("title",t(u).dataset.title),delete t(u).dataset.title),P(p,!1),P(u,null)}ce(()=>{if(!t(f))return;e.slug&&$.markVisited(e.slug);const d=t(f).querySelector("h1");d&&!t(h)&&P(h,d.textContent||"",!0);const O=t(f).querySelectorAll("h2, h3");P(l,Array.from(O).map(o=>({id:o.id,text:o.textContent||"",level:parseInt(o.tagName[1])})),!0),t(f).querySelectorAll(".ev").forEach(o=>{o.setAttribute("tabindex","0"),o.setAttribute("role","note");const _=o.getAttribute("title");_&&o.setAttribute("aria-label",`Evidence: ${_}`),o.addEventListener("click",q=>{q.stopPropagation(),t(p)&&t(u)===o?S():A(o)}),o.addEventListener("keydown",q=>{(q.key==="Enter"||q.key===" ")&&(q.preventDefault(),t(p)&&t(u)===o?S():A(o))})});function n(o){if(!t(p))return;const _=o.target;_.closest(".ev")||_.closest(".ev-popover")||S()}function s(o){o.key==="Escape"&&t(p)&&S()}return document.addEventListener("click",n),document.addEventListener("keydown",s),()=>{document.removeEventListener("click",n),document.removeEventListener("keydown",s)}});var D=bt();Ge("wdxtx4",d=>{De(()=>{He.title=`${(t(h)||"Article")??""} — cix Docs`})});var g=ee(D),m=r(g),k=r(m),w=r(k);a(k);var x=I(k,2);Ne(x,{get md(){return e.content},get plugins(){return We}});var R=I(x,2);{var F=d=>{gt(d,{get slug(){return e.slug},get entry(){return e.entry},get prev(){return e.prev},get next(){return e.next},get position(){return e.position},get total(){return e.total}})},j=d=>{var O=wt(),V=r(O);a(O),L(()=>H(V,"href",`${K??""}/docs`)),c(d,O)};C(R,d=>{e.slug?d(F):d(j,!1)})}a(m),we(m,d=>P(f,d),()=>t(f));var N=I(m,2),M=r(N);at(M,{get headings(){return t(l)}}),a(N),a(g);var W=I(g,2);yt(W,{get target(){return t(u)},get level(){return t(T)},get source(){return t(v)},get visible(){return t(p)},onclose:S}),L(()=>H(w,"href",`${K??""}/docs`)),c(i,D),Y()}function Ht(i,e){J(e,!0),Tt(i,{get slug(){return e.data.slug},get entry(){return e.data.entry},get content(){return e.data.content},get metadata(){return e.data.metadata},get position(){return e.data.position},get total(){return e.data.total},get prev(){return e.data.prev},get next(){return e.data.next}}),Y()}export{Ht as component,Dt as universal};
