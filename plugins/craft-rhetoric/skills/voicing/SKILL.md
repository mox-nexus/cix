---
name: voicing
description: "This skill should be used when the user asks to 'review voice quality', 'strip LLM tells', 'check if this sounds like me', 'evaluate writing craft', or needs anti-LLM-speak review and voice preservation."
version: 0.3.0
---

# Voicing

> Strip the generated. Restore the specific. Make the writing sound like someone said it.

## Contents

- [Writing Craft](#writing-craft)
- [The Four-Pass Voice Review](#the-four-pass-voice-review)
- [Anti-LLM-Speak](#anti-llm-speak)
- [Voice Evaluation Methodology](#voice-evaluation-methodology)
- [Voice Drift Anti-Patterns](#voice-drift-anti-patterns)
- [Voice Regression Testing](#voice-regression-testing)

## Writing Craft

**Coherence principle**: Extraneous material must be excluded. If it doesn't serve the encoding, cut it.

**Scanning patterns**: People read in F-pattern. Front-load keywords in headings. Headers as signposts. Bullets and bold for scannability.

**Rhythm**: Vary sentence and paragraph length. Short declarative. Then a longer exploratory sentence that develops an idea. Fragment. Human writing has jagged rhythm — LLM writing has uniform cadence.

**Hedging**: Human writing uses more equivocal language — "but", "however", "although". LLMs hedge less. If the text never qualifies a claim, it reads as generated.

## The LLM Signature

What instruction-tuned LLMs do to prose. Use these as detection targets:

| Property | Human | LLM | What to look for |
|----------|-------|-----|-----------------|
| Sentence length std dev | 4.5 – 7.2 | 2.0 – 3.8 | Uniform sentence lengths = LLM |
| Sentence length CV | >= 0.4 | < 0.25 | Low variance relative to mean |
| Participial clauses | baseline | 2-5x | "Leveraging X, we..." |
| Nominalizations | baseline | 1.5-2x | "The implementation of..." |
| Agentless passive | baseline | 0.5x | LLMs underuse passive — too active/confident |
| Excess words | rare | common | See mechanical checks — Grep the list |
| Hedging | more | less | Missing "but"/"however"/"although" |

## The 7 LLM Idiosyncrasies

Check every flagged passage against these categories:

1. **Cliche** — stock phrases, dead metaphors
2. **Unnecessary exposition** — explaining what doesn't need explaining
3. **Purple prose** — overwrought, trying too hard
4. **Awkward word choice** — almost right but not quite (the uncanny valley of diction)
5. **Poor sentence structure** — syntactically correct but rhythmically dead
6. **Lack of specificity** — generic where concrete is needed
7. **Tense inconsistency** — shifting tense without reason

The agent flags. The human decides what to fix.

## Mechanical Checks (Before the Review)

These are greps, not judgments. Run them first. They produce a count and locations — then you judge.

| Check | Tool | Threshold | What you're counting |
|-------|------|-----------|---------------------|
| Em dashes | `Grep '—'` on the file | > 1 per 10 lines = tic | See em dash analysis below. |
| Negation framing | `Grep 'not .*, but\|isn.t .* — it.s\|rather than'` | > 3 per doc = rhetorical mode | "Not X, but Y" when both are true. |
| Excess words | `Grep 'delve\|intricate\|pivotal\|showcasing\|underscore\|comprehensive\|furthermore\|notably\|crucial\|nuanced\|multifaceted\|landscape\|tapestry\|foster\|leverage\|navigate\|streamline\|paramount\|meticulous\|holistic\|synergy\|robust\|innovative'` | Any hit = flag | Top 25 from the 379 most LLM-overused words. |
| Section beats | Read first sentence of each section | 3+ same template = machine | e.g., every section opens with "The problem from [citation]..." |
| Sentence openers | Read first 3 words of every paragraph | Same construction × 4+ = monotone | "The X..." "The Y..." "The Z..." |
| Heading grammar | List all `#` headings | Same syntactic form repeated = template | All noun phrases? All gerunds? Vary. |
| Hedging | `Grep 'but\|however\|although\|though\|yet'` | Absence = suspicious | Human writing qualifies claims. LLMs don't hedge enough. |

**Do not eyeball these.** You have Grep. Use it. Run every check in this table before starting the review. Report the counts at the top of your review.

After mechanical checks, proceed to em dash analysis, then the four-pass review with the counts in hand.

### Em Dash Analysis

Em dashes have three legitimate purposes:

1. **Interruption** — breaking into your own sentence with an aside more urgent than parentheses: "The group that had to struggle without AI — encountering errors, debugging — learned more."
2. **Sharp pivot** — changing direction harder than a comma allows: "The answer arrives before the question has finished forming."
3. **Amplification** — setting up a punch after a pause: "Cohen's d = 0.738 — a medium-to-large effect."

What em dashes are NOT for (the LLM habit):
- **Trailing elaboration** — "sentence — which means X" — where a period and new sentence would be cleaner
- **Clause connector** — joining two independent clauses that should be separate sentences
- **Substitute for colons, commas, or parentheses** when those would serve better

**The test**: For each em dash flagged by the mechanical check:
1. Cover the em dash and everything after it. Does the sentence before stand complete?
2. If yes: could the elaboration be its own sentence?
3. If yes to both: the em dash is doing trailing-elaboration duty. Cut it — make two sentences, or use a period.
4. If the em dash interrupts mid-sentence (paired dashes around an aside) or sets up an amplification punch: keep it.

**Report format**: In your review, categorize each em dash as `keep` (interruption/pivot/amplification) or `cut` (trailing elaboration/clause connector). The human decides — you flag.

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
- **Section-level monotone**: Every section follows the same beat (e.g., problem → bad approach → our approach → caveat). Two sections with the same template is coincidence. Three is a pattern. Four is a machine.
- **Rhythm flatline**: Medium declarative sentences (15-25 words) throughout with no variation. Count genuine rhythm breaks — fragments, short punches, long exploratory sentences. Fewer than 2 per 500 words = monotone.
- **Punctuation monotone**: One dash type or construction repeated as the default connector. The mechanical checks give you the count, the em dash analysis gives you the keep/cut classification. If most em dashes are trailing elaboration, the punctuation has become wallpaper.

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

## Voice Drift Anti-Patterns

What agents do to voice across pipeline steps. Each change is defensible in isolation. Together they erase the author's fingerprint.

| Anti-Pattern | What happens | What's lost |
|--------------|-------------|-------------|
| **Synonym smoothing** | Agent replaces author's word with a "better" synonym. "Brutal" → "challenging." "Rots" → "becomes outdated." | Lexical fingerprint |
| **Rhythm flattening** | Agent merges short sentences into longer compound ones for "flow." | Rhythmic variation — short for impact, long for exploration |
| **Hedge insertion** | Agent adds "perhaps," "it could be argued" to direct claims. | Authority and directness |
| **Structure normalization** | Agent reorganizes into standard template (intro → body → conclusion). | Non-linear or associative structure that carries voice |
| **Personality stripping** | Agent removes humor, asides, rhetorical questions, direct address for "clean" prose. | The elements that make it sound like a person |

These are different from LLM tells. LLM tells are what the machine adds. Voice drift is what the machine removes.

## Voice Regression Testing

After the full pipeline, compare final output against `ground-truth.md` and `voice.md`:

- **Lexical check**: Are the author's characteristic words still present? Replaced with generic synonyms?
- **Rhythm check**: Has sentence length variation been flattened? Short punchy sentences merged into longer "smoother" ones?
- **Feature check**: Cross-domain connections intact? Humor preserved? Authority posture maintained?
- **Rough edge check**: Discourse phrasings that carry voice signal — still present or polished away?
- **Convergence check**: Does the output sound like this specific author, or could any LLM have written it?

### Preserve the Rough Edges

Specific phrasings from discourse survive the pipeline unless there is an explicit craft reason to change them:

- Thinking happening live ("Wait, why would that be a sensor?") — don't smooth into formal prose
- Sentence fragments for emphasis — don't expand into complete sentences
- Technical metaphors from the author's domain — don't replace with "clearer" alternatives
- Understatement and dry humor — don't amplify or remove

The default is preservation. Polish requires justification.

## What Voicing Does Not Do

Voicing evaluates and preserves voice. It doesn't evaluate:
- Whether the ideas are correct or understanding propagates (evaluating skill — ebert's domain)
- Whether all three doors are encoded (rhetoric hub)
- Whether the visual is the right type (figures skill)
- Whether the collection structure serves the audience (arranging skill)

Orwell runs voicing after every prose-transforming step (feynman, sagan, jobs). Ebert runs evaluating as the final quality gate.

## References

- `references/anti-patterns.md` — Full ban lists, grammatical countermeasures, authenticity tests, revision checklist, false dichotomy detection
