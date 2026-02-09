# collab-scaffolds

Research-grounded scaffolds for effective human-AI collaboration.

## What This Is

Scaffolding for collaborative building — temporary support designed to be outgrown. Every scaffold is backed by research evidence from 50+ studies (CHI, PNAS, Lancet, NeurIPS, HICSS). Not tutorials — decision frameworks, metacognitive techniques, trust calibration, and the reasoning behind them.

## When It Activates

- Writing code or making technical decisions
- Refactoring and code reviews
- Debugging (especially when stuck)
- Verifying claims or calibrating trust
- Any context where quality matters

## What You Get

### The Skill (collab-craft)

Collaborative building methodology grounded in:
- Software Craftsmanship Manifesto principles
- Metacognitive scaffolding (Cognitive Mirror, PME friction)
- Trust calibration (evidence levels, contrastive explanations)
- Skill preservation (approach crafting, recovery protocols)
- Evidence-based decision making and verification

### The Agent (Mr. Wolf)

**Structured problem solver.** Gets called when you're stuck, going in circles, or debugging isn't converging.

Mr. Wolf:
1. Stops what isn't working
2. Clarifies what's actually happening
3. Identifies the type of problem
4. Breaks it down systematically
5. Verifies before declaring solved

### The Hooks (Automatic Assistance)

Two hooks detect patterns that need intervention:

| Hook | Detects | Response |
|------|---------|----------|
| `detect-debugging-loop` | 3+ consecutive failures | Spawns Mr. Wolf |
| `detect-frustration` | User frustration signals | Spawns Mr. Wolf |

**To disable hooks:** Set environment variable `SKIP_MRWOLF_HOOKS=1`

```bash
SKIP_MRWOLF_HOOKS=1 claude
```

## Structure

```
collab-scaffolds/
├── skills/collab-craft/
│   ├── SKILL.md              # Building methodology (< 500 lines)
│   └── references/           # Deep dives (11 files)
│       ├── metacognitive-scaffolding.md  # Cognitive Mirror, PME, HypoCompass
│       ├── trust-calibration.md          # Evidence levels, contrastive explanations
│       ├── skill-preservation.md         # Atrophy, recovery, job crafting
│       ├── productivity-reality.md       # METR RCT, code quality signals
│       ├── reasoning-scaffolds.md        # Wolf, OODA, hypothesis testing
│       ├── reasoning-verification.md     # CoVe, Pythea
│       ├── behavioral-awareness.md       # Collaboration traps
│       ├── verification-patterns.md      # Code hygiene checklists
│       ├── kaizen-crystallization.md     # Compound learning
│       ├── writing-antipatterns.md       # Writing quality
│       └── principles-and-patterns-examples.md  # Concrete examples
├── agents/
│   └── mrwolf.md             # Structured problem solver
├── hooks/
│   ├── hooks.json            # Hook configuration
│   ├── detect-debugging-loop.sh
│   ├── detect-frustration.sh
│   └── session-start.sh      # Session transparency
├── docs/
│   └── explanation/          # Human-optimized (WHY)
│       ├── methodology.md    # Research base & design rationale
│       └── sources.md        # Full bibliography (50+ studies)
└── scripts/                  # Installation helpers
```

## Philosophy

**You're not done when it works. You're done when it's right.**

Everything you create becomes part of a system others depend on. Scaffolding, not crutches — temporary support designed to make humans more capable, not dependent.
