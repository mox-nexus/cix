# The Problem

AI reliably improves task completion while degrading the capabilities that enable independent work.

---

## Sources

- [METR (2025). Measuring AI Impact on Developer Productivity. RCT.](https://arxiv.org/abs/2507.09089)
- [Lee et al. (2025). Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/10.1145/3613904.3641913)
- [Budzyń et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2413913122)
- [Cui/Demirer et al. (2024). Effects of Generative AI on High Skilled Work. RCTs.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4671691)
- [Stack Overflow Developer Survey (2024-2025).](https://survey.stackoverflow.co/2024/)

---

## Abstract

People complete 26% more tasks with AI assistance (Cui/Demirer, n=4,867). They also score 17% worse on unassisted assessments (Bastani, n=1,000) and lose 20% of skill proficiency after three months of AI use (Budzyń).

The perception gap compounds the problem. Experienced developers predicted AI would make them 24% faster; measurements showed they were 19% slower — a 43-point gap between perception and reality (METR). Trust in AI coding accuracy dropped from 43% to 33% in one year, yet adoption rose from 76% to 84% (Stack Overflow). People use tools they don't trust, perceive benefits they don't get.

Confidence in AI negatively correlates with critical thinking (β = -0.69, Lee). The more you rely on AI, the less you verify it. The less you verify, the more errors propagate.

---

## Explanation

**The paradox is structural, not incidental.**

AI shifts cognitive work from generation to verification. Writing from scratch disappears. Reviewing mostly-correct output appears. This feels easier because the hard part (creation) is gone. But catching subtle errors in plausible-looking code demands sustained attention — a different kind of hard.

Seniors edit AI output enough to offset time savings (30% vs 17% for juniors). They ship 2.5x more AI code to production despite lower trust. They have the judgment to verify; juniors don't.

The productivity illusion persists because generation was visible effort. Verification is invisible effort. The work feels lighter even when it isn't. And the perception gap prevents correction — you can't fix what you don't notice.

**Three mechanisms drive hollowing:**

*Cognitive offloading.* When AI handles thinking, humans stop doing it. Kosmyna's MIT study showed this neurologically — 83% couldn't recall content from their own AI-assisted writing. They didn't forget. They never encoded it.

*Trust without calibration.* Explanations increase acceptance regardless of correctness (Bansal, CHI 2021). When AI is right, explanations help slightly. When AI is wrong, performance degrades. Trust rises; verification falls.

*Skill atrophy.* Skills require practice. Remove the practice, lose the skill. The Lancet study is cleanest: 20% detection rate decline in 12 weeks after AI removal. No equivalent study exists for developers — the technology is too new. But the cognitive mechanisms are identical.

**The perception gap prevents correction.**

People don't notice degradation. They feel more productive while being less capable. This isn't ignorance — it's how expertise works. You can't assess competence in a domain where you lack competence. AI accelerates this by providing confident answers to questions you don't fully understand.

The same studies that show productivity gains show the perception gap. Both effects are real. Productivity now, atrophy later. The question is which dominates over time — and whether design can change the trajectory.
