# Enforcement Spectrum

Decision frameworks for choosing between advisory, suggestive, and blocking enforcement.

## Contents

- [The Problem: Advisory Alone Fails](#the-problem-advisory-alone-fails)
- [The Spectrum](#the-spectrum)
- [Advisory Level](#advisory-level)
- [Suggestive Level](#suggestive-level-most-hooks)
- [Blocking Level](#blocking-level-rare)
- [Design Principles for Hooks](#design-principles-for-hooks)
- [The Enforcement Ladder](#the-enforcement-ladder)
- [Current collab-scaffolds Enforcement Map](#current-collab-scaffolds-enforcement-map)

---

## The Problem: Advisory Alone Fails

SKILL.md and CLAUDE.md instructions are advisory — they compete with training patterns.

**Under pressure, training overrides instructions:**
- Long context
- Complex debugging
- User urgency
- After context compaction

### Evidence

| Source | Observation |
|--------|-------------|
| GitHub #23833 | Speculative execution despite explicit instructions |
| GitHub #21119 | "CLAUDE.md instructions are basically advisory. They compete with training. Hooks are the only reliable enforcement." |
| GitHub #21119 | "Training data creates strong baseline behaviors that explicit instructions can redirect but not eliminate." |
| GitHub #20401 | 3 escalating violations of same instruction in one session |

### Degradation Pattern

1. Works in early context
2. Degrades as context fills
3. Often ignored after compaction
4. Completely fails under time pressure or debugging loops

**Conclusion:** Advisory is for philosophy. Hooks are for behavior.

---

## The Spectrum

Three levels of behavioral guidance, from weakest to strongest.

| Level | Mechanism | Reliability | Use For |
|-------|-----------|-------------|---------|
| **Advisory** | SKILL.md, CLAUDE.md | Low — loses under pressure | Principles, philosophy, guidelines |
| **Suggestive** | Hooks with message, decision: "allow" | Medium — fires every time but can be overridden | Pattern detection, nudges, reminders |
| **Blocking** | Hooks with decision: "block" | High — prevents action | Destructive operations, security gates |

---

## Advisory Level

**Mechanism:** SKILL.md content, CLAUDE.md instructions

**Effective for:**
- Establishing philosophy
- Explaining WHY
- Teaching reasoning frameworks
- General principles

**Fails for:**
- Enforcing specific behaviors under pressure
- Preventing harmful patterns
- Time-critical checks

**Degradation pattern:**
- Works in early context
- Degrades as context fills
- Often ignored after compaction

**Example:**
```markdown
## Compound Value

Every change should make the next change easier.

Quick fixes, workarounds, special cases compound cost.
```

This teaches the principle. It doesn't enforce the behavior.

---

## Suggestive Level (Most Hooks)

**Mechanism:** Hooks that fire every time with a message, decision: "allow"

**Most collab-scaffolds hooks are suggestive** — they preserve agency while creating strong behavioral nudges.

**Pattern:** Directive language that causes action without blocking.

```json
{
  "decision": "allow",
  "message": "🐺 PATTERN DETECTED. You MUST now: 1) ... 2) ..."
}
```

### Why Directive Language

Creates stronger behavioral nudge without blocking user flow.

**Comparison:**

| Language | Effect |
|----------|--------|
| "Consider gathering evidence first." | Often ignored under pressure |
| "You MUST now: 1) STOP 2) Gather evidence 3) Form hypothesis" | Creates action sequence |

### When to Use

- Debugging loops
- Quality gates
- Fidelity checks
- Pattern detection (frustration, scaffolding artifacts)
- Metacognitive checkpoints

### Current Suggestive Hooks

| Hook | Trigger | Language Pattern |
|------|---------|------------------|
| `detect-debugging-loop` | 3 consecutive Bash failures | "You MUST now: 1) Tell user 2) Spawn mrwolf" |
| `detect-frustration` | Frustration phrases in user prompt | "You MUST now: 1) Acknowledge 2) Spawn mrwolf" |
| `speculative-fix-prevention` | Edit/Write during active debugging (2+ failures) | "STOP and gather evidence first: 1) ... 2) ... 3) ..." |
| `scaffolding-cleanup-gate` | Debug artifacts before commit | "Clean up before committing: [list]" |
| `incomplete-refactoring-guard` | Old names still in repo after rename commit | "The refactoring isn't done until grep returns zero hits." |
| `fidelity-checkpoint` | Every 25 interactions | "State the target fidelity before continuing." |

---

## Blocking Level (Rare)

**Mechanism:** Hooks with decision: "block" or exit code 2

**Prevents the action from executing.**

Use sparingly: breaks flow, can frustrate users.

### When to Use

- Security-critical paths
- Destructive operations
- Credential exposure
- Data loss prevention

### Note

**collab-scaffolds currently has no blocking hooks** — all are suggestive by design, preserving agency.

Blocking is reserved for:
- Hardcoded credentials in commits (should be blocked, not warned)
- Destructive git operations without confirmation
- Production deployment without tests passing

---

## Design Principles for Hooks

### 1. Always Exit 0

Non-zero exit codes break the hook system.

```bash
# Correct
echo '{"decision": "allow"}'
exit 0

# Wrong
echo '{"decision": "allow"}'
exit 1  # Breaks the hook chain
```

### 2. Always Provide Opt-Out

Every hook checks environment variable.

```bash
if [[ "${SKIP_MRWOLF_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi
```

**Naming convention:** `SKIP_<CATEGORY>_HOOKS=1`

- `SKIP_MRWOLF_HOOKS` — debugging loop, frustration detection
- `SKIP_EVIDENCE_HOOKS` — speculative fix prevention
- `SKIP_CLEANUP_HOOKS` — scaffolding cleanup gate
- `SKIP_REFACTOR_HOOKS` — incomplete refactoring guard
- `SKIP_FIDELITY_HOOKS` — fidelity checkpoint

### 3. Use Portable Paths

`${CLAUDE_PLUGIN_ROOT}` for hook scripts and resources.

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/detect-debugging-loop.sh"
}
```

### 4. State Files in /tmp with $PPID

Session-scoped state using parent process ID.

```bash
STATE_FILE="/tmp/claude-mrwolf-state-${PPID:-$$}"
```

This ensures:
- State persists across tool calls in same session
- Different sessions don't interfere
- Cleanup happens when session ends

### 5. Language Style by Hook Type

| Hook Type | Language | Example |
|-----------|----------|---------|
| **Action-triggering** (pattern detection) | Directive | "You MUST now: 1) ... 2) ..." |
| **Validation** (pre/post checks) | Suggestive | "Consider X instead. Clean up Y before Z." |

### 6. Timeouts

| Check Type | Timeout |
|------------|---------|
| Simple pattern matching | 5s |
| Git operations | 10s |
| Network calls | 15s |

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/detect-debugging-loop.sh",
  "timeout": 5
}
```

---

## The Enforcement Ladder

Start advisory. Escalate only when behavior consistently violated.

### Decision Tree

```
Is this behavior critical to quality?
├─ No → Don't enforce, maybe mention in docs
└─ Yes
    ├─ Does it happen rarely? → Advisory (SKILL.md)
    ├─ Does it happen under pressure? → Suggestive hook
    └─ Could it cause harm/data loss? → Blocking hook
```

### Escalation Process

1. **Add to SKILL.md (advisory)** — first attempt
   - Explain WHY, teach the principle
   - Works for most behaviors

2. **Add hook with suggestive message** — if advisory fails
   - Fires every time, can't be ignored
   - Preserves agency (decision: "allow")
   - Use directive language for action-triggering

3. **Add hook with blocking decision** — only for critical safety
   - Prevents the action
   - Reserve for security, data loss, credentials

### Example: Scaffolding Artifacts

1. **Advisory (first):** SKILL.md teaches "Complete the Work — remove scaffolding"
2. **Fails:** Claude still commits debug artifacts under pressure
3. **Escalate:** `scaffolding-cleanup-gate` hook warns before commit
4. **Could escalate further:** Block commits with artifacts (not done — preserves agency)

---

## Current collab-scaffolds Enforcement Map

### SessionStart

| Hook | Purpose | Decision | Opt-out |
|------|---------|----------|---------|
| `session-start.sh` | Session transparency (logging location) | allow | None |

### PreToolUse: Bash

| Hook | Purpose | Decision | Opt-out |
|------|---------|----------|---------|
| `scaffolding-cleanup-gate.sh` | Catch debug artifacts before commit | allow (suggestive) | SKIP_CLEANUP_HOOKS |

### PostToolUse: Bash

| Hook | Purpose | Decision | Opt-out |
|------|---------|----------|---------|
| `detect-debugging-loop.sh` | Trigger Mr. Wolf after 3 failures | allow (action-triggering) | SKIP_MRWOLF_HOOKS |
| `incomplete-refactoring-guard.sh` | Catch stale references after rename | allow (suggestive) | SKIP_REFACTOR_HOOKS |

### PostToolUse: Write\|Edit

| Hook | Purpose | Decision | Opt-out |
|------|---------|----------|---------|
| `speculative-fix-prevention.sh` | Prevent editing during debugging without evidence | allow (action-triggering) | SKIP_EVIDENCE_HOOKS |

### UserPromptSubmit

| Hook | Purpose | Decision | Opt-out |
|------|---------|----------|---------|
| `detect-frustration.sh` | Trigger Mr. Wolf on frustration phrases | allow (action-triggering) | SKIP_MRWOLF_HOOKS |
| `fidelity-checkpoint.sh` | Metacognitive fidelity check every 25 interactions | allow (suggestive) | SKIP_FIDELITY_HOOKS |

### Summary Statistics

- **Total hooks:** 7
- **Advisory level:** 0 (philosophy lives in SKILL.md)
- **Suggestive level:** 7 (all current hooks)
- **Blocking level:** 0 (preserving agency by design)
- **Action-triggering:** 3 (Mr. Wolf triggers, speculative fix)
- **Validation/reminder:** 4 (cleanup, refactoring, fidelity)
