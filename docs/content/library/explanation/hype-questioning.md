# Hype & Questioning

Why critical thinking erodes around AI, and how to read the research itself.

---

## Sources

- [Becker et al. (2025). Measuring AI Impact on Developer Productivity. METR.](https://arxiv.org/abs/2507.09089)
- [Lee et al. (2025). Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/10.1145/3613904.3641913)
- [Bansal et al. (2021). Does the Whole Exceed its Parts? Explanations in Human-AI Joint Decision Making. CHI.](https://dl.acm.org/doi/10.1145/3411764.3445717)
- [Shen & Tamkin (2025). When Generative AI Meets Education. Berkeley/Anthropic.](https://arxiv.org/abs/2503.00308)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2413913122)
- [Stack Overflow Developer Survey (2024-2025).](https://survey.stackoverflow.co/2024/)
- [Gerlich et al. (2025). Human Control and Trust in AI Systems. Survey.](https://arxiv.org/abs/2501.09486)
- [Budzyń et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)
- [Cui/Demirer et al. (2024). Effects of Generative AI on High Skilled Work. RCTs.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4671691)

---

## Abstract

The perception gap is structural. Developers predicted 24% speedup, measurements showed 19% slowdown — a 43-point miscalibration. <span class="ev ev-moderate" title="METR RCT, n=16, rigorous but small sample">◐</span> Trust in AI coding accuracy dropped from 43% to 33% in one year while adoption rose from 76% to 84%. <span class="ev ev-moderate" title="Stack Overflow survey, observational, self-report">◐</span> People use tools they don't trust, perceive benefits they don't get. The gap prevents self-correction — you can't fix what you can't see.

Critical thinking erodes as AI confidence rises (β = -0.69). <span class="ev ev-strong" title="Lee CHI 2025, n=319, SEM">●</span> Explanations increase reliance regardless of correctness (Bansal). <span class="ev ev-strong" title="Bansal CHI 2021, controlled experiment">●</span> Higher AI confidence predicts less verification, not better calibration. This is automation bias: the tendency to favor machine output over human judgment.

This article interrogates the evidence itself. The research shows both gains and harms. Both are real. The question is whether we can design interaction patterns that preserve the benefits while avoiding the costs — and whether we're asking hard enough questions about what we think we know.

---

## Explanation

**The central problem isn't that AI tools exist. It's that our perception of them is systematically miscalibrated.**

### The Perception Gap Is Structural

The METR study reveals the mechanism. Sixteen experienced developers, working in their own repositories on real tasks, were 19% slower with AI while predicting they'd be 24% faster. <span class="ev ev-moderate" title="METR RCT, within-subject design, but n=16 limits generalizability">◐</span>

This wasn't user error. It was how perception works. Time spent prompting, reviewing suggestions, fixing integration issues, and context-switching doesn't register as "work." Code appearing on screen feels like productivity. The invisible effort of verification disappears from awareness.

The same pattern appears in aggregate. Stack Overflow's survey shows trust falling (43% → 33%) while adoption rises (76% → 84%). <span class="ev ev-moderate" title="Survey data, observational, no causal mechanism">◐</span> People use tools they don't trust because perceived productivity overrides measured performance.

**This prevents correction.** If you believe you're faster, you won't measure. If you don't measure, you won't discover the gap. The illusion is self-sustaining.

### Why Questioning Erodes: Automation Bias

Automation bias is the tendency to favor machine-generated output over contradictory information from other sources. AI tools trigger this at scale.

**The evidence:**

Lee et al. found β = -0.69: higher confidence in AI significantly predicts less critical thinking enacted. <span class="ev ev-strong" title="CHI 2025, n=319, SEM model">●</span> The more you trust AI, the less you verify it. The less you verify, the more errors propagate.

Bansal et al. showed explanations increase reliance regardless of whether the AI is correct. <span class="ev ev-strong" title="CHI 2021, controlled experiment with correct/incorrect AI">●</span> When AI is right, explanations help slightly. When AI is wrong, performance degrades. Explanations feel like transparency but function as persuasion.

This is the confidence-competence inversion: making AI better at appearing confident can make humans worse at being competent. Trust rises, verification falls, capability erodes.

**The mechanism:** AI provides answers to questions you don't fully understand. Each answer feels like learning. In reality, you're offloading comprehension. You can't assess correctness in domains where you lack expertise. AI accelerates this by removing the friction that forces learning.

### The Vendor Incentive Problem

AI companies have structural incentives to emphasize productivity gains and minimize capability harms. This creates a research asymmetry.

**Credit where due:** Anthropic funded Shen & Tamkin's work showing their own product can harm learning when used without scaffolding. <span class="ev ev-moderate" title="n=52, one library, 70-minute session, small but rigorous">◐</span> That's intellectual honesty worth noting.

**But:** The funded studies are small (n=52) and short-term (70 minutes). The critical longitudinal study doesn't exist — no measurement of developer capability degradation after months of AI use. We're inferring from medical domains (Budzyń colonoscopy study: 20% skill decline in 12 weeks) <span class="ev ev-moderate" title="Lancet RCT, medical domain, transfer to software uncertain">◐</span> and short-term learning experiments.

Cui/Demirer's productivity gains (26% more tasks completed, n=4,867) <span class="ev ev-strong" title="Multiple RCTs, large sample">●</span> and Bastani's learning harms (17% worse on exams, n=1,000) <span class="ev ev-strong" title="RCT, PNAS, one domain">●</span> both come from rigorous sources. They don't contradict — they measure different things. Immediate task performance vs. capability development. Both can be true.

The question is which dominates over time, and whether design choices change the trajectory. The research suggests yes — Bastani's scaffolded AI showed no learning harm, and Shen & Tamkin's Generation-Then-Comprehension pattern achieved 86% mastery. <span class="ev ev-moderate" title="Same studies, small samples, promising but needs replication">◐</span>

But publication incentives favor positive results. We don't know what studies were run and not published.

### Study Limitations: Intellectual Honesty

This library cites research extensively. It's time to question that research.

| Study | Limitation |
|-------|-----------|
| **METR productivity** | n=16, experienced devs only, no juniors, short-term |
| **Shen & Tamkin learning** | n=52, single library, 70 minutes, needs replication |
| **Budzyń colonoscopy** | Medical domain, skill transfer to software uncertain |
| **Gerlich control/trust** | Survey-based, self-report, correlation not causation |
| **Lee critical thinking** | Cross-sectional, no longitudinal, β interpretation |
| **GitClear code quality** | Observational, no causal mechanism proven |
| **Stack Overflow trust** | Survey, observational, self-report bias |

**The critical study that doesn't exist:** Longitudinal measurement of developer capability after 6-12 months of daily AI use. Everything is either short-term (minutes to weeks) or cross-domain inference (medical → software).

We're making decisions based on:
- Small samples (n=16, n=52)
- Short timeframes (70 minutes, single session)
- Adjacent domains (colonoscopy as proxy for coding)
- Observational data (surveys, code analysis without causal proof)

These studies are rigorous within their constraints. But the constraints are severe. We're inferring long-term developer capability effects from evidence that doesn't directly measure them.

### How to Read AI Research

Applied to this very library:

**Check sample size.** n=16 (METR) is rigorous for the design but small for generalization. n=4,867 (Cui/Demirer) is strong. n=52 (Shen & Tamkin) is exploratory.

**Check design.** RCT > controlled experiment > observational > survey > anecdote. METR and Bastani are RCTs. GitClear is observational. Stack Overflow is survey.

**Check domain transfer.** Colonoscopy skill atrophy (medical) → developer capability (software)? Plausible mechanism, uncertain magnitude. This library treats it as moderate evidence, not strong.

**Check timeframe.** 70-minute session (Shen & Tamkin) vs. 12-week crossover (Budzyń) vs. years of practice (what we actually care about). Short studies inform but don't determine long-term effects.

**Check who funded it.** Anthropic funding Shen & Tamkin showing harm? Honest. OpenAI research showing only gains? Scrutinize harder.

**Check what's NOT measured.** No study measures developer capability after 6-12 months of daily AI use. Everything is inference. Reasonable inference, but inference nonetheless.

### The Meta-Question: Can We Design Through This?

The research suggests AI tools can both help and harm. The question is whether interaction design changes the outcome.

**Evidence for "yes":**

Bastani's scaffolded AI (hints, not answers) showed no learning harm. <span class="ev ev-strong" title="Same RCT, n=1,000, within-study comparison">●</span> Shen & Tamkin's Generation-Then-Comprehension (attempt first, then AI) achieved 86% mastery. <span class="ev ev-moderate" title="n=52, 70 minutes, promising pattern">◐</span> Gerlich found user control (β = 0.507) and transparency (β = 0.415) were strongest predictors of appropriate trust. <span class="ev ev-moderate" title="Survey-based, but large effect sizes">◐</span>

Same technology, different design, opposite outcomes.

**The design principles that emerge:**
- Complementary over substitutive (amplify human, don't replace)
- Transparency over opacity (show reasoning, not just results)
- Control over automation (human-initiated, not autonomous)
- Mastery orientation over performance orientation (learning > output)
- Verification independence (generate and review must be separate)

These patterns have evidence. Small studies, short-term, needs replication. But they're testable hypotheses grounded in cognitive science and preliminary empirical work.

### The Questioning Imperative

> "The first principle is that you must not fool yourself — and you are the easiest person to fool." — Richard Feynman

The research suggests:
- AI tools improve immediate task performance (strong evidence)
- AI tools degrade capability development (strong evidence, short-term)
- The perception gap prevents self-correction (moderate evidence)
- Design choices change outcomes (moderate evidence, promising)
- Long-term effects on developers (speculative, no direct measurement)

This library cites the evidence and acknowledges its limits. The methodology is to ground claims in sources while being explicit about inference gaps.

**The honest position:** AI tools show both gains and harms in controlled studies. We don't yet have longitudinal data on developer capability. We're making design decisions based on:
- Rigorous short-term studies
- Cross-domain analogies
- Cognitive science fundamentals
- Preliminary evidence of design patterns that help

That's the state of knowledge. Not settled. Not speculative. Grounded with known limitations.

### What This Means for cix

Every extension in this marketplace should:

1. **Question its own claims** — what's the evidence? what are the limits?
2. **Make perception gaps visible** — measure, don't assume
3. **Optimize for learning** — comprehension over speed
4. **Preserve verification independence** — generate and review stay separate
5. **Acknowledge uncertainty** — speculative when speculative, strong when strong

The goal isn't to eliminate AI tools. The goal is to design them so humans become more capable, not dependent.

The evidence suggests this is possible. Small studies, needs replication, worth trying.

The alternative — uncritical adoption based on perceived productivity — has evidence showing it fails. Larger studies, consistent pattern, worth avoiding.

### The Feynman Standard

Applied to this article:

**Claims made:**
- Perception gap exists (moderate: METR n=16, Stack Overflow survey)
- Critical thinking erodes with AI confidence (strong: Lee CHI, n=319)
- Automation bias operates (strong: Bansal CHI, controlled)
- Design changes outcomes (moderate: Bastani, Shen/Tamkin, small samples)
- Long-term capability effects (speculative: no direct measurement)

**What's NOT known:**
- Developer capability after 6-12 months of daily AI use
- Whether short-term effects compound or plateau
- Magnitude of design interventions at scale
- Replication of promising patterns (Generation-Then-Comprehension, etc.)

**Honest uncertainty:** The evidence strongly suggests AI tools create tradeoffs. It moderately suggests design choices change those tradeoffs. It speculatively predicts long-term capability effects based on short-term studies and adjacent domains.

That's what we know. Act accordingly.

---

## The Core Finding

Critical thinking erodes around AI because perception systematically diverges from reality. Automation bias, vendor incentives, and the invisibility of verification effort create a self-sustaining illusion of productivity.

The research shows both gains and harms. Both are real. The question is whether design can preserve gains while avoiding harms — and whether we're asking hard enough questions about what we think we know.

The evidence says design matters. The evidence is preliminary. The methodology is to act on best available knowledge while acknowledging its limits.

Question everything — including this.
