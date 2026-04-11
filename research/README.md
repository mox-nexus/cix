# Memex Research Program

Foundational research informing the rebuild of memex (a personal memory system for human-AI collaboration archives). Conducted via the `craft-research` pipeline: elicit → collect → extract → verify → synthesize → audit.

## Why this exists

The prior memex-next architecture was designed inside a single working session and lost in the 2026-04-09 home directory disaster. Before rebuilding, we are grounding the design in research across three streams. Architecture follows from understanding, not the other way around.

## Streams

| Stream | Question | Status |
|---|---|---|
| [A. Human memory and cognition](stream-a-human-memory/) | Baseline (RQ0), insight mechanism (RQ1), durable unit of episodic memory (RQ2), retrieval cue (RQ3), metacognition reliability (RQ4). Bridges to Stream B on attention-shift and retrieval-cue parallels. | Scope frozen 2026-04-11, awaiting confirmation. Next: collecting. |
| [B. LLMs and memory structurally](stream-b-llm-memory/) | What do LLMs actually do with memory? Context windows, KV cache, RAG, long-context, MemGPT-style schemes, in-context vs weight memory, attention-as-retrieval. | Pending: Stream A confirmation, then elicit. |
| [C. Technical landscape, hard problems, gaps](stream-c-landscape/) | State of the art in AI memory systems, vector DBs, hybrid retrieval, temporal reasoning, PKM tools, identified hard problems, gaps. Integrates A and B. | Blocked: needs A and B at synthesis phase. |

## Pipeline (per stream)

Each stream runs the standard craft-research pipeline:

1. **Elicit** — scope the inquiry, articulate what's known, define answerable research questions, identify source landscape
2. **Collect** — set up `recon` config to mechanically gather sources (papers, books, posts, code)
3. **Extract** — Claimify atomic claim extraction with verbatim quotes and evidence tiers (per source, parallelizable)
4. **Verify** — CoVE independent verification against sources (catches hallucinations, paraphrase drift)
5. **Synthesize** — cross-source integration, convergence/divergence/gap mapping
6. **Audit** — provenance chain check end-to-end before findings inform design

## What flows out of this

When all three streams pass audit, the synthesis findings become the input to the memex-next design document. The design document is an *architecture grounded in evidence*, with claims traceable back to source material.

The intent is that if any architectural choice is later questioned ("why append-only trails?", "why this particular temporal ranking?"), the answer is not "we discussed it" but "research finding F-23 in stream A and finding F-7 in stream B converge on this; here are the verified source quotes."

## Durability

Research artifacts are tracked in git on the `lance` branch. The branch should be pushed to `origin` as a backup as soon as elicit phase produces meaningful content, so a second disk wipe cannot destroy the research investment.
