# PKM Tools and the Memex Lineage

**Source type:** Web research synthesis
**Collected:** 2026-04-13
**Coverage:** Bush→Nelson→Engelbart→modern PKM, trails, knowledge graphs, effectiveness evidence

---

## 1. The Lineage

**Bush (1945):** The memex was a hypothetical desk-sized device for storing and retrieving personal records via "associative indexing" — linking any two items together and following chains of links ("trails") rather than navigating hierarchical classifications. The core insight: "The human mind operates by association. With one item in its grasp, it snaps instantly to the next that is suggested by the association of thoughts."

**Engelbart (1960s):** Built NLS/Augment, the first working system for collaborative document editing, hyperlinks, and the mouse. Survived idea: **augmentation of human intellect through interactive tools** — the computer as thinking partner, not just calculator.

**Nelson (1960s-present):** Coined "hypertext" (1963). Xanadu proposed transclusion (virtual inclusion of one document inside another), bidirectional links, and versioned content with provenance. What survived: **hyperlinks** (one-directional, degraded from Nelson's vision). What didn't survive: transclusion, bidirectional links, micropayment-based copyright.

**Berners-Lee (1989):** The Web implemented a drastically simplified version — one-directional links, no trail memory, no associative indexing. The simplification enabled adoption but lost Bush's core innovation.

**Modern PKM (2019-present):** Roam Research (2019) reintroduced bidirectional links and block references. These tools are closer to Bush's vision than the Web itself — but still miss trails as first-class objects.

**What survived across the lineage:** hyperlinks, the idea of augmentation.
**What was lost:** trails (named, shareable associative paths), transclusion, bidirectional links at the platform level, provenance tracking.

Sources:
- https://en.wikipedia.org/wiki/Memex
- https://maggieappleton.com/transcopyright-dreams
- https://jasoncrawford.org/the-lessons-of-xanadu

## 2. Trails and Associative Memory

Bush's trails were **named, reusable, shareable paths** through a personal library — not just links, but *sequences with narrative intent*. No modern tool faithfully implements this.

**Closest approximations:**
- **Roam/Logseq backlinks:** Surface associative connections but are *emergent* (discovered), not *authored* (intentionally constructed).
- **Obsidian graph view:** Visualizes the link structure but provides no sequential traversal. It's a map, not a trail.
- **Andy Matuschak's evergreen notes:** Stacked-notes navigation is closest UX to Bush's side-by-side trail display. Principles — atomic, concept-oriented, densely linked — create substrate for trail-like navigation. But trails are still implicit.
- **Notion linked databases:** Enable transclusion-like views but are structured data, not associative paths.

**The gap:** No tool treats a trail as a first-class, named, temporal, shareable object.

Sources:
- https://notes.andymatuschak.org/Evergreen_notes

## 3. PKM Tools — Implicit Cognitive Models

| Tool | Implicit model | Failure for dialogue memory |
|---|---|---|
| **Obsidian** | File cabinet + graph overlay | No temporal model; notes are static documents, not evolving understanding |
| **Roam** | Outliner + associative graph | Block = thought fragment, not conversational exchange. No speaker attribution |
| **Logseq** | Outliner + graph (open-source Roam) | Outliner hierarchy imposes structure conversations don't have |
| **Tana** | Structured database + outliner | Powerful but requires manual schema definition; conversations are unstructured |
| **Notion** | Relational database + documents | Document-centric; treats knowledge as pages, not evolving understanding |

**Common failure pattern:** All assume the human will manually decompose experience into notes/blocks. None model the *conversation* as a native unit. None track how understanding evolves over time (solidification trajectory). None distinguish between something mentioned once and something revisited and deepened across sessions.

## 4. Knowledge Graphs for Personal Knowledge

- **Zep/Graphiti (2024-25):** Temporal knowledge graph for agent memory. Edges have valid_at/invalid_at timestamps. Outperforms MemGPT on Deep Memory Retrieval benchmarks. Closest existing system to time-aware personal knowledge. (arXiv 2501.13956)
- **Mem0 (2024-25):** Hybrid — vector store + key-value store + graph store. Graph layer represents entity relationships but temporal handling is less sophisticated than Zep.
- **Cognee (2024-25):** Converts unstructured data into knowledge graphs through cognitive search. More focused on ingestion-time graph construction than temporal evolution.

**The gap:** None model the solidification trajectory — the progression from fleeting mention to consolidated understanding. They track *what changed* but not *how confident the holder became*.

## 5. Evidence of PKM Effectiveness

**The evidence base is thin.**

- Most "evidence" is survey-based and self-reported. No randomized controlled trials testing whether PKM tools improve recall, insight generation, or knowledge work outcomes.
- Matuschak has noted that spaced repetition (which has strong experimental evidence) is more robustly supported than note-taking systems.
- One practitioner reflection after two years of evergreen notes concluded they were "not optimal for skill acquisition and learning."

**Implication for memex:** The PKM field operates largely on anecdote. A system grounded in Stream A's cognitive science findings would be better positioned to make testable claims about effectiveness.

Sources:
- https://engineeringideas.substack.com/p/reflection-on-two-years-of-writing
- https://en.wikipedia.org/wiki/Personal_knowledge_management
