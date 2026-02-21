# The Risks

These aren't seven separate risks. They're three failure modes that compound.

Every risk associated with uncritical AI adoption traces back to one of three mechanisms: capability drift you can't feel, errors you can't see, and structural fragility that builds quietly. Understanding the mechanisms matters more than cataloging the categories — because the same design choices that prevent one prevent all three.

---

## What you don't practice, you lose

The first mechanism is cognitive offloading. When AI handles reasoning, humans stop performing it. This is rational resource allocation — why think when AI does it faster? But cognition works like muscle: stop using it, lose it.

After three months of AI-assisted colonoscopy, endoscopists' unaided detection rate dropped 20% on their non-AI cases (Budzyń et al., Lancet 2025). <span class="ev ev-moderate" title="Lancet multicentre observational, 19 endoscopists">◐</span> The most vulnerable skills aren't procedural ones like typing or navigation — those remain intact. What erodes is exactly what's most valuable: reasoning about systems, analyzing edge cases, recognizing patterns that don't match the training data. The degradation is targeted.

Novices experience the extreme case. A beginner who receives AI-generated solutions for every problem they encounter may never form the mental models that make expertise possible. Errors are the curriculum — they force diagnosis, and diagnosis builds schema. Remove the errors, and the learning that happens through struggle doesn't happen at all. The study that split AI tutors between "answers" and "hints" found 17% worse exam performance in the direct-answer group (Bastani et al., PNAS 2025) — not because the answers were wrong, but because receiving them bypassed the process that builds understanding.

---

## You can't fix what you can't see

The second mechanism is the perception gap. The harm from the first mechanism would be correctable if people could detect it. The research suggests they largely can't.

16 experienced developers predicted AI would make them 24% faster. Rigorous measurement showed they were 19% slower — a 43-point gap between expectation and reality (METR RCT). <span class="ev ev-moderate" title="METR RCT, n=16">◐</span> The effort feels lighter because the visible work (generation) disappears while the invisible work (verification, integration, fixing) grows. The task completes; the illusion persists.

At scale, the paradox deepens: trust in AI coding accuracy dropped 10 percentage points over a year while adoption rose 8 points. People use tools they don't trust and perceive benefits that measurement doesn't confirm.

Automation complacency amplifies the gap. Confidence in AI output negatively predicts critical thinking (β = -0.69, Lee et al., CHI 2025). <span class="ev ev-strong" title="Lee et al. CHI 2025, n=319">●</span> Developers spend only 22.4% of coding time verifying AI suggestions — the verification that would catch the errors doesn't happen at the rate needed to catch them.

Security degradation is the highest-stakes version of this. 45% of AI-generated code contains critical vulnerabilities — not because the model is malicious, but because it learned from code repositories that contain vulnerabilities. The model reproduces common patterns; common patterns include insecure ones. Independent security review is the countermeasure. But security expertise is one of the skills that atrophies when people stop practicing it.

---

## Individual loss becomes collective fragility

The third mechanism runs at a larger scale than the first two.

When millions of people use the same AI systems, individual capability drift accumulates into homogenization. 70+ language models answering 26,000 open-ended questions converge to the same handful of patterns regardless of temperature or prompting strategy — RLHF training penalizes idiosyncratic responses, even valid ones (NeurIPS Best Paper). A meta-analysis across 28 studies found collective creative diversity drops significantly (g = -0.863) even as individual performance rises slightly. <span class="ev ev-strong" title="NeurIPS Best Paper, 70+ models, 28 studies">●</span>

This matters because diverse groups outperform best-ability homogeneous groups on complex problems. The variety that's eroding isn't decorative — it's the system's ability to handle unexpected failures. Ashby's Law of Requisite Variety: a system can only handle variety in its environment if it has equal or greater internal variety. When AI reduces solution diversity, teams and codebases lose the internal variety needed to absorb shocks.

Code quality erosion compounds this. Code duplication increases 8x after AI adoption. Each generation produces plausible code that works in isolation but duplicates what already exists, because the AI has no awareness of the codebase's existing patterns. By sprint N, the codebase is assembled from components the developer never designed and may not fully understand. Architectural evolution becomes harder as the gap between "what was generated" and "what was understood" grows.

---

## How they compound

The three mechanisms don't operate in isolation.

Skill atrophy makes the perception gap worse — you can't catch what you no longer have the expertise to recognize. The perception gap prevents self-correction — you can't fix degradation you can't see. Code quality erosion creates more complexity, which increases reliance on AI, which accelerates skill atrophy. Homogenization means teams share the same blind spots, so diverse review — one corrective mechanism — stops working.

The perception gap is the central problem. It locks the system: harm feels like help, so experience doesn't teach correction, so the harm continues.

---

## What we don't know

No longitudinal study has tracked developer capability over 2-5 years of heavy AI use. The medical evidence shows 20% skill loss at three months. The developer evidence shows perception gaps and reduced critical thinking in cross-sectional data. But the multi-year trajectory remains unmeasured.

Whether capability atrophy accelerates or plateaus after the initial drop is unknown. Whether early-career AI exposure prevents schema formation in ways that persist are speculative — plausible given the mechanism, but unconfirmed beyond short-term studies. The critical study — cohort design, multiple interaction patterns, capability assessment at 6/12/24 months, comparing assisted and unassisted performance — hasn't been run.

We're making significant decisions on inferences from short-term studies.

---

## The design response

The risks are real and structural. Better models don't fix them. Better prompts don't fix them. They require interaction design that preserves the cognitive engagement that builds capability — control and transparency at the design level, not willpower at the individual level.

That design question is what the rest of the library is about.
