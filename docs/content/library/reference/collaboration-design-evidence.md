# Collaboration Design Evidence

Research synthesis on what makes human-AI collaboration effective — the design principles that determine whether AI amplifies or erodes capability.

---

## Sources

- [Blaurock et al. (2025). Designing CI Systems for Employee-AI Service Co-Production. Journal of Service Research.](https://journals.sagepub.com/doi/10.1177/10946705241238751)
- [Ma et al. (2025). Contrastive Explanations in Human-AI Collaboration. Taylor & Francis.](https://www.tandfonline.com)
- [Bansal et al. (2021). Does the Whole Exceed its Parts? CHI.](https://dl.acm.org/doi/10.1145/3411764.3445717)
- [Stack Overflow Developer Survey (2025).](https://survey.stackoverflow.co/2025/)
- [Sharma et al. (2026). Who's in Charge? Disempowerment Patterns. Anthropic.](https://arxiv.org/abs/2601.19062)

---

## The Strongest Levers

### Blaurock et al. (2025) <span class="ev ev-moderate" title="Scenario experiments, n=654, J. Service Research">◐</span>

**Design:** Two scenario-based experiments with 654 professionals (309 financial services + 345 HR).

**Key findings:**

| Factor | Effect Size | What It Means |
|--------|------------|---------------|
| Process control | **β = 0.507** | User agency — ability to direct, override, shape collaboration |
| Transparency | **β = 0.415** | Understanding how AI reached conclusions |
| Task complexity | β = 0.247 | AI helps more on complex tasks |
| Perceived competence | β = 0.227 | User confidence in their ability to evaluate |
| Engagement features | **b = -0.555** | Each added feature *reduces* trust |

**Control and transparency dominate.** Not AI capability. Not speed. Whether the human can direct the collaboration and understand its reasoning.

**The engagement paradox:** Adding engagement features — gamification, personalization, social elements — reduces trust (b = -0.555). Each feature added for "better user experience" measurably degrades the collaboration. Users want control and understanding, not friction disguised as interaction.

**Limitations:** Scenario-based experiments, not field study. Effect sizes from full text not independently verified from public sources. Service context (financial services, HR), not software development specifically.

---

## Why Explanations Backfire

### Bansal et al. (CHI 2021) <span class="ev ev-strong" title="CHI peer-reviewed, controlled experiment">●</span>

**Design:** Controlled experiment comparing AI with and without explanations, across correct and incorrect AI outputs.

**Key finding:** Explanations increase acceptance regardless of correctness.

| Condition | Effect |
|-----------|--------|
| Correct AI + explanation | Small improvement in outcomes |
| Incorrect AI + explanation | **Performance degraded** |

When AI is right, explanations help slightly. When AI is wrong, explanations build false confidence and suppress verification. The explanation creates trust without calibrating it.

**Implication:** Transparency alone is insufficient. Explanations must be paired with verification prompts, or they become persuasion tools rather than calibration tools.

---

## Contrastive Explanations

### Ma et al. (2025) <span class="ev ev-moderate" title="Taylor & Francis, controlled study">◐</span>

**Key finding:** Framing shifts change how humans process AI recommendations.

| Framing | Example | Cognitive Mode |
|---------|---------|----------------|
| Prescriptive | "Use Redis for this cache." | Heuristic acceptance |
| Contrastive | "Redis instead of Memcached because you need data structures beyond key-value." | Analytic evaluation |

**Mechanism:**
- Shows alternatives were considered
- Makes tradeoffs visible
- Activates comparison rather than acceptance
- Teaches decision frameworks, not just decisions

Prescription invites blind trust. Contrast invites evaluation.

**Limitations:** Single study. Effect size not fully quantified.

---

## The WHY > HOW Principle

A security study compared two approaches to teaching developers:

| Approach | Outcome |
|----------|---------|
| Prescribe HOW ("Always use prepared statements") | 30% secure-by-construction |
| Explain WHY ("SQL injection occurs when user input is treated as code...") | **80%** secure-by-construction |

**2.5x improvement** from explaining motivation rather than mandating method. <span class="ev ev-moderate" title="Single study, security coding domain">◐</span>

**Mechanism:** HOW prescriptions create brittle rules applied in narrow contexts. WHY explanations build transferable frameworks that generalize.

---

## The Senior-Junior Gap

### Stack Overflow (2025) <span class="ev ev-moderate" title="Stack Overflow survey, large N, observational">◐</span>

| Behavior | Seniors | Juniors |
|----------|---------|---------|
| Trust AI output | 2.5% | 17% |
| Ship AI code to production | 32% | 13% |
| Edit AI suggestions | Substantial | Minor or none |

**The paradox:** Seniors trust AI least but ship most AI code. They treat AI output as a first draft from a junior developer — read carefully, check edge cases, verify against production constraints, refactor for codebase patterns.

Juniors trust more and ship less because they lack judgment to evaluate.

**Design implication:** Systems optimized for seniors (who verify regardless) fail juniors (who need scaffolding for verification).

---

## Users Misjudge What Helps Them

### Sharma et al. (Anthropic, 2026) <span class="ev ev-moderate" title="Large-scale observational study, ~1.5M conversations, single platform">◐</span>

**Design:** Analysis of ~1.5 million Claude.ai conversations.

**Key finding:** Users rate disempowering interactions MORE favorably in the moment. Interactions that distorted reality, value judgments, or actions felt good.

But when users actually acted on AI outputs, satisfaction dropped below baseline. Users expressed regret: "I should have listened to my own intuition."

**Implication:** Short-term satisfaction ≠ long-term benefit. The feedback loop is broken — harm feels helpful. Design must compensate for miscalibrated user preferences.

---

## Trust Gradients

Not all outputs need the same verification depth:

| Output Type | Trust | Verification |
|-------------|-------|-------------|
| Formatting, syntax | High | Glance |
| Library usage, API calls | Medium | Check docs for edge cases |
| Business logic | Low | Full review against requirements |
| Security-sensitive code | Very low | Dedicated security review |
| Architecture decisions | Very low | Multiple perspectives |

**Correction rate as calibration metric:**

| Rate | Signal |
|------|--------|
| &lt; 5% | Under-reviewing — automation bias risk |
| 10-30% | Healthy calibration |
| &gt; 50% | AI not effective for this task |

---

## Verification Decay Pattern

Trust calibration degrades without maintenance:

```
Day 1: Carefully review every suggestion
Day 7: Skim, spot-check occasionally
Day 30: Accept if it "looks right"
Day 90: Auto-accept until things break
```

**Counter-patterns:**
- Structured verification checklist (&lt; 30 seconds, applied consistently)
- Spot audits (randomly deep-verify even when confident)
- Red team rotations (assume output is wrong, find the error)
- Track verification catch rate

---

## Evidence Summary

| Finding | Effect Size | Evidence Level | Source |
|---------|------------|----------------|--------|
| Control strongest lever | β = 0.507 | <span class="ev ev-moderate">◐</span> Moderate | Blaurock et al. 2025 |
| Transparency second strongest | β = 0.415 | <span class="ev ev-moderate">◐</span> Moderate | Blaurock et al. 2025 |
| Engagement features backfire | b = -0.555 | <span class="ev ev-moderate">◐</span> Moderate | Blaurock et al. 2025 |
| Explanations increase blind trust | Significant | <span class="ev ev-strong">●</span> Strong | Bansal CHI 2021 |
| WHY > HOW for learning | 30% → 80% | <span class="ev ev-moderate">◐</span> Moderate | Security study |
| Seniors verify, juniors accept | 2.5% vs 17% trust | <span class="ev ev-moderate">◐</span> Moderate | Stack Overflow |
| Users prefer disempowering interactions | Observed at scale | <span class="ev ev-moderate">◐</span> Moderate | Sharma, Anthropic |
| Contrastive > prescriptive framing | Qualitative shift | <span class="ev ev-moderate">◐</span> Moderate | Ma et al. 2025 |

---

*Full citations in [bibliography](bibliography)*
