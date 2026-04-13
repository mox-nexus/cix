# The Concepts

What memex's design rests on. Read this, then forget the papers.

---

## How memory actually works

### Memory is reconstruction, not playback

When you remember a conversation from last week, you're not playing back a recording. You're rebuilding it — right now, from fragments. Bartlett showed this in 1932: people told a Native American folk story and asked to retell it weeks later changed the details to fit their own cultural schemas. They weren't lying. They were remembering. That's what remembering IS.

The implication: there is no "original" stored somewhere. What's stored is a **schema** — a reconstruction template. The schema says "conversation about architecture, with Yash, felt productive, something about trails." The specific words, the exact sequence, the precise ideas — those are rebuilt at recall time from the schema plus whatever you're thinking about right now.

This is why two people remember the same conversation differently. They have different schemas. They're rebuilding different versions from different templates.

### Every time you recall something, you rewrite it

Nader (2009) showed that memories are not consolidated once and then frozen. Every time you reactivate a memory — every time you think about it — it becomes **labile** again. It literally destabilizes at the molecular level (PKMzeta, the protein that maintains synaptic strength, stops doing its job) and has to restabilize. The restabilized version incorporates whatever you were thinking about during the recall.

This is called **reconsolidation**. It means recall is a write operation, not a read.

Think about a conversation you've retold many times. Each retelling changed it a little. The version you remember now is not the original — it's the version that survived repeated reconsolidation. The original is gone. What you have is the nth-generation copy, shaped by every retelling.

For memex: every time the user revisits a memory, that's a reconsolidation event. The system should record the revisit (append to the trail) because the memory LITERALLY CHANGED in the user's mind. The trail captures what happened to the memory over time.

### The thing you remember is not the thing that happened — it's the schema it left behind

Squire (1982) showed that specific episodes can dissipate from storage entirely while still shaping behavior. You can't recall the specific conversation, but the idea it planted is still influencing how you think. Wilson (2002) adds that fresh memories have a quality of "reliving" — you can almost feel yourself back in the room. That quality fades with retelling. The memory crystallizes into "just something I know."

This maps to a two-tier system that both Squire and Tulving describe: **episodic memory** (event-specific, contextual, with that reliving quality) and **semantic memory** (context-free, crystallized, "just something I know"). The boundary isn't sharp or permanent — episodic memories migrate to semantic over time. The episode fades; the schema it shaped persists.

This is the **solidification trajectory**:

```
Fresh episode          → you can almost relive it (episodic: contextual, situated)
Retold a few times     → details fade, core persists
Integrated into schema → "just something I know" (semantic: context-free, durable)
Crystallized artifact  → a principle, a decision, a design doc
```

Each stage is less vivid but more durable. The raw conversation fades. The insight it produced hardens.

For memex: Frame (raw message) → re-accessed Frame → annotated Frame → Artifact. The system should expect Frames to become less useful over time while the Artifacts they generate become more durable. Both need to exist. The Frame is provenance; the Artifact is the living knowledge. The SUPERSEDES relation captures the crystallization: Artifact v3 supersedes v2 supersedes v1, each more settled.

---

## How recall works

### The fog-match (synergistic ecphory)

This is the concept Yash named before learning the term. Tulving (1984) calls it **synergistic ecphory**: recall happens when two things collide — (1) what was stored, and (2) what you're currently thinking about. Neither alone is sufficient. The stored trace needs the right cue, and the cue needs the right trace.

Wiseman & Tulving (1976) demonstrated this sharply: people were shown words paired with weak associates (e.g., "train" paired with "black"). Later, given "black" as a cue, they recalled "train" — even though they FAILED to recognize "train" from a list. The copy of the word itself wasn't enough. The cue that was PRESENT AT ENCODING succeeded where a direct match failed.

This is **encoding specificity**: the best retrieval cue is one that was present when the memory was formed. Not the most "similar" cue. Not the most "relevant" cue. The cue that matches the ENCODING CONDITIONS.

Think about what this means for search. You're looking for something you discussed weeks ago. You don't remember the exact words. But you remember you were working on the reactor pipeline, it was late at night, you were frustrated about dedup logic. That contextual state — the project, the mood, the problem — is the retrieval cue. Content-similarity search ("find text similar to this query") misses this entirely. It matches WHAT was said. Ecphory matches the CONDITIONS under which it was said.

For memex: retrieval should use not just the query text, but the user's current context — what project they're in, what trail they're following, what they've been discussing recently. This is the context vector. It's the "fog" half of the fog-match.

### Context matters for updating memories too

Nader (2009) showed that reconsolidation is context-dependent. In one human study, interfering with a consolidated memory only worked when subjects were in the SAME ENVIRONMENT as the original learning. Different room? No interference. Same room? Memory destabilized.

For memex: if you want to help the user update their understanding (not just recall it), showing them the original conversation context alongside the new information matters. The trail-follow + annotate workflow does this: you revisit old frames IN CONTEXT and add new understanding.

---

## What's special about conversation

### 90% gone in 5 minutes

Stafford (1984): even after only five minutes, people recall about 10% of what was said in a social exchange. This is not a failure of memory. This is normal. Conversations are "jointly created, constantly updated, and necessarily readily accessible by participants" — they are designed for the moment, not for storage.

One more finding: people remember more of their PARTNER's contributions than their own.

This is the fundamental justification for memex. Without external memory, 90% of conversational content vanishes within minutes. The system compensates for a specific, quantified property of how humans process dialogue. The implication for what to weight: the AI's responses may be more recoverable as anchor points for the user than the user's own words.

### Dialogue is joint construction, not alternating monologue

Pickering & Garrod (2004): in conversation, the two speakers' linguistic representations become aligned at multiple levels through a largely automatic process. You don't just take turns talking — you converge. Your mental models sync up. The "output" of a conversation isn't the sum of what each person said. It's the alignment state you reached together.

This reframes what memex should store. The individual message (Frame) is the storage unit — but the RETRIEVAL unit might need to be bigger. Not "the message where Yash said X" but "the exchange where we converged on X." The event worth surfacing isn't a single utterance; it's the moment the two participants clicked into shared understanding, or the moment they diverged and talked past each other.

For memex: chunking conversations by topic shift and alignment event rather than by message count. The conversation structure — not just the content — carries meaning.

---

## Insight

### The click is real and measurable

Beeman (2004), Kounios (2009): insight has a measurable neural signature — a burst of gamma-band activity in the right anterior superior temporal gyrus, starting 0.3 seconds BEFORE the person reports the "aha" moment. It's not just a feeling. It's a distinct neural event.

But it FEELS sudden even though it ISN'T. The brain has been processing continuously — the gamma burst is the culmination. This matters architecturally: the conversation content before the click isn't irrelevant context. It's the substrate from which the insight emerged. Storing the full conversation (not just the insight moment) is correct because the preparatory processing is in the preceding discourse.

### You cannot predict insight, but you can recognize it after

Metcalfe (1986, 1987): people's feeling-of-knowing ratings have nearly zero predictive power for insight problems. They can predict their performance on algebra — gamma of .40. They cannot predict insight — gamma of .08. The comparison isn't subtle: .08 is not significantly above zero.

But Beeman (2004) showed that post-hoc self-reports ("I solved it with insight" vs "I solved it analytically") DO correlate with the neural signatures. You can't predict it. You can recognize it after it happens. These are different temporal windows, not contradictory findings.

For memex: let users tag insights after the fact. Trust those tags. Don't prompt "did you just have an insight?" during the conversation — that interrupts flow and the report wouldn't be reliable anyway. And don't try to detect insight automatically from text — the precursors are neural, not linguistic.

### Delayed annotation is more accurate

Thiede (2003): generating keywords AFTER a delay (not immediately) improves metacognitive accuracy. When you annotate something right after it happens, your judgment is colored by the vividness of the experience. When you annotate it later, you have better calibration of what actually mattered.

There's a related reason to separate capture from annotation: Lutz & Thompson (2003) found that the act of generating a report about an experience can modify the experience. If you're asked "was this an insight?" mid-conversation, the answer changes what the conversation was. Post-hoc annotation avoids this contamination.

For memex: capture is immediate and automatic. Annotation is separate and deliberate — and the system should expect it to happen later, not during the live conversation. The trail-building workflow (revisit and annotate days or weeks after) is better calibrated than inline tagging.

---

## Purpose-neutral storage

Wilson (2002): human mental representations "appear to be to a large extent purpose-neutral" — not indexed to anticipated future use. This gives enormous flexibility. You don't know what you'll need the memory FOR, so encoding it broadly (not narrowly for one anticipated retrieval pattern) is the adaptive strategy.

For memex: embed content broadly (semantic embeddings), don't presuppose future queries. Don't tag-for-retrieval at ingest time. Don't categorize. Store the content and let the retrieval system figure out what's relevant when the time comes. This is the argument for embeddings over categories, and for broad encoding over narrow tagging. The fog-match only works if the stored trace was encoded with enough breadth to be triggered by cues you didn't anticipate.

---

## How LLMs "remember" (and where the analogy breaks)

### Induction heads ARE retrieval

Olsson (2022): in-context learning is mechanistically implemented by **induction heads** — attention heads that find previous occurrences of the current token and predict what followed. This is literal pattern-matching: current token is the retrieval cue, previous occurrence is the stored trace, prediction is the output.

The structural parallel to Tulving's ecphory is genuine at the mechanism level — both are two-input systems. Current state + stored trace → output. The mechanism differs (attention weights vs neural reconsolidation) but the shape is the same.

There's a second, deeper interpretation (von Oswald 2022): in-context learning may be equivalent to gradient descent running in the forward pass. Each transformer layer implements a step of optimization on the in-context examples. If this is right, then context IS training data for a rapid re-learning episode — and the FORM of what memex injects into context matters for how well the LLM uses it. "Learnable" format, not just present.

### The context window is working memory

The KV cache stores encoded representations of all previous tokens. Keys = encoding conditions. Values = stored content. Attention = retrieval (query matches against keys, retrieves weighted values). This is the episodic buffer for the current conversation. When the context window fills up, information is effectively "forgotten" — the parallel to human working memory capacity limits.

Managing what goes into the context window IS managing the LLM's working memory. Memex's recall pipeline is effectively a KV cache population strategy.

### Lost-in-the-middle

An (2024): LLMs attend more to information at the beginning and end of context, less to the middle. U-shaped attention curve. This is the serial position effect — primacy and recency — showing up in transformers for completely different mechanistic reasons than in humans. In humans, primacy and recency effects emerge from working memory dynamics. In LLMs, the effect appears to come from insufficient training supervision on long-context tasks. Same curve, different cause.

For memex: when loading recalled content into the context window, put important information at the beginning or end. If you load many recalled items, those in the middle will be under-attended.

### Where the analogy BREAKS

**Reconsolidation vs catastrophic forgetting.** In humans, retrieval STRENGTHENS memories (reconsolidation restabilizes them). In LLMs, retraining WEAKENS old memories (weight interference overwrites old representations). The directions are OPPOSITE. This is why memex uses RAG (external retrieval into context), not fine-tuning, for memory augmentation. Fine-tuning as memory formation is destructive in LLMs in a way human memory formation is not.

**No insight analogue.** There is no evidence of discontinuous inference in LLMs — no "aha" moment, no sudden restructuring. If insight happens in a human-AI conversation, it happens on the human side. Memex can't detect it from the LLM's behavior; it has to be recognized post-hoc by the user.

**Both confabulate.** Human memory produces plausible-but-wrong reconstructions (Bartlett). LLMs produce plausible-but-wrong generations (hallucination). Both are generative systems. Neither is a reliable record. Memex exists to be the reliable record that neither substrate provides.

---

## The metacognitive asymmetry

Metcalfe (1986, 1987): self-reports are reliable for declarative recall ("do I know this fact?") but unreliable for insight ("will I solve this problem?"). This means:

- User says "this was an important fact" → somewhat trust it
- User says "I just had an insight" → trust that they HAD one (post-hoc recognition works), but their sense of HOW IMPORTANT it is may be poorly calibrated
- User says "I feel like I'm getting close to something" → unreliable for insight, ignore as a detection signal

The system should not uniformly trust or uniformly distrust user tags. The trust level depends on what kind of cognitive event the tag refers to. Declarative recall tags: trust. Insight importance ratings: treat as noisy. Pre-insight signals: discard.

---

## Bush's trails — and what five systems missed

Bush (1945) proposed the memex with one central innovation: **trails**. Named, reusable, shareable associative paths through a personal library. Not just links between items — authored sequences with narrative intent. "The owner of the memex... builds a trail of his interest through the maze of materials available to him."

A trail is:
- **Named** — it has an identity ("the reactor pipeline trail," "the ecphory trail")
- **Ordered** — it has a sequence, a beginning and an end (or at least a direction)
- **Authored** — someone constructed it deliberately, not algorithmically
- **Temporal** — it records WHEN each item was added to the trail
- **Shareable** — it can be given to someone else

The Web implemented links. It did not implement trails. Roam implemented backlinks. It did not implement trails. Obsidian implemented a graph view. It did not implement trails.

Four modern AI memory systems — Letta, Mem0, Zep, Cognee — all share these properties:

1. An LLM decides what to remember (either the reasoning LLM or a separate extraction call)
2. Conversations are decomposed into facts, entities, or blocks — the original dialogue structure is discarded
3. Retrieval is content-similarity (vector search, sometimes + keyword + graph traversal) — none use the searcher's context as a retrieval signal
4. Memories are either current or deleted — no tracking of the progression from tentative mention to consolidated understanding
5. No concept of trails

Zep comes closest on temporal modeling (bi-temporal: when a fact was valid, when it was recorded). Mem0 has the most rigorous extraction pipeline. Cognee is the most local-first. None of them asked: how does memory actually work in humans, and what does that imply for the system design?

The five gaps that fall out of the cognitive science findings, which no existing system fills:

**Ecphoric retrieval** — retrieval that uses the searcher's current cognitive state (project, trail position, recent conversation) as a signal, not just query content. Tulving's encoding specificity says this is where recall lives.

**Conversation as native unit** — storing and retrieving dialogues with structure intact (speaker, turn, topic flow), not decomposing them into extracted facts. Pickering & Garrod say the alignment event — not the utterance — is the meaningful unit.

**Solidification tracking** — tracking how an idea progresses from first mention through re-access and annotation to crystallized understanding. Access count, annotation density, version chain. "Show me ideas I've revisited 5 times but never crystallized into an artifact."

**Trails as first-class objects** — named, temporal, shareable sequences through memory. The core innovation from 1945 that every system since has failed to implement.

**Post-hoc annotation** — separating capture (automatic, immediate) from annotation (deliberate, delayed). Thiede says the delay makes the annotation more accurate. Metcalfe says you can't reliably annotate insight as it happens anyway.

These gaps aren't incidental. They follow directly from what the cognitive science says about how memory forms, consolidates, and is recalled. Memex is the first design that starts there.

---

## How the concepts connect

The fog-match (ecphory) only works because of encoding specificity — which only matters because storage is purpose-neutral (Wilson). If you encoded narrowly for anticipated queries, the breadth needed for unexpected cues wouldn't exist.

Reconsolidation explains why trails matter: every access is a write operation. The trail isn't just a navigation artifact — it's a record of how the memory changed. Each TrailEvent is a reconsolidation event captured.

The solidification trajectory explains why both Frames and Artifacts need to exist: the episode is the provenance, the schema is the living knowledge. You need the Frame to reconstruct the original context; you need the Artifact because that's what the brain actually kept.

The insight mechanism explains the capture/annotate split: you can't tag insight reliably during the conversation (metacognitive asymmetry, .08 gamma), and asking mid-conversation contaminates the experience (Lutz & Thompson). Capture everything, annotate later, trust the post-hoc recognition.

The LLM analogy explains why RAG not fine-tuning: reconsolidation strengthens, catastrophic forgetting weakens. Opposite directions. The external store is the right architecture — memex is the substrate that neither human memory nor LLM weights can be.
