---
name: staging
description: "This skill should be used when the user asks to 'design a scrollytelling experience', 'create staged reveals', 'pace this content', 'design progressive disclosure', or needs medium selection and experience design for content delivery."
version: 0.1.0
---

# Staging

> How the audience encounters understanding matters as much as the understanding itself.

## When to Use

Content needs to be staged — the medium and pacing are the design problem, not just the content. Scrollytelling, progressive disclosure, staged reveals, responsive adaptation, slide decks, interactive experiences.

## Medium Selection

The first decision: what medium serves the audience's journey?

| Information structure | Medium | Why |
|----------------------|--------|-----|
| Linear narrative with reveals | **Scrollytelling** | Pacing serves the argument |
| Key points with supporting detail | **Progressive disclosure** | Reader controls depth |
| Sequential build-up to insight | **Staged reveal** | Each stage adds one concept |
| Dense reference with multiple paths | **Interactive / filterable** | Reader finds their path |
| Persuasive argument with evidence | **Static page** | Don't over-stage — sometimes prose is enough |
| Training or onboarding | **Step-by-step tutorial** | Doing, then understanding |

**The test**: Does staging add to understanding, or does it add friction? If the content lands in a static page, don't add scrollytelling for impact — that's decoration, not design. Stage when the medium carries meaning.

## Beat Structure

Divide the experience into beats — moments where the audience receives one idea.

| Beat property | Design question |
|---------------|-----------------|
| **Information** | What does the reader learn at this beat? |
| **Emotion** | What should they feel? (Curiosity, concern, resolve, clarity) |
| **Action** | What do they do? (Read, scroll, click, wait) |
| **Transition** | How does this beat connect to the next? |

**One idea per beat.** Two ideas in one beat means two beats. If you can't name the single thing the reader gets at each beat, the staging isn't designed yet.

## Progressive Disclosure

Structure content at multiple depths:

| Layer | Audience | Time |
|-------|----------|------|
| **30 seconds** | The scanner | Headline + one insight |
| **5 minutes** | The interested | Full argument, key evidence |
| **Verify** | The skeptic | Sources, methodology, full data |

Each layer is complete for its audience. Nobody feels they missed something — they just didn't need more depth.

## Container Design

The container is the frame around the content — layout, navigation, visual context.

| Container element | Purpose |
|-------------------|---------|
| **Progress indicator** | "Where am I in this experience?" |
| **Navigation** | "Can I skip ahead or go back?" |
| **Visual context** | "What section am I in?" |
| **Responsive adaptation** | "Does this work on my device?" |

**Reduce, don't add.** Every container element competes for attention with the content. If a progress bar distracts from the narrative, remove it.

## Integration Review

After all pieces are built (visuals by tufte, prose by feynman + sagan, voice by orwell), jobs reviews the assembly:

1. **Pacing check**: Does each beat arrive at the right moment?
2. **Propagation check**: Does understanding build across beats, or does each beat stand alone?
3. **Medium check**: Does the staging add to understanding, or add friction?
4. **Responsive check**: Does the experience degrade gracefully on smaller screens?
5. **Reduced motion**: Does the experience convey the same understanding without animation?

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Scrollytelling for static content | Don't stage what doesn't need staging |
| Every beat is the same shape | Vary — some beats are fast, some are slow |
| Motion without meaning | Every animation must carry information |
| Mobile as afterthought | Design mobile-first, enhance for desktop |
| No escape hatch | Let the reader skip ahead if they want |

## Scope

Best for:
- Scrollytelling experiences (ethos pages, narratives)
- Multi-beat presentations
- Staged product reveals
- Interactive documentation

Not for:
- Standard documentation (use feynman directly)
- Single diagrams (use tufte directly)
- Content review (use socrates/orwell)
