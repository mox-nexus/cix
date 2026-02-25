# What cix Does

Two commands. That's the core of what cix does.

```bash
cix source add https://github.com/mox-nexus/cix
cix add craft-rhetoric
```

The first registers a git repository as an extension marketplace. The second installs a package from it.

What you get: a collection of skills, agents, and hooks copied into your Claude configuration directory (`~/.claude/plugins/`). The next time an agent session starts, those extensions are available.

What you don't get: the agent managing this for you. There is no auto-install, no adaptive configuration, no extension that adds other extensions when it decides you need them. The interface is `cix add` — human-initiated, one extension at a time. A tool you installed belongs to you. A tool that installed itself manages you.

[The Design Lever](the-design-lever) established that process control — the human's ability to influence what goes into and comes out of an AI system — is the strongest measured lever for whether the human feels ownership of the jointly-produced work (b=0.715, Blaurock et al. 2025). The installation interface builds that lever in at the start.

---

## What Gets Installed

The `craft-rhetoric` package contains nine agents (feynman, sagan, vyasa, orwell, tufte, jobs, socrates, magellan, planner), seven skills, and their associated reference documents. What Claude reads and what you read are different files in the same package.

Claude reads `skills/rhetoric/SKILL.md` — token-efficient, actionable, no provenance. It describes what to do when a user requests rhetoric work: the pipeline, the agents, the gates, the decision trees. CLAUDE.md is explicit: "Never read `docs/` directories — they contain human-optimized prose that wastes tokens and may confuse actionable guidance with learning material."

You read `docs/explanation/methodology.md` — the reasoning behind the design, where the framework came from, what evidence informed it. The sources are named. The design choices are explained. You can read it and disagree. You can read it and suggest a correction. If you find a problem in the methodology, you can trace it back to the source.

Docs/ exists so that evaluation remains possible before use — not only by the agent, not only after reviewing outputs, but by you, on the methodology itself, before you commit to directing it.

---

## The --skill Problem It Solves

There's an older pattern for giving agents knowledge about tools. A developer writes a skill document describing how their CLI works — what commands exist, when to use which, decision trees for common cases. They host it in a documentation site, or a separate GitHub repo, or a Wiki.

Then the tool changes. The CLI gets a new subcommand. A flag is deprecated. The skill document, authored separately, maintained separately, living in a different repository on a different release cycle, still says the old thing. The agent follows the outdated instructions. Nobody notices until something breaks.

cix tools expose a `--skill` flag:

```bash
cix --skill
memex --skill
```

The output is the SKILL.md document for that tool — the same document the agent would read from an installed extension. It lives inside the Python package at `src/cix/assets/skills/cix/SKILL.md`, loaded via `importlib.resources`.

When the tool ships a new version, the skill ships with it. The description evolves on the same release cycle as the behavior — the agent reads from the same source as the behavior.

This is dependency inversion for cognitive interfaces: instead of the skill depending on the tool documentation (brittle, out-of-band, separate maintainer), the skill is a dependency of the tool itself.

---

## Four Kinds, One Requirement

Every cix extension belongs to one of four kinds.

**Skills** carry decision frameworks and methodology. The craft-rhetoric skill tells an agent how to run a writing pipeline. The arch-guild skill tells an agent how to engage multiple architectural reasoning perspectives. Skills teach the agent how to think, not what to answer.

**Agents** provide a single, named perspective. Feynman encodes comprehension and teaches. Socrates evaluates whether understanding propagates. Each agent is constrained to one perspective — the CLAUDE.md calls this "Orthogonality Lock." Two agents covering the same ground would let the human defer to whichever said what they already believed. One perspective per agent forces synthesis: if you want a complete picture, you have to read multiple agents' outputs and combine them yourself.

**Hooks** trigger on events in the Claude Code workflow. When you save a file, when you commit, when a task completes — a hook can run an agent or execute a check. These augment the workflow without replacing any decision in it.

**MCPs** (Model Context Protocol) bridge to external systems. A database, an API, a service — the MCP makes it accessible to the agent. The human still decides when to invoke it, what to do with the results.

The pattern across all four kinds: additive, not substitutive. The skill adds a decision framework; it doesn't replace judgment. The agent offers a perspective; the human synthesizes. The hook augments a step; it doesn't own the step. The MCP provides access; the human directs use.

---

## Who This Is For, and What Was Chosen Against

The developer who adds `craft-rhetoric` to their Claude configuration is not getting a writing assistant that takes drafts off their hands. They're getting a structured methodology that asks them to articulate — through discourse — what they actually know about their subject before any writing begins.

The discourse step from [The Mechanism](the-mechanism): the agent asks, the human generates. Not "approve this summary." Not "does this capture what you meant?" The human produces the ground truth from their own understanding, and the agent's role is to draw it out through questions.

This is who the methodology serves: someone who wants to understand why their docs read as hollow — and is willing to do the work of generating substance rather than approving synthesis. Someone building a library, writing technical explanations, or producing reference documentation that will be used, not just filed.

What was chosen against: the writing assistant that generates and the human edits. [The Mechanism](the-mechanism) established what happens with that pattern in prose — the correlation between chat-based AI use and knowledge transformation was approximately zero (r≈0, Siddiqui et al. 2025). Prose arrives pre-resolved; the thinking that would have happened through composition doesn't happen. A methodology that starts with AI generation and ends with human editing keeps the human in editorial mode, not generative mode.

The craft-rhetoric plugin operationalizes the opposite design: human generates the substance, agent structures the delivery. Whether this choice produces the intended effect on capability — that remains unmeasured for cix specifically.

---

## The Marketplace as Countermeasure

[The Stakes](the-stakes) described a problem at the level of AI systems themselves: LLM outputs are measurably less diverse than human outputs. RLHF trains models to converge on consensus. The Jiang et al. NeurIPS 2025 paper documented 70+ language models independently reaching for the same river metaphor, the same weaver metaphor, across different architectures.

The same dynamic applies to extension design. A marketplace that provides preset skills — "here are the three approaches to API design, pick one" — is itself a convergence vector. Every team that installs it gets the same three options framed the same way. The options might be good. The narrowing is still real.

cix's response is what the ground truth calls the Dao engagement model: skills designed as methodologies for discovering the user's unique approach, not catalogs of preset answers. The arch-guild skill doesn't say "here is the architecture for your service." It activates a set of distinct reasoning agents — Burner (integrity, boundaries), Erlang (flow dynamics), Karman (truth, correctness) — and those agents ask the developer questions that draw out the architecture that fits their specific constraints. Burner asks: "What is the boundary you're not willing to cross, regardless of performance?" A preset catalog gives three database options ranked by query speed. Burner finds what the team considers inviolable. That answer is not in any catalog, because it has never been asked for.

The output of a dao-aligned skill is a project-specific instance. What the developer brought to the discourse is what the skill reflects back. The skill is the scaffold; the content is the human's.

Whether individual users actually engage deeply enough in discourse to generate unique content — rather than accepting the first agent output that sounds reasonable — is the open question. The ground truth names it explicitly: "Depends on discourse quality — if the human doesn't generate something unique, convergence returns."

---

## What cix Does Not Claim

If you've just read the preceding sections and felt the design make sense — felt the architectural choices map cleanly onto the research — this section is for you. That feeling is accurate about the design. It is not evidence about your use.

There is no evaluation data for any cix plugin. The `build-evals` plugin exists but has not been run. No study has measured whether developers who use craft-rhetoric maintain critical thinking better than developers who use a standard LLM writing assistant. No longitudinal data tracks whether arch-guild users develop stronger architectural reasoning over time, or whether they develop a dependency on the guild's prompting.

The evidence base for cix's design choices is drawn from other domains: Bastani et al.'s high school math students (n~1,000, PNAS), Blaurock et al.'s financial services and HR professionals (N=654, Journal of Service Research), Shen and Tamkin's software developers (n=52, arXiv). These studies establish that engagement model, process control, and mastery orientation are meaningful variables. They do not establish that the specific cix implementation is an effective instance of these variables.

The honest characterization: cix operationalizes the design levers that the evidence supports, for the problem that the research documents. Whether cix's specific implementations actually produce the intended effects — capability compounding rather than atrophy, diversity preservation rather than convergence — is a bet grounded in evidence from other domains, not a measured outcome from cix itself.

This is not a failure of the design. It is the honest state of the art. The research that bears on these questions — including Shen & Tamkin's January 2026 paper on interaction patterns — is weeks old. The project is building on the best available evidence while that evidence is still being gathered.

---

## The Design Logic

[The Design Lever](the-design-lever) established that four design features were tested independently against employee outcomes. Process control and outcome control worked. Transparency helped but required careful implementation to avoid the compliance trap Bansal documented. Engagement features produced nothing.

Human-initiated installation (`cix add`) operationalizes process control: the human decides what cognitive tools enter their workflow.

Dual-content model operationalizes transparency: the methodology is visible and traceable. The docs/ files are designed to enable evaluation, not substitute for it — they include explicit uncertainty, evidence levels, and source citations rather than polished rationales. But the Bansal effect is real: a well-explained methodology can increase compliance without improving calibration. This tension is not resolved in the design (Bansal et al. 2021, CHI).

Orthogonality lock operationalizes mastery orientation: each agent offers one perspective, which forces the human to synthesize. The design creates conditions for evaluation across perspectives rather than delegation to a single comprehensive agent.

Self-describing capabilities (`--skill`) operationalizes the compound value principle: knowledge that stays current with the behavior it describes, because it ships with the behavior.

The design decisions are grounded in the best available evidence. They have not been measured in cix's own operation. That is where the project stands.

Which means this: you are holding a tool whose design encodes the best available answer to a documented problem — and whose effect on your capability is still an open question. Not because the design is uncertain, but because you haven't been measured yet. Neither has anyone else who uses it. Whether the gap between the documented harm and the designed response is actually closed by this specific implementation — that is what using it, and eventually measuring it, will establish.

The bet is made. The evidence is named. The gap is honest.
