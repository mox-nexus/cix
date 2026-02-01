# Skill Formation

How AI assistance affects learning and capability development.

---

## Sources

- [Shen & Tamkin (2026). How AI Impacts Skill Formation. Anthropic.](https://arxiv.org/pdf/2601.20245)
- [Anthropic (2026). AI Assistance and Coding Skills.](https://www.anthropic.com/research/AI-assistance-coding-skills)

---

## Abstract

AI assistance produces productivity gains but impairs skill acquisition. In a randomized experiment with 52 software engineers learning a new Python library, AI users scored 17% lower on mastery assessments (d = 0.738, p = 0.01) without significant speed improvement.

Six distinct interaction patterns emerged. Three preserved learning (65-86% scores): asking conceptual questions only, requesting explanations with code, or generating code then asking follow-up questions. Three impaired learning (24-39% scores): full delegation, progressive reliance, or iterative AI debugging.

The control group encountered more errors and spent more time debugging — this is where learning happened. AI users who delegated finished fastest but learned least.

---

## Explanation

This is Anthropic's own research confirming that *how* you use AI determines whether you learn.

**The interaction patterns matter more than AI access itself.**

| Pattern | Score | What they did |
|---------|-------|---------------|
| Generation-Then-Comprehension | 86% | Generated code, then asked follow-up questions to understand it |
| Hybrid Code-Explanation | 68% | Asked for explanations alongside code |
| Conceptual Inquiry | 65% | Only asked conceptual questions, wrote code themselves |
| AI Delegation | 39% | Asked AI to generate code, pasted it, moved on |
| Progressive Reliance | 35% | Started writing code, gradually delegated more |
| Iterative Debugging | 24% | Had AI fix errors repeatedly without understanding |

**Why errors matter:**

The control group (no AI) encountered median 3 errors vs 1 for AI users. Those errors — especially Trio-specific ones like TypeError and RuntimeWarning — forced understanding of how the library actually works.

AI users who delegated never hit those errors. They completed the task without learning anything about async patterns, error handling, or the library's execution model.

**Participant self-awareness:**

AI users knew something was wrong:
- "I feel like I got lazy"
- "There are still a lot of gaps in my understanding"
- "I wish I'd taken the time to understand the explanations more"

**The implication:**

Productivity and learning are not the same thing. The fastest completion (AI Delegation, 19.5 min) produced the worst learning (39%). The best learning (Generation-Then-Comprehension, 86%) took longer (24 min) but built actual capability.

If you're learning something new, how you interact with AI determines whether you come out more capable or just more dependent.
