# DAO Brand & Aesthetic Vision

> Dao-Aligned Organization — Collaborative Intelligence that amplifies rather than homogenizes.

## When to Use

- Designing UI for DAO/cix ecosystem
- Working on docs/experience (SvelteKit app)
- Creating brand assets
- Making visual design decisions

---

## Core Philosophy

**DAO = Dao-Aligned Organization** (recursive, like GNU)
- Protects the user's unique "way" (道/dao) against AI homogenization
- Wuwei (無為) — effortless action, flowing with natural direction

**Core insight:** The DAO exists to serve the dao. Structure enables flow.

---

## The Dialectical Visual System

This is NOT a color palette. It's a **dialectical process made visible**.

| Element | Color | Meaning | Visual Expression |
|---------|-------|---------|-------------------|
| **Blue** | Human spark | Individuality, creativity, agency | Small, bright, initiates. Appears where user choice matters. |
| **Red** | Machine constraint | Precision, coldness, structure | Containing, structural. Holds but doesn't consume. |
| **Void** | Dialectical gap | Thesis + antithesis don't add | Negative space as pause, not absence. Room for gestalt. |
| **Green** | Emergence/gestalt | Something OTHER, not sum of parts | Rare. At periphery. Earned through mastery. |

**Visual grammar:** `initiation (blue) → held by constraint (red) → across tension (void) → producing emergence (green)`

**NO PURPLE** — Blue and red don't blend. They produce green (emergence) through dialectic, not mixing.

---

## The Triad Colors

| Color | OKLCH | Use |
|-------|-------|-----|
| Blue | `oklch(62% 0.15 240)` | Links, human agency, decision points |
| Red | `oklch(58% 0.18 25)` | Warnings, constraints, limitations |
| Green | `oklch(70% 0.18 145)` | Emergence blocks only (rare!) |

### Luminosity System (4-Layer Glow)

Blue and green **emit**. Red **contains** (no glow).

```css
/* Blue Spark */
--spark-core: oklch(75% 0.18 240);        /* Brightest */
--spark-inner: oklch(62% 0.15 240 / 0.6);
--spark-outer: oklch(55% 0.12 240 / 0.2);
--spark-atmosphere: oklch(50% 0.08 240 / 0.05);

/* Green Emergence */
--emergence-core: oklch(75% 0.2 145);
--emergence-glow: oklch(70% 0.18 145 / 0.3);
```

**Usage:** SparkText for key phrases only, NOT all links. Von Restorff effect requires isolation — if everything glows, nothing stands out.

---

## Glyph Background

CSS gradients creating atmospheric presence. **Felt, not literal.**

```css
--glyph-blue: oklch(62% 0.15 240 / 0.06);   /* Max 0.08 */
--glyph-red: oklch(58% 0.18 25 / 0.03);     /* Max 0.05 */
--glyph-green: oklch(70% 0.18 145 / 0.025); /* Max 0.04 */
```

**Scope:** Ethos + landing pages only. Library stays clean for contemplative focus.

**Test:** If glyph draws eye before content hierarchy, it's too prominent.

---

## 36 Chambers (Emergence Frequency)

**36 emergence blocks total** across entire documentation. Not per page — total.

Like Wu-Tang's 36 Chambers: each one a station of transformation. Scarcity creates weight.

| Layer | Chambers | Why |
|-------|----------|-----|
| Surface (landing) | 4 | Glimpses. Sense the gestalt exists. |
| Banks (ethos) | 9 | Philosophy lives here. |
| Current (catalog) | 5 | More structural. |
| Depth (library) | 18 | Mastery compounds. |
| **Total** | **36** | |

The 9-scale encodes mastery: 9 (awareness) → 18 (competence) → 27 (fluency) → **36 (generativity)**.

**Rule:** If you have >36 emergence-worthy insights, some aren't as emergent as you think.

---

## Typography

| Role | Font | Weight |
|------|------|--------|
| Headings | IBM Plex Sans | 600 |
| Body | IBM Plex Mono | 400 |
| Code | IBM Plex Mono | 400 |

**Monospace body** signals: "this is a tool, not a magazine."

---

## Scale (9-based)

```
9 → 18 → 27 → 36 → 54
```

| Element | Size | Rationale |
|---------|------|-----------|
| Body | 18px | 2 × 9 |
| H2 | 27px | 3 × 9 |
| H1 | 36px | 4 × 9 |

---

## Weighted Rhythm

Asymmetric vertical spacing. More space above (approach) than below (departure).

```css
--pause-before: calc(var(--space-4) * 1.2);
--pause-after: var(--space-2);
--pause-dramatic: calc(var(--space-6) * 1.4);  /* Before emergence */
```

**Void is pause, not absence.** The negative space is where transformation happens.

---

## Express Entry

Return visitors (3+ visits) get condensed navigation. The space recognizes them.

- Auto-detect via localStorage
- User toggle available
- Same space, different entry depth (not a different space)

---

## Content Blocks

### EmergenceBlock (Green)

For gestalt moments — insights that couldn't exist without human+machine collaboration.

```markdown
:::emergence
This is where the paradox resolves...
:::
```

### ConstraintBlock (Red)

For warnings, limitations, anti-patterns.

```markdown
:::constraint
Do not use substitutive design...
:::
```

### SparkText (Blue)

For key conceptual phrases. **Not all links** — only phrases worth remembering.

---

## Research-Backed Guardrails

| Guardrail | Why |
|-----------|-----|
| Reduced motion support | 70M+ users with vestibular disorders |
| 4.5:1 contrast minimum | WCAG accessibility |
| Green = content semantic, not scroll behavior | Gamification backfires (b=-0.555) |
| Glow max 20% on reading surfaces | Higher values disrupt reading |
| SparkText selective only | Von Restorff effect requires isolation |

---

## The Effortless Test

> "If the user notices the design, something is wrong."

Design should disappear, leaving only understanding.

---

## Component Locations

```
docs/experience/src/lib/
├── brand/
│   ├── tokens.css       # All CSS custom properties
│   └── typography.css   # Font loading, base styles
├── components/
│   ├── atmosphere/
│   │   ├── GlyphBackground.svelte
│   │   └── VoidSpace.svelte
│   └── dialectic/
│       ├── SparkText.svelte
│       ├── EmergenceBlock.svelte
│       └── ConstraintBlock.svelte
└── stores/
    └── visitor.ts       # Express entry state
```

---

## Quick Reference

| Decision | Answer |
|----------|--------|
| Should this glow? | Only if it's a key concept worth remembering |
| Is this emergence? | Can it exist without human+machine collaboration? |
| How much glyph opacity? | If you notice it, reduce it |
| Enough void? | Pause should feel like held breath |
| Express entry? | Return visitors get direct access |
