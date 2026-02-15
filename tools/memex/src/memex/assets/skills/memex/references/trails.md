# Trails Reference

Trails are named, ordered paths through fragments — Vannevar Bush's core memex vision. Human-curated, not auto-generated. The act of building a trail builds understanding.

## Creating a Trail

```bash
memex trail create "context engineering"
memex trail create "auth decisions" -d "How we chose JWT over sessions"
```

Trail names are unique. Descriptions are optional.

## Building a Trail from Search

The typical workflow: search → identify → add.

```bash
# Find relevant fragments
memex dig "context engineering"

# Results show @1, @2, @3...
# Add the ones that matter, in the order that tells the story

memex trail add "context engineering" @2 -n "First mention — prompt structure matters more than model choice"
memex trail add "context engineering" @5 -n "The system prompt vs few-shot comparison"
memex trail add "context engineering" @1 -n "Realization: context window is the bottleneck, not reasoning"
```

Notes (`-n`) annotate why this fragment matters in the trail. They're optional but valuable — future-you will forget why you added something.

## Walking a Trail

```bash
memex trail follow "context engineering"
```

Shows all entries in order with notes. Each fragment displays its content, timestamp, source, and annotation.

## Example: Context Engineering Trail

A trail capturing the evolution of thinking about context engineering across multiple conversations:

```bash
memex trail create "context engineering" -d "How context shapes AI output quality"

# 1. The seed — noticing that prompt structure matters
memex dig "prompt structure output quality"
memex trail add "context engineering" @3 -n "Observation: same question, different framing, wildly different output"

# 2. The framework — discovering context windows as the real constraint
memex dig "context window token limit"
memex trail add "context engineering" @1 -n "Key insight: it's not about making the model smarter, it's about what you put in the window"

# 3. The technique — system prompts vs few-shot examples
memex dig "system prompt few-shot"
memex trail add "context engineering" @2 -n "System prompts set the frame, few-shot examples set the pattern"

# 4. The refinement — RAG as context engineering
memex dig "retrieval augmented generation context"
memex trail add "context engineering" @4 -n "RAG is just automated context engineering — retrieval decides what goes in the window"

# 5. The synthesis — context engineering as a discipline
memex dig "context engineering discipline"
memex trail add "context engineering" @1 -n "The shift: from 'prompt engineering' to 'context engineering' — the whole window matters"
```

Walking this trail later:

```bash
memex trail follow "context engineering"
```

Shows the five fragments in sequence, each with its annotation — a narrative of how the thinking evolved.

## Example: Architecture Decision Trail

Capturing a project's key technical decisions across scattered conversations:

```bash
memex trail create "memex architecture" -d "Key design decisions for memex v0.2"

memex dig "hexagonal architecture memex"
memex trail add "memex architecture" @2 -n "Decision: hexagonal over layered — ports enable testing without DuckDB"

memex dig "embedding model selection"
memex trail add "memex architecture" @1 -n "Decision: nomic-embed-text-v1.5 over MiniLM — 768-dim wins on quality"

memex dig "DuckDB corpus"
memex trail add "memex architecture" @3 -n "Decision: DuckDB over SQLite — FTS + VSS in one engine"

memex dig "source adapter pattern"
memex trail add "memex architecture" @1 -n "Decision: source_kind as string, not enum — extensibility over type safety"
```

## Example: Debugging Journey Trail

Preserving the path through a hard debugging session:

```bash
memex trail create "token expiry bug" -d "The three-day JWT debugging saga"

# Add fragments in the order you discovered them
memex trail add "token expiry bug" @4 -n "Symptom: users logged out after exactly 1 hour"
memex trail add "token expiry bug" @2 -n "Red herring: thought it was the refresh token logic"
memex trail add "token expiry bug" @7 -n "Root cause: server clock skew between auth and API services"
memex trail add "token expiry bug" @1 -n "Fix: added clock tolerance to JWT verification"
```

## Multi-Trail Fragments

A fragment can appear on multiple trails. The same conversation about JWT might appear on both "auth decisions" and "token expiry bug" — different trails, different context, different annotations.

## Managing Trails

```bash
memex trail list                    # All trails with entry counts
memex trail delete "old trail"      # Interactive confirmation
memex trail delete "old trail" -y   # Skip confirmation
```

## Trail Design Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Decision trail** | Capture why choices were made | "auth decisions", "tech stack" |
| **Learning trail** | Track understanding of a topic | "context engineering", "rust ownership" |
| **Debug trail** | Preserve a debugging journey | "memory leak investigation" |
| **Onboarding trail** | Curate key context for a new person | "project onboarding", "team norms" |
| **Chronological trail** | Track evolution over time | "product vision Q1-Q2" |

## Tips

- **Name trails for the question they answer**, not the topic. "How we chose the database" is better than "database".
- **Add notes generously.** The note explains why this fragment matters *in this trail's context*. Without it, the trail is just a bookmark list.
- **Trails are cheap.** Create one per investigation. Delete the ones that don't hold up.
- **Order matters.** Fragments are displayed in the order added. Add them in the order that tells the story, not the order you found them.
