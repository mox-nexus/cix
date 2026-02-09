# Craft Explanations: Design Methodology

This document explains WHY the craft-explanations plugin is designed the way it is.

## The Core Insight: Simultaneous Encoding

Traditional explanation design treats teaching as sequential disclosure: first the principle, then the pattern, then the practice. This maps to pedagogical frameworks like Bloom's taxonomy (remember -> understand -> apply) or progressive disclosure (overview -> details -> depth).

The craft-explanations plugin is built on a different insight: **good explanations carry all three dimensions simultaneously**. The receiver pulls what they need based on their current orientation.

This insight comes from the Hindu philosophical framework of the three gunas (Samkhya/Bhagavad Gita):

- **Sattvic** = principle, abstraction, impact over time
- **Rajasic** = pattern, category, relational structure
- **Tamasic** = practice, concrete action, implementation

These aren't quality levels (good/neutral/bad). They're dimensions of perception. All three are present in every phenomenon. The observer's orientation determines which dimension they engage with.

Applied to explanations: the same paragraph can simultaneously convey:
- What to do (practice)
- How it connects to other things (pattern)
- Why it matters (principle)

The reader enters through whichever dimension matches their current need.

## Why "Route, Don't Teach"

The skill files are deliberately lean routing tables rather than comprehensive methodology documents. This is based on two findings:

1. **Prompting Inversion** (arXiv 2510.22251): Explicit procedural constraints on frontier models can *reduce* performance. WHY framing improves from 31.5% to 97.3% vs HOW framing. Compressed behavior triggers achieve 46% token reduction with no quality loss.

2. **Expertise Reversal Effect** (Tetzlaff 2025, n=5,924): What helps novices (high guidance, d=0.505) actively harms experts (d=-0.428). Claude already knows CLT, Diataxis, Feynman technique, etc. Teaching them again wastes tokens and can degrade performance.

The skill tells Claude WHEN to use which technique and WHY — not HOW to apply them.

## Why Four Agents with Different Entry Doors

Initial design mapped agents 1:1 to dimensions: Feynman = practice, Tufte = pattern, Sagan = principle. This was rejected because it decomposes the simultaneous encoding back into sequential traversal.

Instead, each agent enters through a different door but carries ALL three dimensions:

- **Feynman** enters through practice (example-first) but surfaces pattern and principle
- **Sagan** enters through principle (wonder) but grounds in pattern and practice
- **Tufte** enters through pattern (visual structure) but serves practice and principle
- **Socrates** is meta — forces the receiver to traverse all dimensions through questioning

The difference between agents is the entry point, not the content of what they produce.

## Why "Modal Lock" Is the Key Anti-Pattern

Modal lock is Claude's specific failure mode: defaulting to sattvic-rajasic encoding (clean taxonomies, headers, bullet structures) and amplifying the same mode when it doesn't land.

This matters because:
- Most explanation failures aren't knowledge gaps — they're encoding mismatches
- The fix is shifting to the missing dimension, not adding more of what's already there
- "Shift, don't add" is the core correction principle

## Research Base

Key findings informing the design:

| Finding | Source | Design Implication |
|---------|--------|-------------------|
| Coherence principle d=0.86 | Mayer, 23/23 tests | Cut extraneous material ruthlessly |
| Expertise reversal d=0.505/-0.428 | Tetzlaff 2025, n=5,924 | Detect expertise, adapt guidance level |
| WHY framing 31.5% -> 97.3% | Prompting Inversion, arXiv | Route and explain why, don't prescribe how |
| CoVe +23% accuracy | Dhuliawala et al. 2024 | Independent verification prevents hallucination |
| Feynman Bot 1.8x learning | Demszky et al. 2025 | Example-first teaching works |
| Contrastive explanations | Miller 2019 | "Why X, not Y?" is more effective than "Why X?" |

## Sources

- Bastani et al. (2025). Generative AI without guardrails can harm learning. PNAS.
- Dhuliawala et al. (2024). Chain-of-Verification Reduces Hallucination. ACL.
- Miller, T. (2019). Explanation in Artificial Intelligence: Insights from the Social Sciences. AI Journal.
- Tetzlaff et al. (2025). Expertise Reversal Effect meta-analysis. n=5,924.
- arXiv:2510.22251. Prompting Inversion for frontier models.
- Mayer, R. (2009). Multimedia Learning. Cambridge University Press.
- Nielsen Norman Group. F-pattern, scanning, information architecture research.
- Samkhya/Bhagavad Gita. Three gunas philosophical framework.
