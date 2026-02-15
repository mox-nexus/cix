# Ethos

## The Gap

You've felt it.

The autocomplete you accepted without reading. The function you couldn't write when the tool was down. The code review where you approved something because the AI said it was fine.

Something is broken. Not the outputs — the outputs look fine. The problem is underneath.

METR ran a randomized controlled trial with 16 experienced developers on mature codebases. AI tools made them **19% slower**. They predicted being 24% faster.

That 43-point perception gap isn't a flaw in the study. It's the central finding.

**Cognitive systems shaped by delegation lose the ability to evaluate what they delegated.** You can't feel yourself getting worse. The gap between perception and reality widens with each handoff.

## The Atrophy Loop

This isn't "humans get lazy." It's a feedback property. When you offload a cognitive task, three things degrade in sequence:

1. **Skill to produce** — you stop practicing
2. **Judgment to evaluate** — you can't assess what you didn't build
3. **Metacognition to notice the loss** — you can't feel yourself getting worse

The evidence is consistent. Skill degrades measurably — clinicians who trained with AI lost 21% of their detection ability when the AI was removed (Budzyn et al., Lancet GI 2025). Memory degrades — 83% of AI users couldn't recall quotes from their own AI-assisted work (Kosmyna et al., MIT 2025). And it doesn't recover — creativity drops on AI withdrawal, homogeneity persists months later (Liu et al. 2024).

But the same research shows a way out. The pattern of interaction determines the outcome, not the tool itself. Passive consumption predicts atrophy. Active engagement does not (Shen & Tamkin, Anthropic 2026).

The loop compounds beyond individuals. Ten developers who would have produced ten architectures now produce one. Diversity of perspective erodes into monoculture. Market pressure rewards it — faster this quarter. By the time fragility surfaces, the atrophy is deep and the incentive structure rewards more of it.

The loop is invisible from inside.

## The Design Trap

The features you love are the ones that harm you.

Transparency, control, and reciprocity predict successful human-AI collaboration. Engagement features — the polish, the gamification, the frictionless handoff — predict failure (Blaurock et al., J. Service Research 2025).

The things that make AI tools *feel* good are the things that cause harm. And the things that feel like friction — showing reasoning, requiring decisions, deferring at choice points — are the things that work.

| 84% | 33% |
|-----|-----|
| use AI | trust it |

Developers aren't naive. 84% use AI; only 33% trust it. The experienced ones trust it least and use it best. (Stack Overflow Survey 2025)

Same tool, same students, different design, opposite outcomes. Unrestricted AI access caused 17% learning harm. Scaffolded access caused none (Bastani et al., PNAS 2025).

**The tool didn't change. The interaction pattern did.**

## What Kind of Mind

Your notebook isn't just storage. It's part of how you think.

Clark and Chalmers (1998) proposed the **extended mind thesis**: cognitive processes don't stop at the skull. If an external resource performs the same cognitive function as memory, it's part of the cognitive system.

> "If the notebook performs the same cognitive function as memory, it's part of the cognitive system."
> — Clark & Chalmers, 1998

Applied to AI: every extension in cix isn't a tool you use. It's part of the cognitive system the human-AI collaboration forms. The *design* of the extension shapes the *nature* of the mind.

You're not choosing a tool. **You're choosing what kind of mind to build.**

## What to Build

Four verifiable constraints. Each grounded in research, each breaking a specific link in the atrophy loop.

The atrophy loop: Tool does work → Human stops practicing → Can't evaluate output → Loses judgment → Dependency deepens → (repeats)

### Transparent by Design

Show reasoning, not just outputs. Extensions expose decisions, teach domain knowledge, make the invisible visible.

- **Evidence**: Blaurock et al., 2025: transparency (beta=0.415) predicts good outcomes
- **Breaks**: "can't evaluate output"
- **Verification**: Instead of "here's the fix" → "here's what I see, here's my reasoning, you decide"

### Evidence-Driven

Claims backed by data. Extensions prove they work. Build on prior work with attribution.

- **Evidence**: METR, 2025: the 43-point perception gap exists because no one measured
- **Breaks**: "the illusion that things are working"
- **Verification**: Instead of "trust me" → "here's the evidence, here's the uncertainty"

### Enable Diversity

Forkable, composable, multiple approaches coexist. No single blessed way.

- **Evidence**: Liu et al., 2024: homogeneity persists months after AI withdrawal
- **Breaks**: "tool does work one way forever"
- **Verification**: Instead of one solution → multiple perspectives that force human synthesis

### Require Judgment

Present choices at decision points. Extensions defer where expertise matters, amplify where it doesn't.

- **Evidence**: Blaurock et al., 2025: process and outcome control predict collaboration success
- **Breaks**: "dependency deepens"
- **Verification**: Instead of auto-fix → "here are three approaches, each with trade-offs"

---

Every AI tool is an answer to a question most tools never ask:

**What should humans remain capable of?**
