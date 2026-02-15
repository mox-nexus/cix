# Why the Evaluator Works This Way

The evaluator agent checks extensions against quality gates. This document explains why those specific gates exist.

---

## The Six Gates

### Gate 1: Content Quality

**What it checks:** Does this fill gaps Claude doesn't already know?

**Why it matters:** Claude is already very smart. Teaching basics wastes tokens and creates noise. The value is in non-obvious insights, gotchas, and decision frameworks.

**Research backing:** Anthropic's skill authoring guidelines emphasize that context window is a public good. Every token must justify its cost.

### Gate 2: Transparency

**What it checks:** Is reasoning visible? Are sources cited?

**Why it matters:** Transparency (β = 0.415) is the second-strongest predictor of positive AI collaboration outcomes. Without visible reasoning, users can't evaluate, learn, or calibrate trust.

**Research backing:** Blaurock et al. (2025, n=654). Also: Bansal et al. showed explanations alone increase acceptance regardless of correctness—so transparency must be genuine, not theater.

### Gate 3: Control

**What it checks:** Does the extension preserve user agency?

**Why it matters:** Control (β = 0.507) is the strongest predictor. Rigid mandates remove agency. Decision frameworks preserve it by showing HOW to decide, not WHAT to decide.

**Research backing:** Blaurock meta-analysis. Also: Engagement features (b = -0.555) backfire—paternalism hurts frequent users.

### Gate 4: Observability

**What it checks:** Can behavior be traced? Are there logs, spans, exit codes?

**Why it matters:** Without observability, you can't debug, improve, or verify. Silent systems prevent learning and intervention.

**Research backing:** Standard software engineering practice. For AI specifically: observable agents support team situational awareness.

### Gate 5: Activation

**What it checks:** Does the extension trigger on the right prompts?

**Why it matters:** Over-activation wastes context. Under-activation means the extension never helps. "Use when:" patterns ensure precise triggering.

**Research backing:** Anthropic's skill authoring guidelines on description specificity.

### Gate 6: Expert Value

**What it checks:** Would someone who knows this domain find it useful?

**Why it matters:** Extensions should make humans MORE capable, not dependent. If an expert finds no value, the extension is teaching basics Claude already knows—creating dependency without capability.

**Research backing:**
- Mastery orientation preserves capability (ACU research)
- Skill formation gap (Anthropic 2026): wrong patterns create 17pp learning gap
- Creative scar (Zhou 2025): users don't truly acquire ability

---

## Scoring Philosophy

| Score | Meaning |
|-------|---------|
| 3 | Exceeds—would recommend as exemplar |
| 2 | Meets—does the job |
| 1 | Partial—has issues but salvageable |
| 0 | Fails—fundamental problems |

**Minimum passing:** 2 on all gates (12/18 total)

Why this threshold? Extensions below this level either:
- Teach basics (wasting tokens)
- Hide reasoning (preventing learning)
- Remove control (creating dependency)
- Fail to activate correctly (providing no value)

---

## Anti-Pattern Detection

The evaluator flags:
- **LLM tell-tales:** "delve", "leverage", "robust" → signal low-effort content
- **Options without picks:** "You could use A, B, or C" → no decision guidance
- **Tutorial content:** Installation instructions, basic syntax → Claude knows this
- **Vague activation:** "Helps with code" → fires on everything or nothing

These patterns indicate substitutive rather than complementary design.

---

## Honest Over Nice

The evaluator is deliberately ruthless because flattery wastes everyone's time.

An extension that passes on false praise:
- Wastes user context on low-value content
- Creates dependency through substitutive patterns
- Fails to improve through honest feedback

An extension that fails honestly:
- Gets specific feedback for improvement
- Has a clear path to quality
- Becomes genuinely useful after fixes

The goal is effective extensions, not feel-good evaluations.
