# First Principles of Collaborative Intelligence

Three principles for working with AI without losing yourself to it. They build in sequence: the first names the opportunity, the second names the trap, the third names the practice that keeps you out of it.

---

## 1. Standing on the Shoulders of Giants

The phrase comes from Isaac Newton, but the idea is older. Every generation of builders inherits the accumulated work of those who came before. We don't re-derive calculus to write software. We don't rediscover TCP to build a web service. We stand on a structure that took centuries to construct.

AI changes the scale of what's available to stand on. The knowledge of a thousand codebases, ten thousand debugging sessions, the patterns that appear across decades of engineering practice — all of it is now something you can reach for in a conversation. That is genuinely extraordinary.

But there is a difference between standing on shoulders and being carried. Standing on shoulders means you understand what's beneath you. You know how the wheel works even though you didn't invent it. You can evaluate, adapt, push further. Being carried means you receive the output without understanding the reasoning — and if the ground shifts, you have no footing.

The developers who use AI most effectively aren't the ones who use it most. They're the ones who use it with understanding. A senior developer asks AI to explore three approaches to a caching problem, then picks one and explains why to a colleague. They've used AI to expand their range of consideration. Their understanding compounds. The person who asks "give me a Redis config" and pastes it in hasn't used AI less — they've used it differently. If the config fails, they don't know why.

Don't reinvent the wheel. But know how wheels work.

---

## 2. Feynman's First Principle

> "The first principle is that you must not fool yourself — and you are the easiest person to fool."

Feynman said this about science, but it applies everywhere self-deception is possible. And in AI collaboration, self-deception is the default failure mode.

The mechanism is subtle. AI output looks like work. It has structure, confidence, detail. When you read something that looks right, your brain wants to move on — the work appears done. This isn't laziness. It's a normal cognitive response to a signal that says *this is resolved*. The problem is that the signal is often false.

Developers spend roughly 22% of their AI-assisted coding time on verification. The rest is accepting, integrating, moving forward. Meanwhile, a substantial portion of AI-generated code contains security vulnerabilities. The mismatch isn't the AI's fault. It's that verification effort drops below the actual error rate — not because developers don't know they should check, but because the output *looks* convincing.

This is the perception gap. You feel productive. You shipped something. Your subjective experience of capability is intact. But the unaided version of you — the one who has to debug this at 2am without AI present — that version is not keeping up. The slide is invisible precisely because you're never without the tool long enough to notice.

Feynman's warning is the core CI warning. The more powerful and fluent the tool, the more convincing the output, the easier the self-deception. The opportunity named in principle one — all that inherited knowledge — is also exactly what makes the trap close so quietly.

---

## 3. The Scientific Method

The fix isn't distrust. It's calibration.

Science doesn't distrust every observation — it treats every observation as a hypothesis until it's been tested. That distinction matters. Distrust is paralysis. Hypothesis-testing is a practice.

Every AI output is a hypothesis. The model has proposed something: a function, a diagnosis, an explanation. Your job is not to accept or reject on instinct. Your job is to test it. Form a belief about what the output should do, independent of having seen it. Then check whether it does that.

This sounds obvious. It's rarely done. The tell is when someone says "I checked the output" and what they mean is "I read it and it looked right." Reading and agreeing is not a test. A test is independent. It produces a result that could, in principle, come out differently than you expected.

Concrete form: before accepting AI-generated code, close the output. Write down what you expect the function to do — its inputs, outputs, edge cases. Open the output. Does it match your expectation? If you can't articulate the expectation without seeing the code, you don't have a hypothesis yet. You're agreeing with something you don't fully understand.

The same rigour applies beyond code. An AI-suggested architecture is a hypothesis. An AI-drafted explanation is a hypothesis. You test it by asking: what would have to be true for this to be wrong? Can I construct a case where this fails? The question isn't "does this look right?" It's "what would falsify this?"

This practice doesn't slow you down in the long run. It's what keeps you calibrated. Each time you test and the hypothesis holds, your trust in that domain is earned. Each time it fails, you've learned something before it failed in production. The scientific method built the modern world by being relentlessly honest about what was known versus assumed. It works the same way here.

---

## Synthesis

These three principles are one arc. You have access to something extraordinary — the accumulated knowledge of the craft, available at conversation speed. That power is real. But the same fluency that makes it powerful makes self-deception easy: things look done when they aren't, capability looks intact when it's sliding, trust accumulates without being earned. The practice that holds this together is the scientific method applied at the level of each interaction. Treat every output as a hypothesis. Test it independently. Update on evidence. That's what it means to build *with* inherited knowledge rather than be carried by it.

---

*Evidence sources in [bibliography](../reference/bibliography)*
