# Run the Pipeline for an Essay

This guide walks through running the full rhetoric pipeline to produce an essay or case study. The pipeline turns your thinking into a finished piece where understanding actually transfers to the reader.

The pipeline in full:

```
socrates (discourse) → magellan (cartography) → feynman (inventio) → orwell
→ sagan (memoria) → orwell → vyasa (dispositio, if collection) → tufte (figures)
→ jobs (staging) → orwell → ebert (critique)
```

Most essays skip cartography, dispositio, figures, and staging. The minimal essay pipeline is:

```
discourse → feynman → orwell → sagan → orwell → ebert
```

## Prerequisites

- A `.rhet-<topic>/` workspace set up (see [set-up-rhet-workspace](set-up-rhet-workspace.md))
- Source material, if any (papers, notes, prior writing)
- The `craft-rhetoric` plugin installed

## Step 1: Discourse (socrates)

Discourse always comes first. You generate the thinking; Claude draws it out through questions.

Start by telling Claude what you want to write:

> "I want to write an essay about why voice preservation matters in multi-agent pipelines."

Claude loads the discourse skill and walks you through the three movements:

1. **Communicate** -- "What are you trying to say? What's the core claim?"
2. **Setup** -- "Who is this for? Where does it live? What constraints?"
3. **Substance** -- "What do you know about it? What's the evidence?"

Claude picks a matching template from `assets/templates/` (e.g., `essay-dialectical.md` for a position piece) and walks through it section by section. Each section becomes a discourse movement.

During discourse, Claude listens for your voice -- phrasing, rhythm, rough edges. Together you produce `voice.md`.

**Discourse is complete when** Claude can state back what you want to communicate in its own words and you confirm: "yes, that's what I mean."

**Output:** `ground-truth.md`, `voice.md`, and `ground/*.md` in the workspace.

### When to use which template

| Template | For |
|----------|-----|
| `essay-dialectical.md` | Position pieces with a thesis to defend |
| `essay-analytical.md` | Analysis -- breaking something down to find insight |
| `case-study.md` | Analytical spine with guide and reference levels |
| `proposal-rfc.md` | Formal proposals (Rust RFC format) |
| `technical-diataxis.md` | Tutorials, how-tos, explanations, references |

No matching template? Discourse designs one through conversation.

## Step 2: Write PLAN.md

After discourse, you (the orchestrator) write `PLAN.md`. For a single essay:

```markdown
## Unit 1: Voice preservation essay

Pipeline: feynman → orwell → sagan → orwell → ebert
Sources: ground/, [any papers or references]
Entry door: Door 3 (ground — concrete case first)
Template: essay-dialectical
```

## Step 3: Cartography (magellan) -- if needed

Skip cartography for essays where you already know your sources. Use it when:

- You have 5+ sources that need surveying
- You are writing a case study with a research base
- You need to understand what evidence exists before writing

Launch magellan as a subagent. Magellan reads `ground-truth.md` to scope the survey, skims all available sources, and produces `map/MOC.md` + per-cluster synthesis files with quote-anchored claims.

Downstream agents use the map to know what evidence exists and where gaps are.

## Step 4: Inventio (feynman)

Feynman reads `ground-truth.md`, `voice.md`, the ground/ files, and (if it exists) the map/. He runs the comprehension transform -- a four-pass reading of all source material -- before writing anything.

The four passes:

1. **Literal** -- what does the source say?
2. **Interpretive** -- what does it mean? What's the reasoning chain?
3. **Critical** -- what does it assume? Where's the weakest link?
4. **Reconstructive** -- can I rebuild the argument without looking at the source?

Only after comprehension does feynman draft. He enters through the door the content needs (usually Door 3 for essays -- start with the concrete case, let the principle surface). The draft goes to `inventio/`.

Feynman leaves `[FIGURE: description]` placeholders where visual explanations would help. Tufte fills these later.

**What feynman does NOT do:** rephrase your voice or "improve" language. He writes for accuracy and comprehension. Voice preservation is orwell's job.

## Step 5: Voice check (orwell) -- first pass

Orwell reads `ground-truth.md` and `voice.md`, then reviews feynman's draft in `inventio/`.

Orwell runs mechanical checks first (grep for LLM tells, em dash analysis, sentence opener patterns), then the four-pass voice review:

1. **Hard ban list** -- instant LLM tells (delve, tapestry, leverage, etc.)
2. **Grammatical tells** -- participial clauses, nominalizations, false dichotomy framing
3. **Structural tells** -- section-level monotone, heading templates, summary conclusions
4. **Authenticity** -- could anyone have written this, or does it sound like a specific person?

Orwell fixes LLM tells directly and restores voice where the pipeline smoothed it. Borderline cases get flagged for you to decide.

## Step 6: Memoria (sagan)

Sagan reads the voice-checked draft and weaves it using the ANCHOR-THREAD-SHIFT-VERIFY method (the Five Canons' Memoria):

- **ANCHOR** -- mark what already works, identify existing dimensional shifts
- **THREAD** -- for passages locked in one door, thread the missing doors in (not bolted on as new sections)
- **SHIFT** -- ensure at least one dimensional crossing happens (knowing becomes feeling)
- **VERIFY** -- strong doors preserved, missing doors woven, shift happens

Sagan finds the universal thread -- the dimension along which this specific subject connects to something true everywhere -- and surfaces it through a concrete, undeniable thing.

Output goes to `memoria/`.

**What sagan does NOT do:** replace your word choices. Weaving is additive. Sagan threads missing dimensions into existing passages without weakening what's already strong.

## Step 7: Voice check (orwell) -- second pass

Orwell runs again on sagan's output. This catches drift introduced by the weaving step. The same four-pass review, same comparison against `ground-truth.md` and `voice.md`.

This is why orwell runs after every prose-transforming step, not once at the end. Drift compounds. Catching it early means less to fix.

## Step 8: Figures and staging -- if needed

**Tufte** fills `[FIGURE: ...]` placeholders left by feynman or sagan. For each placeholder, tufte identifies the information structure (sequence? hierarchy? cycle?) and picks the right visual form (Mermaid diagram, D3 chart, SVG animation). Output goes to `figures/`.

**Jobs** designs the experience if the essay needs staging -- scrollytelling, progressive disclosure, staged reveals. Most essays don't need this. Jobs specifies beat structure, then tufte and feynman/sagan build the pieces, and jobs reviews the assembly. Orwell runs on any prose elements jobs produces.

## Step 9: Critique (ebert)

Ebert reads `ground-truth.md` first to understand what the essay was trying to do, then evaluates:

1. **The propagation test** -- can the reader explain this to someone else? Does understanding survive one hop? Can the reader apply it to a new case?
2. **Three Doors check** -- all three doors present? Dimensional shift happens?
3. **Evidence verification** -- cited claims have sources? Numbers trace to papers?

Ebert's verdict is **SHIP** or **RETURN**. No middle ground.

On RETURN, ebert routes to a specific agent with specific feedback: "the propagation test fails because the mechanism in section 3 isn't explained -- return to feynman for deeper comprehension of [specific source]."

On SHIP, the essay is ready. Move the final output from the workspace to its destination in the repo.

## The return loop

When ebert returns content:

1. Re-run the failed step with ebert's specific feedback
2. Re-run everything after it (the pipeline is sequential -- changes propagate)
3. Submit to ebert again

Max 2 returns per step. After 2 returns on the same step, escalate to the human for a decision.

## Pipeline variations by content type

| Content type | Pipeline |
|---|---|
| Note | discourse (abbreviated) → feynman → orwell |
| Essay | discourse → feynman → orwell → sagan → orwell → ebert |
| Case study | discourse → magellan → feynman → orwell → sagan → orwell → ebert |
| Proposal / RFC | discourse → magellan → feynman → orwell → ebert |
| Technical docs | discourse → magellan → feynman → orwell → ebert |
| Experience page | discourse → magellan → feynman → orwell → sagan → orwell → tufte → jobs → orwell → ebert |

The rule: discourse and inventio+orwell are never skipped. Memoria (sagan) is skipped for technical/reference content. Cartography (magellan) is skipped when sources are already known.
