# cix

Collaborative Intelligence Extensions — a marketplace of cognitive extensions for Claude Code.

## The Problem

AI tools create a paradox: they make you faster today while making you less capable tomorrow.

Research from premier venues (CHI, PNAS, Nature, NeurIPS) shows the pattern consistently:

| Finding | Source | What It Means |
|---------|--------|---------------|
| 26% more tasks completed | Cui/Demirer RCTs (n=4,867) | Immediate productivity gains are real |
| 17% worse performance without AI | Bastani et al. PNAS (n=1,000) | Learning degradation is measurable |
| 20% skill reduction after 3 months | Lancet colonoscopy study | Expertise atrophies from disuse |
| 83% couldn't recall their own work | Lee et al. CHI 2025 | Cognitive offloading has memory costs |

The problem isn't AI. The problem is **substitutive AI** — tools designed to do your thinking for you.

## The Solution

**Complementary AI** — tools that amplify your capability rather than replace it.

Same technology. Different design philosophy. Opposite outcomes.

Consider GPT Tutor research (Bastani et al.):
- **GPT Base** (direct answers): 17% harm to learning
- **GPT Tutor** (hints only): No harm to learning

The difference: one substitutes for thinking, the other supports it.

cix provides extensions built on complementary principles:
- Extensions show reasoning, not just answers
- Human makes the decisions, AI provides perspectives
- Each interaction builds capability rather than dependency
- Control remains with you

## Quick Start

**Try it now** (zero install):
```bash
uvx cix install arch-guild
```

**Install the CLI:**
```bash
uv tool install cix
cix install arch-guild
```

**Or via Claude Code marketplace:**
```bash
claude plugin marketplace add mox-nexus/cix
```

For detailed usage, see the [experience site](https://mox-nexus.github.io/cix/).

## Extensions

Browse the [catalog](https://mox-nexus.github.io/cix/catalog).

## Design Principles

Every extension in cix follows these principles:

**Complementary, not substitutive.** Extensions amplify human capability. They show reasoning and provide perspectives, but you make the decisions.

**Transparent by default.** You see the reasoning, not just the conclusion. Evidence levels (Strong/Moderate/Weak/Speculative) communicate certainty honestly.

**Human-initiated control.** Extensions respond to your direction, not autonomous optimization. Control is the strongest lever (β = 0.507 per research).

**Composable, not comprehensive.** Small, focused extensions that combine rather than one monolithic tool. Forces you to synthesize perspectives.

**Teach frameworks, not answers.** Extensions make you better at the domain. They explain "why" and "how to think about this," not just "do this."

Research shows these design choices work: users maintain critical thinking (OR = 35.7) when tools support mastery rather than just performance.

## Why This Matters

> "An AI that makes humans dependent has failed. An AI that makes humans more capable has succeeded."

The goal isn't better tools. The goal is better humans.

cix exists because:
- 40-50% of AI-generated code contains security vulnerabilities
- Developers spend only 22.4% of time verifying AI suggestions
- Senior developers trust AI least but use it most effectively
- Neural connectivity "systematically scales down" with unreflective AI use

The industry needs extensions designed with human capability as the success metric, not task completion speed.

## Architecture

```
cix/
├── tools/cix/              # CLI (Python + uv)
│   └── src/cix/
│       ├── domain/         # Pure business logic
│       ├── ports/          # Interface definitions
│       ├── adapters/       # Implementations
│       └── application/    # Use case orchestration
├── plugins/                # Marketplace extensions
├── docs/
│   ├── experience/         # SvelteKit static site
│   └── content/            # Markdown content (mdsvex)
└── .claude/                # Project-specific extensions
```

The CLI uses hexagonal architecture for testability and protocol independence. Plugins are distributable packages that Claude Code loads.

## Contributing

cix is pre-alpha. Everything is subject to change.

**To contribute an extension:**

1. Follow the dual-content model (Claude-optimized SKILL.md, human-optimized docs/explanation/)
2. Ensure complementary design (amplify, don't replace)
3. Ground claims in evidence with traceable sources
4. Include evals demonstrating activation and quality
5. Submit a pull request to this repository

See `plugins/extension-dev` for authoring guidance.

**Design standards:**
- Extensions must make humans more capable, not dependent
- Reasoning must be transparent
- Control remains with the human
- Claims must be evidence-based and sourced

**Quality bar:**
- Does the extension teach, or just execute?
- Can the user work without it after using it?
- Is the reasoning visible, not hidden?
- Are success criteria human capability, not task speed?

## Documentation

The [experience site](https://mox-nexus.github.io/cix/) provides:
- Full methodology and research synthesis
- Plugin reference documentation
- Evidence base with citations
- Design philosophy and patterns

For local development:
```bash
cd docs/experience
bun install
bun run dev
```

## Research Foundation

cix is grounded in research synthesis from:

- Bastani et al. (2025). "Generative AI without guardrails can harm learning." PNAS.
- Lee et al. (2025). "The Impact of Generative AI on Critical Thinking." CHI.
- Kosmyna et al. (2025). "Your Brain on ChatGPT: Cognitive Debt." MIT Media Lab.
- Blaurock et al. (2024). "Designing Collaborative Intelligence Systems." Journal of Service Research.
- Cui/Demirer et al. (2024). "Effects of Generative AI on High Skilled Work." Multiple RCTs.

Full bibliography with 50+ sources: `docs/content/library/reference/bibliography.md`

## Status

Pre-alpha. The core thesis is stable, but APIs and structure may change. Use in production at your own risk.

## License

MIT

---

*This is the alpha era of cix. Every decision should be evidence-based, every extension should be complementary, every user should become more capable.*
