# The Risks of Uncritical AI Adoption

Seven categories of measurable harm from substitutive AI use in software development.

---

## Sources

- [Budzyń et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet Gastroenterology & Hepatology.](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00301-2/fulltext)
- [Gerlich (2025). AI Tools in Society. MDPI Societies.](https://www.mdpi.com/2075-4698/15/1/6)
- [Kosmyna et al. (2025). Your Brain on ChatGPT. MIT Media Lab.](https://www.media.mit.edu/)
- [Lee et al. (2025). Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/full/10.1145/3706598.3713778)
- [METR (2025). Measuring AI Impact on Developer Productivity. RCT.](https://arxiv.org/abs/2507.09089)
- [Veracode (2025). AI Code Generation Security Analysis.](https://www.veracode.com/)
- [Shukla et al. (2025). Security Degradation in AI-Generated Code. arXiv.](https://arxiv.org/)
- [Perry et al. (2025). Vulnerability Inheritance in AI Code. arXiv.](https://arxiv.org/)
- [GitClear (2025). Coding on Copilot: 2024 Data.](https://www.gitclear.com/)
- [DORA (2024). State of DevOps Report.](https://dora.dev/)
- [Bastani et al. (2025). Generative AI Can Harm Learning. PNAS.](https://www.pnas.org/doi/10.1073/pnas.2422633122)
- [Bansal et al. (2021). Does the Whole Exceed its Parts? CHI.](https://dl.acm.org/doi/)
- [Stack Overflow Developer Survey (2024-2025).](https://survey.stackoverflow.co/2024/)
- [Jiang et al. (2025). Artificial Hivemind. NeurIPS Best Paper.](https://arxiv.org/abs/2510.22954)
- [Meta-analysis (2025). Generative AI and Creativity. arXiv.](https://arxiv.org/abs/2505.17241)
- [Hong & Page (2004). Groups of Diverse Problem Solvers. PNAS.](https://www.pnas.org/)
- [Ashby (1956). Law of Requisite Variety.](https://en.wikipedia.org/wiki/Variety_(cybernetics))

---

## Abstract

AI adoption creates seven measurable risk categories. Cognitive skills atrophy at 20% after three months of AI-assisted practice (Budzyń). <span class="ev ev-moderate" title="Lancet crossover RCT, medical domain">◐</span> Code quality degrades with 8x duplication increases and refactoring plummets (GitClear, 211M LOC). <span class="ev ev-moderate" title="Large-scale code analysis, observational">◐</span> Security deteriorates as 45% of AI-generated code contains critical vulnerabilities (Veracode). <span class="ev ev-moderate" title="Large-scale security analysis">◐</span>

The perception gap compounds every risk. Developers believe they're 24% faster with AI while measurements show they're 19% slower — a 43-point miscalibration (METR). <span class="ev ev-moderate" title="RCT, n=16, rigorous but small">◐</span> Trust in AI accuracy dropped from 43% to 33% in one year, yet adoption rose from 76% to 84% (Stack Overflow). <span class="ev ev-moderate" title="Large survey, observational">◐</span> People use tools they don't trust, perceive benefits they don't get, and can't see the degradation.

The risks aren't hypothetical. They're measured, cataloged, and accelerating.

---

## Explanation

### 1. Skill Atrophy

**The evidence is stark.** Remove AI assistance after three months, and diagnostic accuracy drops 20% (Budzyń). <span class="ev ev-moderate" title="Lancet crossover RCT, colonoscopy study">◐</span> This isn't forgetting — it's neural pathway degradation from disuse. The brain treats AI-assisted work differently at a physiological level, with "systematically scaled down" connectivity during collaboration (Kosmyna, MIT Media Lab). <span class="ev ev-moderate" title="EEG study, small n">◐</span>

The mechanism is cognitive offloading: r = -0.75 correlation between delegating thinking to AI and critical thinking capacity (Gerlich, n=666). <span class="ev ev-moderate" title="Survey study, single source">◐</span> When AI handles reasoning, humans stop performing it. This isn't laziness — it's rational resource allocation. Why think when AI does it faster?

**The bifurcation matters.** Not all skills atrophy equally:

| Skill Type | Vulnerability | Why |
|------------|--------------|-----|
| **Cognitive** (design, architecture) | High | Easily offloaded |
| **Perceptual** (pattern recognition) | High | Requires active practice |
| **Motor/Procedural** (typing, tools) | Low | Physically encoded |

The skills most at risk are exactly those most valuable: reasoning about systems, analyzing edge cases, designing abstractions, recognizing code smells. Meanwhile, typing speed and IDE shortcuts — the procedural skills — remain intact. We're losing capability where it matters most.

**Aviation provides the sobering parallel.** Seventy-seven percent of pilots report degraded manual flying skills from automation reliance. <span class="ev ev-moderate" title="Aviation domain, survey data">◐</span> Software development involves more abstract reasoning than motor control. Whether cognitive skills atrophy faster or slower than motor skills remains unknown, but the mechanism is identical: remove practice, lose proficiency. <span class="ev ev-speculative" title="Cross-domain inference">◌</span>

### 2. Security Degradation

**Forty-five percent.** That's the proportion of AI-generated code containing critical vulnerabilities (Veracode). <span class="ev ev-moderate" title="Large-scale security audit">◐</span> Not minor issues — critical. SQL injection, hardcoded credentials, insecure deserialization, missing validation. The patterns AI learned from training data, now replicated at scale.

**The iteration paradox compounds the problem.** Common intuition suggests more refinement produces more secure code. Measurements show the opposite. Vulnerabilities per thousand lines of code: 2.1 on first generation, 6.2 after refinement (Shukla). <span class="ev ev-moderate" title="arXiv preprint, security analysis">◐</span> Each iteration adds code without removing vulnerabilities from previous passes. Security degrades with effort.

Perry et al. analyzed 7,703 files. <span class="ev ev-moderate" title="Large-scale file analysis">◐</span> The finding: AI inherits vulnerabilities from training data systematically. When Stack Overflow is training corpus and Stack Overflow contains insecure patterns, AI reproduces them faithfully. The model has no concept of "this pattern is insecure." It knows only "this pattern is common."

**Model size provides no protection.** Larger models aren't more secure. Better prompts don't eliminate the vulnerability inheritance. The only reliable countermeasure is independent security review — which requires the security expertise that AI is actively eroding through offloading.

### 3. Code Quality Erosion

**Eight times.** Code duplication increased 8x after AI adoption (GitClear, 211M lines analyzed). <span class="ev ev-moderate" title="Large-scale observational study">◐</span> Refactoring activity plummeted. Copy-paste patterns surged. The codebase shifts from architected to assembled.

The mechanism: AI generates fresh solutions without awareness of existing patterns. Each generation produces plausible code that works in isolation but duplicates what already exists. The human who would have searched for reusable components instead gets a new implementation — faster to accept than to find and refactor.

**DORA metrics tell the downstream story.** Deployment stability: -7.2%. Throughput: -1.5%. (DORA 2024) <span class="ev ev-moderate" title="Industry survey, large sample">◐</span> The most rigorous measurement of engineering effectiveness shows AI correlating with slight degradation across both stability and speed. The quality debt compounds silently.

The explainability gap opens wider each sprint. Developer writes 500 LOC, understands all. AI generates 2,000 LOC, developer understands 60%. Next iteration builds on that 60%, understanding drops to 30%. By sprint N, the codebase is assembled from components the developer never designed and doesn't fully comprehend. Debugging becomes archaeological work. Maintenance becomes guesswork. Architecture evolution becomes impossible.

### 4. The Perception Gap

**You can't fix what you can't see.** Experienced developers predicted AI would make them 24% faster. Rigorous measurement showed they were 19% slower. The gap: 43 percentage points between perception and reality (METR). <span class="ev ev-moderate" title="RCT, n=16, controlled conditions">◐</span>

Time spent prompting, reviewing, fixing, integrating — all uncounted in subjective assessment. The effort feels lighter because generation (visible work) disappears. Verification (invisible work) appears. The task completes. The illusion persists.

**The trust-behavior divergence amplifies the problem.** Trust in AI coding accuracy: 43% in 2023, dropped to 33% in 2024. Usage: 76% to 84% in the same period (Stack Overflow). <span class="ev ev-moderate" title="Developer survey, large sample">◐</span> Trust drops, adoption rises. People use tools they don't trust, perceive benefits contradicted by measurement, and make decisions based on false premises.

Managers allocate timelines assuming productivity gains that don't exist. Developers underinvest in verification because the work feels complete. Teams ship faster while quality degrades. The perception gap prevents correction at every level.

### 5. Automation Complacency

**Confidence in AI negatively predicts critical thinking at β = -0.69 (Lee et al., CHI 2025).** <span class="ev ev-strong" title="CHI peer-reviewed, n=319, structural equation modeling">●</span> The more you trust AI, the less you verify it. The less you verify, the more errors propagate.

The mechanism is automation bias: repeated experience of AI being correct → reduced vigilance. This manifests in verification latency — time between receiving AI output and meaningful review. Immediate acceptance signals rubber-stamping. Ten to thirty seconds suggests scanning, not reviewing. Genuine review takes minutes.

**Explanations make it worse.** When AI provides reasoning alongside answers, acceptance increases regardless of correctness (Bansal, CHI 2021). <span class="ev ev-strong" title="CHI peer-reviewed, controlled experiment">●</span> Correct AI + explanation: slight help. Incorrect AI + explanation: performance degrades. The explanation creates false confidence. Human evaluation collapses.

Developers spend only 22.4% of coding time verifying AI suggestions. <span class="ev ev-moderate" title="Observational study">◐</span> The correction rate — how often suggestions get modified before acceptance — provides calibration signal. Under 5%: automation bias risk. 10-30%: healthy. Above 50%: AI ineffective for this domain. Most developers can't report their own correction rate.

### 6. Homogenization

**g = -0.863.** Meta-analysis across 28 studies, n=8,214. <span class="ev ev-strong" title="Meta-analysis, large sample">●</span> AI-assisted outputs show 0.863 standard deviations less diversity than human-only outputs. This isn't small. It's structural convergence toward training data patterns.

Jiang et al. (NeurIPS 2025 Best Paper) tested 70+ LLMs across 26,000 queries. <span class="ev ev-strong" title="Best Paper, comprehensive evaluation">●</span> Convergence appeared across all models. Temperature scaling didn't help. Ensembling didn't help. The models share training data, converge to shared patterns, produce homogenized outputs regardless of sampling method.

**Why homogenization matters:** Hong & Page proved mathematically that diverse groups outperform best-ability homogeneous groups for complex problem-solving. <span class="ev ev-strong" title="PNAS, formal proof">●</span> Diversity isn't fairness theater — it's functional necessity. Different perspectives catch different errors, explore different solutions, prevent groupthink failure modes.

Ashby's Law of Requisite Variety: a system can only regulate variety in its environment if it has equal or greater internal variety. <span class="ev ev-moderate" title="Cybernetics principle, theoretical">◐</span> When everyone uses the same AI generating the same solutions, the system loses the variety needed to handle unexpected problems. Fragility increases invisibly until the shock that reveals it.

### 7. Novice Vulnerability

**Seventeen percent.** Students with unrestricted ChatGPT access scored 17% worse on exams without AI (Bastani, PNAS, n=1,000). <span class="ev ev-strong" title="RCT, large sample, PNAS">●</span> Students with hint-only AI showed no degradation. Same technology. Different interaction pattern. Opposite outcomes.

The mechanism: direct answers bypass desirable difficulties — the productive struggle that builds understanding. Errors force diagnosis. Diagnosis builds mental models. Remove errors, remove learning. The control group encountered median 3 errors. AI users who delegated encountered 1 error. They finished faster and learned nothing about why their code didn't work. The errors were the curriculum.

**Novices lack the foundational schema needed to evaluate AI output.** An expert sees generated code and recognizes patterns, evaluates tradeoffs, spots subtle issues. A novice sees generated code that runs and assumes correctness. Expert judgment catches AI failures. Novice acceptance amplifies them.

A novice who learns to program with AI may never develop:
- Mental models of program execution
- Debugging intuition
- Design reasoning
- Error recognition patterns

These aren't taught — they're built through struggle. Receiving solutions feels like learning but produces no schema formation. The brain never engages. The knowledge never encodes.

### The Compounding Problem

**These seven risks don't exist in isolation.** They compound.

Skill atrophy → reduced ability to catch security issues → vulnerabilities propagate.
Perception gap → under-investment in verification → automation complacency → more errors.
Code quality erosion → harder to debug → more reliance on AI → faster skill atrophy.
Homogenization → less diverse solutions → fragility → shocks the system can't absorb.
Novice vulnerability → no foundational schema → permanent capability gap → dependency.

Each risk makes the others worse. The system is dynamically unstable.

### When Risk Is Acceptable

**Not all AI use produces these outcomes.** The determining factor is complementary vs substitutive design.

| Pattern | Human Role | Outcome |
|---------|-----------|---------|
| **Substitutive** | Approves AI work | Atrophy |
| **Complementary** | Steers AI, retains reasoning | Capability maintained |

Complementary patterns that preserve capability:
- AI handles boilerplate, human handles architecture (Approach Crafting)
- AI generates, human comprehends through questions (86% mastery pattern)
- AI provides perspective, human synthesizes across multiple viewpoints
- AI explains reasoning, human evaluates logic chains

The distinction: who does the thinking? If AI thinks and human approves, capability erodes. If human thinks and AI amplifies, capability compounds.

### The Unsolved Questions

**No longitudinal study tracks developer capability over 2-5 years of heavy AI use.** We have three-month medical studies showing 20% skill loss. We have cross-sectional developer data showing perception gaps and reduced thinking. But the multi-year trajectory with varied interaction patterns remains unknown.

Whether cognitive skills atrophy faster or slower than motor skills is speculative. <span class="ev ev-speculative" title="Inference from adjacent domains">◌</span> Whether early-career AI exposure prevents schema formation permanently is unknown. <span class="ev ev-speculative" title="Hypothesis, no direct evidence">◌</span> Whether complementary design actually prevents long-term atrophy is plausible but unproven beyond 12 weeks. <span class="ev ev-speculative" title="Inference from mechanism understanding">◌</span>

The research we need: cohort study, multiple interaction patterns, capability assessment at 6/12/24 months, measuring both assisted and unassisted performance. Until that exists, we're making trillion-dollar bets on inferences from short-term studies.

### Risk Mitigation

The risks are real, measured, and structural. They're not eliminated by better models or clearer prompts. They require design interventions:

**Preserve the generative step** in learning contexts. Attempt-first protocol: 15-30 minutes unassisted before AI consultation.

**Inject metacognitive friction** at decision points. Planning, monitoring, evaluation checkpoints. Single-point friction ("are you sure?") is insufficient.

**Reduce AI-confidence signals.** Don't project certainty. Show uncertainty. Invite verification.

**Boost self-confidence signals.** "You have the production context I lack." Shift authority back to human.

**Maintain variety.** Don't standardize on single AI. Multiple perspectives, human synthesis, preserved diversity.

**Measure what matters.** Correction rate, verification latency, independent capability checks. Perception is unreliable.

**Protect novices.** Hint-only mode for learning. Direct answers prevent schema formation.

### Summary

Seven risk categories, all measured:

1. **Skill atrophy**: 20% at 3 months, cognitive skills most vulnerable
2. **Security degradation**: 45% critical vulnerabilities, worse with iteration
3. **Code quality erosion**: 8x duplication, -7.2% stability
4. **Perception gap**: 43-point miscalibration prevents correction
5. **Automation complacency**: β = -0.69 confidence → less critical thinking
6. **Homogenization**: g = -0.863 diversity reduction, fragility increase
7. **Novice vulnerability**: 17% learning harm from direct answers

The risks compound. The perception gap prevents correction. Substitutive use guarantees degradation. Complementary design offers protection but requires intentional effort.

The question isn't whether to use AI. The question is whether we design collaboration that maintains human capability or surrenders it.
