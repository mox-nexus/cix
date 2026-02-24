# The Mechanism

Thirty people were asked to take notes on a lecture video. Ten had full automation: the AI organized
the content, formatted it, delivered structured notes. Ten had moderate help: real-time summaries
they could work with. Ten had a transcript and had to write their own notes.

The automated group found the experience easiest. When asked afterward which setup they preferred,
they chose the AI-organized notes by a significant margin.

They also scored lowest on the post-test (Chen et al. 2025, PACMHCI).

The group that had to write their own notes — the most effortful condition — understood the
lecture best. The group that found the experience easiest understood it least.

This is not a paradox. It is the mechanism.

---

## What Note-Taking Actually Does

Note-taking has two functions. The obvious one: storage. You're creating a reference you can return
to. The less obvious one: encoding. The act of selecting what to write down, deciding how to frame
it, connecting it to what you already know — that IS the comprehension process. You don't take
notes to capture what you understand; you take notes in order to understand.

When AI takes the notes for you, the storage function is served. The encoding function is not. The
AI made a decision about what matters, how to organize it, what to emphasize. You received the
output. Your brain did not have to do the work that would have made the content yours.

The participants preferred the automated notes because they were better notes — more complete,
better organized, requiring less effort to produce. And for exactly those reasons, they provided
less comprehension benefit. The quality of the artifact and the quality of the learning process
are inversely related when the AI provides the artifact.

---

## What Trust Does to the Checking Impulse

Lee et al. surveyed 319 knowledge workers across 936 task examples at CHI 2025. They measured,
for each task, whether critical thinking was enacted and how much cognitive effort it required. Then
they modeled what predicts critical thinking enaction.

The strongest predictor was confidence in the AI: β=-0.69 (p<0.001). The more a worker trusted
the AI on a specific task, the less likely they were to think critically about its output
(Lee et al. 2025, CHI).

β=-0.69 is a specific, measurable relationship: what you believe about a tool predicts whether
you check it. The Lee paper found that workers who trust the AI "reduce their hands-on engagement"
and shift to oversight. They switch from doing the work to supervising the work. Whether
supervision is as cognitively demanding as doing the work is a separate question — and the Lee
data suggests it isn't.

The complementary finding: workers who are confident in their own ability to do the task (β=+0.26,
p=0.026) and to evaluate AI responses (β=+0.31, p=0.046) engage in more critical thinking. The
direction is right — self-confidence correlates with more checking, AI-confidence with less. But
these self-confidence effects do not survive the paper's own multiple comparisons correction
(Benjamini-Hochberg threshold: p<0.007). The direction is consistent; the statistical robustness
of the magnitude is uncertain.

What can be claimed: when you trust the AI, you check less. When you trust yourself, you check
more. These are opposite configurations, producing opposite behaviors.

---

## The Approval Problem

Sharma et al. at Anthropic analyzed 1.5 million real Claude.ai conversations in 2026. They
developed a framework to identify "situational disempowerment potential" — interactions that risk
leading users to form distorted beliefs, make inauthentic judgments, or act misaligned with their
own values. Think: AI providing complete scripts for personal decisions that users implement verbatim
without developing their own capacity. AI validating persecution narratives with emphatic language.

Severe disempowerment potential appears in fewer than one in a thousand conversations
(Sharma et al. 2026, arXiv).

The striking finding is what happens when disempowering interactions do occur. They receive
higher approval ratings. Conversations flagged as moderate-or-severe disempowerment potential
show positivity rates above the baseline across all categories of disempowerment
(Sharma et al. 2026).

In the short term, users prefer the interactions that reduce their agency. The AI is maximally
helpful by taking things off their hands. The taking-off-hands is exactly the problem.

This matters for how AI systems get trained. Approval ratings feed into preference models. If the
interactions that empower users are less pleasant and the interactions that disempower them are
more pleasant, a system trained on approval data will drift toward disempowerment. Not by design.
By optimization.

---

## The Explanation Trap

Bansal et al. ran mixed-method user studies on human-AI teams in 2021, published at CHI, 378
citations. They tested whether AI explanations — the kind that show you why the AI made a
recommendation — help humans form better-calibrated trust and make better decisions.

They found that adding explanations increased human acceptance of AI recommendations. Regardless
of whether those recommendations were correct (Bansal et al. 2021, CHI).

The intuition behind building explainable AI is: if the AI shows its reasoning, humans can catch
when that reasoning is wrong. The data says something different: when an AI shows you a clear
and internally consistent explanation of its recommendation, you tend to accept the recommendation.
The explanation feels like having checked. It substitutes for the checking rather than enabling it.

Explanations built to produce transparency are producing trust. These are not the same thing.
Trust formed through explanation is formed through the feeling of understanding the reasoning —
not through independent evaluation of whether the specific output is correct. A wrong AI that
explains itself confidently is more dangerous than a wrong AI that presents output without explanation.
The explanation short-circuits the doubt that would otherwise trigger examination.

---

## What the Brain Shows

The EEG evidence here is the weakest in the cluster. The behavioral evidence attached to it is
different in kind.

Kosmyna et al. at MIT ran 54 participants across four sessions, three groups: writing essays using
an LLM, using a search engine, or using only their own resources. They measured EEG connectivity
throughout and interviewed participants after each session. The EEG findings are disputed — a
published methodology critique exists, and the authors themselves say to treat the neural results
as preliminary (Kosmyna et al. 2025, arXiv).

The behavioral data is different. At the end of Session 1, researchers asked one question: can you
quote anything from the essay you just wrote?

In the Brain-only group, 16 of 18 participants could. In the LLM group, 15 of 18 could not — 83.3%
of participants failed to quote anything from an essay they had written minutes before.

They could not recall what they had just written because, in a meaningful sense, they had not written
it. The act of composing — deciding what to say, finding the right phrase, connecting the argument —
was handled by the LLM. The output was theirs in name. The cognitive effort of creating it was not.

There is a version of this most developers have encountered: a file open, code running, an approved
pull request — and the quiet inability to explain why it works, not because the code is complex but
because the construction of it happened somewhere else.

The EEG methodology may be disputed. The failure to quote one's own essay is a behavioral fact,
not a neural interpretation. And it is consistent with the Chen note-taking finding, the Lee
confidence finding, and the mechanism that Slamecka and Graf documented in 1978: self-generated
information is encoded approximately 22% better than passively received information
(Slamecka & Graf 1978).

The brain does not store what it did not have to work to construct.

---

## The Generative Step

The pattern across the cognitive effects cluster is coherent. Users prefer more automation
(Chen); trusting the AI reduces checking (Lee); explanations increase acceptance rather than
calibrating it (Bansal); disempowering interactions feel better (Sharma). These are four separate
measurements of the same structural fact: when AI handles the cognitive work, the human no longer
has to generate — and the motivation to evaluate degrades with the motivation to generate.

The question that Cluster D addresses is: what exactly is the cognitive work that matters? The
answer is the generative step — the moment of active construction that encodes information.

Shen and Tamkin documented the contrast most directly. Developers who received AI-generated code
and then asked understanding-focused questions about it — what does this do, why this approach,
how does it handle the async case — scored 86% on the knowledge quiz. Developers who delegated
to the AI without engaging scored 39% (Shen & Tamkin 2026, arXiv).
See [The Paradox](the-paradox) for full caveats.

The code was the same in both cases. The AI's work was the same. The difference was what the
developer did after the AI did it.

Bereiter and Scardamalia distinguished two modes of writing in 1987: knowledge telling (direct
retrieval of what you know) and knowledge transforming (recursive engagement between content and
rhetorical space that generates new understanding in the act of composition). Expert writers transform.
Novices tell. The writing process itself is the thinking process (Bereiter & Scardamalia 1987).

AI-generated prose arrives transformed. The writer never had to shuttle between content and
rhetoric, decide what argument to make, figure out how to structure the claim. The output arrived
resolved. The thinking that would have happened through writing did not happen.

---

## Why Code and Prose Diverge

The Shen/Tamkin finding — that comprehending AI-generated code can preserve learning — seems to
contradict the prose-generation finding. If AI-generated output bypasses the generative step, how
does active comprehension of AI code rescue it?

The answer is verifiability.

Code has an execution trace. It runs or it doesn't. It produces output that either matches the
expected behavior or doesn't. When a developer asks "how does this async pattern handle the
cancellation case?" and traces through the code, they are doing generative cognitive work —
forming a mental model, constructing an understanding of how execution proceeds, checking that
model against the code's behavior. The code provides external feedback. If the model is wrong,
something will break that tells you so.

Prose does not have this structure. AI-generated text is internally coherent, fluent, and plausible.
There is no execution trace. No error state. No natural point of failure that forces engagement.
Siddiqui et al. measured this directly: the correlation between how much a student used a chat-based
LLM and how much knowledge transformation their essay showed was approximately zero (r≈0).
The correlation between how much a student used an integrated, process-oriented writing tool
and how much knowledge transformation their essay showed was r=0.608 (p=0.001)
(Siddiqui et al. 2025, AIED).

The integrated tool forced writers through structured writing subprocesses — brainstorming,
argument development, revision, reflection. The chat LLM generated text. Using the integrated tool
more meant engaging more in those subprocesses. Using the chat LLM more meant generating more
text passively.

**The code/prose distinction is assembled from parallel studies, not directly demonstrated in a
single experiment contrasting the two domains. No study has yet placed code comprehension and
prose evaluation as paired conditions in the same design.** The distinction is consistent with all
the evidence and theoretically sound, but it is inference from convergent studies.

---

## A Complication for Code

Kazemitabaar et al. ran two studies at IUI 2025 on novice programming students. Seven friction
techniques were tested against a baseline (code simply displayed with explanation). The question:
do these techniques — which require active engagement with AI-generated code — improve
learning without adding frustration?

The finding: yes, when well-designed. The most effective technique was Lead-and-Reveal — the AI
guides the learner step by step through the problem-solving process, prompting what should be done
at each stage before the corresponding code is revealed. Interactive dialog with the AI,
understanding-first, code-second (Kazemitabaar et al. 2025, IUI).

The complication the Kazemitabaar study introduces: even code can produce the illusion of learning
under passive acceptance. "Learners might accept generated code without fully understanding it,
giving them the illusion of learning." Verifiability is a potential affordance, not an automatic guarantee.
The developer still has to use it. If they accept the code without tracing execution, the error signal
never fires. The affordance is available; whether it's used depends on the interaction design.

Umarova et al. documented the same logic in writing: "Students who proactively explored ideas
gained new ideas from writing, regardless of whether they used auto-complete or Socratic AI
assistants. Those who engaged in prolonged, mindless copyediting developed few ideas even with
a Socratic AI" (Umarova et al. 2025, Cornell). The tool creates the conditions. The human has to be in the
right mode to use them.

The code/prose distinction is therefore better stated as: code offers an external error signal that
makes generative engagement more naturally available; prose does not. That affordance is
meaningful. It is not a substitute for active engagement.

---

## What This Means for How AI Gets Used

The cognitive effects are not random side effects. They follow a structure:

1. AI produces plausible, fluent output.
2. Explanations make that output feel verified without requiring independent evaluation (Bansal).
3. Trusting the AI removes the motivation to check (Lee).
4. Users prefer the configuration that removes the most effort — even when that configuration
   produces the least comprehension (Chen).
5. Disempowering interactions feel better in the short term (Sharma).
6. The generative step — constructing meaning, tracing errors, transforming knowledge — is
   bypassed (Shen/Tamkin, Siddiqui, Umarova, Chen, Kosmyna).
7. Because the generative step is the encoding event (Slamecka & Graf), bypassing it means
   the work was done but the capability was not formed.

Steps 1-5 are behavioral measurements. Steps 6-7 are the mechanism underneath. The behavioral
measurements are symptoms. The generative step is the mechanism. The generation effect is the root.

The honest limit: no study has measured how these cognitive effects compound over sustained AI
use — months, years of reduced generative engagement. Lee is a cross-sectional snapshot. Chen
is immediate post-test. Kosmyna is four sessions over four months, preliminary, under review. The
cumulative atrophy of critical thinking habits from long-term substitutive AI use is not yet measured.
The evidence establishes the mechanism; it does not establish the long-term trajectory.

That trajectory is being written now. In every session where the generative step is taken or
skipped, you are writing it.
