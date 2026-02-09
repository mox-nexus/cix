# The Path Forward

Evidence-based practices that preserve human capability while using AI effectively.

---

## Sources

- [Shen & Tamkin (2026). How AI Impacts Skill Formation. Anthropic.](https://arxiv.org/pdf/2601.20245)
- [Freise et al. (2025). Job Crafting with AI. HICSS.](https://hdl.handle.net/10125/107542)
- [Lee et al. (2025). The Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/full/10.1145/3706598.3713778)
- [Tomisu et al. (2025). Cognitive Mirror. Frontiers in Education.](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1510919/full)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2422633122)
- [Budzyń et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)
- [Pallant et al. (2025). Mastery Orientation. ACU Research Bank.](https://doi.org/10.3316/informit.106046894747026)

---

## Abstract

The problem is real. The solutions are also real.

AI generates code, then the human asks follow-up questions — 86% mastery. AI generates, human accepts — 39% mastery. <span class="ev ev-moderate" title="RCT, n=52, Anthropic 2026">◐</span> The technology is identical. The variable is engagement, not who generates the code.

Developers who assign AI to mundane work while reserving hard problems for themselves upskill. Developers who delegate hard problems to AI atrophy. <span class="ev ev-moderate" title="HICSS 2025, qualitative study">◐</span> The differentiator is task allocation.

Mastery-oriented users maintain critical thinking at 35.7x the odds of performance-oriented users. <span class="ev ev-moderate" title="Single study, odds ratio">◐</span> The largest effect size in the literature. Frame interactions as learning, not just task completion, and capability compounds instead of eroding.

Three months of AI-assisted work produces measurable skill degradation. <span class="ev ev-moderate" title="Lancet crossover RCT, medical domain">◐</span> Relearning takes less than 50% of original training time. <span class="ev ev-moderate" title="Cognitive science, multiple studies">◐</span> Periodic unassisted work prevents atrophy. Weekly practice maintains skills; quarterly deep work rebuilds them.

---

## Explanation

The research doesn't just document what fails. It shows what works.

### Generation-Then-Comprehension

**Source:** Shen & Tamkin (Anthropic 2026)

The highest-performing interaction pattern wasn't writing code without AI. It was AI generates, then human comprehends through questioning.

| Interaction Pattern | Mastery Score | What Happened |
|---------------------|---------------|---------------|
| Generation-Then-Comprehension | 86% | AI generated code → human asked follow-up questions |
| Hybrid Code-Explanation | 68% | Human requested explanations alongside code |
| Conceptual Inquiry | 65% | Human asked conceptual questions, wrote code themselves |
| AI Delegation | 39% | Human accepted AI code without engagement |
| Progressive Reliance | 35% | Human started writing, gradually delegated more |
| Iterative Debugging | 24% | AI fixed errors repeatedly without explanation |

**The insight:** AI generation is not the problem. Disengagement is the problem.

The 86% mastery group generated code faster than the no-AI control group while learning more than those who wrote code themselves. They leveraged speed AND built understanding. The failure mode isn't accepting AI output — it's accepting without comprehending.

**Pattern in practice:**

```
✅ Human: "Explain how this async pattern handles cancellation."
✅ Human: "Walk me through why you chose this data structure."
✅ Human: "What edge cases does this miss?"

❌ Human: "Looks good." [paste, commit, move on]
```

For learning contexts where foundational schema must be built, the interaction flips — human generates, AI critiques. <span class="ev ev-moderate" title="Same RCT, task variation">◐</span> This builds generative capability directly. But for established practitioners, AI generation followed by active comprehension is both faster and more educational.

### Job Crafting

**Source:** Freise et al. (HICSS 2025)

Two task allocation patterns produce opposite outcomes.

**Approach Crafting** — assign AI to mundane work, reserve hard problems for yourself:

```
AI: Boilerplate, CRUD, formatting, test scaffolding
Human: Architecture, domain models, edge cases, design decisions
```

Result: Human practices hard skills more, not less. AI removes friction that consumed cognitive budget. Skills compound.

**Avoidance Crafting** — use AI to avoid cognitively demanding tasks:

```
AI: Complex algorithms, architecture, debugging hard problems
Human: Review, simple implementations, routine changes
```

Result: Human stops practicing the skills that matter most. Capability erodes. AI becomes essential because the human is no longer capable without it.

**The differentiator:** Not usage frequency. Not AI capability. What the human reserves for themselves.

| Reserved for Human | Trajectory |
|-------------------|-----------|
| Hard cognitive work (architecture, design, analysis) | Upskilling |
| Review and approval only | Atrophy |

**Implementation:**

When an AI offers to handle something, ask: "Is this routine or is this where I learn?"

- Routine → delegate
- Cognitively challenging → keep

The goal is more hard problems per day, not fewer. AI should free bandwidth to tackle harder challenges, not eliminate challenge entirely.

### Mastery Orientation

**Source:** Pallant et al. (2025)

Frame interactions as learning opportunities, not just task completion.

| Orientation | Critical Thinking Maintenance |
|------------|------------------------------|
| Mastery (focused on learning) | OR = 35.7 |
| Performance (focused on output) | Baseline |

Odds ratio of 35.7 is the largest effect size in the collaborative AI literature. <span class="ev ev-moderate" title="Single study, odds ratio">◐</span> It dominates control (β = 0.507) and transparency (β = 0.415) — the second and third strongest levers.

**What mastery orientation looks like:**

```
Performance: "Get this done fast."
Mastery: "What can I learn from this?"

Performance: "Did it work?"
Mastery: "Why did it work?"

Performance: "Ship and move on."
Mastery: "What's the transferable principle?"
```

**Implementation for extensions:**

Frame every interaction as a learning moment:

```
✅ "Let's understand why this approach works..."
✅ "What's the transferable principle here?"
✅ "Where might this pattern break down?"

❌ "Here's the solution."
❌ "This will work."
```

The subtle shift from "getting it done" to "learning while getting it done" changes everything.

### Recovery Protocols

**Source:** Budzyń et al. (Lancet 2025), cognitive science literature

Measurable skill degradation occurs in 3 months of AI-assisted work. <span class="ev ev-moderate" title="Lancet crossover RCT, medical domain">◐</span> But skills aren't permanently lost — they're dormant. Relearning takes less than 50% of original training time (the Savings Effect). <span class="ev ev-moderate" title="Cognitive science, multiple studies">◐</span>

Three evidence-based approaches:

**1. Switch-Off Protocol**

Periodic work without AI assistance.

| Frequency | Duration | Purpose |
|-----------|----------|---------|
| Weekly | 2-4 hours | Maintain baseline capability |
| Monthly | Full day | Test independent function |
| Quarterly | Complex task end-to-end | Deep capability assessment |

The work must be cognitively challenging. Doing easy tasks without AI doesn't exercise the skills at risk. Architecture decisions, debugging complex issues, designing from scratch — these maintain the capabilities most vulnerable to atrophy.

**2. Simulator Protocol**

Attempt-first before AI consultation. <span class="ev ev-speculative" title="Aviation training analogy + Bastani PNAS findings">◌</span>

```
Before AI assistance: 15-30 minutes of independent effort
"What's your diagnosis?"
"Walk me through your approach."
```

The effort itself is valuable, even if the conclusion is wrong. This preserves problem-solving practice while still leveraging AI for efficiency. The human works harder per problem, but solves more problems per day.

**3. Hybrid Protocol**

Generation-Then-Comprehension as daily practice (see above). AI generates, human comprehends through questioning. Speed is preserved, understanding compounds.

### Metacognitive Scaffolding

**Source:** Lee et al. (CHI 2025), Tomisu et al. (2025)

Three techniques that restore critical engagement.

**1. PME Friction** — Planning, Monitoring, Evaluation checkpoints

| Phase | Prompt | Effect |
|-------|--------|--------|
| Planning | "What's your approach before I assist?" | Preserves generative step |
| Monitoring | "Does this match what you expected?" | Maintains engagement |
| Evaluation | "What would you change next time?" | Crystallizes learning |

Lee et al. found three-component friction significantly restored metacognitive engagement that was otherwise suppressed by AI confidence. <span class="ev ev-strong" title="CHI peer-reviewed, n=319, SEM">●</span> Single-point friction was insufficient — all three phases needed.

**2. Cognitive Mirror** — reflect reasoning back with questions

Instead of answering directly, mirror the human's thinking:

```
Human: "Should I use Redis or PostgreSQL for this cache?"

Substitutive: "Use Redis — it's faster for caching."

Cognitive Mirror:
"You're thinking about caching. Let me reflect what I see:
- You have a read-heavy workload
- You mentioned durability matters for this data
- You're already running PostgreSQL

What's driving the instinct toward Redis specifically?
What happens if the cache goes down?"
```

This forces articulation of reasoning, evaluation of logic, and discovery of gaps. The human builds transferable frameworks instead of receiving one-time answers. <span class="ev ev-moderate" title="Frontiers in Education, qualitative study">◐</span>

**3. Confidence-Competence Calibration**

Two confidence signals with opposite effects:

| Confidence Type | Effect on Critical Thinking | Mechanism |
|----------------|----------------------------|-----------|
| AI-confidence (trust in AI) | β = -0.69 | "AI is reliable" → cognitive offloading |
| Self-confidence (trust in self) | β = +0.35 | "I can evaluate" → active engagement |

**Design response:** Reduce AI-confidence signals, boost self-confidence signals.

```
❌ "The answer is X." (projects authority)
✅ "Based on what I see, X seems right — but you have
    context I lack. What does your experience suggest?"
```

High AI confidence → low human engagement. Moderate AI confidence + high self-confidence → sustained thinking quality. <span class="ev ev-strong" title="CHI peer-reviewed, n=319, SEM">●</span>

### Novice Protection

**Source:** Bastani et al. (PNAS 2025)

Direct AI answers harm learning for novices. Hint-only AI shows no harm. <span class="ev ev-strong" title="RCT, n=1,000, PNAS">●</span>

| Experience Level | Recommended Interaction | Why |
|-----------------|------------------------|-----|
| Novice (0-2 years) | Hint-only, Socratic, explain reasoning | Schema not yet formed |
| Intermediate (2-5 years) | Collaborative with verification | Schema needs reinforcement |
| Expert (5+ years) | Full collaboration | Schema robust |

**What this looks like:**

```
Novice request: "How do I handle null?"

❌ "Add if (value != null) on line 12."
✅ "What happens when this function receives null?
    Walk me through the execution."
```

The novice must build mental models of program execution, debugging intuition, design reasoning. These form through struggle. Providing solutions prevents formation of the schema that makes someone capable.

For intermediates and experts, full collaboration preserves capability because the schema already exists. The judgment to evaluate AI output is present. For novices, it isn't yet.

### Protective Factors

Characteristics that predict maintained capability during AI use:

| Factor | Effect | Mechanism |
|--------|--------|-----------|
| Skepticism | Maintains verification | Senior devs trust AI least (2.5%) but use effectively |
| Second-reader approach | Treats AI output as draft | Preserves evaluative practice |
| Deep domain expertise | Can evaluate meaningfully | Judgment precedes collaboration |
| Active direction | Tells AI what to do | Preserves agency |
| High self-confidence | β = +0.35 for critical thinking | Willing to override AI |

The pattern: users who maintain capability treat AI as a tool they control, not an authority they obey.

**Implication:** Extensions should support active direction, encourage verification, surface uncertainty, and affirm the human's capability to evaluate.

### The Scaffolding Metaphor

**Source:** Vygotsky's Zone of Proximal Development

Scaffolding in construction is temporary support designed to be removed. The goal is a building that stands alone.

AI collaboration should work the same way. The goal isn't permanent dependency. The goal is temporary support that enables capability the human couldn't achieve alone — then becomes unnecessary as that capability internalizes.

```
Day 1: AI explains async patterns, human doesn't yet understand
Week 2: AI reminds of edge cases, human catches most
Month 3: Human designs async patterns fluently, AI rarely needed
```

If the pattern goes the other direction — more dependency over time — the design has failed.

### Success Metrics

How to know if collaboration is working:

**Positive signals:**
- "I would approach this differently now than a month ago"
- "I caught an error in AI output I wouldn't have noticed before"
- "I understand why this works, not just that it works"
- Human spends more time on harder problems than before

**Warning signals:**
- "I don't know how I'd do this without AI"
- "I trust the output without checking"
- "I feel less confident in my judgment than before"
- Difficulty working unassisted for short periods

The goal is compounding capability, not compounding dependency.

---

## Key Principles

Synthesizing the evidence into actionable guidance:

1. **Engagement over generation** — Who generates code matters less than whether the human comprehends it. AI can generate; the human must understand.

2. **Reserve hard problems** — Delegate routine work. Keep cognitively challenging work. The hard work is where learning happens.

3. **Frame as learning** — Mastery orientation (OR = 35.7) dominates all other factors. "What can I learn?" beats "how fast can I ship?" for long-term capability.

4. **Practice unassisted** — Weekly 2-4 hours maintains skills. Monthly full days test capability. Quarterly complex tasks rebuild atrophied skills.

5. **Scaffold, don't substitute** — Temporary support that builds capability, not permanent crutches that create dependency.

6. **Protect novices** — Hints and explanations build schema. Direct answers prevent formation of foundational understanding.

7. **Surface uncertainty** — High AI confidence reduces human thinking. Show reasoning, acknowledge limits, invite verification.

8. **Multiple checkpoints** — Planning, monitoring, evaluation. Single-point friction is insufficient.

These aren't expensive. They require intentionality in design.

---

## The Hope

The problem is real. Cognitive offloading is real. Skill atrophy is real. Perception gaps are real.

The solutions are also real.

AI that explains its reasoning maintains critical thinking. AI that invites questions builds understanding. AI that surfaces uncertainty preserves verification. AI that frames interactions as learning produces 35.7x better outcomes than AI that optimizes for task completion.

The same technology, designed differently, produces opposite trajectories. Not "use AI less" — use AI differently. Generation-Then-Comprehension users learned more than those who worked without AI while completing tasks faster. Both learning and productivity increased.

The path forward exists. The evidence shows what works. The question is whether the defaults we establish now create positive or negative compounding.

Design determines the trajectory.
