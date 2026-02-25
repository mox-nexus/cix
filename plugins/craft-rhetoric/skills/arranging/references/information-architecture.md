# Information Architecture

How to organize information so people can find it. The prior question before "how do I write this?" is "where does this live?"

## Core Principles

### 1. Match User Mental Models

People have expectations about where things live. Structure should match how they think, not how you organized it internally.

| Your logic | Their logic |
|------------|-------------|
| "We organized by team" | "I need to do X, where is it?" |
| "This is technically accurate" | "I expected it to be here" |
| "It's in the advanced section" | "I didn't know it was advanced" |

**Test**: Ask someone unfamiliar where they'd look for X. If they guess wrong, the architecture is wrong.

### 2. One Home for Each Thing

Every piece of information has exactly one canonical location. Other places link to it.

| Problem | Symptom | Fix |
|---------|---------|-----|
| Same info in multiple places | Inconsistency when one updates | Single source, link everywhere else |
| Unclear where something belongs | People create duplicates | Define clear categories |
| "It could go either place" | It goes in both, eventually conflicts | Make a decision, document it |

### 3. Progressive Depth, Not Progressive Hiding

Organize by depth of detail, not by "basic vs advanced" judgment.

```
Layer 1: What you need to know (everyone)
Layer 2: How it works (practitioners)
Layer 3: Why it works (evaluators)
Layer 4: Primary sources (researchers)
```

Everyone enters at layer 1. They go deeper if they need to. Nobody is told "this isn't for you."

### 4. Findability Over Elegance

A messy structure people can navigate beats an elegant structure they can't.

| Elegant but unfindable | Findable but messy |
|------------------------|-------------------|
| Perfect taxonomy nobody understands | Redundant navigation paths |
| Minimal categories | Multiple ways to find same thing |
| "It's logically consistent" | "I found what I needed" |

When in doubt, add navigation, not categories.

## Organizational Patterns

### By Task (Recommended for docs)

```
getting-started/     -> "I'm new"
how-to/              -> "I need to do X"
concepts/            -> "I need to understand Y"
reference/           -> "I need to look up Z"
```

Maps to Diataxis. Works because it matches user intent.

### By Topic

```
authentication/
database/
api/
deployment/
```

Works when users know what topic they need. Fails when they don't know the right word.

### By Audience

```
for-developers/
for-operators/
for-executives/
```

Works when audiences are distinct. Fails when someone is multiple roles.

### Hybrid (Common)

```
getting-started/      -> by task (entry point)
guides/
  ├── authentication/ -> by topic (once they know what they need)
  ├── database/
  └── api/
reference/            -> by task (lookup)
```

## Navigation Patterns

### Multiple Entry Points
Don't assume everyone enters at the home page. Search lands people on random pages. Every page should orient the reader.

### Breadcrumbs
Show where they are: `Home > Guides > Authentication > OAuth Setup`

### Cross-Links
Connect related content across categories. Don't trap readers in one branch.

### Navigation Aids

| Aid | Purpose |
|-----|---------|
| Table of contents | Overview of current page |
| Sidebar nav | Overview of section |
| Breadcrumbs | Location in hierarchy |
| "See also" links | Related content |
| Search | Escape hatch when nav fails |

## Common Mistakes

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Too many categories | Trying to be comprehensive | Fewer categories, more cross-links |
| Too few categories | Trying to be simple | If people can't find things, add structure |
| Organizing by internal structure | "That's how our code is organized" | Organize by user mental model |
| Deep nesting | Trying to be precise | Flatter is usually better |
| No landing pages | Jumping straight to content | Every section needs an overview |

## Deciding Where Content Lives

| Content type | Lives in | Because |
|--------------|----------|---------|
| "What is X?" | Explanation | Conceptual |
| "How do I do X?" | How-to | Task-oriented |
| "What exactly does X do?" | Reference | Lookup |
| "Research shows X" | Reference/research | Evidence |
| "Citation for X" | Bibliography | Source |

If something could go in two places, it goes in the deeper one and gets linked from the shallower one.

---

**Sources**: Rosenfeld, Morville & Arango (2015) *Information Architecture* 4th ed., Nielsen Norman Group IA research, Wodtke & Govella (2009) *Information Architecture: Blueprints for the Web*
