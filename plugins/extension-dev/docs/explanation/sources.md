# Sources

## Skill Authoring

**Anthropic. Skill Authoring Best Practices.**
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Core guidance on writing effective Skills: progressive disclosure, conciseness, testing with multiple models, avoiding anti-patterns.

---

## Research Foundations

### Transparency and Control

**Blaurock et al. (2024). "AI-Based Service Experience: A Meta-Analysis of 106 Studies." Journal of Service Research.**

- Transparency: β = 0.415 (significant positive effect)
- Process Control: β = 0.507 (strongest predictor)
- Engagement features: b = -0.555 (negative for frequent users)

### Cognitive Effects

**Lee H.P. et al. (2025). "The Impact of Generative AI on Critical Thinking." CHI 2025.**
- AI confidence negatively correlates with critical thinking (β = -0.69)

**Gerlich (2025). "AI Use and Critical Thinking." Societies.**
- Strong negative correlation (r = -0.75)

**Kosmyna et al. (2025). "Your Brain on ChatGPT: Cognitive Debt." MIT Media Lab.**
- 83% of AI users couldn't recall content from AI-assisted work

### Skill Formation (Anthropic, January 2026)

**Shen & Tamkin (2026). ["How AI Impacts Skill Formation."](https://arxiv.org/abs/2601.20245) Anthropic.**
- RCT with 52 developers learning Python Trio
- AI group: 50% quiz score vs Control: 67% (Cohen's d = 0.738)
- 17 percentage point gap ≈ 2 letter grades
- Six interaction patterns identified: 3 preserve learning, 3 don't

### Disempowerment (Anthropic, January 2026)

**Sharma et al. (2026). ["Who's in Charge? Disempowerment Patterns."](https://arxiv.org/abs/2601.19062) Anthropic.**
- ~1.5 million Claude.ai conversations analyzed
- Users rate disempowering interactions MORE favorably
- Satisfaction drops below baseline when users act on AI outputs
- "I should have listened to my own intuition"

### Skill Degradation

**Budzyń, B. et al. (2025). ["Endoscopist deskilling risk after AI exposure in colonoscopy."](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract) Lancet Gastroenterol. Hepatol.**
- 20% relative decline in unaided ADR (28.4% → 22.4%) after AI-assisted colonoscopy introduced. Multicentre observational, 19 endoscopists.

**Zhou et al. (2025). ["Creative Scar."](https://www.sciencedirect.com/science/article/abs/pii/S0160791X25002775) Technology in Society.**
- 7-day lab experiment with 2-month follow-up (longitudinal!)
- Creativity drops on AI withdrawal, homogeneity persists months later
- "Users do not truly acquire ability, just lose it when AI gone"

**Fernandes et al. (2025). "LSAT Performance with AI." CHI 2025.**
- Performance gain d = 1.23 with AI, capability not retained

### Learning Orientation

**ACU (2025). "Mastery vs Performance Orientation." Australian Catholic University.**
- Mastery orientation correlates with maintained critical thinking
- Performance orientation correlates with degraded critical thinking
- *Note: Single institutional study; pattern consistent with literature but effect sizes need replication*

### Code Security

**Tihanyi et al. (2024). "AI Code Vulnerabilities." Empirical Software Engineering.**
- 62% of AI-generated code contains vulnerabilities

**Fu et al. (2024). "Python CWE Weaknesses." ACM TOSEM.**
- 29.5% of AI Python code has CWE weaknesses

**Perry et al. (2025). "7,703 AI-Generated Files."**
- Security degrades 3x through iteration

### Verification

**Dhuliawala et al. (2024). "Chain-of-Verification Reduces Hallucination." ACL 2024.**
- CoVE achieves 50-70% hallucination reduction

### Homogenization & Diversity

**Jiang et al. (2025). ["Artificial Hivemind."](https://arxiv.org/abs/2510.22954) NeurIPS 2025 Best Paper.**
- 70+ LLMs tested on 26,000 queries
- 25 models writing "metaphor about time" → only 2 clusters emerged
- Temperature/ensembling don't help; RLHF punishes diversity

**Meta-analysis (2025). ["Generative AI and Creativity."](https://arxiv.org/abs/2505.17241) arXiv.**
- 28 studies, n=8,214 participants
- Diversity reduction: **g = -0.863** (large negative effect)
- Individual performance up (+0.27), collective diversity down hard

**Doshi & Hauser (2024). ["Individual Creativity vs Collective Diversity."](https://www.science.org/doi/10.1126/sciadv.adn5290) Science Advances.**
- Individual novelty: +8.1%
- Story similarity: +10.7%
- "Social dilemma: individually better off, collectively homogenized"

**Hintze et al. (2026). ["Visual Elevator Music."](https://www.cell.com/patterns/fulltext/S2666-3899(25)00299-5) Patterns/Cell.**
- 700 AI image runs converged to just 12 motifs
- "Bland, pop culture, generic - opposite of creative"

**Mitigation: Wan & Kalman (2025). ["AI Personas Preserve Diversity."](https://arxiv.org/abs/2504.13868)**
- 10 diverse AI personas eliminated homogenization effect
- Design CAN preserve diversity

---

## Statistical Glossary

| Statistic | Meaning |
|-----------|---------|
| **d** (Cohen's d) | Effect size (0.2 small, 0.5 medium, 0.8 large) |
| **β** (beta) | Regression coefficient (strength/direction) |
| **r** (correlation) | Linear relationship (0.3 moderate, 0.5 strong) |
| **OR** (odds ratio) | Likelihood ratio (OR=35.7 = 35.7x more likely) |

## Caveats

- Most studies are not software-developer specific (Anthropic 2026 is developer-focused)
- Longitudinal studies now emerging (Zhou 2025: creative scar persists 2 months)
- Effect sizes transfer imperfectly across domains
- Research provides direction, not precision
- Homogenization research is strong (NeurIPS Best Paper, Science Advances, Nature)
