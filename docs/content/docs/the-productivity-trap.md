# The Productivity Trap

Before the study ended, METR researchers asked the 16 developers to estimate how much AI had affected their completion time. They said it made them 20% faster.

It had actually made them 19% slower.

Before the tasks even began, those same developers had predicted AI would make them 24% faster. The gap between prediction and reality was 43 percentage points — not because the developers were careless or naive. They were experienced open-source contributors, average five years on the specific repository they were working in, tens to hundreds of hours of prior LLM experience, using the best available tools: Cursor Pro with Claude 3.5 and 3.7. Every expert group consulted — economists, ML researchers — predicted speedup. The direction of prediction was unanimous and wrong. And when the study was over, they still thought the AI had helped ([Becker et al. 2025](/docs/bibliography#becker-2025)).

That perception gap is the first part of the problem. The second part lives one level deeper.

---

Three randomized controlled trials at Microsoft, Accenture, and an anonymous Fortune 100 electronics company. Combined sample: 4,867 software developers. Result: developers who adopted GitHub Copilot completed 26% more tasks per week than those without it — a local average treatment effect, measuring the gain among those who actually used the tool. Less experienced developers benefited more, in both adoption rate and magnitude of gain ([Cui et al. 2024](/docs/bibliography#cui-2024), SSRN). These are not estimates or surveys. Random assignment, measured task completion.

So: one study shows +26%. Another shows -19%. Both are RCTs. They are not measuring the same thing in the same population — the Cui study used corporate settings with mixed-experience teams on assigned tasks; the METR study used experienced contributors working on their own mature codebases, with frontier agentic AI. Both found the same directional pattern: AI benefits less experienced workers more. The most plausible reconciliation is also the most important thing to understand about this technology: **AI helps on unfamiliar ground, hurts on familiar ground.**

The harm has its own evidence.

---

## The Learning Tax

Judy Shen and Alex Tamkin at Anthropic gave 52 crowd-sourced developers a task using a new asynchronous Python library that none of them had used before. Half got access to an AI assistant. Half did not. Afterward, both groups took a knowledge quiz.

The AI-assisted group scored 17% lower. Cohen's d = 0.738 — a medium-to-large effect. p = 0.010. And the AI group did not complete the task any faster: the time difference was not statistically significant (p = 0.391) ([Shen & Tamkin 2026](/docs/bibliography#shen-2026), arXiv).

The group that had to struggle without AI — encountering errors, debugging without assistance — learned more. The group that used AI to solve the task didn't learn the library. They also didn't finish faster. They paid the learning tax without getting the productivity gain.

The [Bastani et al.](/docs/bibliography#bastani-2025) study at PNAS puts a sharper edge on this. Nearly 1,000 high school students in Turkey were given access to GPT-4 tutors during math practice. Two designs: GPT Base (unconstrained, like standard ChatGPT) and GPT Tutor (guardrails that gave hints instead of answers).

During practice:
- GPT Base: +48% improvement
- GPT Tutor: +127% improvement
- Both AI groups outperformed control

On the unassisted exam afterward:
- GPT Base: **-17% vs control** (statistically significant)
- GPT Tutor: no significant difference from control

([Bastani et al. 2025](/docs/bibliography#bastani-2025), PNAS)

The same tool. Different design. GPT Base delivered a large in-the-moment gain and erased it afterward. GPT Tutor delivered an even larger in-the-moment gain without the erasure. And the students using GPT Base did not notice: they "do not perceive any reduction in their learning or subsequent performance as a consequence of copying solutions" ([Bastani et al. 2025](/docs/bibliography#bastani-2025), PNAS).

The perception gap from the METR study is structural. When AI absorbs a task, the person who handed it over feels the completion — not the atrophy.

---

## Why the Gap Exists

The Shen/Tamkin control group scored higher not because they were smarter, or more motivated, or had better documentation. They scored higher because they encountered more errors.

Here is what the METR screen recordings showed: when AI was allowed, developers spent less time actively coding and more time prompting AI, waiting on and reviewing AI outputs. They were still working. They just weren't doing the work that builds understanding.

The AI is functioning correctly. If you've spent an afternoon prompting and reviewing AI output — productive, efficient, done by five — and realized the next morning you can't reconstruct how the solution works, you've already met the mechanism.

When a developer hits an unfamiliar async pattern and has to figure out why their code is hanging — consult the docs, form a hypothesis, test it, fail, form another — that sequence of error and resolution is the encoding event. The concept enters memory because the brain had to work to construct it. [Slamecka and Graf](/docs/bibliography#slamecka-1978) documented this: people retain self-generated information roughly 22% better than information they receive passively ([Slamecka & Graf 1978](/docs/bibliography#slamecka-1978)).

AI gives the resolution before the error has had time to encode anything. The answer arrives before the question has finished forming. The cognitive gap — the space between encountering a problem and resolving it — is where learning lives. **AI closes the gap. That is the mechanism.**

The note-taking study makes this concrete. [Chen et al.](/docs/bibliography#chen-2025) at PACMHCI 2025 asked 30 people to take notes on lecture videos under three conditions each (within-subject, counterbalanced): full automation (AI organized and formatted the content), intermediate assistance (real-time AI summaries), and minimal assistance (transcript only). The automated group found the experience easiest. When asked which setup they preferred, they chose the AI-organized notes. They also scored lowest on the post-test.

Note-taking has two functions. The obvious one is storage — you're creating a reference. The less obvious one is encoding: selecting what to write down, deciding how to frame it, connecting it to what you already know — that *is* the comprehension process. You don't take notes to capture what you understand; you take notes in order to understand. When AI takes the notes for you, the storage function is served. The encoding function is not. The quality of the artifact and the quality of the learning are inversely related when the AI provides the artifact.

This applies to writing as much as to code. [Bereiter and Scardamalia](/docs/bibliography#bereiter-1987) distinguished in 1987 between knowledge telling (direct retrieval of what you know) and knowledge transforming (recursive engagement between content and argument that generates new understanding through composition). Expert writers transform. AI-generated prose arrives pre-resolved — the writer never had to form the thought, shuttle between content and claim, decide what to say. The output is complete. The thinking that would have happened through writing did not happen ([Bereiter & Scardamalia 1987](/docs/bibliography#bereiter-1987)).

[Kosmyna et al.](/docs/bibliography#kosmyna-2025) at MIT ran 54 participants through essay-writing sessions: one group using an LLM, one using a search engine, one using only their own resources. At the end of Session 1, researchers asked one question: can you quote anything from the essay you just wrote?

In the brain-only group, 16 of 18 participants could. In the LLM group, 15 of 18 could not — 83.3% failed to quote anything from an essay they had written minutes before. The EEG methodology in that study is disputed and the authors themselves treat the neural results as preliminary ([Kosmyna et al. 2025](/docs/bibliography#kosmyna-2025), arXiv). The behavioral finding is not a neural interpretation. It is a behavioral fact. They could not recall what they had written because, in a meaningful sense, they had not written it.

---

## Trust Compounds It

[Lee et al.](/docs/bibliography#lee-2025) surveyed 319 knowledge workers across 936 task examples at CHI 2025. For each task, they measured whether critical thinking was enacted and how much cognitive effort it required. Then they modeled what predicts critical thinking.

The strongest predictor was confidence in the AI: β = -0.69 (p < 0.001). The more a worker trusted the AI on a specific task, the less likely they were to think critically about its output ([Lee et al. 2025](/docs/bibliography#lee-2025), CHI).

What you believe about a tool predicts whether you check it. Workers who trusted the AI shifted from doing the work to supervising it. The self-confidence effects run opposite — more self-confidence correlated with more checking — but those effects don't survive the paper's own multiple comparisons correction (Benjamini-Hochberg threshold: p < 0.007). The direction is consistent; the statistical robustness of the magnitude is uncertain. What can be stated: AI confidence and critical thinking move in opposite directions.

Then there is what [Bansal et al.](/docs/bibliography#bansal-2021) found at CHI 2021 (378 citations). They tested whether AI explanations — the kind that show you the AI's reasoning — help humans form better-calibrated trust and make better decisions. Adding explanations increased human acceptance of AI recommendations regardless of whether those recommendations were correct ([Bansal et al. 2021](/docs/bibliography#bansal-2021), CHI).

The intuition behind explainable AI is that if the AI shows its reasoning, humans can catch when the reasoning is wrong. The data says something different. When an AI shows you a clear and internally consistent explanation of its recommendation, you tend to accept the recommendation. The explanation substitutes for checking rather than enabling it. A wrong AI that explains itself confidently is more dangerous than a wrong AI that presents output without explanation. The explanation short-circuits the doubt that would otherwise trigger examination.

**Explanations built to produce transparency are producing trust.**

Plausible AI output arrives. An explanation makes it feel verified. Trust in the AI removes the motivation to check. The checking doesn't happen. The cognitive gap — the space where understanding would have formed — is closed. The skill is not formed. The person does not notice, because the task is done.

The generation effect — [Slamecka & Graf 1978](/docs/bibliography#slamecka-1978), replicated across decades — is the root. The brain does not store what it did not have to work to construct. Trust, transparency, and fluent output are three different paths to the same bypass.

---

## What Remains Unmeasured

There is no longitudinal study measuring developer capability — not task performance, but underlying capability — after extended AI use without AI access. The Shen/Tamkin study is 35 minutes. The Bastani study is the most rigorous evidence on the learning mechanism but involves high school students learning math, not professional developers working on production systems over months and years.

This gap matters and should be stated plainly. The research establishes the mechanism: closing the cognitive gap reduces skill formation in controlled settings. It establishes a parallel-domain pattern: observational evidence from medicine suggests real-world skill decline following AI adoption ([Budzyń et al. 2025](/docs/bibliography#budzyn-2025), Lancet). It does not establish what happens to a software developer's fundamental capability after two years of AI-assisted work.

The honest claim is not "we know developer capability declines." The honest claim is: every mechanism the research documents, and every parallel domain studied, points the same direction. And the METR perception data suggests that if decline is happening, we would not detect it from inside our own experience. The developers who couldn't sense a 43-point gap between their prediction and measured reality are the same developers evaluating whether their own capability is intact.

What the research does establish is the shape of the interaction that determines which outcome you get. Shen and Tamkin's data makes this precise. Developers who received AI-generated code and then asked understanding-focused questions about it — what does this do, why this approach, how does it handle the async case — scored 86% on the knowledge quiz. Developers who delegated to AI without engaging afterward scored 39%. The code was identical. The AI's contribution was identical. The difference was what the developer did after the AI finished.

The productivity gain and the learning harm come from the same behavior: handing the problem to AI instead of working through it. Using AI to handle what you would otherwise have had to figure out is exactly what delivers the +26% and exactly what atrophies the capability you would have built by figuring it out. The default design — give me the answer — optimizes for the gain and produces the harm. The question of what that interaction pattern means for a developer's capability a year from now is the question the research has not yet answered. The mechanism it has measured is precise enough to see which direction the answer points.

