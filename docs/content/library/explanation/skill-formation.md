# Skill Formation

The interaction pattern, not the technology, determines whether you learn.

---

You're learning a new Python library. You've never used Trio before—async programming, concurrency, error handling patterns all new to you. You have two hours to build a working prototype.

You could grind through the docs, hit errors, debug stack traces, slowly piece together how it works. Or you could ask Claude to generate the code, paste it in, ship it.

Both get you to working code. Only one leaves you more capable.

## The Six Patterns

Anthropic ran an experiment with 52 software engineers learning Trio. <span class="ev ev-moderate" title="RCT, n=52, Anthropic 2026">◐</span> Same AI assistant. Same task. Six different ways people chose to interact.

Three patterns preserved learning. Three destroyed it.

**Generation-Then-Comprehension** (86% mastery): Generate code with AI, then ask follow-up questions to understand what it did. "Why did you use `trio.open_nursery()` here? What happens if I remove this line?"

**Hybrid Code-Explanation** (68% mastery): Request explanations alongside code. "Show me how to handle timeouts in Trio and explain when each pattern applies."

**Conceptual Inquiry** (65% mastery): Only ask conceptual questions. Write all code yourself. "What's the difference between structured and unstructured concurrency?"

These three patterns have something in common: errors. Users hit TypeError exceptions, RuntimeWarnings, async context issues. They debugged them. That debugging is where learning happened.

Now the three patterns that failed:

**AI Delegation** (39% mastery): Ask AI to generate code, paste it, move on. Fastest completion time (19.5 minutes). Worst learning outcome.

**Progressive Reliance** (35% mastery): Start writing code yourself, gradually hand more to the AI as you realize it's faster. Watch your understanding erode in real-time.

**Iterative Debugging** (24% mastery): Have AI fix your errors without understanding what broke or why the fix works. The error message becomes a handoff, not a learning signal.

The gap between best and worst: **86% vs 24%**. Same AI. Same task. Different interaction choices.

## Errors Are the Curriculum

The control group—no AI access—encountered a median of 3 errors during the task. <span class="ev ev-moderate" title="Same RCT, n=52">◐</span> The AI group encountered 1.

Those two extra errors weren't obstacles. They were the lesson.

When you hit `TypeError: 'async for' requires an object with __aiter__ method`, you learn something about Python's async protocol. When you see `RuntimeWarning: Trio cannot be run from a running event loop`, you learn about execution contexts. When your timeout doesn't work, you learn about cancellation scopes.

AI users who delegated never encountered these. They copied working code and moved on. The code ran. They learned nothing about why.

The errors weren't bugs in the process. The errors *were* the process.

## What People Noticed

The participants who delegated to AI knew something was wrong:

- "I feel like I got lazy"
- "There are still a lot of gaps in my understanding"
- "I wish I'd taken the time to understand the explanations more"

They completed the task. They passed the immediate test—ship working code. But they failed the actual test: can you do this again without the AI?

The mastery assessment came later, after the task, without AI access. That's where the 86% vs 24% gap appeared. The people who delegated couldn't reconstruct what they'd built. They'd outsourced not just the typing, but the thinking.

## Productivity vs Capability

The AI Delegation pattern produced the fastest task completion. It also produced the worst learning.

The Generation-Then-Comprehension pattern took 23% longer. It produced 2.2x better learning outcomes.

This is the tradeoff: you can optimize for speed today or capability tomorrow.

If you're learning something new—a framework, a library, a domain—the interaction pattern determines which path you're on:

**Path 1: Capability compounds**
You generate code with AI, then interrogate it. Why this pattern? What does this function do? What happens if I change this parameter? You hit errors. You debug them. You emerge able to work in this domain with or without AI.

**Path 2: Dependency compounds**
You ask AI to solve the problem. You paste the solution. You move to the next problem. You complete tasks faster. Your ability to work independently atrophies. Six months later, you can't remember how any of it works without the AI.

The gap between these paths is measurable. It's not subtle. It's 86% mastery vs 24%.

## The Mechanism

Why does Generation-Then-Comprehension work when AI Delegation fails?

The difference is **error exposure**.

When you generate code and then ask questions, you're still in the loop. You see what the AI produced. You ask why. Those questions create cognitive load. You're forced to reconcile the code with your mental model. The mismatch triggers learning.

When you debug errors—even AI-generated code—you're building pattern recognition. This error message maps to this mistake. This warning means I misunderstood this concept. Over time, you internalize the library's execution model.

When you delegate fully, none of this happens. The code works. Your mental model stays shallow. You never reconcile anything because you never look closely enough to notice the gaps.

The AI becomes a black box. Put problem in, get solution out. Learning requires opening the box.

## What This Means

If you're building something you already know how to build, AI acceleration makes sense. Generate, review, ship.

If you're learning something new, the pattern shifts:

1. **Ask the AI to generate**, but don't stop there
2. **Ask follow-up questions** about what it produced
3. **Let errors happen**—they're teaching you
4. **Debug with understanding**, not just iteration

The goal isn't to avoid AI. The goal is to use it in ways that make you more capable, not more dependent.

The difference between 86% and 24% mastery is entirely within your control. It's not about the AI. It's about how you choose to interact with it.

---

[Full skill formation evidence →](../reference/skill-formation-evidence)
