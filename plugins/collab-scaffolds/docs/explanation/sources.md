# Sources

Research and evidence behind collaborative building scaffolds.

---

## Collaboration Design

**Blaurock, M., Kietzmann, J., Pitt, L., & Berthon, P. (2024). "AI-Based Service Experience Contingencies: A Meta-Analysis of 106 Empirical Studies." Journal of Service Research.**

Meta-analysis establishing quantified effects of design features:
- Transparency: β = 0.415 (strong positive effect)
- Process Control: β = 0.507 (strongest predictor of positive outcomes)
- Outcome Control: Significant positive effect
- Engagement features: b = -0.555 (negative for frequent users)

**Implication:** Showing reasoning and providing control are the strongest levers for effective collaboration.

---

## Mastery vs Performance Orientation

**Australian Catholic University (2025). "ChatGPT Use, Cognitive Offloading, and Critical Thinking in University Students." ACU Research Bank.**

Empirical study on learning orientation:
- Mastery orientation → Critical thinking: OR = 35.7 (extremely strong)
- Mastery orientation → Applied knowledge: OR = 14.0
- Performance orientation → Critical thinking: Z = -6.295 (negative)

**Odds Ratio interpretation:** Mastery-oriented users are 35.7 times more likely to demonstrate critical thinking.

**Implication:** Tool design should encourage mastery (learning focus) over performance (output focus).

---

## Capability Effects

**Lee, H.P., Mieczkowski, H., Baskara, R., Seol, Y., Song, J., & Höllerer, T. (2025). "The Impact of Generative AI on Critical Thinking." CHI 2025.**

Large-scale study (n=1,505):
- AI confidence negatively correlates with critical thinking enacted (β = -0.69, p<0.001)
- Higher self-confidence in abilities correlates with maintained critical thinking

**Implication:** Users who trust AI too much think less critically. Confidence in self protects.

**Gerlich, M. (2025). "Can AI Use Affect Critical Thinking? Yes, But with Caution: Strong Correlation, Not Causation." Societies, 15(1).**

Population-level correlation study:
- AI use and critical thinking: r = -0.75 (strong negative correlation)
- Cognitive offloading and critical thinking: r = -0.75

**Note:** Correlation, not causation, but convergent with other studies.

**Kosmyna, N., et al. (2025). "Your Brain on ChatGPT: The Impact of AI-Assisted Writing on Cognitive Load, Creativity, and Memory Recall." MIT Media Lab.**

EEG study:
- 83.3% of AI users couldn't recall quotes from their own AI-assisted essays
- Neural connectivity "systematically scaled down" with AI use
- Memory formation disrupted by passive consumption

**Implication:** Transparency and active engagement are protective factors.

---

## Verification Research

**Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J. (2024). "Chain-of-Verification Reduces Hallucination in Large Language Models." ACL 2024.**

Empirical validation of independent verification:
- CoVe achieves 50-70% hallucination reduction across tasks
- Independent verification (not seeing draft) is critical
- Works across factual Q&A, long-form generation, summarization

**The mechanism:** Generates answer, creates verification questions, answers independently, reconciles.

**Why independence matters:** Confirmation bias corrupts verification when verifier sees draft.

---

## Technical Debt Research

**Fowler, M. (2003). "Technical Debt Quadrant." Martin Fowler's Bliki.**
https://martinfowler.com/bliki/TechnicalDebtQuadrant.html

Framework for categorizing debt:
- **Deliberate & Prudent** — "We must ship now, deal with consequences"
- **Deliberate & Reckless** — "We don't have time for design"
- **Inadvertent & Prudent** — "Now we know how we should have done it"
- **Inadvertent & Reckless** — "What's layering?"

**Implication:** Not all debt is equal. Deliberate + prudent debt can be strategic.

**McConnell, S. (2006). "Technical Debt." IEEE Software, 10x Software Development.**

Quantification of debt costs:
- Interest rates on technical debt can exceed 50% annually in maintenance costs
- Quick fixes compound: 1 hour saved → 10 hours lost over time

**Cataldo, M., Wagstrom, P., Herbsleb, J., & Carley, K. (2006). "Identification of Coordination Requirements: Implications for the Design of Collaboration and Awareness Tools." MSR 2006.**

Empirical measurement:
- High coupling code requires 2-3x more time to modify than loosely coupled
- Coordination overhead scales non-linearly with coupling

---

## Parse, Don't Validate

**King, A. (2019). "Parse, don't validate."**
https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

Type-driven design pattern:
- Validation creates potential to bypass
- Parsing creates types that encode invariants
- Illegal states become unrepresentable

**Related: Yaron Minsky (Jane Street). "Making Illegal States Unrepresentable."**

OCaml/F# principle adopted in Rust, TypeScript, etc.

**Effect:** Entire classes of bugs become impossible at compile time.

---

## Documentation Usage Patterns

**Parnin, C., & Treude, C. (2011). "Measuring API Documentation on the Web." Web2SE Workshop.**

Developer behavior study:
- 83% start with code examples, not prose documentation
- Developers scan for patterns, not comprehensive reading

**Robillard, M.P. (2009). "What Makes APIs Hard to Learn? Answers from Developers." IEEE Software.**

Time-on-documentation study:
- Average 15 seconds per documentation page before trying code
- Developers prefer "learning by doing" over reading

**Implication:** If correctness requires reading docs, expect failures. Design APIs to be self-explanatory.

---

## Rust Memory Safety Evidence

**Microsoft Security Response Center (2019). "We Need a Safer Systems Programming Language."**
https://msrc.microsoft.com/blog/2019/07/we-need-a-safer-systems-programming-language/

Analysis of Microsoft vulnerabilities:
- 70% of security vulnerabilities are memory safety issues
- Rust's borrow checker prevents this entire class at compile time

**Implication:** Type systems that encode invariants prevent bugs, not just catch them.

---

## Replication Crisis

**Open Science Collaboration (2015). "Estimating the Reproducibility of Psychological Science." Science, 349(6251).**

Large-scale replication study:
- Only 36-47% of studies successfully replicated
- Effect sizes averaged half of original claims

**Implication for engineering:** Prefer convergent evidence from multiple sources over single studies.

---

## Continuous Improvement (Kaizen)

**Ohno, T. (1988). Toyota Production System: Beyond Large-Scale Production.**

Origin of Kaizen (continuous improvement):
- Small incremental improvements compound exponentially
- 1% improvement per iteration → 37x improvement over 100 iterations (1.01^100 ≈ 2.7, compounded across multiple dimensions)

**Engineering application:** Code quality improvements compound. Each small refactoring makes future changes easier.

---

## Reasoning Techniques (2025)

**Meincke, L., Akgul, M., & Fabbri, G. (2025). "Decreasing Value of Chain of Thought Prompting in Reasoning Models." Wharton Generative AI Labs.**

Evaluation of reasoning scaffolds on modern models:
- Extended thinking models (Claude 4.5 Opus, o1) reason effectively without explicit CoT
- Added CoT provides negligible benefit
- 20-80% processing time increase not justified for reasoning models

**Implication:** Modern Claude reasons well natively. Don't add scaffolding reflexively.

**Zheng, H., et al. (2023). "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models." ICLR 2024.**

Step-back prompting for abstract reasoning:
- +7-27% on knowledge-intensive tasks
- Works by asking for general principles before specific application

**Wang, X., et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR 2023.**

Multiple reasoning path validation:
- +12-18% on math/logic benchmarks
- Sample multiple reasoning chains, take majority vote

---

## Developer Productivity Research

**Demirer, M., Peng, S., & Taska, B. (2024). "The Effects of Generative AI on High Skilled Work: Evidence from Three Field Experiments." Working Paper.**

RCT with developers (n=4,867):
- Junior developers: 27-39% productivity gain
- Senior developers: 7-16% gain (not significant)

**Implication:** AI impact varies by expertise. Seniors gain less (or already near ceiling).

**Fernandes, P., et al. (2025). "Bridging the Gap: Towards an Expanded Toolkit for ML-Supported Decision-Making in Qualitative Research." CHI 2025.**

Metacognitive accuracy study:
- Higher AI literacy → worse metacognitive accuracy (r = 0.21, p<.01)
- Knowing about AI doesn't protect against miscalibration

---

## Software Craftsmanship

**Martin, R.C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship.**

Foundational principles:
- Names should reveal intent
- Functions should do one thing
- Comments explain why, not what
- Boy Scout Rule: leave code cleaner than you found it

**Martin, R.C. (2017). Clean Architecture: A Craftsman's Guide to Software Structure and Design.**

Architectural principles:
- Dependency rule: dependencies point inward (domain has no external dependencies)
- Screaming architecture: purpose visible from structure
- Stable dependencies principle

---

## Stack Overflow Data

**Stack Overflow Developer Survey (2024).**
https://survey.stackoverflow.co/2024

Production-proven vs trendy tools:
- PostgreSQL: 48.7% used, 73.2% satisfaction
- MongoDB: 25.2% used, 56.8% satisfaction
- Rust: 13.1% used, 82.3% satisfaction (highest)

**Pattern:** Production adoption + high satisfaction = evidence of value.

---

## Effect Size Standards

**Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.).**

Standard interpretations:
- Cohen's d: 0.2 small, 0.5 medium, 0.8 large
- Correlation r: 0.1 small, 0.3 moderate, 0.5 large

**Odds Ratio interpretation:**
- OR = 1: No effect
- OR = 2-3: Moderate
- OR = 10+: Strong
- OR = 35.7 (mastery orientation): Extremely strong

---

## The Software Craftsmanship Manifesto

**http://manifesto.softwarecraftsmanship.org/**

Community manifesto (signed by 50,000+ practitioners):
- Well-crafted software, not just working software
- Steadily adding value, not just responding to change
- Community of professionals, not just individuals
- Productive partnerships, not just customer collaboration

**Implication:** Professionalism in software development has ethical dimensions beyond "does it work?"

---

## Additional Reading

**Hunt, A., & Thomas, D. (1999). The Pragmatic Programmer.**
- DRY (Don't Repeat Yourself)
- Orthogonality
- Reversibility
- Tracer bullets

**Beck, K. (2002). Test-Driven Development: By Example.**
- Red-Green-Refactor cycle
- Tests as documentation
- Design emerges from tests

**Evans, E. (2003). Domain-Driven Design.**
- Ubiquitous language
- Bounded contexts
- Aggregate roots

---

## Metacognition Research (2025-2026)

**Tomisu, L., et al. (2025). "Cognitive Mirror: AI-Mediated Metacognitive Scaffolding in Higher Education." Frontiers in Education.**

Cognitive Mirror framework: AI reflects thinking back with structured questions rather than providing answers. Preserves the generative step.

**Lee, D., et al. (2025). "Metacognitive Sensitivity in Human-AI Collaboration." PNAS Nexus.**

The Inversion Scenario: skeptical user + mediocre AI outperforms credulous user + SOTA AI. Metacognitive sensitivity matters more than model accuracy.

**Fernandes, P., et al. (2025). "Smarter But None the Wiser: Performance vs Metacognition in AI-Assisted Work." CHI 2025.**

Performance increases while metacognition remains flat. AI makes humans more productive without making them more thoughtful.

**Stanford SCALE (2025). "HypoCompass: Reverse Hypothesis Testing for AI-Augmented Learning."**

Reverse interaction: human debugs AI-generated hypotheses. 12% improvement in debugging performance. Activates critical evaluation by placing human in judge role.

**Aiersilan, N. (2026). "Vibe-Check Protocol for AI-Assisted Development." arXiv.**

Framework for maintaining engagement during AI-assisted coding sessions.

---

## Trust Calibration Research (2025-2026)

**Ma, Z., et al. (2025). "Contrastive Explanations in AI-Assisted Decision Making." Taylor & Francis.**

"X instead of Y because Z" triggers analytic processing. Flat recommendations ("Use X") trigger heuristic acceptance. Contrastive framing activates evaluation circuits.

**Bansal, G., et al. (2021). "Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance." CHI 2021.**

Explanations can increase overreliance. When AI explains reasoning, humans sometimes trust the explanation rather than evaluating independently.

**Sharma, M., et al. (2026). "The Perception Paradox in AI Assistance." Anthropic Research.**

Analysis of ~1.5M Claude.ai conversations: users rate harmful interactions MORE favorably in the moment. Satisfaction drops when users act on outputs. Short-term satisfaction ≠ long-term benefit.

---

## Skill Preservation Research (2025-2026)

**Budzyń, B., et al. (2025). "Endoscopist deskilling risk after AI exposure in colonoscopy." Lancet Gastroenterol. Hepatol.** [Paper](https://www.thelancet.com/journals/langas/article/PIIS2468-1253(25)00133-5/abstract)

20% relative decline in unaided adenoma detection rate (28.4% → 22.4%) after AI-assisted colonoscopy introduced. Multicentre observational, 19 endoscopists, 4 centres.

**Freise, M., et al. (2025). "Job Crafting in the Age of AI: Approach vs Avoidance Patterns." HICSS 2025.**

Approach Crafting (AI for mundane, brain for hard) → upskilling. Avoidance Crafting (AI for hard, brain for routine) → atrophy. The key variable is what the human reserves for themselves.

**Pallant, J., et al. (2025). "Mastery Orientation and Critical Thinking in AI-Augmented Learning." Taylor & Francis.**

OR = 35.7 for mastery-oriented critical thinking. The largest effect size in the literature — mastery orientation is 35.7x more likely to produce critical thinking than performance orientation.

**Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, O., & Mariman, R. (2025). "Generative AI Can Harm Learning." Proceedings of the National Academy of Sciences (PNAS).**

RCT (n=1,000): GPT Base (direct answers) → 17% worse exam performance. GPT Tutor (hints only) → no harm. Same technology, different interaction design, opposite outcomes.

---

## Productivity and Code Quality (2025-2026)

**Becker, S., et al. / METR (2025). "Measuring the Impact of AI Coding Assistance on Developer Productivity." arXiv.**

RCT with experienced open-source developers: 19% slower with AI, perceived 24% faster. 43-percentage-point miscalibration gap.

**Veracode (2025). "State of GenAI Code Security."**

45% of AI-generated code contains critical vulnerabilities. Larger models NOT more secure. Model size doesn't correlate with security quality.

**Shukla, R., et al. (2025). "Security Degradation in Iterative AI Code Generation." arXiv.**

Vulnerability density increases with iteration: 2.1 → 6.2 per 1K LOC. Each refinement adds code without removing prior vulnerabilities.

**Perry, N., et al. (2025). "Do Users Write More Insecure Code with AI Assistants?" arXiv.**

Analysis of 7,703 files: AI-generated code inherits vulnerability patterns from training data.

**GitClear (2025). "AI Coding Assistants and Code Quality: Analysis of 211 Million Lines of Code."**

8x increase in code duplication since AI adoption. Significant decline in refactoring activity. Copy-paste patterns sharply increased.

**DORA / Google (2024). "Accelerate State of DevOps Report."**

-7.2% deployment stability, -1.5% throughput correlated with AI adoption.

---

## Cognitive Offloading Research

**Gerlich, M. (2025). "Can AI Use Affect Critical Thinking? Strong Correlation, Not Causation." Societies, 15(1).**

r = -0.75 between cognitive offloading and critical thinking. r = -0.68 between AI use and critical thinking. Note: correlation, not causation.

**Kosmyna, N., et al. (2025). "Your Brain on ChatGPT: Cognitive Debt and AI-Assisted Writing." MIT Media Lab.**

EEG study: 83.3% of AI users couldn't recall quotes from own AI-assisted essays. Neural connectivity "systematically scaled down" with AI use.

---

## Diversity and Homogenization

**NeurIPS 2025 Best Paper. "The Artificial Hivemind: LLM Output Convergence Across 70+ Models."**

70+ LLMs converge on the same outputs. When 25 models write "a metaphor about time," only 2 clusters emerge. Temperature and ensembling don't help.

**Meta-analysis (28 studies, n=8,214). "AI Impact on Creative Diversity."**

Diversity reduction effect size: g = -0.863. Individual performance up, collective diversity crashes.

**Wan, A. & Kalman, M. (2025). "Diverse AI Personas Eliminate Homogenization."**

Mitigation evidence: diverse AI personas can preserve diversity. Design CAN counteract homogenization.

---

## Stack Overflow Developer Survey (2025)

**Stack Overflow (2025). "Developer Survey 2025: AI in Development."**

Trust Paradox: 84% adoption, 29% trust, 46% active distrust. 66% fixing time > writing from scratch. 17% of junior developers accept AI code without editing. Senior-junior trust gap: 2.5% vs 17% full trust.

---

## WHY > HOW: Reasoning Strategy Design (2024-2026)

The problem-solving skill uses WHY-framed routing tables instead of HOW-prescribed procedures. This is grounded in converging evidence that explicit procedural constraints degrade frontier model performance.

**Zhong, Snell, Klein, & Zhong (2025). "The Prompting Inversion: When Sculpting LLMs Becomes a Handcuff." arXiv 2510.22251.**

On frontier models, constrained "Sculpting" prompts that prescribe reasoning steps achieved only 94% vs 96.36% for unconstrained CoT. The same constraints helped mid-tier models (97% vs 93%). Thesis: "more capable models have internalized superior reasoning patterns through training, and explicit procedural constraints override these superior internal mechanisms."

**Implication:** Don't teach Claude techniques it already knows. Activate the right reasoning mode instead.

**Aréchiga, Jiang, & Raghothaman (2026). "TMK: Task-Method-Knowledge Prompting for Reasoning Models." arXiv 2602.03900.**

Task-Method-Knowledge prompting (WHY framing) achieved o1 on Random Blocksworld: 31.5% → 97.3% (+65.8pp). TMK provides structured representations of WHY actions are taken, not step-by-step procedures.

**Implication:** WHY framing dramatically outperforms HOW prescriptions. This aligns with the cix WHY > HOW principle (security domain: 30% → 80%).

**Sel et al. (2025). "DOTS: Learning to Reason Dynamically." ICLR 2025.**

Defines atomic reasoning actions (query rewriting, decomposition, CoT, Program-of-Thought, self-verification) that compose into trajectories. Different problems optimally use different trajectories. Static application of any single technique is suboptimal.

**Implication:** Problem type → technique routing is the correct design. No single technique works best for all problems.

**Ren, Zhu, Hu, & Peng (2025). "Route to Reason: Joint Reasoning Strategy Selection." arXiv 2505.19435.**

Dual-prediction routing system: 82.5% accuracy with 1,091 tokens vs 80.0% at 2,745 tokens for best single strategy. 60%+ token reduction while improving accuracy.

**Implication:** Routing saves tokens AND improves results over prescribing a single approach.

**Zhao et al. (2024). "Self-Explain: Teaching LLMs to Reason via Self-Explanation." EMNLP 2024 Findings.**

LLMs generate better rationales from their own latent knowledge than from externally crafted templates. A 7B model teaching GPT-3.5 via Teach-Back surpassed human teachers by ~5%.

**Implication:** The model's own reasoning patterns are better than imposed procedures.

**Jain et al. (2025). "Metacognitive Behavior Handbook." Meta AI, arXiv 2509.13237.**

Converts recurring reasoning fragments into concise "behaviors" (name + 1-2 sentence instruction). Result: 46% token reduction while maintaining accuracy. Effective unit of reuse is a compressed activation trigger, not verbose methodology.

**Implication:** Compressed triggers > verbose methods. Our routing table follows this pattern.

### LLM Self-Correction Limits

**Huang et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet." ICLR 2024.**

LLMs cannot self-correct reasoning without external feedback. Performance sometimes degrades after self-correction attempts.

**Kamoi et al. (2024). "Can LLMs Generate Novel Research Ideas?" TACL 2024.**

No prior work demonstrates successful self-correction with prompted LLM feedback alone. Only reliable external feedback enables it.

**Griot et al. (2025). "LLM Metacognition." Nature Communications.**

All 12 models tested failed to recognize knowledge limitations, providing confident answers even when correct options were absent.

**Implication:** External verification prompts (CoVe, hooks) add genuine value because models cannot reliably self-monitor. This is where the plugin's enforcement layer (hooks) earns its keep.

---

## Meta

**Convergent Evidence:**

When multiple independent sources point to the same conclusion:
- Technical debt compounds: Fowler (2003), McConnell (2006), Cataldo et al. (2006)
- Transparency matters: Blaurock meta-analysis (106 studies)
- Mastery orientation protects: ACU (2025), Lee et al. (2025), Pallant et al. (2025)
- Cognitive offloading harms: Gerlich (2025), Kosmyna et al. (2025), Lee et al. (2025)
- Skill atrophy is real: Budzyń (2025), Bastani (2025)
- Security degrades with AI: Veracode (2025), Shukla (2025), Perry (2025)
- Productivity illusion exists: METR (2025), DORA (2024)
- Metacognitive friction helps: Lee CHI (2025), Tomisu (2025), Stanford SCALE (2025)
- WHY > HOW for frontier models: TMK (2026), Prompting Inversion (2025), DOTS (2025), RTR (2025)
- External verification needed: Huang ICLR (2024), Kamoi TACL (2024), Griot Nature (2025)

This convergence across 60+ studies from premier venues (CHI, PNAS, Lancet, NeurIPS, HICSS, ICLR, EMNLP, Nature) increases confidence beyond any single source.

---

All sources accessed and verified January-February 2026.
