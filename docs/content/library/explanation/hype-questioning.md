# Hype & Questioning

Why we believe AI makes us faster when it doesn't — and how to read research (including this library's) without fooling yourself.

---

## The Gap You Can't See

You're reading a vendor blog post: "Developers using our AI tool complete 40% more tasks." Sounds good. You try it. Code appears on screen faster than you've ever written it. You feel productive. You ship features. Everyone's happy.

Three months later, your team is finding more bugs in production. Code reviews take twice as long. You can't explain how parts of your own codebase work without prompting the AI again. But you're still using the tool because it *feels* fast.

This is the perception gap. And it's not a bug — it's how these tools work on human cognition.

**The mechanism:** Time spent prompting, reviewing suggestions, fixing integration errors, and context-switching doesn't register as "work." Code appearing on screen feels like productivity. The invisible effort disappears from your awareness. You perceive speed. Measurements show slowdown. <span class="ev ev-moderate" title="METR study, n=16 developers, rigorous within-subject design but small sample">◐</span>

One study measured this precisely: experienced developers predicted they'd be 24% faster with AI. They were actually 19% slower. That's a 43-point miscalibration. Not user error. Structural misperception. [See productivity evidence →](../reference/productivity-evidence)

The gap prevents self-correction. If you believe you're faster, you won't measure. If you don't measure, you won't discover the truth. The illusion sustains itself.

## Why Critical Thinking Erodes

Here's the pattern researchers found: the more confident you are in AI, the less you verify its output. Higher AI confidence predicts less critical thinking (β = -0.69). <span class="ev ev-strong" title="Lee et al. CHI 2025, n=319, structural equation modeling">●</span> Not "some people verify less." Systematic correlation. Trust goes up, questioning goes down. [See cognitive effects evidence →](../reference/cognitive-effects-evidence)

This has a name: **automation bias**. The tendency to favor machine-generated output over contradictory information from other sources. You've experienced it with GPS navigation—taking the suggested route even when you know a better one exists. AI coding tools trigger this at industrial scale.

Another study tested it directly: when AI provides explanations along with answers, people rely on those answers more—*regardless of whether the AI is correct*. <span class="ev ev-strong" title="Bansal et al. CHI 2021, controlled experiment with correct and incorrect AI">●</span> When AI is right, explanations help slightly. When AI is wrong, performance degrades. Explanations feel like transparency. They function as persuasion.

**The confidence-competence inversion:** Making AI better at appearing confident makes humans worse at being competent.

You can't assess correctness in domains where you lack expertise. AI provides answers to questions you don't fully understand. Each answer feels like learning. In reality, you're offloading comprehension. Students who used unrestricted AI assistance scored 17% worse on exams testing the same material. <span class="ev ev-strong" title="Bastani et al. PNAS 2025, n=1,000, randomized controlled trial">●</span> Same knowledge domain. Different pathway to get there. Opposite outcomes. [See skill formation evidence →](../reference/skill-formation-evidence)

## Reading AI Research Without Getting Fooled

Let's apply this to claims you'll encounter—including the ones this library makes.

### 1. Check the Sample Size

n=16 tells you something different than n=4,867. Small samples (n=16, n=52) can be rigorous—but they're exploratory, not definitive. Large samples (n=1,000+) provide stronger evidence of effects. When you see a claim, ask: how many people were actually studied?

The perception gap study? n=16 developers. Rigorous design, meaningful finding, but limited generalizability. The productivity gains study? n=4,867 across multiple trials. Much stronger generalization. Both are cited in this library. They don't have equal weight.

### 2. Check the Study Design

Hierarchy of evidence:
- **Randomized controlled trial (RCT)** — assigns participants randomly, controls for confounds
- **Controlled experiment** — manipulates variables but less random assignment
- **Observational study** — watches what happens naturally, can't prove causation
- **Survey** — self-report, subject to perception bias
- **Anecdote** — individual experience, not generalizable

When a vendor says "our tool improves productivity," ask: compared to what? How was that measured? Who did the measuring?

### 3. Check Domain Transfer

A study on medical residents learning colonoscopy found 20% skill degradation after 12 weeks without practice. <span class="ev ev-moderate" title="Budzyń et al. Lancet 2025, RCT in medical domain">◐</span> Does that apply to developers using AI coding assistants? Maybe. Plausible mechanism (skill atrophy from automation). Uncertain magnitude (different domains, different task structures). [See skill formation evidence →](../reference/skill-formation-evidence)

This library treats it as moderate evidence, not strong. The mechanism is credible. The transfer is uncertain. That matters.

### 4. Check the Timeframe

A 70-minute session tells you something. It doesn't tell you what happens after six months of daily use. Short-term studies inform. They don't determine long-term effects.

Most AI-and-learning research measures effects over minutes to weeks. The critical question—developer capability after 6-12 months of daily AI use—has no direct measurement. We're inferring from short-term learning studies and cross-domain analogies. Reasonable inference. Still inference.

### 5. Check Who Funded It

Vendor-funded research showing harm deserves credit. When Anthropic funded a study that showed their own product can harm learning when used without scaffolding, that's intellectual honesty. When OpenAI publishes research showing only benefits, scrutinize harder. Not because they're lying—because incentives shape what gets studied and what gets published.

Publication bias favors positive results. We don't know what studies were run and not published.

### 6. Check What's NOT Measured

The critical study that doesn't exist: longitudinal measurement of developer capability after extended AI use. Everything is either short-term (minutes to weeks) or cross-domain (medicine → software). We're making decisions based on:
- Small samples (n=16, n=52)
- Short timeframes (70 minutes, single sessions)
- Adjacent domains (colonoscopy as proxy for coding)
- Survey self-reports (perception, not performance)

These studies are rigorous within their constraints. The constraints are severe.

## The Vendor Incentive Problem

AI companies optimize for adoption. Adoption correlates with perceived productivity, not measured capability development. This creates a structural problem: the features that feel best may harm most.

Stack Overflow's survey revealed the tension: trust in AI accuracy fell from 43% to 33% in one year. Adoption rose from 76% to 84%. People use tools they don't trust. [See productivity evidence →](../reference/productivity-evidence)

Why? Because perceived productivity overrides measured performance. The perception gap makes bad tools feel good. Market incentives optimize for feel, not outcome.

## Applying This to cix Itself

Let's interrogate the claims this library makes.

**Claims with strong evidence:**
- AI tools improve immediate task performance (multiple large RCTs)
- AI tools can degrade learning when unrestricted (RCT, n=1,000)
- Critical thinking correlates negatively with AI confidence (n=319, structural modeling)
- Automation bias affects AI-assisted decisions (controlled experiments)

**Claims with moderate evidence:**
- The perception gap exists at scale (small rigorous study + survey data)
- Design patterns can preserve learning (small samples, promising but needs replication)
- Control and transparency predict appropriate trust (survey-based, large effects but self-report)

**Claims that are speculative:**
- Long-term capability effects on developers (no direct measurement, inferred from short-term and cross-domain)
- Magnitude of design interventions at scale (preliminary evidence only)
- Whether short-term effects compound or plateau over years

The methodology is to ground claims in sources while being explicit about inference gaps. When this library cites medical skill atrophy as evidence for developer capability risk, it's making a cross-domain inference. Plausible. Not proven. The evidence markers reflect that: moderate, not strong.

## Can Design Change Outcomes?

The research suggests yes—with caveats.

Same study, same technology, different design: when AI gave direct answers, students scored 17% worse on exams. When AI gave hints (not answers), no learning harm. <span class="ev ev-strong" title="Bastani et al. PNAS 2025, within-study comparison">●</span> Another pattern: attempt-first-then-AI achieved 86% mastery. Direct-to-AI did not. <span class="ev ev-moderate" title="Shen & Tamkin 2025, n=52, 70 minutes, promising but small">◐</span> [See collaboration design evidence →](../reference/collaboration-design-evidence)

User control was the strongest predictor of appropriate trust (β = 0.507), followed by transparency (β = 0.415). <span class="ev ev-moderate" title="Gerlich et al. 2025, survey-based but large effect sizes">◐</span> Not just nice-to-have features. Measurable effect sizes on calibration.

Same technology. Different interaction patterns. Opposite outcomes.

**The design principles that emerge:**
- Complementary over substitutive (amplify, don't replace)
- Transparency over opacity (show reasoning, not just results)
- Control over automation (human-initiated, not autonomous)
- Mastery-oriented over performance-oriented (optimize for learning, not output)
- Independent verification (generation and review must be separate)

These principles have evidence. Small studies, short timeframe, needs replication at scale. But they're testable hypotheses, not speculation. [See collaboration design evidence →](../reference/collaboration-design-evidence)

## The Questioning Imperative

Richard Feynman: "The first principle is that you must not fool yourself—and you are the easiest person to fool."

The research shows AI tools create tradeoffs: immediate productivity gains, potential long-term capability costs. Both can be true. The question is whether design choices change the trajectory.

The evidence says design matters. The evidence is preliminary. We're acting on best available knowledge while acknowledging its limits.

**What this means for using AI tools:**

1. **Measure, don't assume.** Perception diverges from reality. Track outcomes, not feelings.

2. **Question your own confidence.** Higher trust in AI predicts less verification. When you feel certain, verify harder.

3. **Check who benefits from the claim.** Vendors optimize for adoption. Adoption optimizes for perceived productivity. Neither optimizes for your capability.

4. **Preserve friction where it matters.** The effort that feels wasteful might be the effort that causes learning.

5. **Verify independently.** If AI generated it, review it without AI assistance. Explanations persuade. Verification requires separation.

6. **Ask what's not measured.** Short-term gains don't guarantee long-term capability. The critical study often doesn't exist yet.

## The Honest Position

This library exists because the evidence suggests AI tools, as commonly used, degrade the cognitive foundations that enable long-term capability. The evidence also suggests design changes outcomes. Small studies, promising patterns, needs replication.

That's the state of knowledge: grounded, preliminary, worth acting on. Not settled. Not speculative. Evidence with acknowledged limits.

The alternative—uncritical adoption based on perceived productivity—has evidence showing it fails. Larger studies. Consistent pattern. Worth avoiding.

**The goal:** Design AI tools that make humans more capable, not dependent. Preserve gains, avoid costs. Optimize for compounding mastery, not immediate output.

The research suggests this is possible. The research is preliminary. The methodology is to build extensions grounded in best available evidence while making uncertainty explicit.

Question everything—including this library. If you can't trace a claim to its source and evaluate that source yourself, you're trusting, not verifying. The evidence markers in this text are not decorative. They're invitations to check. [All evidence documented in reference section →](../reference/productivity-evidence)

The first step toward calibrated trust is recognizing when you've stopped questioning.
