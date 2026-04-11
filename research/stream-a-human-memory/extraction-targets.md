# Stream A — First-Batch Extraction Targets

**Input:** research/stream-a-human-memory/triage.md (127 triaged papers)
**First-batch size:** 25 papers, high-confidence topical fit, covering all five research questions plus cross-disciplinary bridges
**Mode:** abstract-based Claimify extraction (full-text download deferred — abstracts carry the main claims for initial synthesis, can expand later for load-bearing papers)
**Output:** per-paper extraction files at research/stream-a-human-memory/extractions/<paper-slug>.md

## Why this selection

Manually curated from the triage output to bias toward:
1. **Topical precision** — cut the keyword-noise papers (immunology, linguistics, ML) that per-query triage didn't filter
2. **Tradition coverage** — at least one canonical source per RQ, plus at least one phenomenology-neuroscience bridge and one semiotics bridge
3. **Abstract availability** — papers with populated abstracts, so first-pass extraction has material to work on
4. **Yash's novelty target** — include predictive-coding-meets-insight (Friston), phenomenology-neuroscience integrations (Lutz & Thompson), and the Tulving Festschrift for current-state synthesis

---

## RQ0 — Baseline: cognitive science view of memory architecture

### 1. Squire 1984 — The Neuropsychology of Memory
- Citations: 2129
- OpenAlex: W* (from `openalex-rq0-episodic-semantic-systems`)
- Why: Larry Squire, canonical figure in declarative/non-declarative memory taxonomy

### 2. Nader & Hardt 2009 — A single standard for memory: the case for reconsolidation
- Citations: 781
- Why: The memory reconsolidation finding is a major shift in RQ0 baseline understanding — it says memories are NOT fixed after consolidation but re-malleable each time they're retrieved. Directly relevant to Yash's model of ideas "solidifying over time."

### 3. Renoult & Irish 2019 — From Knowing to Remembering: The Semantic-Episodic Distinction
- Citations: 344
- Why: Recent integrative paper on the semantic/episodic boundary, directly RQ0

### 4. Rauchs et al 2005 — The relationships between memory systems and sleep stages
- Citations: 267
- Why: Consolidation mechanism, cross-memory-system

### 5. Cabeza & Nyberg 2000 — Imaging Cognition II: An Empirical Review of 275 PET and fMRI Studies
- Citations: 3639
- Why: Comprehensive neuroimaging review of memory processes

## RQ1 — Insight mechanism

### 6. Kounios & Beeman 2009 — The Aha! Moment
- Citations: 413
- Why: The canonical modern statement of the insight-neuroscience research program

### 7. Beeman et al 2004 — Neural Activity When People Solve Verbal Problems with Insight
- Citations: 1029
- Why: The foundational fMRI study of insight events; direct RQ1 mechanism evidence

### 8. Subramaniam & Kounios 2008 — A Brain Mechanism for Facilitation of Insight by Positive Affect
- Citations: 382
- Why: Affect-insight interaction — what conditions produce the click

### 9. Friston & Lin 2017 — Active Inference, Curiosity and Insight
- Citations: 376
- Why: **NOVELTY** — predictive-coding / free-energy framework applied to insight. Bridges insight research with active inference, which is also Stream B territory (LLM-relevant).

### 10. Sandkühler & Bhattacharya 2008 — Deconstructing Insight: EEG Correlates of Insightful Problem Solving
- Citations: 219
- Why: Methodology-focused — how to detect insight in neural signals, which directly addresses the "is the click textually visible" question

## RQ2 — Storage unit for episodic memory

### 11. Bartlett & Kintsch 1995 — Remembering (reissue)
- Citations: 2362
- Why: The canonical reconstructive memory text. Without this, Stream A has no schema-theory foundation.

### 12. Pickering & Garrod 2004 — Toward a mechanistic psychology of dialogue
- Citations: 2593
- Why: **DIRECTLY RELEVANT** to memex's conversation domain. Alignment in dialogue, interactive alignment model.

### 13. Stafford & Daly 1984 — CONVERSATIONAL MEMORY
- Citations: 108
- Why: Explicit conversation-memory study — the sub-literature we went looking for

### 14. Wagoner 2013 — Bartlett's concept of schema in reconstruction
- Citations: 82
- Why: Modern reinterpretation of Bartlett; clarifies what schema theory actually claims

### 15. Wilson 2002 — Six views of embodied cognition
- Citations: 4438
- Why: Cross-cutting relevance (appeared in 2 queries); central framing paper for embodied cognition's stakes on memory

## RQ3 — Retrieval cue

### 16. Tulving 1984 — Précis of Elements of Episodic Memory
- Citations: 804
- Why: Tulving's own distilled statement of episodic memory theory

### 17. Roediger & Craik 2014 — Varieties of Memory and Consciousness: Essays in Honour of Endel Tulving
- Citations: 1654
- Why: Recent integrative volume on the Tulving tradition — perfect for current-state synthesis on encoding specificity

### 18. Wiseman & Tulving 1976 — Encoding specificity: Relation between recall superiority and recognition failure
- Citations: 107
- Why: Direct encoding specificity paper, Tulving-authored

### 19. Wagner 1999 — Working Memory Contributions to Human Learning and Remembering
- Citations: 194
- Why: Bridge between working memory and long-term encoding

### 20. Buckner 1996 — Beyond HERA: Contributions of specific prefrontal brain areas to long-term memory retrieval
- Citations: 184
- Why: Neural retrieval evidence for RQ3

## RQ4 — Metacognition reliability

### 21. Metcalfe & Wiebe 1987 — Intuition in insight and noninsight problem solving
- Citations: 745
- Why: **INSIGHT + METACOG BRIDGE** — tests whether people have accurate feelings-of-knowing for insight vs. non-insight problems. Directly relevant to "is 'I just understood something' a reliable report."

### 22. Metcalfe 1986 — Feeling of knowing in memory and problem solving
- Citations: 334
- Why: Foundational Metcalfe metacognition

### 23. Thiede & Anderson 2003 — Accuracy of metacognitive monitoring affects learning of texts
- Citations: 742
- Why: Empirical test of metacognitive accuracy under realistic conditions

### 24. Dunlosky & Bjork 2013 — Handbook of Metamemory and Memory
- Citations: 296
- Why: Cross-cutting reference appearing in 2 queries; comprehensive metamemory

## P2-bridges — novelty and cross-disciplinary

### 25. Lutz & Thompson 2003 — Neurophenomenology: Integrating Subjective Experience and Brain Dynamics
- Citations: 417
- Why: **THE** canonical neurophenomenology paper. Integrates first-person phenomenology with third-person neuroscience. Direct answer to whether phenomenology-neuroscience hybrids exist as research programs, not just philosophical position-papers.

---

## Deferred for later batches

After first-batch extraction + verify, the next batches should include:

- **Engelbart 1962** "Augmenting Human Intellect" — PKM lineage, but a foundational framework paper not a claim-heavy study
- **Clark & Chalmers 2010 "The Extended Mind"** and Clark 2013 "Whatever next?" — extended mind, predictive brains
- **Gallagher 2017** "Past, Present and Future of Time-Consciousness: From Husserl to Varela and Beyond" — direct Husserl-Varela bridge
- **Kull, Deacon, Emmeche 2009** "Theses on Biosemiotics" — biosemiotics as cognition
- **Andrews et al 2024** "Semiosis and embodied cognition: the relevance of Peircean semiotics to cognitive neuro" — very recent Peirce-cognition bridge
- **Uhlhaas & Mishara 2006** "Perceptual Anomalies in Schizophrenia: Integrating Phenomenology and Cognitive Neuroscience" — another phenomenology-neuroscience bridge
- **Fuchs 2007** "Temporal Structure of Intentionality and Its Disturbance in Schizophrenia" — phenomenology of time
- **Burgess & Maguire 2002** "Human Hippocampus and Spatial and Episodic Memory" — cognitive neuroscience
- **Squire & Stark 2004** "The Medial Temporal Lobe" — cognitive neuroscience
- **Kumaran & McClelland 2012** "Generalization through recurrent interaction of episodic memories" — memory-and-imagination
- **Binder & Desai 2009** "Where Is the Semantic System? A Critical Review and Meta-Analysis" — semantic memory

~15 additional papers, raising total extracted to ~40 across both batches.
