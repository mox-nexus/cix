# CIX Experience (Documentation Site)

> SvelteKit-powered documentation and landing experience for CIX.

## Component Architecture

### Landing Page Composition

The landing page uses a **composition pattern** where:

1. **Components declare minimum size** - each component specifies what it needs at minimum
2. **Composition decides maximum** - the grid distributes remaining space
3. **Sigil expands** - center component fills available space after others take their minimum

```
DESKTOP (100vh Canvas)
┌────────────────────────────────────────────────────────┐
│                     NORTH (auto)                       │
│                   BrandHero                            │
├──────────┬─────────────────────────────┬───────────────┤
│   WEST   │         CENTER (1fr)        │     EAST      │
│ (min-c)  │      Sigil expands to       │   (min-c)     │
│Philosophy│      fill this space        │  QuickStart   │
├──────────┼─────────────────────────────┼───────────────┤
│MARGIN-SW │        SOUTH (auto)         │  MARGIN-SE    │
│Manifesto │      NavigationCTA          │   (empty)     │
└──────────┴─────────────────────────────┴───────────────┘

MOBILE (Scrollytelling)
┌──────────────────┐
│ 1. North (brand) │  ← Each section is
├──────────────────┤     100vh "slide"
│ 2. Center (sigil)│
├──────────────────┤
│ 3. South (CTAs)  │  ← Smaller sections
├──────────────────┤     are 50vh
│ 4. West (philo)  │
├──────────────────┤
│ 5. East (quick)  │
├──────────────────┤
│ 6. SW (manifesto)│
└──────────────────┘
```

### Component Responsibilities

| Component | Location | Min Size | Purpose |
|-----------|----------|----------|---------|
| `LandingComposition` | `landing/` | 100vh | Grid layout with 7 snippet slots |
| `BrandHero` | `landing/` | auto | CIX + tagline (north) |
| `Philosophy` | `landing/` | 160px | Methodology text (west) |
| `Sigil` | `landing/` | fills | Animated SVG + cage (center) |
| `QuickStart` | `landing/` | 200px | Install cmd + demo (east) |
| `NavigationCTA` | `landing/` | auto | Links (south) |
| `TypewriterManifesto` | `manifesto/` | auto | AMPLIFY RADICAL... (margin-sw) |
| `MarginSW/SE` | `landing/` | auto | Slot wrappers for margins |

### Key Principles

**Components declare min, composition decides max:**
```css
/* In component */
.quickstart {
  min-width: 200px; /* I need at least this */
}

/* In composition */
grid-template-columns: minmax(min-content, 1fr) ...;
/* Grid distributes remaining space */
```

**Desktop = Canvas, Mobile = Scrollytelling:**
- Desktop: Fixed 100vh, no scroll, all content visible
- Mobile: Flex column, each section becomes a scroll "slide"
- CSS `order` property controls mobile scroll sequence

**Sigil expands to fill:**
```css
.pos-center {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0; /* Allow shrinking if needed */
}

.sigil {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Maintain aspect ratio */
}
```

---

## File Structure

```
docs/experience/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── landing/           # Landing page components
│   │   │   │   ├── LandingComposition.svelte
│   │   │   │   ├── BrandHero.svelte
│   │   │   │   ├── Philosophy.svelte
│   │   │   │   ├── Sigil.svelte
│   │   │   │   ├── QuickStart.svelte
│   │   │   │   ├── NavigationCTA.svelte
│   │   │   │   ├── MarginSW.svelte
│   │   │   │   ├── MarginSE.svelte
│   │   │   │   └── index.ts
│   │   │   ├── manifesto/         # Manifesto components
│   │   │   │   ├── TypewriterManifesto.svelte
│   │   │   │   └── index.ts
│   │   │   ├── glyph/             # Sigil compositions
│   │   │   │   └── CanonicalSigil.svelte
│   │   │   └── dialectic/         # Dialectical notation
│   │   └── brand/
│   │       └── tokens.css         # Design tokens (OKLCH)
│   └── routes/
│       └── +page.svelte           # Landing page route
└── CLAUDE.md                      # This file
```

---

## Design Tokens

The site uses OKLCH color system with dialectical semantics:

| Token | Color | Meaning |
|-------|-------|---------|
| `--ci-blue` / `--spark-*` | Blue | Human agency, spark |
| `--ci-red` / `--constraint-*` | Red | Machine constraint |
| `--ci-green` / `--emergence-*` | Green | Synthesis, emergence |

4-layer luminosity system for glows:
- `--spark-core` → `--spark-inner` → `--spark-outer` → `--spark-atmosphere`

---

## Accessibility

- `prefers-reduced-motion`: Disables animations, shows static content
- `TypewriterManifesto`: Detects motion preference in JS, shows full words immediately
- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`
- Skip link provided

---

## Adding New Landing Components

1. Create component in `src/lib/components/landing/`
2. Declare `min-width` or `min-height` the component needs
3. Export from `landing/index.ts`
4. Add snippet slot to `LandingComposition` if needed
5. Compose in `CanonicalSigil.svelte`
