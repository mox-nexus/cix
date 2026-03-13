# Trail Architecture: Associative Paths Through Knowledge

**Date**: 2025-02-15
**Participants**: user, claude

user: Memex needs a way to link related conversations across sessions. Not just search — curated paths.

claude: This is Vannevar Bush's original "trail" concept from "As We May Think" (1945). A trail is:
- An ordered sequence of fragments
- Curated by the user (not algorithmic)
- Named and reusable
- Cross-session by definition

Implementation:
```
memex trail create "auth-evolution"
memex trail add "auth-evolution" @3  (from search results)
memex trail add "auth-evolution" @7
memex trail follow "auth-evolution"
```

Stored as edges in the knowledge graph: `TRAIL_MEMBER` edges with an `order` property.

user: How does this differ from `memex similar`?

claude: `similar` is algorithmic — finds fragments with high embedding cosine similarity. It discovers connections you didn't know about.

`trail` is intentional — you curate the path. You decide what connects. The human makes the associative links, not the algorithm.

Both are valuable. `similar` for exploration. `trail` for synthesis.

**Decision**: Implement trails as ordered, named sequences in the knowledge graph.

**Key fact**: Trail commands are: create, add, delete, follow, list. Stored as TRAIL_MEMBER edges with order property.
