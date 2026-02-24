# The Paradox

Before the study ended, METR researchers asked the 16 developers to estimate how much AI had
affected their completion time. They said it made them 20% faster.

It had actually made them 19% slower.

That 39-percentage-point gap — between what developers believed afterward and what happened — is
the cleanest demonstration of the problem. Before the tasks even began, the developers had predicted
AI would make them 24% faster. The gap between prediction and reality was 43 percentage points. Not because the developers were foolish. They were experienced
open-source contributors, each with an average of five years on the specific repository they were
working in. They were using the best available AI tools (Cursor Pro with Claude 3.5/3.7). They had
tens to hundreds of hours of prior LLM experience. And when the study was over, they still
thought the AI had helped. [Solid — Becker/METR 2025, S17, n=16, arXiv preprint.]

The perception gap is the first part of the paradox. The second part is harder — and it lives
one level deeper than productivity.

---

## The Gain Is Real

Three randomized controlled trials at Microsoft, Accenture, and an anonymous Fortune 100
electronics company. Combined sample: 4,867 software developers. Result: developers using GitHub
Copilot completed 26% more tasks per week than those without it. Less experienced developers
benefited more — both in adoption rate and magnitude of productivity gain. [Solid — Cui et al. 2024,
S18, three RCTs, SSRN working paper.]

This is not a survey or an estimate. It is measured task completion with random assignment, run
by the companies themselves as part of ordinary business decisions about whether to adopt the
technology. The 26% figure is a local average treatment effect for actual adopters — the gain
for developers who used the tool, not the full population including those who used it minimally.

The productivity gain is real, consistent across three experiments, and larger for developers
earlier in their careers. Any honest account includes it.

---

## The Two Studies in Tension

The METR study (S17) and the Cui et al. study (S18) seem to contradict each other. One shows +26%.
The other shows -19%. Both are RCTs.

They are not measuring the same thing in the same population. The Cui study ran in corporate settings
with mixed-experience teams using an autocomplete-style Copilot (the 2022-2023 version) on
assigned tasks. The METR study ran in 2025, used frontier agentic AI (Cursor Pro + Claude 3.7), and
recruited experienced contributors working on their own mature codebases — projects with 23,000
stars on average, where the developers had made over 1,500 commits each.

Both studies also found the same directional pattern on experience: AI benefits less experienced
workers more. The Cui study finds this explicitly across their three experiments. The METR study
recruited experienced developers precisely because the experienced-developer case
was understudied. [Solid — S18 and S17 both establish experience gradient.]

The most plausible reconciliation: AI helps on unfamiliar ground, hurts on familiar ground. [Assumed —
this is the inference from both findings read together; no single study tests this directly.] This is
not the same as saying AI doesn't work. It is saying the gain is conditional — and the condition
is something worth knowing.

Even within the METR study, the perception gap is the most striking finding. Economists forecast
the AI would speed developers by 39%. ML researchers forecast 38%. Every expert group predicted
speedup. Every developer, before and after the study, believed speedup. The direction of prediction
was unanimous and wrong. [Solid — Becker/METR 2025, S17.]

---

## The Harm Is Also Real

A different research team ran a different kind of study. Judy Shen and Alex Tamkin at Anthropic
gave 52 crowd-sourced developers a task using a new asynchronous Python library (Trio) that
none of them had used before. Half got access to an AI assistant. Half did not.

Afterward, both groups took a knowledge quiz. The AI-assisted group scored 17% lower. Cohen's
d = 0.738 — a medium-to-large effect. The p-value was 0.010. And the AI group did not even
complete the task faster: the time difference was not statistically significant (p=0.391). [Solid —
Shen & Tamkin 2026, S1, n=52 RCT, arXiv preprint. Single domain, crowd-sourced participants,
35-minute task — controlled study limitations.]

The group that struggled without AI — encountering errors, debugging without assistance —
learned more. The group that used AI to complete the task faster (or tried to) didn't learn the library.

This is the second part of the paradox. Not that AI is unproductive. It's that the productivity gain
and the learning harm can coexist — and the conditions that produce the gain are the same conditions
that produce the harm.

---

## The Paradox Has Structure

The Bastani et al. study at PNAS shows the structure most clearly. Nearly 1,000 high school students
in Turkey were given access to GPT-4 tutors during math practice sessions. Two designs: GPT Base
(unconstrained, like standard ChatGPT) and GPT Tutor (guardrails that gave hints instead of answers).

During practice:
- GPT Base: +48% improvement
- GPT Tutor: +127% improvement
- Both AI groups outperformed control

On the unassisted exam afterward:
- GPT Base: **-17%** vs control (statistically significant)
- GPT Tutor: no significant difference from control
[Solid — Bastani et al. 2025, S2, n~1,000 field experiment, PNAS peer-reviewed.]

The same tool. Different design. One version delivered a large in-the-moment gain and erased it
afterward. The other delivered an even larger in-the-moment gain without the erasure.

And the students using GPT Base did not notice: "students often use GPT Base as a 'crutch' by
asking for and copying solutions... they do not perceive any reduction in their learning or subsequent
performance as a consequence of copying solutions." [Solid — Bastani et al. 2025, S2.]

The perception gap doesn't belong only to the METR developers. It is structural. When AI absorbs
a task, the person who handed it over doesn't feel the atrophy. They feel the completion.

---

## Why the Gap Exists

The control group in the Shen/Tamkin study scored higher not because they were smarter, or more
motivated, or had better documentation. They scored higher because they encountered more errors.

The METR screen recordings document how AI-assisted developers spent their time: when AI was
allowed, developers spent less time actively coding and more time prompting AI, waiting on and
reviewing AI outputs. The developers were still working. They just weren't doing the work that
builds understanding.

This is not a bug in the AI. It is the function of the AI working correctly.

When a developer hits an unfamiliar async pattern and has to figure out why their code is hanging —
consult the docs, form a hypothesis, test it, fail, form another — that sequence of error and resolution
is the encoding event. The concept enters memory because the brain had to work to construct it.
The generation effect, documented since Slamecka and Graf in 1978, shows that self-generated
information is retained approximately 22% better than passively received information. [Foundational —
Slamecka & Graf 1978, S32, not in paper collection; cite from bibliography.]

AI gives the resolution before the error has had time to encode anything. The answer arrives before
the question has finished forming. The cognitive gap — the space between encountering a problem
and resolving it — is where learning lives. AI closes the gap.

**The learning happens in the gap. AI closes the gap. That is the mechanism.**

This is why Bereiter and Scardamalia's 1987 distinction between knowledge telling and knowledge
transforming matters for any AI collaboration involving prose or ideas: expert writing is a recursive
process that generates new understanding through the act of composition. AI-generated prose
arrives pre-resolved — the writer never had to form the thought. [Foundational — Bereiter &
Scardamalia 1987, S33, not in paper collection; cite from bibliography.]

---

## What Engagement Changes

Shen and Tamkin identified six distinct interaction patterns among the AI-assisted developers in their
study. Three preserved learning. Three did not.

The three that harmed learning shared a structure: the developer handed the task to the AI. Not out
of laziness — out of efficiency. Ask AI to generate code, paste it as answer (AI Delegation: 39% quiz
score). Start with questions, delegate by the end (Progressive AI Reliance: 35%). Use AI to verify
and troubleshoot, 5-15 queries (Iterative AI Debugging: 24%). [Solid — S1, qualitative typology;
pattern groups n=2-6 each (Generation-Then-Comprehension n=2), small clusters.] Each pattern, from inside, looks like competent tool use.
The developer is engaged. They are questioning the AI, iterating, checking the output. What they are
not doing is forming the resolution themselves.

The three that preserved learning shared a different structure: the developer used AI as a reference
while remaining cognitively engaged. Generation-Then-Comprehension (generate code with AI, then
ask understanding-focused questions: **86%** quiz score). Hybrid Code-Explanation (mix generation
and explanation queries: 68%). Conceptual Inquiry (ask only conceptual questions, resolve errors
independently: 65%). [Solid — S1, same caveats.]

The gap between 86% and 24% is not a gap between smart and careless developers. It is a gap in
who was doing the cognitive work. The Generation-Then-Comprehension pattern generated code with
AI — that part is identical to delegation — but then asked understanding-focused questions afterward.
The critical step was not what the AI did. It was what happened after the AI did it.

The Pallant et al. study in higher education quantified this gap from a different direction. Using
qualitative content analysis of 192 student reflections (Studies in Higher Education), they found
that students using GenAI in a mastery-oriented way — constructing and augmenting knowledge
rather than regurgitating AI output — were 35.782 times more likely to demonstrate critical thinking
(OR=35.782, p<0.001). [Probable — Pallant et al. 2025, S4, QCA design, not RCT; self-selection possible.]

The same tool. Radically different outcomes depending on whether the human remained in the loop
as a learner, or exited the loop as a delegator.

---

## The Evidence in Medicine

The medical literature provides the clearest view of what long-term skill exposure looks like
in practice — because medicine has been studying this longer, and because the outcome (adenoma
detection rate) is an objective clinical measure.

Budzyń et al. studied 19 endoscopists across four Polish hospitals as AI polyp detection was
introduced. They compared three months of colonoscopies before and three months after AI exposure
— but specifically studied performance on non-AI-assisted procedures. Before AI: adenoma detection
rate of 28.4%. After three months with AI: 22.4%. Absolute decline: 6.0 percentage points.
Relative decline: 21%. [Solid — Budzyń et al. 2025, S14, n=1,443, Lancet. Observational — cannot
definitively establish causation. Other explanations cannot be ruled out.]

This is not a controlled experiment. Confounds exist. But the pattern is consistent with every
controlled study: skill practiced through automation instead of direct performance atrophies.

Natali et al. draw the distinction between two threats: deskilling (the degradation of skills that
experts already have, from reduced practice) and "upskilling inhibition" — the suppression of
opportunities for trainees and novices to develop skills in the first place, when AI consistently
provides the answer before the learner can attempt the problem. [Probable — Natali et al. 2025,
S16, mixed review; conceptual distinction, not primary empirical finding.]

Both threats operate simultaneously. Experts lose what they have. Novices never develop it.
The "never-skilled" population is harder to identify than the "deskilled" one — there is no prior
baseline to compare against. But the mechanism is the same: the cognitive gap was closed before
learning could happen.

---

## The Critical Gap in the Developer Evidence

The research literature contains no longitudinal study measuring developer capability — not task
performance, but capability — after extended AI use without AI access.

The Shen/Tamkin study is 35 minutes. The Budzyń study is 3 months and observational. The Bastani
study is the most rigorous but involves high school students learning math, not professional software
developers learning their craft over months and years.

This gap matters. The research establishes the mechanism — cognitive offloading reduces skill
formation in controlled settings. It establishes the pattern in medicine — real-world skill decline
follows AI adoption. It does not establish, empirically, what happens to a software developer's
fundamental capability after two years of AI-assisted coding.

The honest claim is not "we know developer capability declines." The honest claim is: every mechanism
we understand, and every parallel domain we have studied, points in the same direction. And the
perception evidence (developers who cannot detect a 43-point gap between predicted and actual
productivity) suggests that if the decline is happening, we would not be able to see it from inside
our own experience. [Solid — METR gap; Solid — PNAS students didn't perceive harm. Gap statement
itself: confirmed in cluster synthesis and ground truth.]

---

## What This Means for Who Uses AI

The Cui data shows that less experienced developers gain more from AI tools. The METR data shows
that highly experienced developers on real work may gain nothing, and may lose time. Both studies
find the same experience gradient.

The Liang survey of 410 developers at ICSE 2024 shows what developers actually use AI for:
reducing keystrokes, finishing fast, recalling syntax. Not brainstorming. Not architectural reasoning.
Not working through a design problem. The primary barrier to adoption is control — developers
can't get the tool to generate what they want. [Solid — Liang et al. 2024, S19, n=410, ICSE.]

These are the conditions that maximize productivity gain and, if the mechanism generalizes, maximize
skill harm. The less experienced developer who uses AI to recall syntax and avoid errors is the
developer gaining the most from the tool and potentially offloading the most practice.

This is the paradox's sharpest form: the developers who benefit most from AI adoption are also
the developers whose skill formation is most at risk from it. The gain is largest for the people
most in the learning phase of their career. The harm mechanism is strongest for people in the
learning phase of their career.

---

## What the Paradox Is Not

The paradox is not: "AI is bad." The productivity gains are real and large. For developers early
in their careers, on assigned tasks, using autocomplete-style tools: the evidence says they complete
more work.

The paradox is not: "The productivity gains are fake." The gain in tasks completed is real. Whether
that translates to better software — fewer bugs, better architecture, lower maintenance burden —
is a separate question that neither the Cui study nor any other study in this cluster measures.

The paradox is: the same engagement model that produces the immediate gain also produces the
downstream cost. Using AI to handle what you would otherwise have to figure out is exactly what
delivers the +26% and exactly what atrophies the capability you would have built by figuring it out.

The design of the interaction determines which you get. And the default design — give me the
answer — optimizes for the gain and produces the harm. The developer who finished the task, closed
the ticket, and moved on to the next one may have learned less about their own codebase than the
developer who spent an extra hour stuck. That's not a small observation — it's a description of how
most AI-assisted development actually goes, most days. What it means for a developer's capability
a year from now is the question the research has not yet answered.
