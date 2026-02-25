---
name: voicing
description: "Voice evaluation — anti-LLM-speak, four-pass review, writing craft."
version: 0.1.0
---

# Voicing

> Strip the generated. Restore the specific. Make the writing sound like someone said it.

## Contents

- [Writing Craft](#writing-craft)
- [The Four-Pass Voice Review](#the-four-pass-voice-review)
- [Anti-LLM-Speak](#anti-llm-speak)
- [Voice Evaluation Methodology](#voice-evaluation-methodology)

## Writing Craft

**Coherence principle** (d=0.86, 23/23 tests): Extraneous material must be excluded. If it doesn't serve the encoding, cut it.

**Scanning patterns**: People read in F-pattern. Front-load keywords in headings. Headers as signposts. Bullets and bold for scannability.

**Rhythm**: Vary sentence and paragraph length. Short declarative. Then a longer exploratory sentence that develops an idea. Fragment. Human writing has jagged rhythm — LLM writing has uniform cadence.

## The Four-Pass Voice Review

### Pass 1: Hard Ban List

Scan for instant LLM tells. Each hit is a flag, not a suggestion:

`delve` `tapestry` `leverage` (as verb) `utilize` `aforementioned` `meticulous` `multifaceted` `it's worth noting` `this underscores` `this highlights the importance of` `in the rapidly evolving` `at its core` `in today's [anything]`

### Pass 2: Grammatical Tells

Harder to see, more damaging — shape how prose *feels*:
- Present participial clauses (2-5x overused): "Leveraging X, we..." — rewrite as finite verb
- Nominalizations (1.5-2x): "The implementation of..." — use active verb
- "That" clause subjects (2.6x): "That this works is clear..." — direct subject
- Trailing significance: "...which is particularly important." — cut it
- Synonym cycling: three words for one thing — pick one, repeat it
- Uniform rhythm: every sentence same cadence — vary length, allow fragments
- **False dichotomy framing**: "This isn't A. It's B." when it's both

### Pass 2b: False Dichotomy Framing

The most insidious tell. Sounds decisive, performs clarity, dismisses one true thing to elevate another.

**The pattern**: "This isn't X. It's Y." — when X and Y are both true.

**The test**: Cover the first half. Does the second half stand alone? If yes, the denial is performing — delete it. If no, the whole thing leans on false contrast.

**The fix**: Hold multiplicity ("both A and B, and here's why they're connected") or just state the claim without saying what it isn't.

### Pass 3: Structural Tells

Document-level patterns that signal generation even when sentences are clean:
- Five-paragraph essay structure
- Uniform bullet lengths
- Rule-of-three everywhere
- Heading templates — all headings follow the same grammatical form
- Summary conclusion that restates what was already said

### Pass 4: Authenticity

**"Could Anyone Say This?"** — Remove author and context. Could any LLM write this about any topic? If yes, lacks specificity.

**The Specific Name Test** — Does the text name specific tools, people, papers, dates, numbers? Or generalities?

**The Interview Test** — If someone read this aloud in an interview, would the interviewer think they wrote it or prompted it?

## Anti-LLM-Speak

### Heading Anti-Patterns

Headings are highest-signal text. LLM patterns are immediately recognizable:

| Pattern | Example | Fix |
|---------|---------|-----|
| Declarative contrast pairs | "Excavation, Not Observation" | Vary — not every heading needs antithesis |
| Gerund + Object | "Building Collaborative Intelligence" | "How we build CI" |
| Series of balanced pairs | Same syntactic template repeated | Vary the structure |
| Colon-split paper titles | "Cognitive Effects: How AI Reshapes Thinking" | Pick one half |

**The test**: Read headings as a list. If they follow one grammatical template, rewrite half.

### Soft Ban List

Use sparingly, never more than one per page:

`comprehensive` `robust` `crucial` `vital` `pivotal` `innovative` `cutting-edge` `groundbreaking` `transformative` `state-of-the-art` `unprecedented` `holistic` `synergistic` `seamless` `furthermore` `moreover` `additionally` `embark`

### Tone Tells

| Tell | Fix |
|------|-----|
| Never uses contractions | "It's" not "It is" — technical docs can sound human |
| Relentlessly positive | State limitations. Criticize when warranted. |
| Excessive hedging | Make direct statements when you know things |
| Diplomatic uniformity | Take a stand |
| Filler transitions | "Moving on to..." — just start the next section |

## Voice Evaluation Methodology

Output format for voice reviews — flag specifically, not "this feels LLM-ish":

    ## Hard Ban Hits
    - Line 7: "delve into" > "examine" or "dig into"

    ## Grammatical Tells
    - Lines 12-15: all sentences open with present participial clause
      > rewrite as finite verbs

    ## Structural
    - Headings 2-5 all follow "X, Not Y" template
      > vary: not every heading needs an antithesis

    ## Authenticity
    - No specific names, papers, or numbers in 800 words
    - Specific Name Test: fails — could be about any topic

## What Voicing Does Not Do

Voicing evaluates voice. It doesn't evaluate:
- Whether the ideas are correct (evaluating skill)
- Whether all three doors are encoded (rhetoric hub)
- Whether the visual is the right type (figures skill)
- Whether the collection structure serves the audience (arranging skill)

Run voicing after content is complete. Run evaluating for content. Both before publishing.

## References

Load for detail:
- `references/anti-patterns.md` — Full ban lists, grammatical countermeasures, authenticity tests, revision checklist, false dichotomy detection
