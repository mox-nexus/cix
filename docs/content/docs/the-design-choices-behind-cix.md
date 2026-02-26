# The Design Choices Behind cix

```bash
claude marketplace add mox-labs/cix
```

That installs a package of extensions — agents, skills, reference files. What those extensions contain, and how they're structured, follows from four design principles. Each one responds to something the [prior two articles](/docs/the-productivity-trap) documented.

---

## Transparency by default

The [first article](/docs/the-productivity-trap) established a perception gap: developers thought AI made them 24% faster while it made them 19% slower. The [second](/docs/same-tool-different-design) showed that transparency — making AI reasoning visible — is one of the strongest levers against blind acceptance. It also showed the complication: [Bansal et al.](/docs/bibliography#bansal-2021) (2021, CHI) documented that explanations increase acceptance regardless of correctness. A well-explained methodology can produce compliance rather than evaluation.

Transparency helps — until it presents a polished rationale for a conclusion already reached, at which point it substitutes for evaluation entirely.

cix extensions are transparent in a way that creates the *condition* for genuine evaluation rather than the *feeling* of it.

Every cix extension ships two layers.

**Agent-facing**: `SKILL.md` — token-efficient, actionable, no prose. Decision trees, pipeline definitions, gate criteria. This is what Claude reads during a session.

**Human-facing**: `docs/` — the reasoning behind the design, where the framework came from, what evidence informed it. Sources named. Design choices explained. You can trace any claim back to its source. If you find a problem in the methodology, you have the thread to pull.

The agent never reads `docs/`. You never need to read `SKILL.md`. Both describe the same system from different angles, for different audiences.

This is the specific thing transparency means here: not an explanation of the recommendation, but access to the reasoning *before* the recommendation. Open to inspection before you decide whether to trust what it produces. You don't have to take the skill at its word. You can read it and decide.

Tools describe themselves the same way:

```bash
cix --skill
memex --skill
```

The `--skill` flag outputs the same SKILL.md an agent reads — co-located in the Python package, shipping on the same release cycle as the tool itself. Think `--help` for humans, `--skill` for agents. When the tool changes, the skill changes with it. No drift between documentation and behavior.

The `craft-evals` plugin ships evaluation frameworks for measuring whether extensions actually work. OTel references in `craft-extensions` make agent behavior observable. Transparency isn't a principle statement — it's instrumented.

---

## Discourse-driven generation

The convergence problem from the [previous article](/docs/same-tool-different-design): AI outputs are measurably less diverse than human outputs (g=-0.863 across 28 studies with high between-study heterogeneity; [Holzner et al. 2025](/docs/bibliography#holzner-2025), n=8,214). [Jiang et al.](/docs/bibliography#jiang-2025) demonstrated that 70+ language models independently reach for the same metaphors, the same framings, across different architectures.

A marketplace that ships preset answers — here are three approaches to API design, ranked by query speed — narrows in the same way. Every team gets the same three options, framed the same way. The product is the convergence.

cix skills are structured differently. They don't give answers. They give methodology for discovering *your* answer.

`craft-rhetoric` is the clearest example of this. Before any content is produced, the skill runs a discourse step: an agent asks what you're trying to communicate, to whom, with what evidence, and why it matters. You answer. The ground truth you articulate — your intent, your claims, your honest uncertainties — becomes the input to every downstream step. The content that emerges is yours in a specific, non-metaphorical sense: it came from what you knew and believed, not from what the model defaults to.

The methodology requires the human to generate the inputs the model needs to help them. The skill is the scaffold. The understanding was always going to have to come from you.

This depends entirely on what you bring. If you accept the first agent output that sounds reasonable, the scaffold hasn't helped. The methodology only resists convergence when someone actually uses it to think.

---

## Diverse agent teams

The orientation finding from [Pallant et al.](/docs/bibliography#pallant-2025) (2025, Studies in Higher Education) was not subtle: students using AI in a mastery-oriented way — constructing and augmenting knowledge rather than copying output — were 35.8 times more likely to demonstrate critical thinking — not a percentage-point improvement but a thirty-five-fold difference.

The interaction structure determines which orientation emerges. An agent that gives you a verdict — "here is the right architecture" — makes passive acceptance the natural response. An agent that gives you a perspective and asks you to synthesize it with three others makes you structurally responsible for the conclusion.

The guild-arch plugin is built on this distinction. Instead of one "architecture review" agent that delivers a verdict, it activates distinct reasoning perspectives:

- **Burner** asks about the constraints your team considers inviolable, regardless of performance
- **Erlang** asks about flow dynamics and backpressure
- **Knuth** asks about algorithmic complexity at scale
- **Vector** asks where the attack surface is

No single agent gives you "the architecture." Each agent asks questions from its perspective. You synthesize. The architecture that emerges reflects your constraints, not a preset template.

Consider what Burner surfaces that no catalog ever could. A catalog gives you three database options ranked by query speed. Burner asks what the team considers inviolable. The team says: no vendor lock-in, ever, because of what happened two years ago. That answer was never in any catalog. It was never known until asked. It is the most important input to the architectural decision, and it lives only in the humans in the room.

The same pattern runs through `craft-rhetoric`: nine agents — feynman for comprehension, orwell for voice, socrates for evaluation, vyasa for structure — each with orthogonal concerns. They don't converge on consensus. They maintain distinct viewpoints that the human must reconcile. The reconciliation is the thinking.

---

## Marketplace as methodology

The three principles above — transparency, discourse-driven generation, diverse agent teams — address what a single extension does and how it interacts with the human using it. The fourth addresses what a marketplace does to the people who build with it.

The observable phenomenon: project names (Sentinel, Forge, Nexus), landing pages that could have been generated from the same prompt, product copy that sounds like everyone else's copy — all converging through shared AI systems.

<chart id="naming-convergence"></chart>

A marketplace of preset skills accelerates this. Teams reach for the same options, framed the same way, and the distinctiveness that was always downstream of the human thinking drains out. The collapse [Shumailov et al.](/docs/bibliography#shumailov-2024) documented at model level happens at culture level too.

The response inverts the marketplace dynamic. Every skill interaction should produce a project-specific instance reflecting what the human brought — not a template customized with the human's name, but a skill applied to the human's actual constraints, beliefs, and context.

This is the newest principle and the least validated. The research establishes that engagement model matters ([Bastani et al. 2025](/docs/bibliography#bastani-2025), PNAS), that mastery orientation produces dramatically different outcomes (OR=35.8, [Pallant 2025](/docs/bibliography#pallant-2025)), and that process control is the strongest measured lever (b=0.715, [Blaurock et al. 2025](/docs/bibliography#blaurock-2025)). Marketplace as skill — not catalog — is our synthesis of those findings into marketplace-level design.

Whether it works at scale is being evaluated. This honesty is structural, not decorative — if the skill doesn't produce meaningfully different outputs across teams, it's a principle statement without evidence behind it, and the design should change.

---

## Where we are

There is a question underneath all four principles. It is not "do these design choices improve productivity?" Productivity is already improved; the evidence from [Cui et al.](/docs/bibliography#cui-2024) (2024, SSRN) is clear enough. The question is whether the humans who use these extensions are more capable six months from now than they are today. Whether the understanding compounds instead of atrophying. Whether the tool made itself legible enough that the human never stopped being the one who knew things.

That question will be answered by what the measurements show. Not by the design choices themselves.

The only honest position is that the design is an extrapolation. It extends from the best available evidence about what makes AI interactions compound capability rather than replace it. The research points clearly enough that building against its direction would require active rationalization. But the extrapolation has not yet been validated in the specific context it was designed for.

That is where we are. And that is the right place to be — building the measurement infrastructure to find out whether it works.
