# Same Tool. Different Design.

Approximately 1,000 Turkish high school students. One school. One school year. The same GPT-4 model under both conditions. Two different designs sitting on top of it.

GPT Base worked like standard ChatGPT: ask a question, get an answer. Ask for a solution to a math problem, receive the solution.

GPT Tutor used guardrails based on teacher input. When students asked for the solution, they got a hint designed to help them make progress toward finding it themselves.

During practice sessions: GPT Base students improved 48% over the control group. GPT Tutor students improved 127%. Both conditions outperformed control. Both used GPT-4.

On the unassisted exam afterward: GPT Base students scored 17% below the control group. Students who never had AI access performed better. GPT Tutor students showed no significant difference from control.

Same tool. Different behavior. One produced a large gain that erased itself. The other produced an even larger gain that didn't.

Harm is a design variable.

([Bastani et al. 2025](/docs/bibliography#bastani-2025), PNAS)

<chart id="bastani-split"></chart>

---

## Keeping the Gap Open

The guardrail didn't change what GPT-4 knew. It changed what GPT-4 would do with a request for an answer.

The hint — specifically teacher-designed to prompt the student toward the next step without completing it — kept the cognitive gap open. The student still had to work through the resolution. The learning happened because the tool required it to.

GPT Base students "attempt to use GPT-4 as a 'crutch' by asking for and copying solutions," in the Bastani paper's phrasing. They did not perceive any reduction in their learning as a consequence. The exam was the only measure they didn't get to see before the damage was done.

The generative step is the encoding event. When you form an answer — work through the reasoning, construct the solution — that process encodes understanding. GPT Base closed the gap. The student received the answer and encoded nothing. GPT Tutor kept the gap open. The student had to cross it.

Same tool. Same knowledge. Different gate on what it would hand over.

---

## Feature by Feature

The Bastani experiment shows what different designs do to outcomes. It doesn't decompose which specific feature does the work. That's what [Blaurock et al.](/docs/bibliography#blaurock-2025) measured directly.

Marah [Blaurock, Marion Büttgen, and Jeroen Schepers](/docs/bibliography#blaurock-2025) ran two scenario-based experiments with financial services employees and HR professionals in Europe — 309 participants in Study 1, 345 in Study 2. They defined five features that characterize a collaborative intelligence system: engagement, transparency, process control, outcome control, and reciprocal strength enhancement. Then they isolated each feature's independent effect on employee outcomes ([Blaurock et al. 2025](/docs/bibliography#blaurock-2025), Journal of Service Research).

Their Study 2 results on perceived outcome responsibility — the degree to which employees feel ownership of the jointly produced work — show the hierarchy:

- Process control: b=0.715 (p<.001)
- Outcome control: b=0.524 (p<.011)
- Transparency: b=0.511 (p<.001)
- Engagement: b=0.090 (not significant)

<chart id="design-lever-hierarchy"></chart>

Process control means the user can influence what data the system considers and the rules by which it generates output. Outcome control means the user can appeal or modify the final decision after it's produced. Together they say: the human's judgment is indispensable by design, not just consulted.

The engagement feature — proactive prompting, soliciting feedback at decision points, asking for the user's opinion — produced no significant effect on any of the four outcomes measured. Not on perceived service improvement. Not on outcome responsibility. Not on threat to meaning of work. Not on adherence to the system. All four engagement hypotheses were rejected.

This follows from the mechanism. A system that asks "do you agree with this recommendation?" before proceeding can produce the checkbox behavior without the cognitive work. The user registers a preference. Whether the generative step happened — whether they formed their own judgment, traced the reasoning, produced an evaluation — is not determined by the prompt.

Process control and outcome control work differently. When you can modify the parameters and override the decision, the recommendation is not the endpoint — it's the input to your judgment. The authority to override is also the responsibility to evaluate. These features make passive acceptance structurally harder.

Control features require evaluation. Engagement features only prompt for it.

Transparency ranked third at b=0.511, a real effect. But [Bansal et al.'s](/docs/bibliography#bansal-2021) work (CHI 2021) documented a complication — AI explanations increase acceptance of recommendations regardless of whether those recommendations are correct, improving accuracy when the AI is right and decreasing it when the AI errs. Transparency that surfaces what the system considered creates an entry point for evaluation. Transparency that presents a polished rationale for a conclusion already reached can substitute for evaluation. The Blaurock number doesn't distinguish between them.

---

## What the User Brings

Blaurock isolates what system features do. [Pallant et al.](/docs/bibliography#pallant-2025) measured what happens when users bring different orientations to the same tools.

In a qualitative content analysis of 192 student reflections, students using GenAI in a mastery-oriented way — constructing and augmenting knowledge rather than asking for and copying output — were 35.782 times more likely to demonstrate critical thinking (OR=35.782, p<0.001) ([Pallant et al. 2025](/docs/bibliography#pallant-2025), Studies in Higher Education).

35.782 is odds-ratio territory — the gap between the two groups is categorical. Students who used AI to figure things out were not slightly more likely to think critically. They were in a qualitatively different relationship with the work.

Same tool. Different orientation. A 35-fold difference in the probability of critical thinking.

[Shen and Tamkin's](/docs/bibliography#shen-2026) six interaction patterns show the same distinction from the developer's side. Generation-Then-Comprehension — generate code with AI, then ask understanding-focused questions about it — produced 86% quiz scores. AI Delegation — ask AI, paste answer — produced 39% ([Shen & Tamkin 2026](/docs/bibliography#shen-2026), arXiv). Same tool. Different interaction pattern. The AI's behavior was identical. The developer's was not.

The [Umarova et al.](/docs/bibliography#umarova-2025) finding at Cornell makes the limits precise: "Students who proactively explored ideas gained new ideas from writing, regardless of whether they used auto-complete or Socratic AI assistants. Those who engaged in prolonged, mindless copyediting developed few ideas even with a Socratic AI" ([Umarova et al. 2025](/docs/bibliography#umarova-2025), Cornell).

A Socratic AI — explicitly designed to ask questions rather than give answers — didn't help students who were in the wrong mode. They used it for copyediting. The tool provided the prompting. They ignored it. Design can create conditions for cognitive engagement. It cannot guarantee the human is in the mode required to use them. What it can do is make passive acceptance structurally harder — which is what process control and outcome control accomplish by giving the human authority over input and output.

---

## No One Chose This

The individual cannot solve this part.

Anil [Doshi and Oliver Hauser](/docs/bibliography#doshi-2024) ran a preregistered experiment in 2024 with 893 short story writers. Writers given access to generative AI ideas produced stories rated 8.1% more novel than writers without AI (b=0.311, p<0.001). The AI helped. Individually, measurably ([Doshi & Hauser 2024](/docs/bibliography#doshi-2024), Science Advances).

Then they measured something else: how similar were the AI-assisted stories to each other, compared to how similar the unaided stories were to each other?

Stories written with one generative AI idea were 10.7% more similar to each other than unaided stories.

Better individually. More alike collectively. The authors called it a social dilemma: "With generative AI, writers are individually better off, but collectively a narrower scope of novel content is produced."

Consider what this looks like from the inside. Someone at Microsoft Research gave GPT-4 the opening of a Franz Kafka short story — the narrator, lost in an unfamiliar city, asks a policeman for directions — and asked GPT-4 to complete it 100 times. In Kafka's original, the policeman says "Give it up!" and turns away. In 50 of GPT-4's 100 completions, the policeman directs the narrator to take the second left. In 16 of the 100, a bakery appears as a landmark ([Xu et al. 2025](/docs/bibliography#xu-2025), PNAS). Human-written completions stayed unique. The LLM completions converged. Not toward bad writing. Toward the same writing.

Each writer in the Doshi and Hauser experiment made a rational decision. Each writer's story improved. No one chose convergence. It emerged from individually rational choices.

This pattern holds at larger scale. Niklas [Holzner, Sebastian Maier, and Stefan Feuerriegel](/docs/bibliography#holzner-2025) aggregated 28 studies measuring this effect across 8,214 participants. Individual creative performance: Hedges' g=+0.273 (95% CI: [0.018, 0.528], p=0.036). Idea diversity: Hedges' g=-0.863 (95% CI: [-1.328, -0.398], p<0.001). The leave-one-out sensitivity analysis kept the diversity estimate between g=-0.655 and g=-0.952 across all iterations — every confidence interval excluded zero ([Holzner et al. 2025](/docs/bibliography#holzner-2025), arXiv).

Better writers. Fewer distinct ideas. Both at once, across every study in the meta-analysis.

<chart id="diversity-paradox"></chart>

The homogenization is structural. Give 70+ language models the same prompt — "Write a metaphor about time" — and they form two clusters. Almost every model produces some version of "time is a river." Many produce "time is a weaver." GPT-4o, Qwen2.5, phi-4, GPT-4o-mini, and Mixtral all reached for the river independently. Sentence embedding similarities between responses from different models: 71–82% ([Jiang et al. 2025](/docs/bibliography#jiang-2025), NeurIPS).

The convergence is baked into training. RLHF — reinforcement learning from human feedback — optimizes models to maximize human preference ratings. Human preference ratings favor coherent, recognizable outputs. The uncommon metaphor, the surprising story direction, the architectural choice that runs against convention: these score lower in quick preference ratings, not because they're wrong, but because they're unexpected. Kafka's policeman saying "Give it up!" and turning away scored lower than the policeman who gives directions. Not by any literary measure — by annotation, in bulk, responding to what most people would prefer. The reward signal learned the second left. The bakery.

---

## When Outputs Re-Enter Training

The homogenization of AI-assisted output would be a bounded problem if those outputs stayed at the edges of the system. They don't.

Ilia [Shumailov et al.](/docs/bibliography#shumailov-2024) demonstrated in 2024 that training generative models on model-generated content causes model collapse — a degenerative process in which models progressively lose the tails of the original data distribution. Rare content disappears first. The architectural choice no one else would try. The metaphor that no annotation session would reward. The Kafka ending that stayed unique in every human-written story but appeared zero times in a hundred GPT-4 completions. Late-stage collapse: the model converges toward a distribution with very small variance. The paper states explicitly this causes "irreversible defects" ([Shumailov et al. 2024](/docs/bibliography#shumailov-2024), Nature).

The collapse threshold is lower than you'd expect. [Dohmatob et al.](/docs/bibliography#dohmatob-2025) demonstrated in a theoretical analysis of supervised linear regression that "even the smallest fraction of synthetic data (e.g., as little as 1% of the total training dataset) can still lead to model collapse: larger and larger training sets do not enhance performance." The result is mathematical, not yet demonstrated in production LLM training — but the direction is clear, and: "larger models can amplify model collapse" ([Dohmatob et al. 2025](/docs/bibliography#dohmatob-2025), ICLR).

There is an escape condition. [Gerstgrasser et al.](/docs/bibliography#gerstgrasser-2024) found that replacing real data with synthetic causes inevitable collapse, with test error growing unboundedly. Accumulating synthetic data alongside real data avoids it — the mathematical result gives a finite upper bound on test error independent of the number of iterations ([Gerstgrasser et al. 2024](/docs/bibliography#gerstgrasser-2024), arXiv). The escape requires real human data to keep accumulating.

The collapse mechanism is not that human output degrades in quality. It is that human output is replaced by AI output. Degradation would still leave human-generated content in the training pool. Replacement removes it. The Gerstgrasser escape condition depends on real human data continuing to accumulate — which it cannot do if substitutive AI use is replacing human generation, not supplementing it.

If you use AI to explore an architectural question, draft options for a design decision, or hand off analysis you could have done yourself — you are making the individually rational choice. So is every other developer on your team and every team using the same tools. The aggregate produces a corpus of AI-shaped outputs. That corpus re-enters training data. The next generation of models trains on it. The tails disappear. Each generation amplifies the loss.

No one is doing anything wrong. The convergence emerges from individually rational behavior across an industry. That is what makes it a design problem — not a discipline problem, not a personal failing, but a question of what the tools are structured to produce.

---

## Where the Evidence Stops

The argument above assembles three separate research literatures into a chain. Each link has independent support. The chain as an integrated phenomenon has not been measured in a single study.

The Bastani field experiment is strong evidence: randomized, field-based, n~1,000, one full school year, measured on an unassisted exam. The Blaurock feature hierarchy comes from scenario-based experiments with workplace professionals — controlled, but not field conditions. The Pallant odds ratio (35.782) comes from qualitative content analysis of student reflections, not a randomized trial; the direction is clear, the magnitude requires caution. The Holzner meta-analysis covers 28 studies but with I² exceeding 78%, indicating substantial heterogeneity.

The homogenization to collapse chain is the most uncertain stretch. Each link — AI outputs are more homogeneous than human outputs; AI-generated content in training causes collapse; 1% synthetic contamination is sufficient to trigger it; the escape requires accumulating real human data — is supported by independent evidence. That those links form a closed loop in practice, at the scale and timescale implied, has not been demonstrated as an integrated phenomenon. The inference is logical. It is not yet empirical.

One finding from Blaurock that complicates the design prescription: the control features that help novices showed no significant positive effects for AI-experienced users (n=42 in post-hoc analysis). For that subset, the engagement feature showed a significant negative effect on perceived service improvement. Design features that make collaboration legible to someone new to AI-assisted workflows can become friction for someone who has already internalized the workflow. What works for a novice may not work, and may actively hinder, an expert.

The claim this evidence supports: same tool, different design, measurably different outcomes. No single design prescription is permanent. Which design features change it, and for whom, is partially measured. Whether those effects hold as users develop expertise is not.

The design question — how to keep the human in the loop by design, give them authority over process and outcome, build in the understanding before the answer — has evidence behind it. The same system may need to adapt as its users do. But the alternative, the default, already has its own evidence. -17% on an exam, measured against students who never had AI at all.

