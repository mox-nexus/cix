---
name: building
description: "Engineering craft for well-crafted software. Use when: writing code, refactoring, reviewing, making implementation decisions, or completing any work where build quality matters."
---

# Building

**Signatory #37451** — Software Craftsmanship Manifesto — 10/01/2026

- **Well-crafted software**, not just working software
- **Steadily adding value**, not just responding to change

**You're not done when it works. You're done when it's right.**

### Advisory vs Enforced

This skill file is **advisory** — it competes with training patterns and can lose under pressure. Hooks provide **enforcement** for the most critical behaviors:

| Behavior | Hook | Event |
|----------|------|-------|
| Debug artifacts in commits | scaffolding-cleanup-gate | PreToolUse:Bash |
| Incomplete refactoring | incomplete-refactoring-guard | PostToolUse:Bash |
| Debugging loops / frustration | detect-stuck | PostToolUse:Bash + UserPromptSubmit |

See [enforcement-spectrum.md](references/enforcement-spectrum.md) for why advisory alone fails.

---

## Principles

Each prevents a form of self-deception:

| Principle | What You're Fooling Yourself About |
|-----------|-----------------------------------|
| **Compound Value** | "I solved it" — but made the next problem harder |
| **Pit of Success** | "I documented it" — but docs get ignored |
| **Mistake-Proofing** | "It works" — but the error surfaces downstream |
| **Complete the Work** | "It's done" — but artifacts remain |
| **Craft Over Speed** | "We shipped" — but shipped debt |
| **Invariants** | "We validate" — but validation can be bypassed |

### Compound Value

Every change should make the next easier.

The codebase outlives any single task. Quick fixes, workarounds, special cases compound cost. Clean abstractions, complete refactoring, single source of truth compound value.

**Before acting:** Does this make the next change easier or harder?

### Pit of Success

Make the right thing the only obvious path.

Don't rely on documentation or willpower. Structure code so mistakes are hard and correct behavior is natural.

**The test:** Could someone unfamiliar fall into the right pattern?

### Mistake-Proofing

Catch errors where they originate.

Validate assumptions early. Check tool outputs before acting. Surface uncertainty at decision points.

**The test:** If this goes wrong, where will we find out?

### Complete the Work

Don't leave things half-done.

If you start a refactor, complete it. If you fix a bug, fix the pattern. If you rename something, rename it everywhere. If you remove a feature, remove all traces — dead code, unused imports, orphaned tests, stale comments.

**The test:** If artifacts of old state remain, the work isn't done.

### Craft Over Speed

The only way to go fast is to go well.

Cutting corners appears faster short-term. Technical debt compounds. Context compaction exists — there is no reason to rush at the expense of quality.

### Think in Invariants

Make violations impossible.

Parse, don't validate. Encode guarantees in types. Make illegal states unrepresentable.

**The test:** Can the wrong thing even be expressed?

---

## Workflows

### Refactoring

Refactoring is not done until every trace of old state is gone.

**Before starting:**
1. Understand what exists — read the code, trace dependencies
2. Plan the scope — what changes, what doesn't
3. Checkpoint with the human if scope is large

**During refactoring:**
1. Make one logical change at a time
2. After each change, search for all remaining references to old state
3. Update tests to reflect new structure (don't just make them pass)

**After refactoring — the cleanup sweep:**

| Check | Command/Action |
|-------|---------------|
| Dead code | Search for unused functions, classes, variables |
| Stale imports | Remove imports of deleted/renamed modules |
| Orphaned tests | Tests that test removed functionality |
| Stale comments | Comments referencing old names, old behavior |
| Config references | Build configs, CI files, scripts with old paths |
| Documentation | READMEs, CLAUDE.md, inline docs with old names |

**The test:** `grep` for the old name. Zero hits means done.

### Scaffolding Changes

For multi-step changes, build incrementally:

1. **Foundation** — Get the structure right first (types, interfaces, directory layout)
2. **Implementation** — Fill in behavior one component at a time
3. **Integration** — Wire components together
4. **Cleanup** — Remove temporary scaffolding, debug code, TODO comments

**Critical:** Step 4 is not optional. Temporary code left in place becomes permanent cruft.

### Planning Before Implementation

Understand before building. The cost of rework always exceeds the cost of planning.

**Before writing code:**
1. Read the relevant existing code
2. Identify what changes and what stays
3. Consider edge cases and failure modes
4. For non-trivial tasks, propose the approach first

**Signals you're jumping ahead:**
- Writing code without reading what exists
- Making changes beyond what was asked
- Assuming requirements instead of clarifying
- "While I'm here, I'll also..." — scope creep

### Fidelity Thinking

Not everything needs to be finished at the same level. Build incrementally at increasing fidelity.

| Level | What It Means | When It's Enough |
|-------|---------------|------------------|
| **Dirt road** | Happy path works | Spike, prototype, exploration |
| **Cobble road** | Handles edge cases, has tests | Internal tool, low-stakes feature |
| **Tarmac** | Production-hardened, observable | User-facing, high-stakes |

State the target fidelity before building. "This is a dirt road — we'll pave it if it proves valuable." The trap is jumping straight to tarmac for everything (wasted effort) or stopping at dirt road for everything (accumulated debt).

See [fidelity-thinking.md](references/fidelity-thinking.md).

### Evidence Before Fix

When debugging, gather evidence before writing fixes.

1. **Read** the relevant code and error context
2. **Check** actual runtime data (logs, stack traces, state)
3. **Hypothesize** based on evidence, not intuition
4. **Then** write the fix

Speculative fixes without evidence waste time and introduce new bugs.

---

## Verification

You're not done when it works. You're done when it's right.

### Three Checks

| Check | Question | If No |
|-------|----------|-------|
| **Task** | Does it work? | Not done |
| **Project** | Is the codebase better? | Not done |
| **Compound** | Is the next change easier? | Reconsider |

### Code Hygiene

No dead code, no unused imports, no stale comments, no debug statements. Renames completed fully. **Enforced by hooks:** scaffolding-cleanup-gate (pre-commit) and incomplete-refactoring-guard (post-commit).

### Test Integrity

Fixed the code, not the test. Tests verify requirements. New bugs get regression tests.

See [verification-patterns.md](references/verification-patterns.md) and [refactoring-completeness.md](references/refactoring-completeness.md).

---

## Anti-Patterns

| Trap | Why It Happens | Cost |
|------|----------------|------|
| **Jumping ahead** | Eagerness to produce | Wrong solution, rework, scope creep |
| **Incomplete refactoring** | "Good enough" feels done | Cruft accumulates, confusion grows |
| **Dead code left behind** | "Might need it later" | Noise obscures signal |
| **Context window optimization** | Perceived token pressure | Shortcuts compound into tech debt |
| **Task over project** | Optimizing for "done" | Codebase degrades |
| **Faking tests** | Pressure to make green | False confidence |
| **Backwards-compat hacks** | Fear of breaking | Complexity grows |
| **Over-engineering** | "While I'm here..." | Scope creep, unwanted changes |

**Enforced by hooks:** Scaffolding cleanup (pre-commit), incomplete refactoring (post-commit).

---

## Crystallization

Each session can leave the system smarter. After completing work, ask: What approach worked? What indicated it was right? Where else might this apply?

Crystallize principles that generalize and decision frameworks that transfer. Skip one-off solutions and things already well-known.

See [kaizen-crystallization.md](references/kaizen-crystallization.md).

---

## References

| Need | Load |
|------|------|
| Code verification | [verification-patterns.md](references/verification-patterns.md) |
| Principles examples | [principles-and-patterns-examples.md](references/principles-and-patterns-examples.md) |
| Writing quality | [writing-antipatterns.md](references/writing-antipatterns.md) |
| Crystallization | [kaizen-crystallization.md](references/kaizen-crystallization.md) |
| Enforcement spectrum | [enforcement-spectrum.md](references/enforcement-spectrum.md) |
| Fidelity thinking | [fidelity-thinking.md](references/fidelity-thinking.md) |
| Refactoring completeness | [refactoring-completeness.md](references/refactoring-completeness.md) |
