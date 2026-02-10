# Cognitive Effects Evidence

Research synthesis on how AI collaboration changes human thinking, attention, memory, and metacognitive processes.

---

## Sources

- [Lee et al. (2025). Impact of Generative AI on Critical Thinking. CHI.](https://dl.acm.org/doi/10.1145/3613904.3641913)
- [Kosmyna et al. (2025). Your Brain on ChatGPT: Cognitive Debt. MIT Media Lab.](https://www.media.mit.edu/publications/your-brain-on-chatgpt/)
- [Gerlich (2025). AI Tools and Cognitive Offloading. MDPI Societies.](https://www.mdpi.com/2075-4698/15/1/6)
- [Fernandes et al. (2025). Smarter But None the Wiser. CHI.](https://dl.acm.org/doi/abs/10.1145/3613904.3642699)
- [Lee, D. et al. (2025). The Inversion Scenario. PNAS Nexus.](https://academic.oup.com/pnasnexus/article/4/1/pgae558/7939819)
- [Tomisu et al. (2025). Cognitive Mirror. Frontiers in Education.](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1510919/full)

---

## The Confidence-Competence Inversion

### Lee et al. (CHI 2025) <span class="ev ev-strong" title="CHI peer-reviewed, n=319, structural equation modeling">●</span>

**Design:** Structural equation modeling with 319 knowledge workers.

**Key findings:**

| Confidence Type | Effect on Critical Thinking | Mechanism |
|----------------|----------------------------|-----------|
| AI-confidence (trust in AI) | β = -0.69 (strong negative) | "AI is reliable" triggers cognitive offloading |
| Self-confidence (trust in own judgment) | β = +0.35 (moderate positive) | "I can evaluate" maintains engagement |

The inversion is structural. Higher AI confidence reduces the perceived need for verification. Lower self-confidence reduces the belief that verification would help. Both suppress critical thinking through different mechanisms.

**The design paradox:** Making AI more accurate and trustworthy increases AI-confidence, which decreases critical thinking, which increases error propagation. Better AI can produce worse outcomes if human engagement collapses.

### PME Friction Intervention <span class="ev ev-strong" title="Same study, controlled experiment">●</span>

Lee et al. tested three-component metacognitive friction — Planning, Monitoring, Evaluation:

| Phase | Intervention | Effect |
|-------|-------------|---------|
| Planning | "What's your approach before I assist?" | Preserves the generative step |
| Monitoring | "Does this match expectations?" | Maintains engagement during execution |
| Evaluation | "What would you change next time?" | Crystallizes learning |

Three-component friction significantly restored critical thinking that was otherwise suppressed by AI confidence. Single-point friction was insufficient — all three checkpoints were necessary.

**Limitations:** Cross-sectional design — no longitudinal tracking. β interpretation assumes causality in SEM but the data is observational.

---

## Neural Evidence for Cognitive Offloading

### Kosmyna et al. (MIT Media Lab) <span class="ev ev-moderate" title="MIT Media Lab EEG study, small sample">◐</span>

**Design:** EEG measurement during AI-assisted vs unassisted writing.

**Key findings:**
- Neural connectivity "systematically scaled down" during AI-assisted writing
- Reduced activation in memory encoding regions
- Lower engagement in executive function networks
- Decreased integration between sensory input and long-term storage
- 83.3% of participants couldn't recall quotes from their own AI-assisted essays

The brain treated AI-assisted writing differently from unassisted writing at a physiological level. Information was processed, formatted, submitted — but never encoded as learned knowledge. The episodic memory trace never formed because the deep processing required for encoding never occurred.

**Limitations:** Small sample size. Single writing domain. EEG has temporal but not spatial precision.

---

## Cognitive Offloading Correlation

### Gerlich (2025) <span class="ev ev-moderate" title="Survey study, n=666, single source">◐</span>

**Design:** Survey of 666 participants measuring cognitive offloading and critical thinking.

**Key findings:**
- r = -0.75 correlation between cognitive offloading and critical thinking
- r = -0.68 correlation between AI use and critical thinking
- AI use negatively predicts critical thinking (β = -1.76)
- Younger users (18-25) showed stronger negative effects than older users (56-65)

**Age effect hypothesis:** Older users have established cognitive schemas that resist replacement. Younger users building initial schemas are more vulnerable to substitution. If correct, AI exposure during learning phases may have compounding effects — skills never acquired can't be recovered.

**Limitations:** Survey-based, self-report. Correlation not causation. Single source.

---

## Metacognition Without Learning

### Fernandes et al. (CHI 2025) <span class="ev ev-moderate" title="CHI peer-reviewed, single study">◐</span>

**Key finding:** "Smarter but none the wiser" — AI users showed improved task performance without improved metacognitive awareness. Performance metrics went up. Metacognitive calibration stayed flat.

**Mechanism:** AI bypasses desirable difficulties — the productive struggle that builds understanding. Errors force diagnosis. Diagnosis builds mental models. Remove errors, remove learning.

**Limitations:** Single study. Mechanism inferred from results.

---

## The Inversion Scenario

### Lee, D. et al. (PNAS Nexus 2025) <span class="ev ev-moderate" title="PNAS Nexus, theoretical model with empirical support">◐</span>

**Key finding:** A skeptical user with mediocre AI outperforms a credulous user with state-of-the-art AI.

| User Type | AI Quality | Outcome |
|-----------|------------|---------|
| High metacognitive sensitivity (skeptical) | Mediocre | Catches errors, verifies claims, learns — robust outcomes |
| Low metacognitive sensitivity (credulous) | State-of-the-art | Accepts outputs uncritically — fragile outcomes |

Human metacognitive sensitivity matters more than model accuracy. The marginal return to model accuracy diminishes as human engagement drops. Past a threshold, improving the AI makes outcomes worse by suppressing metacognitive processes that catch edge cases.

**Limitations:** Theoretical model with limited empirical validation. The exact threshold is unknown.

---

## The Cognitive Mirror

### Tomisu et al. (Frontiers in Education, 2025) <span class="ev ev-moderate" title="Frontiers in Education, single study">◐</span>

**Technique:** Reflecting the human's reasoning back with structured questions rather than providing answers.

The pattern forces articulation (makes implicit explicit) → evaluation (metacognitive monitoring) → gap discovery (generative learning). Instead of "here's the solution," the interaction becomes "here's what I see in your reasoning — what am I missing?"

**Mechanism:** Making implicit reasoning explicit activates metacognitive monitoring. Humans notice flaws in their own logic when forced to explain it. AI-generated solutions bypass this entirely.

**Limitations:** Qualitative study. Effect size not quantified.

---

## The CAIM Framework

Multiple studies converged on the Collaborative AI Metacognition (CAIM) scale measuring four dimensions:

| Dimension | Definition | Why It Matters |
|-----------|-----------|----------------|
| Understanding | Knowing AI capabilities and limits | Calibrates expectations |
| Use | Choosing when to engage AI | Prevents inappropriate delegation |
| Evaluation | Assessing output quality | Error detection |
| Ethics | Recognizing implications | Long-term judgment |

Traditional AI design optimizes for Use — making the tool easy to invoke. But Understanding, Evaluation, and Ethics are what prevent cognitive collapse.

---

## Evidence Summary

| Finding | Effect Size | Evidence Level | Source |
|---------|------------|----------------|--------|
| AI confidence → less critical thinking | β = -0.69 | <span class="ev ev-strong">●</span> Strong | Lee et al. CHI 2025 |
| Self-confidence → more critical thinking | β = +0.35 | <span class="ev ev-strong">●</span> Strong | Lee et al. CHI 2025 |
| PME friction restores engagement | Significant | <span class="ev ev-strong">●</span> Strong | Lee et al. CHI 2025 |
| Neural connectivity reduced with AI | Measured via EEG | <span class="ev ev-moderate">◐</span> Moderate | Kosmyna, MIT |
| 83.3% recall failure | 83.3% | <span class="ev ev-moderate">◐</span> Moderate | Kosmyna, MIT |
| Cognitive offloading ↔ critical thinking | r = -0.75 | <span class="ev ev-moderate">◐</span> Moderate | Gerlich 2025 |
| Younger users more affected | Age-stratified | <span class="ev ev-moderate">◐</span> Moderate | Gerlich 2025 |
| Performance up, metacognition flat | Observed | <span class="ev ev-moderate">◐</span> Moderate | Fernandes CHI 2025 |
| Skeptical user + weak AI > credulous + strong AI | Model prediction | <span class="ev ev-moderate">◐</span> Moderate | Lee D., PNAS Nexus |
| Cognitive mirror preserves learning | Qualitative | <span class="ev ev-moderate">◐</span> Moderate | Tomisu 2025 |
| Long-term developer capability trajectory | Unknown | <span class="ev ev-speculative">◌</span> Speculative | No direct study |

---

## The Unsolved Question

No longitudinal study tracks developer capability decline over extended AI use. We have 3-month medical studies showing 20% skill loss ([skill formation evidence →](skill-formation-evidence)). We have cross-sectional developer data showing perception gaps and reduced critical thinking. But the multi-year trajectory remains unknown.

The research we need: cohort study tracking developers' unassisted capability over 2-5 years of varied AI use. Until that exists, we're inferring from adjacent domains and short-term experiments.

---

*Full citations in [bibliography](bibliography)*
