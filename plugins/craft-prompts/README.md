# craft-prompts

Prompt engineering techniques for different model architectures and execution patterns. What works for Claude doesn't work for o1 — this plugin provides architecture-aware guidance grounded in research.

## When to Use

- Prompting reasoning models (o1, o3, Gemini Deep Think)
- Running AI-assisted deep research with citation accuracy
- Synthesizing multiple papers into coherent analysis
- Orchestrating Claude Code subagents for parallel work

## Skills

| Skill | Use When |
|-------|----------|
| `deep-reasoning` | Prompting extended thinking models — chain-of-thought, budget allocation, constraint framing |
| `deep-research` | AI-assisted research — source verification, citation grounding, iterative refinement |
| `synthesize-papers` | Multi-paper analysis — cross-paper themes, contradictions, evidence synthesis |
| `multi-agent` | Orchestrating subagents — task decomposition, context isolation, result aggregation |

## Key Principles

- **Architecture-aware** — reasoning models need different prompts than autoregressive models
- **Evidence over intuition** — techniques backed by ACL, NeurIPS, and Meta Research findings
- **Isolation-aware** — subagents see only what you give them; context design matters
- **Composable** — each skill is orthogonal, combine as needed

## License

MIT
