# Hype & Questioning

The productivity claims are real and so are their limits — here's how to read both, including the claims this library makes.

---

## Automation Bias

Before the checklist, one mechanism worth naming: **automation bias**. The tendency to favor machine-generated output over contradictory information from other sources — even when you know better.

You've experienced it with GPS. You take the suggested route even when you know a shortcut exists. AI coding tools trigger the same mechanism, at industrial scale.

What makes it insidious: when AI provides explanations along with answers, people rely on those answers more — regardless of whether the AI is correct. <span class="ev ev-strong" title="Bansal et al. CHI 2021, controlled experiment with correct and incorrect AI">●</span> Correct AI with explanations: helps slightly. Incorrect AI with explanations: performance degrades. Explanations feel like transparency. They function as persuasion.

This scales up: higher AI confidence predicts less critical thinking (β = -0.69). <span class="ev ev-strong" title="Lee et al. CHI 2025, n=319, structural equation modeling">●</span> Not "some people verify less." Systematic correlation. The confidence-competence inversion: making AI better at appearing confident makes humans worse at being competent.

The checklist below exists because automation bias applies to research too. Including AI research.

## Reading AI Research Without Getting Fooled

### 1. Check the Sample Size

n=16 tells you something different than n=4,867. Small samples can be rigorous — but they're exploratory, not definitive. When you see a claim, the first question is: how many people were actually studied?

The perception gap study (experienced developers predicted 24% faster, measured 19% slower) used n=16 developers. Rigorous within-subject design, meaningful finding, limited generalizability. The productivity gains study used n=4,867 across multiple trials. Both are cited in this library. They don't carry equal weight.

### 2. Check the Study Design

Hierarchy of evidence:
- **Randomized controlled trial (RCT)** — assigns participants randomly, controls for confounds
- **Controlled experiment** — manipulates variables but less random assignment
- **Observational study** — watches what happens naturally, can't prove causation
- **Survey** — self-report, subject to perception bias
- **Anecdote** — individual experience, not generalizable

When a vendor says "our tool improves productivity," ask: compared to what? How was that measured? Who did the measuring?

### 3. Check Domain Transfer

A multicentre observational study found endoscopists' unaided detection rate declined 20% after regular AI-assisted colonoscopy was introduced. <span class="ev ev-moderate" title="Budzyń et al. Lancet 2025, multicentre observational, 19 endoscopists">◐</span> Does that apply to developers using AI coding assistants? Maybe. The mechanism is plausible — skill atrophy from automation. The magnitude is uncertain — different domains, different task structures.

This library treats it as moderate evidence, not strong. The mechanism is credible. The transfer is uncertain. That distinction matters.

### 4. Check the Timeframe

A 70-minute session tells you something. It doesn't tell you what happens after six months of daily use.

Most AI-and-learning research measures effects over minutes to weeks. The critical question — developer capability after 6-12 months of daily AI use — has no direct measurement. We're inferring from short-term learning studies and cross-domain analogies. Reasonable inference. Still inference.

### 5. Check Who Funded It

Vendor-funded research showing harm deserves credit. When Anthropic funded a study showing their own product can harm learning when used without scaffolding, that's intellectual honesty. When a company publishes research showing only benefits, scrutinize harder. Not because they're lying — because incentives shape what gets studied and what gets published.

Publication bias favors positive results. We don't know what studies were run and quietly shelved.

### 6. Check What's NOT Measured

The critical study that doesn't exist: longitudinal measurement of developer capability after extended AI use. Everything is either short-term (minutes to weeks) or cross-domain (medicine to software). Current decisions rest on:
- Small samples (n=16, n=52)
- Short timeframes (70 minutes, single sessions)
- Adjacent domains (colonoscopy as proxy for coding)
- Survey self-reports (perception, not performance)

These studies are rigorous within their constraints. The constraints are severe.

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

When this library cites medical skill atrophy as evidence for developer capability risk, it's making a cross-domain inference. Plausible. Not proven. The evidence markers reflect that: moderate, not strong.

## The Vendor Incentive Problem

AI companies optimize for adoption. Adoption correlates with perceived productivity, not measured capability development. This creates a structural problem: the features that feel best may harm most.

Stack Overflow's developer survey: trust in AI accuracy fell from 43% to 33% in one year. Adoption rose from 76% to 84%. People use tools they don't trust. [See productivity evidence →](../reference/productivity-evidence)

The perception gap makes bad tools feel good. Market incentives optimize for feel, not outcome.

## What to Do With This

1. **Measure, don't assume.** Perception diverges from reality. Track outcomes, not feelings.

2. **Question your own confidence.** Higher trust in AI predicts less verification. When you feel certain, verify harder.

3. **Check who benefits from the claim.** Vendors optimize for adoption. Adoption optimizes for perceived productivity. Neither optimizes for your capability.

4. **Preserve friction where it matters.** The effort that feels wasteful might be the effort that causes learning.

5. **Verify independently.** If AI generated it, review it without AI assistance. Explanations persuade. Verification requires separation.

6. **Ask what's not measured.** Short-term gains don't guarantee long-term capability. The critical study often doesn't exist yet.

---

The evidence markers in this library are not decorative. They're invitations to check. If you can't trace a claim to its source and evaluate that source yourself, you're trusting, not verifying.

Feynman: "The first principle is that you must not fool yourself — and you are the easiest person to fool."

[All evidence documented in reference section →](../reference/productivity-evidence)
