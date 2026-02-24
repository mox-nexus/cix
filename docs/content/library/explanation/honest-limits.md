# Honest Limits

You have read about the paradox, the mechanism, the design lever, the stakes, and what cix
does about it. The evidence for each is real. Now the question worth asking: where should you
stop trusting it?

This article answers that question. Not by undermining what the prior articles established —
the mechanisms are genuine, the effects are measured, the design evidence is the best in the
corpus. But by naming, precisely, what the research has not measured, what claims were
assembled from parallel studies rather than directly tested, and what about cix itself remains
a bet rather than a finding.

An argument that doesn't name its limits isn't stronger for the omission. It is weaker — the
unaddressed gaps return as doubt, and you have no way to locate them. These gaps have edges.
Naming them is what makes the positive claims trustworthy.

The reader who skips this article is in the same position as the METR developers who believed
AI had made them 20% faster when it had made them 19% slower. The perception gap is easiest
to close from inside the argument, when everything lines up. This is the article that lines up
differently.

---

## The Study That Doesn't Exist

The most significant gap in this entire library is also the most relevant to the people it's
written for.

No study has measured developer capability — not task performance, not satisfaction ratings,
but the actual cognitive capability to reason through unfamiliar technical problems without AI —
after extended real-world AI use. Not 35 minutes. Not 10 weeks of math homework. After two
years of AI-assisted professional coding. [Solid — confirmed absent from the research collection. See [The Paradox](the-paradox), "The Critical Gap in the Developer Evidence."]

The closest analogues are:
- Shen & Tamkin (2026): a 35-minute task with a new Python library. One session.
- Bastani et al. (2025): 10 weeks of high school math, with a clean post-withdrawal exam.
  High school students, not professional developers.
- Budzyń et al. (2025): 3-month observational study of endoscopists in Poland, a different
  domain, a different kind of skill, with the observational caveats that entails.

These establish the mechanism. They do not establish what happens to a software developer's
fundamental problem-solving capability after two years of consistent AI delegation. [Solid for
the gap itself; Solid for the mechanism studies; Probable for the medical analogue.]

The honest claim is not "developer capability declines." The honest claim is: every mechanism
the research documents, and every parallel domain studied, points in the same direction. And
the METR perception data — 16 developers who couldn't detect a 43-point gap between predicted
and actual productivity — suggests that if the decline is happening, we would not detect it from
inside our own experience. [Solid — Becker/METR 2025, S17. The 43-point gap is measured directly
within the study.]

This is the gap that matters most to the person reading this article right now. Not a gap in
theory. A gap in measurement of what is happening to you specifically.

---

## Two Claims Assembled From Parallel Studies

The prior articles made two claims the research supports but doesn't demonstrate directly.
Both are well-reasoned. Neither has been directly tested.

**The code/prose distinction**

The full construction of this distinction — how code's verifiability differs from prose's absence of external error signal — is in [The Mechanism](the-mechanism). What follows here is where that distinction's evidence breaks down.

[The Mechanism](the-mechanism) argued that code and prose differ in how AI collaboration affects the generative cognitive
step. Code has an execution trace: you can run it, observe its behavior, catch where your mental
model was wrong. That external error signal makes active comprehension of AI-generated code
a genuine generative step — you are forced to construct and test a mental model. Prose has no
equivalent signal. AI-generated text is internally coherent and plausible; there is no natural
failure point that forces engagement. The Siddiqui et al. correlation (r=0.608 for integrated tool
vs r≈0 for chat-based LLM) and Umarova et al.'s finding that interaction pattern overrides tool
type — these converge on the distinction. So does Shen & Tamkin's finding that
Generation-Then-Comprehension (86%) outperforms AI Delegation (39%) even when the code
was AI-generated.

No single study has placed code comprehension and prose evaluation as paired conditions in
the same experiment. The distinction is assembled from these parallel studies, not demonstrated
directly. [Solid for each individual study; the code/prose distinction itself is an inference from
convergent evidence. See [The Mechanism](the-mechanism), "Why Code and Prose Diverge."]

The boundary is also blurry. Code has execution traces; but architectural decisions, abstract
system design, complex reasoning about performance tradeoffs — these are code-adjacent work
where verifiability may not provide the same natural forcing function. If you built your
understanding of [The Mechanism](the-mechanism) on the code/prose distinction, this limit matters. The distinction is real.
Where exactly it holds — where the verifiability of code provides genuine forcing and where it
breaks down — is not measured.

**The homogenization → collapse chain**

The stakes in [The Stakes](the-stakes) depended on this chain holding together as a sequence: substitutive use
replaces human output with AI-generated output → AI outputs are measurably less diverse than
human outputs → homogenized content accumulates in public training data → future models
trained on that data progressively lose the tails of the distribution.

Each link in this chain has strong independent evidence. Homogenization is established: Holzner
et al.'s meta-analysis of 28 studies (g=-0.863 diversity reduction, n=8,214) [Probable — arXiv
preprint, submitted to ACM CHI, not yet peer-reviewed]; Jiang et al.'s demonstration across
70+ language models that RLHF optimizes for consensus [Solid — NeurIPS 2025];
Doshi & Hauser's social dilemma result (+8.1% individual quality, +10.7% collective similarity)
[Solid — Science Advances, preregistered, n=893]. Model collapse dynamics are established:
Shumailov et al. showed tails disappear first, irreversibly [Solid — Nature, Vol 631].
Gerstgrasser et al. showed replacement → inevitable collapse; accumulation → bounded error
[Solid for mathematical result — arXiv, Stanford/MIT/Maryland/Harvard; not peer-reviewed].

What has not been demonstrated is the chain as an integrated phenomenon. No study measures
substitutive AI use at scale → contamination of public corpora → collapse dynamics in
next-generation models as a continuous, observed process. The individual links are established;
the loop is a logical inference from those links. [See [The Stakes](the-stakes), "The Collapse Chain." This inference is the strongest available
case for a systemic risk — it must be stated as an inference, not as established fact.]

There are additional uncertainties within the chain. Dohmatob et al.'s 1% synthetic data
threshold — "even the smallest fraction of synthetic data... can still lead to model collapse"
— comes from a supervised linear regression model, not from production LLM training. Whether
frontier model training is subject to the same dynamics at the same thresholds is not known.
[Solid direction; uncertain specific threshold — see [The Stakes](the-stakes) for the caveat, confirmed against Dohmatob source text.]

---

## What We Don't Know About Collaborative Generation

[The Mechanism](the-mechanism) established what goes wrong when AI generates prose and humans evaluate it. What it
did not establish is what to do instead — precisely.

The Bastani study showed that hint-based design (GPT Tutor) eliminated learning harm while
preserving gains. Shen & Tamkin's Generation-Then-Comprehension pattern showed that active
comprehension after AI code generation preserved learning. Kazemitabaar et al.'s Lead-and-Reveal
technique — where the AI guides the learner through the problem-solving process, prompting
what to do at each stage before revealing the code — was the most effective of seven tested
friction techniques. [Solid — Kazemitabaar et al. 2025, IUI, N=82+42. Population: novice
undergraduates, data structures course, not professional developers.]

These are useful. They don't answer the question of how collaborative generation should work
for prose and ideas at the scale of professional knowledge work.

Should the human produce a rough draft and the AI refine it? Should they alternate passes?
Should the AI generate options and the human choose and extend? The ground truth names this
directly: "The exact interaction model for prose/ideas is an open question." [Ground truth
discourse, Step 4, item 4.] No study has directly tested these alternatives as paired conditions.
Siddiqui et al.'s integrated writing tool (Script&Shift) provides evidence that scaffolded
subprocesses preserve knowledge transformation — but it is a single study with n=30 per
condition, on undergraduate source-based writing, at arXiv preprint stage.

The collaborative generation model is unresolved. It is the next design question, not a solved one.

---

## What About cix Specifically

Everything in [The Design Lever](the-design-lever) about design levers is about other people's systems. Bastani's GPT Tutor
ran at a Turkish high school. Blaurock's experiments enrolled financial services employees and
HR professionals. Shen & Tamkin's study used crowd-sourced developers in a 35-minute task
on a Python async library.

No study has measured what happens to developers who use cix extensions. Not whether their
critical thinking is preserved. Not whether their architectural reasoning compounds or atrophies.
Not whether the discourse step in craft-rhetoric actually produces unique content or whether
users accept the first synthesis that sounds reasonable. The `build-evals` plugin exists; it has
not been run. [Solid — see [What cix Does](what-cix-does), "What cix Does Not Claim."]

This means every specific claim about cix is an extrapolation:

- Human-initiated installation (`cix add`) operationalizes process control (b=0.715 for outcome responsibility taking, Blaurock).
  Measured in scenario-based evaluation of financial services employees, not in cix use. Whether
  it produces the same felt ownership in a developer's actual workflow is not known.

- The dual-content model (SKILL.md for agents, docs/ for humans) operationalizes transparency.
  But the Bansal et al. finding — that explanations increase acceptance regardless of correctness —
  warns that well-documented methodology can produce compliance rather than evaluation. Whether
  the docs/ layer enables genuine calibration or serves as a reassurance artifact that users skim
  and accept is not measured. [Solid — Bansal et al. 2021, CHI, 378 citations, multi-study.]

- The dao engagement model — skills as methodologies for discovering the user's unique approach,
  not catalogs of preset answers — is meant to resist the homogenization cix documents. It depends
  on the discourse step producing something the human actually generated, not something they
  approved. Whether that happens in practice depends entirely on whether the human brings
  something to discover. [Architectural — ground truth Step 4 item 5, and Wan & Kalman 2025
  as proof-of-concept countermeasure, arXiv preprint, single modified replication, not independently
  replicated.]

The design choices are grounded. The outcomes are not measured. That is where the project stands.

---

## The Bet Against Market Forces

The research in [The Paradox](the-paradox) through [The Stakes](the-stakes) exists inside a market context that the research itself doesn't
resolve. The productivity gains are real: Cui et al.'s three corporate RCTs measured +26% task
completion across 4,867 developers. [Solid — Cui et al. 2024, S18, SSRN working paper.] That
signal is what organizations measure, fund, and adopt.

A 26% task completion gain appears in a dashboard in week three. Skill atrophy — if it matches
what the mechanism predicts — would appear in year two of a capability assessment that hasn't
been run. The skill harm, the homogenization, the collapse dynamics operate on timescales and
at levels that don't show up in quarterly productivity dashboards. The market follows the signal
it can read.

cix is building against this. The dominant market incentive is the immediate gain. The cix
hypothesis is that the longer-term costs matter enough to invest in complementary design now,
before the measurement exists to prove it at scale.

This is a bet, not a finding. The evidence provides the mechanism and the direction. It does not
guarantee that complementary design at scale produces the outcomes the theory predicts, on the
timescale that matters for individual career development or collective epistemic health. The
honest framing from the ground truth discourse: "Market forces favor quick wins. Mastery
orientation is not the primary market driver. cix is betting against the dominant incentive
structure." [Ground truth Step 4, item 1.]

---

## What This Is Not

Reading this article after the previous five, the temptation is to conclude the whole project is
shakier than it seemed. Resist it.

The developer capability study doesn't exist. The code/prose distinction is an inference from
parallel studies. The homogenization chain is assembled from three separate literatures. No cix
plugin has evaluation data. These are four specific absences — not a general condition of
uncertainty hanging over the whole library. They have edges. Other things are established.

The gaps named here are specific. They don't undermine the claims that are established. The
+26% productivity gain is real. The mechanism — AI closes the cognitive gap, the gap is where
learning happens — is supported by multiple independent studies across multiple domains. The
design lever evidence is the strongest cluster in the entire corpus: one field experiment
(Bastani, PNAS, n~1,000), one RCT (Shen/Tamkin, arXiv, n=52), one experimental feature
isolation (Blaurock, Journal of Service Research, N=654), one large QCA (Pallant, Studies in
Higher Education, n=192) — all pointing in the same direction, different populations, different
designs, different domains.

The research shows design can steer toward positive outcomes. It is the best-supported finding
in this library. The same study that shows -17% exam
performance for GPT Base shows no significant harm for GPT Tutor. Same model. Different design.
[Solid — Bastani et al. 2025, S2, PNAS.]

The gaps are not a reason to doubt the design. They are a map of what to measure next. What
happens to developer capability over two years of AI use. Whether code comprehension and prose
evaluation differ in a direct paired test. Whether the homogenization–collapse chain operates as
integrated phenomenon at measurable scale. How collaborative generation for prose should be
structured. Whether cix's specific implementations produce the intended effects.

These are research questions. They are not answered. They are also not the questions you are
waiting on to decide whether the engagement model you use with AI tools today matters.

The mechanism is understood. The design lever is identified. The choice is available now.
