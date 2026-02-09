# collab-scaffolds

Research-grounded scaffolds for effective human-AI collaboration.

## What This Is

Scaffolding for collaborative building — temporary support designed to be outgrown. Every scaffold is backed by research evidence from 50+ studies (CHI, PNAS, Lancet, NeurIPS, HICSS). Two skills, two agents, aligned with the Software Craftsmanship Manifesto.

## When It Activates

- Writing code or making technical decisions
- Refactoring and code reviews
- Debugging (especially when stuck)
- Verifying claims or calibrating trust
- Any context where quality matters

## What You Get

### Skills

**collab-craft** — Collaborative behaviors for effective CI:
- Software Craftsmanship Manifesto alignment
- Building principles (compound value, complete the work, craft over speed)
- Collaboration patterns (Generation-Then-Comprehension, Task Stewardship)
- Workflows (refactoring, scaffolding, planning before implementation)
- Trust calibration (evidence levels, contrastive explanations)
- Anti-patterns (jumping ahead, incomplete refactoring, vibe coding, avoidance crafting)

**problem-solving** — Structured thinking and metacognition:
- Wolf Protocol (stop → classify → break down → verify)
- Metacognitive scaffolds (Cognitive Mirror, PME Friction, HypoCompass)
- Reasoning frameworks (Hypothesis Testing, OODA, Decision Framework)
- Verification (CoVe, Pythea, contrastive explanations)
- Uncertainty calibration and evidence levels

### Agents

**Mr. Wolf** — Structured problem solver. Gets called when you're stuck, going in circles, or debugging isn't converging. Loads `problem-solving` skill.

**Duck** — Rubber duck debugging through Socratic dialogue. Helps you think through problems by asking questions, not giving answers. Loads `problem-solving` skill.

| | Duck | Wolf |
|---|------|------|
| **Trigger** | "I need to think this through" | "I'm stuck, nothing's working" |
| **Mode** | Socratic — asks questions | Directive — breaks it down |
| **Goal** | You articulate → you discover | Problem classified → systematically solved |

### Hooks

| Hook | Detects | Response |
|------|---------|----------|
| `detect-debugging-loop` | 3+ consecutive failures | Spawns Mr. Wolf |
| `detect-frustration` | User frustration signals | Spawns Mr. Wolf |
| `session-start` | Session begins | Shows available skills |

## Structure

```
collab-scaffolds/
├── skills/
│   ├── collab-craft/              # CI collaboration behaviors
│   │   ├── SKILL.md               # Building, collaboration, workflows (< 500 lines)
│   │   └── references/            # Deep dives (8 files)
│   │       ├── trust-calibration.md
│   │       ├── skill-preservation.md
│   │       ├── productivity-reality.md
│   │       ├── behavioral-awareness.md
│   │       ├── kaizen-crystallization.md
│   │       ├── verification-patterns.md
│   │       ├── writing-antipatterns.md
│   │       └── principles-and-patterns-examples.md
│   └── problem-solving/           # Structured thinking & metacognition
│       ├── SKILL.md               # Wolf Protocol, scaffolds, verification (< 300 lines)
│       └── references/            # Deep dives (3 files)
│           ├── metacognitive-scaffolding.md
│           ├── reasoning-scaffolds.md
│           └── reasoning-verification.md
├── agents/
│   ├── mrwolf.md                  # Structured problem solver
│   └── duck.md                    # Rubber duck (Socratic dialogue)
├── hooks/
│   ├── hooks.json
│   ├── detect-debugging-loop.sh
│   ├── detect-frustration.sh
│   └── session-start.sh
├── docs/
│   └── explanation/               # Human-optimized (WHY)
│       ├── methodology.md
│       └── sources.md
└── scripts/                       # Installation helpers
```

## Philosophy

**You're not done when it works. You're done when it's right.**

Everything you create becomes part of a system others depend on. Scaffolding, not crutches — temporary support designed to make humans more capable, not dependent.
