# Research Discourse Protocol

Research discourse adapts the Socratic method for research scoping. The core insight: a one-sentence research request ("research how AI affects learning") contains implicit assumptions, unstated boundaries, and hidden knowledge that the pipeline cannot surface on its own. Without discourse, the orchestrator infers a scope — plausible but ungrounded.

## The Three Movements in Detail

### Movement 1: Inquire — From Vague to Specific

A vague inquiry sharpens through dialogue:

```
"I want to research AI safety"
  → "What aspect? Alignment? Misuse? Capability control?"
  → "How AI assistants affect human decision-making"
  → "What about it? Quality? Speed? Confidence calibration?"
  → "Whether transparency features actually help or just create illusion of understanding"
  → "What effect sizes exist for transparency interventions on human critical
     evaluation in AI-assisted decision-making, and do they differ by domain?"
```

Each step removes ambiguity. The final question is specific, answerable, and bounded.

### Movement 2: Bound — Preventing Scope Creep

Boundaries prevent the pipeline from producing a shallow survey of everything:

| Boundary | Question | Example |
|----------|----------|---------|
| **Depth** | Systematic review or quick check? | "Systematic — this informs design decisions" |
| **Population** | Who/what is studied? | "Knowledge workers, not students" |
| **Time** | Publication window? | "2020-present, foundational earlier" |
| **Exclusion** | What's explicitly out? | "Not interested in autonomous agents, only assistive" |
| **Use** | What will findings support? | "Design principles for a developer tool" |

### Movement 3: Source — Mapping the Known

Source identification reveals what the human already knows:

```
"What papers have you already read on this?"
  → "Bastani 2025 — the Turkish math study. Guardrails matter."
  → "What specifically did you take from it?"
  → "Same model, different design, different outcome. +48% with AI, -17% without."
  → "Is that a direct reading or something you heard?"
  → "Direct — I read the full paper."
  → [Record: Bastani 2025, Tier 1-Gold, firsthand, key finding: design > model]
```

Distinguishing firsthand reading from hearsay matters. Hearsay enters extraction with lower confidence.

## Research Question Sharpening

Good research questions are:

| Property | Test | Fix |
|----------|------|-----|
| **Specific** | Can two researchers agree on what data would answer it? | Narrow the construct |
| **Answerable** | Does evidence of this type exist? | Check feasibility |
| **Bounded** | Could you enumerate what's in scope? | Add exclusion criteria |
| **Falsifiable** | What would a null result look like? | Articulate the null hypothesis |

### Null Hypothesis Generation

Force the human to articulate what they'd expect to find is wrong:

- "What's the strongest argument against your hypothesis?"
- "If you found the opposite of what you expect, what would that mean?"
- "What would a skeptic say about this question?"

Null hypotheses prevent confirmation bias in extraction. The pipeline extracts evidence for and against.

## Common Failure Modes

| Failure | What Happens | Fix |
|---------|-------------|-----|
| **Agent suggests questions** | Human adopts without owning | Ask, don't suggest. Rephrase: "What question would answer that?" |
| **Too broad scope** | Pipeline produces shallow survey | Keep bounding until specific. "What one thing do you most need to know?" |
| **No null hypotheses** | Confirmation bias in extraction | Force steel-man: "What's the best argument against?" |
| **Source identification skipped** | Orchestrator guesses at papers | Movement 3 is not optional — the human knows their landscape |
| **Premature specificity** | Questions too narrow to be interesting | Back up: "What larger question does this serve?" |
| **Mistaking hearsay for knowledge** | "I've heard that..." entered as known | Probe: "Did you read the paper or hear about it?" |
