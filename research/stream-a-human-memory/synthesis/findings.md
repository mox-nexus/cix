# Stream A Synthesis: Human Memory and Cognition

**Scope:** research/stream-a-human-memory/scope.md
**Sources:** 20 papers, 176 claims across cognitive psychology, cognitive neuroscience, phenomenology, embodied cognition, metacognition
**Verification:** CoVE completed on 15 load-bearing claims. Results: 11 VERIFIED, 4 CORRECTED, 0 REFUTED. Corrections applied inline below (marked with [CORRECTED]). See verification/load-bearing-claims.md for full CoVE protocol output.

---

## RQ0 — What does cognitive science say about memory architecture?

### Finding 0.1: Memory is organized into multiple functionally distinct systems
CLAIM: At minimum two major systems are well-attested: declarative (explicit) and procedural (implicit). Within declarative, a further distinction between episodic (event-specific) and semantic (context-free knowledge) is widely accepted but debated as to whether it's a functional distinction or a neuroanatomical one.
EVIDENCE:
- [tulving1984:c1] Episodic and semantic memory are "functionally separate albeit closely interacting systems"
- [tulving1984:c3] Tulving characterizes the acceptance as "tentative, not conclusive"
- [squire1982:c11-c13] Declarative/procedural dissociation established via amnesia: procedural learning spared, declarative impaired
- [squire1982:c20] The amnesic deficit is NOT selective for episodic — semantic is equally impaired, challenging episodic/semantic as the neuropsychologically relevant boundary
- [rauchs2005:c3-c4] Tulving's finer SPI taxonomy (procedural, perceptual, semantic, episodic) is more pertinent than declarative/non-declarative for understanding sleep's role
CONFIDENCE: HIGH — converging evidence across traditions (Tulving functional, Squire neuropsychological, Rauchs sleep research)
DIVERGENCE: Tulving cuts episodic/semantic; Squire cuts declarative/procedural. Both could be true at different levels of analysis. Rauchs suggests Tulving's finer taxonomy is more useful for some purposes.
ARCHITECTURAL IMPLICATION: Memex operates in the declarative domain (Squire's cut). Everything memex stores — conversations, documents, insights — is declarative. The episodic/semantic distinction within declarative IS relevant to memex: conversations are episodes; crystallized insights become semantic. Memex should model the transition from episodic to semantic, not just store one type.

### Finding 0.2: Consolidation is not one-time — memories are rewritten on retrieval
CLAIM: The classical view (Squire) that consolidation is a one-time post-learning process has been fundamentally challenged by reconsolidation (Nader). Memories re-enter a labile state on every reactivation and must restabilize.
EVIDENCE:
- [squire1982:c7] Classical: medial temporal consolidation "can continue for up to a few years after initial learning"
- [nader2009:c5] "memories are not consolidated just once: they can return to a labile state and need to be reconsolidated when reactivated"
- [nader2009:c9] Reconsolidation demonstrated across tasks, species, and amnesic treatments — "a fundamental mnemonic process"
- [nader2009:c10] Evidence at behavioral, physiological, and molecular levels
- [nader2009:c4] Memory requires continuous molecular maintenance (PKMzeta)
CONFIDENCE: HIGH — reconsolidation is well-replicated and established
DIVERGENCE: Squire 1982 vs Nader 2009 is a historical progression, not a live debate. The field has largely accepted reconsolidation as real, while retaining Squire's framework for the initial consolidation window.
ARCHITECTURAL IMPLICATION: **LOAD-BEARING.** The "stored unit" in memex is not static. Every recall is a potential modification event. Memex should model recall as a write operation, not a read operation. Trail annotations, re-access patterns, and re-retrieval contexts should be stored because they literally change what the memory IS. The append-only TrailEvent model from the pre-disaster design session is exactly right — each access creates a new version of the memory.

### Finding 0.3: Permanent storage is neocortical; hippocampal structures handle formation
CLAIM: Squire proposes that long-term memory is stored in neocortex, not in the hippocampal/medial temporal structures that are essential for its formation and initial consolidation. [CORRECTED — source hedges with "It appears that"; extraction originally stated as fact]
EVIDENCE:
- [squire1982:c6] "It appears that these brain regions constitute an essential neuroanatomical substrate for the formation of new memories" — note hedge
- [squire1982:c2] H.M. retained premorbid memories but couldn't form new declarative ones
- [cabeza2000:c1-c2] Encoding activates left prefrontal + medial temporal; retrieval activates prefrontal + medial temporal + posterior midline
CONFIDENCE: HIGH
ARCHITECTURAL IMPLICATION: Two-stage storage is natural: an ingestion/formation layer (like the reactor pipeline) and a long-term layer (like the Lance store). The formation layer transforms raw input into storable form; the long-term layer holds it. This maps well to memex's existing architecture.

### Finding 0.4: Specific episodes can dissipate while shaping durable schemas
CLAIM: Individual episodic memories can fade from explicit retrieval while still influencing cognition through incorporation into generic schematic representations.
EVIDENCE:
- [squire1982:c16] "Memory of a particular face, word, or event could dissipate from storage but could nevertheless influence behavior by virtue of having been incorporated into more generic representations or schemata"
- [squire1982:c17] An experience might leave no recognizable trace yet "tune or elaborate neural mechanisms (schemata)"
- [bartlett1995:c6] Memory is "a process of reconstruction" not faithful reproduction
- [wilson2002:c15] Fresh episodic memories have "reliving" quality; retelling crystallizes them (Round-2 note: source supports "crystallize through retelling"; the further framing "into semantic form" is a cross-source inference using squire1982:c16-c17, not in wilson2002 alone)
CONFIDENCE: HIGH — Bartlett, Squire, and Wilson converge from different traditions
ARCHITECTURAL IMPLICATION: **MAPS TO IDEA SOLIDIFICATION.** Yash's intuition that "over time an idea solidifies" is exactly this process: the specific episode fades, but the schema it shaped persists. Memex's Frame→Artifact→Trail model captures this: Frames are the raw episodes, Artifacts are the crystallized forms, and Trails record the curation path. The system should expect Frames to become less useful over time while the Artifacts they generate become more durable.

---

## RQ1 — What is the mechanism of insight events ("clicks")?

### Finding 1.1: Insight is a real cognitive event with measurable neural signatures
CLAIM: Insight is not merely a subjective feeling but a distinct neural process. The signature is a sudden burst of gamma-band activity in the right anterior superior temporal gyrus (RH aSTG), beginning 0.3 seconds before the reported moment of insight.
EVIDENCE:
- [beeman2004:c1] fMRI: increased RH aSTG activity for insight vs noninsight solutions
- [beeman2004:c2] EEG: gamma burst in RH aSTG 0.3s before insight solutions
- [beeman2004:c4] Insight engages "distinct neural and cognitive processes" within a shared cortical network
- [kounios2009:c8] "insight is the culmination of a series of brain states and processes"
- [kounios2009:c9] These processes "operate at different time scales"
CONFIDENCE: HIGH — replicated across EEG and fMRI, multiple studies
ARCHITECTURAL IMPLICATION: The click IS real and detectable — but only with neural instrumentation, not from text alone. Memex cannot detect insight events from conversation transcripts via neural signatures. However, the gamma burst occurs 0.3s BEFORE the conscious report, meaning the brain process leads the phenomenology. Detection in text would require identifying the phenomenological report (the "oh" moment), not the neural precursor.

### Finding 1.2: Insight is phenomenologically sudden but neurally continuous
CLAIM: The subjective experience of insight is sudden and appears disconnected from preceding thought, but the neural substrate shows continuous preparatory processing.
EVIDENCE:
- [kounios2009:c6] "the experience of insight is sudden"
- [kounios2009:c7] "can seem disconnected from the immediately preceding thought"
- [kounios2009:c8] Despite this, insight "is the culmination of a series of brain states"
- [beeman2004:c6] The insight-associated RH aSTG region "was also active during initial solving efforts"
CONFIDENCE: HIGH
ARCHITECTURAL IMPLICATION: The click feels discontinuous but isn't. This means memex shouldn't model insight as a rupture in the conversation — it should model the BUILDUP. The conversation content before the click is not irrelevant context; it's the substrate from which the click emerged. Storing the full conversation (not just the insight moment) is correct because the preparatory processing is in the preceding discourse.

### Finding 1.3: Insight cannot be predicted pre-hoc by metacognitive monitoring
CLAIM: People cannot predict which problems they will solve via insight. Feeling-of-knowing and warmth ratings fail to forecast insight solutions, even though they accurately predict non-insight (incremental) solutions.
EVIDENCE:
- [metcalfe1986:c5] FOK rank ordering "did not relate to problem solution" for insight problems
- [metcalfe1986:c8] "predictive metacognitions were nonexistent for the problems"
- [metcalfewiebe1987:c12] FOK-performance gamma for insight = .08 (vs .40 for algebra)
- [metcalfewiebe1987:c14] "The idea that subjects may have privileged access to idiosyncratic information... was overwhelmingly wrong"
- [metcalfewiebe1987:c8] 78% of correct insight solutions showed ≤1 point warmth change on 10-point scale [CORRECTED — primary source is Metcalfe 1986b, cited in Metcalfe & Wiebe 1987 introduction]
CONFIDENCE: HIGH — replicated across two Metcalfe studies, two different measures (FOK and warmth), two experiment designs
ARCHITECTURAL IMPLICATION: **LOAD-BEARING.** Memex cannot detect insight BEFORE it happens via user self-report. Pre-click signals ("I feel like I'm getting close") are unreliable for insight. Detection must be post-hoc.

### Finding 1.4: Insight CAN be reported reliably post-hoc
CLAIM: While people cannot predict insight, they CAN accurately report THAT insight occurred after the fact. Self-reports of "solved with insight" vs "solved analytically" correlate with objective neural differences.
EVIDENCE:
- [beeman2004:c5] Subjects' post-hoc self-report of insight vs non-insight "correlated with objective neural differences"
- [metcalfewiebe1987:c7] Step-function warmth pattern (measurable signature) aligns with self-reported insight
CONFIDENCE: MEDIUM — fewer sources directly on this point
DIVERGENCE: Metcalfe shows FOK FAILS pre-hoc; Beeman shows self-report WORKS post-hoc. These are not contradictory — they're about different temporal windows. Prediction fails; recognition succeeds.
ARCHITECTURAL IMPLICATION: Memex should let users TAG insights after the fact (trail annotations, "click markers"), and those tags should be trusted. What memex should NOT do is prompt "did you just have an insight?" mid-conversation — that interrupts the flow and the report wouldn't be reliable anyway.

### Finding 1.5: Positive affect facilitates insight via preparatory brain states
CLAIM: People in positive mood solve more problems with insight. The mechanism is preparatory: positive mood modulates ACC activity BEFORE the problem, biasing processing toward insight rather than analytic strategy.
EVIDENCE:
- [subramaniam2008:c1-c3] Positive mood → more insight solutions; ACC mediates the preparatory bias
CONFIDENCE: MEDIUM — single study, though large sample (n=79) with fMRI
ARCHITECTURAL IMPLICATION: Mood/context at the time of the conversation matters for whether insights happen. Memex doesn't control mood, but this finding suggests that the CONDITIONS under which conversations happen (relaxed vs stressed, exploratory vs task-focused) affect what kinds of cognitive events occur. Metadata about conversational context could be valuable for retrieval.

### Finding 1.6: Insight can be modeled as Bayesian model reduction (active inference)
CLAIM: In the free-energy / active inference framework, insight corresponds to Bayesian model reduction — pruning unnecessary structure from generative models. This process shares mechanisms with sleep.
EVIDENCE:
- [friston2017:c1] Insight as minimizing expected variational free energy
- [friston2017:c4] "Bayesian model reduction evinces mechanisms associated with sleep and has all the hallmarks of 'aha' moments"
- [friston2017:c5] People attain insight from "just a handful of observations" — sample-efficient unlike deep learning
CONFIDENCE: LOW — single theoretical paper, computational simulations not behavioral data
ARCHITECTURAL IMPLICATION: Bridge to Stream B. If insight is model reduction (pruning), then the LLM analogue might be attention weight reorganization or context compression. The sample-efficiency claim (humans need few observations for insight, ML needs many) is a fundamental structural difference between human and machine memory.

---

## RQ2 — What is the durable unit of episodic memory?

### Finding 2.1: Memory is reconstructive, not reproductive
CLAIM: What is "stored" is not a faithful recording but a schema — a framework from which memories are reconstructed at retrieval time. The act of remembering is an act of construction.
EVIDENCE:
- [bartlett1995:c6] "memory is a process of reconstruction"
- [bartlett1995:c5] Subjects changed culturally unfamiliar details, demonstrating schema-driven distortion
- [squire1982:c16-c17] Specific episodes dissipate; schemas persist and continue to influence behavior
- [nader2009:c5] Reconsolidation: memories are rewritten on each retrieval
CONFIDENCE: HIGH — Bartlett (1932), Squire (1982), and Nader (2009) converge across 77 years
NULL HYPOTHESIS EVALUATION: RQ2 null said "the 'durable unit' question is malformed — memory is a process, not an object." The evidence PARTIALLY SUPPORTS the null: memory is indeed reconstructive (a process), not a stored object. But schemas ARE stored structures (Bartlett, Squire). So the answer is: the durable unit is a schema (a reconstruction template), not an episode (a recording). The question is NOT malformed — it just has a different answer than "episode."
ARCHITECTURAL IMPLICATION: **LOAD-BEARING.** Memex's Frame (raw message) is the episode. The episode WILL fade in human memory. What persists is the schema it shaped. Memex should therefore store BOTH the raw frame (which the human will forget) AND some representation of what the frame contributed to understanding (the Artifact/Abstract). The Frame is for re-access; the Artifact is for what the human actually remembers.

### Finding 2.2: Conversations are uniquely fragile memory stimuli
CLAIM: Conversations are jointly created, constantly updated, and after only 5 minutes, people can recall only ~10% of what was said.
EVIDENCE:
- [stafford1984:c1] Conversations are "jointly created, constantly updated, and necessarily are readily accessible by participants" — distinct from other memory stimuli
- [stafford1984:c2] "even after only five minutes people are able to recollect only about 10% of what was said in a social exchange"
- [stafford1984:c4] People remember more of their partner's comments than their own
CONFIDENCE: HIGH (for the fragility claim) / MEDIUM (for the 10% figure — single 1984 study)
ARCHITECTURAL IMPLICATION: **THE FUNDAMENTAL JUSTIFICATION FOR MEMEX.** Without external memory aid, 90% of conversational content vanishes within minutes. This is not a failure of human memory — it's normal. Memex exists to compensate for this specific property of conversational memory. The fact that people remember their partner's contributions more than their own suggests memex should weight the OTHER speaker's content (the AI's or collaborator's responses) as more likely to be the user's anchor for recall.

### Finding 2.3: Dialogue involves interactive alignment — jointly constructed representations
CLAIM: In dialogue, interlocutors' linguistic representations become aligned at multiple levels through a largely automatic process. What is "stored" from a conversation may not be individual utterances but a jointly constructed alignment state.
EVIDENCE:
- [pickering2004:c2] "linguistic representations employed by the interlocutors become aligned at many levels, as a result of a largely automatic process"
- [pickering2004:c1] Dialogue is "the most natural and basic form of language use" — not a variant of monologue
CONFIDENCE: MEDIUM — well-cited (2593) but single theoretical account
ARCHITECTURAL IMPLICATION: Memex currently decomposes conversations into individual messages (Frames). If dialogue is actually about ALIGNMENT between speakers, the unit of memory should be the alignment event (where the two speakers converged or diverged), not the individual message. This suggests a new primitive: an "alignment frame" that captures the state of shared understanding at a point in the conversation.

### Finding 2.4: Mental representations are purpose-neutral
CLAIM: Wilson argues that what humans store appears to be largely purpose-neutral — not indexed to anticipated future use, or at minimum containing information beyond the originally conceived purpose. This gives adaptive flexibility. [CORRECTED — source hedges with "appear to be to a large extent" and offers weaker alternative]
EVIDENCE:
- [wilson2002:c11] "Our mental representations... appear to be to a large extent purpose-neutral, or at least to contain information beyond that needed for the originally conceived purpose" — note double hedge
- [wilson2002:c12] Purpose-neutral encoding gives "an enormous advantage in problem-solving flexibility"
- [wilson2002:c10] Glenberg proposes memory as "encoding of patterns of possible physical interaction" — but Wilson partially rejects this for being too action-indexed
CONFIDENCE: MEDIUM — Wilson's verdict, supported by argument but limited direct evidence cited
ARCHITECTURAL IMPLICATION: Memex should encode broadly, not narrowly for anticipated retrieval patterns. The current approach of embedding content for semantic search IS purpose-neutral (it doesn't presuppose what the query will be). This validates the embedding approach over, say, tag-based or category-based storage.

---

## RQ3 — What brings a memory back?

### Finding 3.1: Retrieval requires both the stored trace AND the current cognitive state (synergistic ecphory)
CLAIM: Recall is not a simple lookup. It's the joint product of what was stored AND what the person is currently thinking about. Tulving calls this "synergistic ecphory" — the stored episodic information and the "cognitively present retrieval information" jointly construct the recalled experience.
EVIDENCE:
- [tulving1984:c10] "'synergistic' refers to the joint influence that the stored episodic information and the cognitively present retrieval information exert on the construction of the product of ecphory"
- [tulving1984:c9] Ecphory is "one of the central elements of retrieval"
- [tulving1984:c11] Encoding specificity figures prominently
- [wiseman1976:c4] People recall words they FAIL to recognize — the "right" cue (one present at encoding) succeeds where a copy of the item itself fails
CONFIDENCE: HIGH — Tulving's framework, replicated experimentally by Wiseman & Tulving 1976
ARCHITECTURAL IMPLICATION: **THIS IS THE FOG-MATCH.** Yash's intuition that recall happens when "the fog matches" is exactly synergistic ecphory. Retrieval is not content-similarity search alone — it's the match between the searcher's current state and the encoded state. Memex's retrieval should consider not just WHAT the user is searching for (query content) but the CONTEXT in which they're searching (what conversation they're in, what topic they've been working on, what mood/project/focus). This argues for contextual retrieval features beyond pure semantic search.

### Finding 3.2: Reconsolidation-based interference in humans is context-dependent
CLAIM: In one human study, reactivation-dependent interference with consolidated episodic memory occurred only when subjects were in the same spatial environment as original learning. [CORRECTED — original claim overgeneralized from one study's interference effects to "reconsolidation requires context reinstatement" in general]
EVIDENCE:
- [nader2009:c12] "reactivation-dependent interference effects in consolidated episodic memory were found only when human subjects were exposed to the interfering material in the same environment in which the original learning took place"
CONFIDENCE: MEDIUM — single finding, but from a well-controlled study
ARCHITECTURAL IMPLICATION: The encoding context matters not just for retrieval (Finding 3.1) but for memory UPDATE (reconsolidation). If memex wants to help the user update their understanding (not just recall it), providing the original encoding context (the conversation where the idea originated) alongside the new information may be important. The trail-follow + annotation workflow already does this: you revisit old frames in context and add new understanding.

### Finding 3.3: Retrieval phenomenology is embodied "reliving" that crystallizes over time
CLAIM: Fresh episodic retrieval has a quality of "reliving" with visual, kinesthetic, and spatial impressions. This quality diminishes with retelling as memories crystallize. (The further claim that crystallization is *into semantic form* requires squire1982:c16-c17 + bartlett1995:c6, not wilson2002:c15 alone — see Round-2 verification note.)
EVIDENCE:
- [wilson2002:c15] "recalling an episodic memory has a quality of 'reliving'... This is especially true when memories are fresh, before they have become crystallized by retelling"
CONFIDENCE: MEDIUM — single source on this specific point
ARCHITECTURAL IMPLICATION: The transition from vivid reliving to crystallized semantic memory IS the solidification process Yash described. Memex could track this transition: a frame that has been accessed and annotated many times is "crystallized" (semantic); a frame rarely accessed retains its episodic quality (contextual, situated). Access count and annotation density could be proxies for the reliving→crystallized transition.

---

## RQ4 — How reliable is metacognitive self-report?

### Finding 4.1: Metacognition is domain-asymmetric — reliable for declarative recall, unreliable for insight
CLAIM: People accurately predict their memory performance on factual/declarative tasks, but completely fail to predict insight performance. FOK and warmth ratings track incremental progress but are blind to sudden insight.
EVIDENCE:
- [metcalfe1986:c4] FOK shows positive correlation with memory task performance
- [metcalfe1986:c5] FOK "did not relate to problem solution" for insight
- [metcalfe1986:c7] Replicated across recognition and generation tests
- [metcalfewiebe1987:c12] Algebra FOK gamma = .40 (significantly above zero); insight FOK gamma = .08 (not significant)
- [metcalfewiebe1987:c14] Normative predictions outperform self-predictions for insight (interaction F(1,46) = 10.13)
CONFIDENCE: HIGH — replicated across multiple studies and measures
NULL HYPOTHESIS EVALUATION: RQ4 null said "metacognitive self-report is generally unreliable." The evidence says it's MORE NUANCED: self-report IS reliable for declarative memory, but IS unreliable for insight. The null is partially supported — memex should not uniformly trust or uniformly distrust user tags. The trust level depends on what kind of cognitive event the tag refers to.
ARCHITECTURAL IMPLICATION: User-tagged "this was important" labels on factual content (declarative recall) should be somewhat trusted. User-tagged "I just had an insight" labels should be treated with MORE skepticism — not because the user is wrong about HAVING had an insight (Finding 1.4 says post-hoc report IS reliable), but because their sense of HOW IMPORTANT the insight is may be poorly calibrated.

### Finding 4.2: First-person reports can modify the reported experience (reactivity)
CLAIM: The act of generating a report about an experience can alter that experience — the metacognitive observation problem.
EVIDENCE:
- [lutzthompson2003:c7] "the process of generating first-person reports about an experience can modify that experience"
- [lutzthompson2003:c6] First-person reports "can be biased or inaccurate"
CONFIDENCE: MEDIUM — stated as a methodological challenge, not a quantified effect
ARCHITECTURAL IMPLICATION: Asking users to annotate conversations ("was this an insight?") during the conversation may change the nature of the conversation. The annotation itself becomes part of the experience. Post-hoc annotation (after the conversation ends) may be more reliable than inline annotation. This argues for memex's trail annotation happening AFTER ingest, not during the live conversation.

### Finding 4.3: Delayed reflection improves metacognitive accuracy
CLAIM: Generating keywords after a delay (rather than immediately) improves metacognitive monitoring accuracy and downstream learning.
EVIDENCE:
- [thiede2003:c2-c3] Delayed keyword generation → better monitoring accuracy → better regulation → better comprehension
CONFIDENCE: MEDIUM — single study, well-cited (742)
ARCHITECTURAL IMPLICATION: If users annotate memex content AFTER a delay (not immediately), their annotations will be more accurate. This argues for a "revisit and annotate" workflow rather than "tag as you go." The trail-building workflow (curate a trail days or weeks after the conversation) is better calibrated than inline tagging.

---

## Cross-Cutting Findings

### Finding X.1: The solidification trajectory (from reliving to schema)
Multiple sources converge on a trajectory for how ideas solidify:
1. **Fresh episode** — embodied reliving with sensory detail [wilson2002:c15]
2. **Retelling/re-access** — each retrieval is a reconsolidation event that can modify [nader2009:c5]
3. **Schema incorporation** — specific details dissipate, but generic schema persists [squire1982:c16-c17, bartlett1995:c6]
4. **Crystallized semantic knowledge** — no longer episodic, now "just something I know" [wilson2002:c15]

This is the EXACT trajectory Yash described: "over time an idea solidifies and gets fleshed out."
ARCHITECTURAL IMPLICATION: Memex should model this trajectory explicitly. A frame starts as an episode (raw, contextual, timestamped). Through trail curation and re-access, it becomes associated with annotations and other frames. Eventually, the insight it contained may be expressed as an Artifact (a design doc, a decision, a principle) — at which point the original frame is the provenance, not the active memory. The SUPERSEDES relation captures this: Artifact v3 supersedes v2 supersedes v1, each more crystallized.

### Finding X.2: The fog-match is real — it's called synergistic ecphory
Tulving's synergistic ecphory [tulving1984:c10] + Nader's context-dependent reconsolidation [nader2009:c12] + Bartlett's schema-driven reconstruction [bartlett1995:c6] all point to the same thing: retrieval is not content lookup, it's the collision of current cognitive state with stored traces. The "fog" is the current state; the "match" is ecphory.
ARCHITECTURAL IMPLICATION: Memex's hybrid search (BM25 + semantic + recency) approximates content-similarity retrieval, but misses the context dimension. Adding a "current context" signal (what project is the user in, what have they been discussing recently, what trail are they following) would better model ecphory. The temporal ranking we discussed (recency boost as third RRF rank source) is one dimension of this. Project/topic context is another.

---

## Gap Analysis

### Theoretical Gaps
- **No formal model of the reliving→crystallization transition.** Wilson names it; nobody quantifies it. When does a memory stop being episodic and become semantic? What triggers the transition? Number of accesses? Time? Schema integration events?
- **No Peircean semiotic model of insight.** Yash's "sign → interpretant → mark" framing was load-bearing in scope.md. The 20 sources don't address Peirce at all. The semiotics literature is missing from this corpus. Stream A needs Peirce/Eco/Deacon sources to evaluate whether the semiotic vocabulary adds something the cognitive science vocabulary doesn't.

### Methodological Gaps
- **No ecological validity studies of insight in conversation.** All insight research (Kounios, Beeman, Metcalfe) uses laboratory problem-solving (anagrams, compound remote associates). Whether the click in a conversation follows the same pattern (gamma burst, step-function warmth, unpredictable FOK) is unstudied.
- **Conversational memory research is thin.** Only Stafford & Daly 1984 directly studies memory for conversations. The 10% recall figure needs replication with modern methods. Pickering & Garrod is about dialogue processing, not dialogue MEMORY.

### Empirical Gaps
- **No data on conversational-memory loss trajectory.** Stafford says 10% after 5 minutes. What about after 1 hour, 1 day, 1 week? The forgetting curve for conversational content is unknown.
- **No studies of insight in human-AI conversation specifically.** All studies use human-human or human-problem-solving. Whether insight operates the same way when the interlocutor is an AI is a Stream C question.
- **Reconsolidation boundary conditions in naturalistic settings.** Nader's evidence is largely from fear conditioning. Whether conversational memories follow the same reconsolidation dynamics is unknown.

### Practical Gaps
- **No existing system implements ecphoric retrieval.** All search systems use content-similarity (semantic search, keyword match). Nobody has built retrieval that models the user's current cognitive state as a retrieval cue. This is where memex could be genuinely novel.
- **No existing system models the solidification trajectory.** Note-taking tools store notes. None track the reliving→crystallization progression of an idea across conversations.

---

## Null Hypothesis Evaluation

| Null Hypothesis | Verdict | Evidence |
|---|---|---|
| RQ0: No coherent view; traditions disagree | **PARTIALLY REFUTED.** Multiple systems exist and converge (declarative/procedural, episodic/semantic). But the RIGHT taxonomy depends on the question being asked (Rauchs). | Convergence on multi-system memory; divergence on which cut matters |
| RQ1: Insight is not a unified mechanism; click is post-hoc construction | **REFUTED.** Insight has measurable neural signatures (gamma burst, RH aSTG), distinct from non-insight solving. It IS a real mechanism. But it cannot be predicted pre-hoc by self-report. | Beeman 2004, Kounios 2009, Metcalfe 1986/1987 |
| RQ2: The unit question is malformed; memory is process not object | **PARTIALLY SUPPORTED.** Memory IS reconstructive (Bartlett), not stored objects. But schemas ARE persistent structures (Squire). The answer: the durable unit is a schema (reconstruction template), not an episode. | Bartlett, Squire, Wilson |
| RQ3: Retrieval is not predictable from storage structure | **PARTIALLY REFUTED.** Encoding specificity (Tulving) provides a clear, replicated link between encoding conditions and retrieval success. But retrieval is also context-dependent (Nader) and affected by affect (Subramaniam). It's predictable but multi-factorial. | Tulving 1984, Wiseman 1976, Nader 2009 |
| RQ4: Metacognitive self-report is generally unreliable | **PARTIALLY SUPPORTED.** It's unreliable for insight (Metcalfe) but reliable for declarative recall. Domain-asymmetric, not uniformly unreliable. Reports can also modify experience (Lutz/Thompson). | Metcalfe 1986/1987, Lutz & Thompson 2003 |

---

## Summary

- **Total findings:** 14 (5 RQ0, 6 RQ1, 4 RQ2, 3 RQ3, 3 RQ4, 2 cross-cutting)
- **HIGH confidence:** 9 | **MEDIUM:** 5 | **LOW:** 1
- **Key convergence:** Reconstruction (Bartlett) + schema persistence (Squire) + reconsolidation (Nader) + purpose-neutral storage (Wilson) converge on a model where memory is actively maintained, reconstructed at retrieval, and modified by every access. This is not a passive archive — it's a living, self-revising system.
- **Key divergence:** The right memory taxonomy depends on the question (Tulving's episodic/semantic for functional analysis, Squire's declarative/procedural for neuroanatomy, Tulving's SPI for sleep). No single cut is universally correct.
- **Critical gaps:** No ecological studies of insight in conversation; no data on conversational forgetting curves beyond 5 minutes; no system implements ecphoric (context-dependent) retrieval; the Peircean semiotic framework is entirely absent from the evidence base.

## Architectural Implications for Memex (consolidated)

1. **Recall is a write operation.** Every retrieval modifies the memory (reconsolidation). Model trail access and recall events as write events, not reads. The append-only TrailEvent pattern is correct.
2. **Store both episodes and schemas.** Frames are episodes that will fade; Artifacts are the crystallized schemas. Both are needed. The system should support and track the transition between them.
3. **Insight detection is post-hoc only.** Pre-event detection via self-report is empirically unsupported. Let users tag after the fact; don't prompt mid-conversation.
4. **The fog-match is real — it's ecphory.** Retrieval should incorporate context (project, recent activity, conversational trajectory), not just content similarity. This is where memex can be genuinely novel.
5. **90% loss in 5 minutes.** This is why memex exists. The system is compensating for a specific, quantified property of conversational memory.
6. **Purpose-neutral storage is correct.** Broad encoding (embeddings) without presupposing future retrieval patterns is the right approach. It matches how human memory actually encodes.
7. **Delayed annotation > immediate annotation.** Post-conversation trail building is better calibrated than inline tagging.
8. **Track the solidification trajectory.** Frame → re-accessed Frame → annotated Frame → Artifact. The system should make this progression visible and queryable.


---

## Round 2 Verification — Cross-Model CoVE (2026-04-25)

**Protocol:** Independent re-verification of synthesis-cited unverified claims via Gemini CLI (`gemini -p`), cross-model from Claude (extractor). Source contexts loaded from `sources/full-text/` where available, fallback to extraction file.

**Results (47 claims):** 45 VERIFIED, 2 CORRECTED, 0 REFUTED, 0 INSUFFICIENT, 47/47 VERBATIM quote match.

**No claims refuted; no quote fabrications detected; all corrections are precision-tightening rather than direction-changes.**

### Corrections applied to synthesis

- **nader2009:c4** — Synthesis already hedged correctly; extraction over-reach did not propagate.
- **tulving1984:c11** — Synthesis already hedged correctly; extraction over-reach (characterizing Part III as "experimental work on synergistic ecphory") did not propagate.
- **wilson2002:c15** — CORRECTED: synthesis text in Findings 0.4 evidence list and 3.3 CLAIM line softened — "crystallize into semantic form" replaced with "crystallize"; the semantic-form framing is now attributed to cross-source inference (squire1982:c16-c17 + bartlett1995:c6).

### Verification artifacts

- Per-claim verdicts: `verification/cove-gemini-round-2.jsonl`
- Verifier script: `research/.tools/verify_cove.py`

### Audit verdict (this stream)

The corpus stands. The synthesis findings remain sound; the corrections above sharpen wording without changing architectural conclusions. **Verification rate after Round 2: 100% of synthesis-cited claims independently verified by a second model.**
