# Why radix is shaped this way

This document is for humans evaluating *why* the radix skill takes the shape it does — the design rationale and the literature that backs it. The skill itself (`skills/radix/SKILL.md`) is operational and doesn't need this material at runtime.

## The problem radix addresses

Elite codebases — across any language or domain — encode expert knowledge that doesn't appear in their docs. Maintainers' design decisions, tradeoffs, the mental models behind their abstractions, the antipatterns they've learned to avoid — these live in commit history, PR discussions, RFCs, code comments, and the *shape* of the code itself, not in formal documentation.

Capturing this knowledge systematically is hard. Falessi et al. 2013 (TOSEM) examined Design Rationale Documentation (DRD) approaches and concluded the full DRD process is "too onerous for systematic industrial use" — capturing all the rationale takes more effort than the original engineering work, so it doesn't get done at scale. The knowledge stays tacit.

radix takes a narrower bet: don't try to capture *all* rationale upfront. Capture rationale *post hoc*, by mining the artifacts maintainers already produce (commits, PRs, RFCs, code), and structure the output so it can be queried and built on. The cost is bounded; the output is incremental; the process is repeatable across domains.

## The why-vs-what thesis

Public training datasets — TheStack, BigCode, language-specific curated corpora, official docs in pretraining — cover the *what* layer. They contain every public file's text, every API definition, every tutorial example. A model trained on them knows the **journeyman layer** of any well-documented language.

What public datasets miss:

- **Why the code changed** — the failure mode encoded in revert messages; the alternatives that were tried before the current settle. Static snapshots have only the settle.
- **Why this code is correct despite looking dangerous** — the cross-reference between a `// SAFETY:` (or `// NOTE:` or `// must not`) comment and the invariant it protects. The comment is in TheStack; the cross-reference is not a separate signal.
- **Why this exact shape recurs** — convergent design choices across multiple elite codebases. Each signature is in TheStack; the cross-codebase aggregation that surfaces "5 elites converge on this bound shape" is not.
- **Why an RFC's rejected alternatives were rejected** — public datasets have the accepted RFC, not the deliberation.
- **Why a closed-without-merge PR didn't work** — not in TheStack as a separate category.

That gap **is** stewardship-tacit expertise. radix mines it.

## The cognitive grounding

Five lines of cognitive-science research inform radix's design.

### Brooks 1983 — top-down comprehension by hypothesis

[doi:10.1016/s0020-7373(83)80031-5]

Brooks proposed that experts read code top-down, generating hypotheses about what each section *probably does* based on naming and structure, then verifying selectively. Naming and structure carry the load. This grounds radix's emphasis on *reconnaissance before extraction* (Phase 3b): without orientation, bottom-up reading produces noise.

### Letovsky 1986 — multiple cognitive processes in comprehension

[Letovsky, S. (1986). Cognitive processes in program comprehension. *Empirical Studies of Programmers*, 1, 58–79. ACM Digital Library: dl.acm.org/doi/10.5555/21842.21849]

Letovsky identified that programmers don't comprehend code via a single strategy — they use a mix of top-down hypothesis-formation, bottom-up scanning, and inquiry-driven targeted reading depending on the task. This grounds radix's *one mode per pass* discipline: different mining modes (oscillations vs scars vs signatures) require different reading strategies.

### Soloway & Ehrlich 1984 — programming plans + rules of programming discourse

[doi:10.1109/TSE.1984.5010283]

Soloway & Ehrlich identified two types of knowledge expert programmers use: (1) **programming plans** — generic program fragments representing stereotypic action sequences, and (2) **rules of programming discourse** — conventions governing program structure. This grounds radix's `signatures` mode (cross-codebase recurrence captures programming plans) and the future `aesthetic` mode (discourse rules).

### Pennington 1987 — program model + domain model

[doi:10.1016/0010-0285(87)90007-7]

Pennington's empirical study found that experts construct two coexisting mental models when reading code: the **program model** (procedural / control-flow / data-flow structure as text) and the **domain model** (semantic / problem-domain entities and relationships). radix's `signatures` mode covers both: structural shape accommodates program-model artifacts (type AST, generic bounds) and domain-model artifacts (entities and relationships the types represent).

### Burkhardt, Détienne & Wiedenbeck 1997 — static-vs-dynamic situation models

[isbn:978-0-387-35175-9 chapter 55]

The Burkhardt-Détienne-Wiedenbeck refinement (extending van Dijk-Kintsch's situation-model framework to programming) found the expert advantage in object-oriented comprehension is concentrated in the *static* situation model (objects, relationships, goals — what the program *is*) — experts and novices are statistically equivalent on the *program model* (control/data flow as text) and on the *dynamic* situation model (state evolution over time).

This refinement matters because it suggests the highest-yield mining modes are those that capture static structure: `signatures` (and the structural-shape parts of patterns). Dynamic-flow extraction is comparatively low-yield.

## The eight mining modes — extraction layered with synthesis

Eight modes across two phases. Extraction modes capture direct WHY signal per row; synthesis modes layer interpretation across rows. Claude does both — tools (`git`, `rg`, `gh`, `ast-grep`, etc.) are *locators* that surface candidate content; Claude reads, projects, and captures.

**Extraction modes (Phase 3c, per-row):**

| Mode | Layer of WHY | Primary artifact source |
|---|---|---|
| **oscillations** | *Why the code changed* — failure modes in revert messages | git history (novel within surveyed MSR — no Tier 1 source studies oscillation-as-primary-signal) |
| **scars** | *Why this code is correct despite looking dangerous* — invariants justifying careful choices | doc comments + cross-references (Falessi 2013 grounds the motivation: DRD is too onerous → tacit residue is rational) |
| **signatures** | *Why this exact shape* — typed shapes anchoring structural reasoning | code structure (static-situation-model anchor per Burkhardt 1997) |
| **schemas** | *Why this graph of types and relationships* — labeled property graph (CPG-aligned per Yamaguchi 2014) | code structure across types; aggregable cross-source |

**Synthesis modes (Phase 4, cross-row):**

| Mode | What it captures | Reads… |
|---|---|---|
| **models** | Program-model + domain-model artifacts (Pennington 1987) — what the program *is* in entities/relationships, vs what it *does* moment-to-moment | signatures + schemas + naming + module organization across sources |
| **tradeoffs** | Decisions with named alternatives + rationale | RFCs + PR archaeology + oscillations + "we chose X" comments |
| **antipatterns** | Approaches that look reasonable but fail | oscillations (reverts) + closed-without-merge PRs + scars-with-replacement |
| **aesthetics** | What "right" feels like (style, naming, comment voice, error-message density) | scars + signatures + style guides + cross-codebase consistency signals |

Principles emerge across modes via rule of three: any synthesis-mode finding recurring in ≥3 independent sources gets promoted to a principle. Not a separate mode — a promotion criterion.

## Why no quadrant model in the operational skill

An earlier draft mapped modes onto a 2×2 (Tacit/Explicit × Knowledge/Procedure). Several modes straddled cells (`aesthetic` is both tacit-felt and explicitly-stated in style guides; `practice`, when included, carries tacit when-to-apply judgment alongside its explicit step-sequence). The flat list — extraction modes capturing direct WHY signal, synthesis modes layering interpretation — is more honest. The 4-quadrant model is a defensible practitioner heuristic for organizing extended mode sets; the operational skill doesn't need it.

## Why a workflow skill, not a config-driven runtime

Earlier drafts attempted a configuration-driven pipeline: a YAML domain config, recon as the collector, distillation Components running per-mode against a Construct (matrix's blackboard). That shape made sense in the broader cix-stack ontology but had two problems:

1. **The Components don't exist yet.** Writing config before the consumer is theater.
2. **The user-facing question isn't "which collector wires to which Component."** It's "given this dataset and this goal, what do I do, in what order, and how do I resume across sessions?"

So radix-as-skill became radix-as-workflow: an operational playbook Claude follows, with shell tools (`git`, `rg`, `ast-grep`, `gh`) as the actual collection mechanism, and typed JSONL as the output format.

For the future-runtime migration path (when JSONL → Construct Frames becomes load-bearing), see `composition-with-cix-stack.md`. The row shapes are designed to survive the transition.

## v1 scope — what this skill is for

v1 of radix is for mining tacit knowledge from code-and-around-code artifacts in **any language or domain that qualifies for mining**. The qualifying test (the "3-filter rule" from the mining playbook):

- Is the knowledge **tacit**? (lives in code/git/expert practice, not in docs/tutorials/training datasets)
- Do **models get it wrong**? (current LLMs fail in characteristic ways suggesting missing understanding)
- Is it **expensive to reverse**? (mistakes are costly — security, correctness, performance, irreversibility)

If all three pass, the domain qualifies. If any fail (e.g., frontend frameworks where docs are extensive and mistakes cheap; API design where SS8/SS9 conventions cover most ground), spend effort on curating existing artifacts instead.

Rust is a worked example of a qualifying domain — see `skills/radix/references/exemplars/rust.md`. The 28-repo Rust corpus is one mining run an operator can do with this skill; the skill itself isn't tied to it.

## What we don't claim

- We don't claim radix recovers expert *cognition*. It recovers expert *artifacts*. The cognition→artifact correlation is an open research question.
- We don't claim a fixed cross-domain ratio of tacit-vs-explicit knowledge in code. Different domains will surface different ratios; the mining run produces the empirical answer for the domain mined.
- We don't claim the eight modes are exhaustive. They were chosen because each captures a distinct, identifiable layer of the WHY signal that public datasets miss. Other modes can be added when the cut earns its keep.
