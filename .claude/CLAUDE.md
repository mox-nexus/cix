# Collaborative Intelligence Extensions (cix)

> **Liberation through Collaborative Intelligence**
> Extensions that enhance human capability, not replace it.

## Mission

Build a marketplace of cognitive extensions grounded in the **Collaborative Intelligence** thesis: AI tools should amplify human capability and judgment, not substitute for them. Every extension in this ecosystem must make humans more capable, not dependent.

---

## The Evidence Base

This project is grounded in rigorous research synthesis from premier venues (CHI, ICSE, Nature, PNAS, NeurIPS). The findings are sobering:

### The Central Paradox

**AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable long-term human capability.**

| Finding | Source | Implication |
|---------|--------|-------------|
| 26% more tasks completed with AI | Cui/Demirer RCTs (n=4,867) | Productivity gains are real |
| 17% worse exam performance without AI | Bastani et al. PNAS (n=1,000) | Learning harm is real |
| 20% skill reduction after 3 months | Lancet colonoscopy study | Deskilling is measurable |
| β = -0.69 correlation | Lee et al. CHI 2025 | AI confidence → less critical thinking |

### Key Research Findings

**On Cognitive Offloading:**
- Higher confidence in AI significantly predicts less critical thinking enacted
- Neural connectivity "systematically scaled down" with AI use (MIT Media Lab EEG study)
- 83.3% of AI users couldn't recall quotes from their own AI-assisted essays

**On Trust Calibration:**
- Developers spend only 22.4% of coding time verifying AI suggestions
- Explanations alone *increase* overreliance (Bansal et al. CHI 2021)
- Senior developers trust AI least (2.5%) but use it most effectively

**On Skill Atrophy:**
- The critical study doesn't exist: no longitudinal measurement of developer capability without AI after extended AI use
- Aviation research: 77% of pilots report degraded manual skills from automation
- Protective factor: high self-confidence correlates with maintained critical thinking

**On Learning:**
- GPT Tutor (hints only): No harm to learning
- GPT Base (direct answers): 17% harm to learning
- Same technology, different design philosophy, opposite outcomes

---

## Design Philosophy

### Complementary vs Substitutive

The fundamental design decision for every extension:

| Substitutive | Complementary |
|--------------|---------------|
| AI does the work, human approves | AI amplifies, human remains central |
| Human capability atrophies | Human capability compounds |
| "Here's the answer" | "Here's how to think about this" |
| Trust becomes binary (accept/reject) | Trust becomes informed |
| Skills erode over time | Skills strengthen over time |

**Every extension MUST be complementary.** This is not a guideline—it's the core value proposition.

### The WHY > HOW Principle

From claude-1337 research:

| Approach | Outcome |
|----------|---------|
| Prescribe HOW (do X, then Y, then Z) | 30% secure-by-construction |
| Explain WHAT + WHY | **80% secure-by-construction** |

**2.5x improvement** from explaining motivation rather than mandating method.

Extensions should teach reasoning frameworks, not prescribe solutions:
```
❌ "Always use prepared statements for SQL"
✅ "SQL injection occurs when user input is treated as code.
    Prepared statements separate data from code.
    Consider: where does untrusted input enter your query?"
```

### The Saarthi Principle

AI as **Saarthi** (Sanskrit: सारथी, charioteer) — not a tool to be used or master to obey, but a collaborative partner that guides while humans act.

Krishna doesn't take the reins from Arjuna. He guides while Arjuna makes decisions and takes action.

---

## Extension Design Principles

### 1. Additive, Not Replacing

Extensions add capability without removing the human's ability to work without them.

```
✅ "Here's what I see. Here's my reasoning. You decide."
❌ "I've handled it. Here's the result."
```

### 2. Transparent Reasoning

The human should understand WHY the extension reached its conclusion.

```
✅ Evidence levels: Strong / Moderate / Weak / Speculative
✅ Show the chain: Observation → Analysis → Recommendation
❌ "Trust me, this is correct."
```

### 3. Human-Initiated Control

Extensions respond to human direction, not autonomous optimization.

```
✅ Human: "Review for security" → Agent provides analysis
❌ Agent autonomously "fixes" security issues
```

### 4. Composable, Not Comprehensive

Small, focused extensions that combine > one monolithic "do everything" agent.

```
✅ security-review + api-contracts + observability → Human synthesizes
❌ "full-code-review-agent" that handles everything opaquely
```

### 5. Teach the Framework, Not the Answer

Extensions should make humans better at the domain, not dependent on the tool.

```
✅ "Here's how to think about rate limiting: [framework]"
❌ "Here's your rate limiting config: [solution]"
```

---

## The Collaboration Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   HUMAN INTENT                                          │
│   ↓                                                     │
│   EXTENSION provides perspective / analysis / options   │
│   ↓                                                     │
│   HUMAN evaluates, learns, decides                      │
│   ↓                                                     │
│   EXTENSION executes within human-defined bounds        │
│   ↓                                                     │
│   HUMAN CAPABILITY INCREASES                            │
│   ↓                                                     │
│   [Loop continues - human more capable each cycle]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What makes it collaborative:**
- Human initiates each cycle
- Human makes final decisions
- Human learns through the process
- Extensions amplify, never replace

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Complementary Alternative |
|--------------|---------|---------------------------|
| **Auto-fix** | Human doesn't learn why | Explain issue, offer fix, human applies |
| **Black box** | Human can't evaluate | Show reasoning at every step |
| **Scope creep** | Agent does more than asked | Strict orthogonality constraints |
| **Confidence theater** | Fake certainty | Explicit uncertainty (evidence levels) |
| **Memory hoarding** | Private agent state | Shared knowledge substrate |
| **Paternalism** | "I know better" | "Here's my perspective, you decide" |

---

## Extension Types

### Skills
**Purpose:** Decision frameworks and methodology
**Pattern:** Teaches HOW to think about a domain
**Example:** Reasoning patterns for security analysis

### Agents
**Purpose:** Specialized perspectives for delegation
**Pattern:** Offers viewpoint, human synthesizes
**Example:** Security architect perspective

### Hooks
**Purpose:** Event-triggered behaviors
**Pattern:** Enhances existing workflow
**Example:** Metacognitive check before accepting AI suggestions

### MCPs (Model Context Protocol)
**Purpose:** External service integration
**Pattern:** Bridges systems, human orchestrates
**Example:** Knowledge base connector

---

## The Verification Imperative

> "Can't vibe through answers. Must ground in evidence."

### Why Verification Matters

Research shows:
- 40-50% of AI-generated code contains security vulnerabilities
- LLMs cannot reliably self-correct without external feedback
- Verification must be decoupled from generation to be effective

### Chain-of-Verification Pattern

Independent verification prevents hallucination from corrupting fact-checking:
1. Generate initial response
2. Plan verification questions targeting specific claims
3. Answer each question **independently** (without access to initial response)
4. Synthesize corrections

This achieves **50-70% hallucination reduction** (Dhuliawala et al. ACL 2024).

---

## Protective Practices

Based on research, extensions should encourage:

### 1. Attempt-First Protocol
Spend 15-30 minutes on problems before AI consultation. This preserves problem-solving practice.

### 2. Verification Workflows
Require human review of all AI contributions regardless of perceived quality.

### 3. Metacognitive Prompts
"What do you think the answer is?" before revealing AI analysis.

### 4. AI-Free Assessment Periods
Periodic work without AI to maintain baseline capability.

### 5. Explicit Uncertainty Communication
Never project false confidence. Use evidence levels:
- **Strong**: Multiple peer-reviewed sources
- **Moderate**: Single quality source or converging indirect evidence
- **Weak**: Expert opinion or theoretical prediction
- **Speculative**: Reasonable inference without direct evidence

---

## Success Criteria

An extension succeeds when:

1. **Human capability increases** — The user is more capable after using the extension than before
2. **Reasoning is transparent** — The user understands why, not just what
3. **Control remains with human** — User can work without the extension if needed
4. **Learning happens** — Each interaction builds understanding
5. **Trust is calibrated** — User knows when to rely and when to verify

An extension fails when:

1. Human becomes dependent
2. Trust becomes binary (accept/reject without evaluation)
3. Skills atrophy from disuse
4. Reasoning becomes opaque
5. Control shifts from human to AI

---

## The Deeper Why

> "An AI that makes humans dependent has failed.
> An AI that makes humans more capable has succeeded."

Collaborative extensions aren't just better engineering. They're **ethical design**.

The goal isn't to build better tools. The goal is to build tools that make better humans.

---

## Project Architecture

```
cix/
├── tools/cix/              # CLI package (hexagonal architecture)
│   └── src/cix/
│       ├── domain/         # Pure domain models
│       ├── ports/          # Interface definitions
│       ├── adapters/       # Implementations
│       └── application/    # Use case orchestration
├── plugins/                # Marketplace plugins (distributable)
└── .claude/                # Project-specific Claude extensions
```

### Hexagonal Architecture

- **Domain**: Pure business logic with no external dependencies
- **Ports**: Interfaces for what cix needs (driven) and how users interact (driving)
- **Adapters**: Implementations of ports (git, filesystem, CLI)
- **Application**: Use case orchestration through ports

This enables:
- Testing without external dependencies
- Multiple implementations (git + local, CLI + API)
- Clear separation of concerns
- Protocol independence

---

## Working Conventions

### Scratch Directory

When taking notes or preserving context across sessions, use `scratch/` in the project root.

### Evidence-Based Claims

All claims in extensions should be traceable:
```
✅ "According to Bastani et al. (PNAS 2025), unrestricted ChatGPT use caused 17% worse exam performance"
❌ "AI harms learning"
```

### Uncertainty Acknowledgment

When evidence is limited:
```
✅ "This is speculative - no direct research exists, but analogous domain findings suggest..."
❌ "Research shows..." (when it doesn't)
```

---

## References

Core research informing this project:

- Bastani et al. (2025). "Generative AI without guardrails can harm learning." PNAS.
- Lee et al. (2025). "The Impact of Generative AI on Critical Thinking." CHI.
- Kosmyna et al. (2025). "Your Brain on ChatGPT: Cognitive Debt." MIT Media Lab.
- Dhuliawala et al. (2024). "Chain-of-Verification Reduces Hallucination." ACL.
- Hemmer et al. (2024). "Complementarity in Human-AI Collaboration." EJIS.
- Cui/Demirer et al. (2024). "Effects of Generative AI on High Skilled Work." RCTs.

Full bibliography in `research/bibliography.md`.

---

*This is the alpha era of cix. Every decision should be evidence-based, every extension should be complementary, every user should become more capable.*
