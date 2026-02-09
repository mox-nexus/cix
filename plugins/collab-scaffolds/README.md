# collab-scaffolds

Research-grounded scaffolds for effective human-AI collaboration.

## What This Is

Scaffolding for collaborative building — temporary support designed to be outgrown. Every scaffold is backed by research evidence from 50+ studies (CHI, PNAS, Lancet, NeurIPS, HICSS). Three skills, three agents, four hooks, aligned with the Software Craftsmanship Manifesto.

## When It Activates

- Writing code or making technical decisions
- Refactoring and code reviews
- Debugging (especially when stuck)
- Verifying claims or calibrating trust
- Any context where quality matters

## What You Get

### Skills

**building** — Engineering craft for well-crafted software:
- Building principles (compound value, complete the work, craft over speed)
- Workflows (refactoring, scaffolding, fidelity thinking, evidence before fix)
- Verification (three checks, code hygiene, test integrity)
- Advisory vs Enforced behavior mapping

**collaboration** — Human-AI partnership patterns:
- Scaffolding philosophy (Vygotsky ZPD)
- Collaboration patterns (Generation-Then-Comprehension, Task Stewardship)
- Trust calibration (evidence levels, contrastive explanations, falsification)
- Control and transparency frameworks

**problem-solving** — Structured thinking and metacognition:
- Wolf Protocol (stop → classify → route → verify)
- Metacognitive scaffolds (Cognitive Mirror, PME Friction, HypoCompass)
- Problem → Technique routing (DAC, Five Whys, OODA, Hypothesis Testing)
- Verification (CoVe, contrastive explanations)
- Iteration awareness and context health monitoring

### Agents

**Mr. Wolf** — Structured problem solver. Gets called when you're stuck, going in circles, or debugging isn't converging. Loads `problem-solving` skill.

**Duck** — Rubber duck debugging through Socratic dialogue. Helps you think through problems by asking questions, not giving answers. Loads `problem-solving` skill.

**Advocate** — Devil's advocate for verification. Challenges solutions, falsifies claims, runs CoVe on citations. Models can't self-correct without external feedback — Advocate is that feedback. Loads `problem-solving` skill.

| | Duck | Wolf | Advocate |
|---|------|------|----------|
| **Trigger** | "I need to think this through" | "I'm stuck, nothing's working" | "Is this actually right?" |
| **Mode** | Socratic — asks questions | Directive — routes to technique | Adversarial — tries to prove it wrong |
| **Goal** | You articulate → you discover | Problem classified → solved | Solution survives challenge → ship |

### Hooks

| Hook | Event | Detects | Response |
|------|-------|---------|----------|
| `detect-stuck` | PostToolUse:Bash + UserPromptSubmit | 3+ failures OR frustration language | Spawns Mr. Wolf |
| `scaffolding-cleanup-gate` | PreToolUse:Bash | Debug artifacts in commits | Blocks commit with list |
| `incomplete-refactoring-guard` | PostToolUse:Bash | Old names after rename | Directs cleanup |
| `session-start` | SessionStart | Session begins | Shows available skills |

All hooks are **suggestive** (decision: "allow" with message), never blocking — preserving user agency while nudging behavior. Opt-out: `SKIP_MRWOLF_HOOKS=1` or `SKIP_CLEANUP_HOOKS=1`.

## Structure

```
collab-scaffolds/
├── skills/
│   ├── building/                 # Engineering craft
│   │   ├── SKILL.md              # Principles, workflows, verification (< 250 lines)
│   │   └── references/           # Deep dives (7 files)
│   │       ├── verification-patterns.md
│   │       ├── principles-and-patterns-examples.md
│   │       ├── writing-antipatterns.md
│   │       ├── kaizen-crystallization.md
│   │       ├── enforcement-spectrum.md
│   │       ├── fidelity-thinking.md
│   │       └── refactoring-completeness.md
│   ├── collaboration/            # Human-AI partnership
│   │   ├── SKILL.md              # Trust, control, transparency (< 200 lines)
│   │   └── references/           # Deep dives (4 files)
│   │       ├── trust-calibration.md
│   │       ├── skill-preservation.md
│   │       ├── productivity-reality.md
│   │       └── behavioral-awareness.md
│   └── problem-solving/          # Structured thinking & metacognition
│       ├── SKILL.md              # Wolf Protocol, routing, verification (< 280 lines)
│       └── references/           # Deep dives (4 files)
│           ├── metacognitive-scaffolding.md
│           ├── reasoning-scaffolds.md
│           ├── reasoning-verification.md
│           └── iteration-limits.md
├── agents/
│   ├── mrwolf.md                 # Structured problem solver
│   ├── duck.md                   # Rubber duck (Socratic dialogue)
│   └── advocate.md               # Devil's advocate (verification)
├── hooks/
│   ├── hooks.json
│   ├── detect-stuck.sh                  # Wolf trigger (failures + frustration)
│   ├── scaffolding-cleanup-gate.sh      # Pre-commit debug artifact check
│   ├── incomplete-refactoring-guard.sh  # Post-commit old name check
│   └── session-start.sh                 # Context loading
├── docs/
│   ├── explanation/              # Human-optimized (WHY)
│   │   ├── methodology.md
│   │   └── sources.md
│   ├── how-to/                   # Human-optimized (HOW)
│   │   ├── recognize-debugging-loops.md
│   │   ├── calibrate-trust.md
│   │   ├── apply-fidelity-thinking.md
│   │   └── verify-refactoring.md
│   └── tutorials/                # Human-optimized (LEARN)
│       ├── mastery-oriented-session.md
│       ├── debugging-with-mrwolf.md
│       └── rubber-duck-with-duck.md
└── scripts/                      # Installation helpers
```

## Philosophy

**You're not done when it works. You're done when it's right.**

Everything you create becomes part of a system others depend on. Scaffolding, not crutches — temporary support designed to make humans more capable, not dependent.
