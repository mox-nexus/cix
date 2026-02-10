---
name: weaving
description: "Re-weave existing content across all three doors. Use when: content is modal-locked, explanation doesn't land, Socratic review identified gaps, content needs Door 3 ground or Door 2 constituency, need to make content wider not louder."
version: 0.1.0
---

# Weaving

> Take what exists and thread the missing doors through it. Not after it. Into it.

## When to Use

You have content that's modal-locked — strong in one or two doors, weak in others. The framework is in the craft-explanations skill. This skill is the executable method for applying it.

Typical triggers:
- Socratic review identified missing doors
- "This doesn't land" — explanation fails despite being correct
- "Too abstract" — Door 1 dominant, Door 3 missing
- "Who is this for?" — Door 2 missing
- "Just steps, no understanding" — Door 3 dominant, Door 1 missing

## The Workflow

### 1. DIAGNOSE

Identify what's present and what's missing. If Socrates hasn't run, do this yourself:

| Check | Question |
|-------|----------|
| **Door 1** | Can the principle-seeker pull their thread from any passage? |
| **Door 2** | Is there a specific constituency? Can I name who this is for? |
| **Door 3** | Can the ground-seeker find something solid at every point? |
| **Weave** | Is it woven or sequenced? (Three doors in a trench coat?) |
| **Shift** | Does the explanation cross doors at least once? |

Output: which doors are strong, which are weak, where specifically.

### 2. ANCHOR

Before changing anything, mark what already works.

- Identify passages with genuine weight — don't touch these
- Identify the entry door — what does the content lead with? Preserve that
- Identify existing dimensional shifts — these are the strongest moments

**The rule: never weaken a strong door to strengthen a weak one.** Weaving is additive threading, not redistribution.

### 3. THREAD

The core technique. For each passage that's locked in one door, thread the missing door INTO that passage.

**Threading Door 3 (Ground) into Door 1 (Principle):**

The passage states a universal truth. Drop one concrete, undeniable thing into the same breath — a specific number, a named artifact, something the reader's hands remember.

```
Before (Door 1 only):
"Communication fails when dimensional mismatch happens."

After (Door 1 + Door 3 threaded):
"Communication fails when dimensional mismatch happens — you've felt it,
the silence after a presentation where everything was correct and nothing landed."
```

The principle is intact. The ground is now woven in. The reader who needs Door 3 has something to carry.

**Threading Door 2 (Constituency) into Door 1 (Principle):**

The passage states a universal truth. Name who it's true *for* — make the abstract concrete for a specific person in a specific situation.

```
Before (Door 1 only):
"Wider encoding survives lossy compression through organizational layers."

After (Door 1 + Door 2 threaded):
"Wider encoding survives lossy compression — the engineer's insight
makes it through three layers of management because it was encoded
in principle, in trade-offs their manager cares about, and in a
working prototype the VP can see."
```

**Threading Door 1 (Principle) into Door 3 (Ground):**

The passage gives concrete steps. Thread in *why these steps and not others* — make the reason visible without interrupting the flow.

```
Before (Door 3 only):
"Run the tests. Check the coverage report. Fix failures."

After (Door 3 + Door 1 threaded):
"Run the tests — they're the only objective measure of whether your change
does what you think. Check the coverage report. Fix failures before anything else,
because a broken test is a lie you told your future self."
```

### 4. SHIFT

Check that at least one dimensional crossing happens — a moment where understanding moves from one door to another.

| Desired shift | Technique |
|---------------|-----------|
| Door 1 → Door 3 | Follow a principle with an undeniable example that makes the reader *feel* it |
| Door 3 → Door 1 | After concrete steps, surface why those steps matter — the moment "doing" becomes "understanding" |
| Door 2 → Door 3 | After naming alternatives, show what the chosen path looks like in practice |
| Door 3 → Door 2 | After showing the thing working, zoom out to who it serves and what it was chosen over |

**The test**: Can the reader point to a moment where they crossed from one kind of knowing to another?

### 5. VERIFY

Re-check the woven content:

- [ ] Strong doors preserved — nothing that worked was weakened
- [ ] Missing doors now present — not as sections, as threads in existing passages
- [ ] At least one dimensional shift — a crossing happens
- [ ] Still woven, not sequenced — no "Principle Section" / "Ground Section" bolted on
- [ ] Constituency named or clear — the reader knows who this is for
- [ ] Weight present — at least one thing that doesn't argue for itself

If verification fails, return to THREAD. Don't add sections. Re-encode.

## Threading Moves

Quick reference — the specific craft moves for threading each door:

| Thread this door | Into existing content by | Watch out for |
|------------------|------------------------|---------------|
| **Door 3** | Drop one specific, undeniable thing (number, name, sensation) | Generic examples (Door 1 in costume) |
| **Door 2** | Name the constituency, show what was chosen against | Listing options without choosing |
| **Door 1** | Surface the reason beneath the step — why this, not that | Interrupting the flow with theory |

## Anti-Patterns

| Anti-pattern | What's happening | Fix |
|--------------|------------------|-----|
| **Bolting on** | Adding a "Practical Examples" section at the end | Thread into existing passages |
| **Redistribution** | Weakening Door 1 to strengthen Door 3 | Weaving is additive, not zero-sum |
| **Door 1 in costume** | "Example: consider a hypothetical system..." | Use real names, real numbers, real weight |
| **Over-threading** | Every sentence carries all three doors explicitly | Not every sentence needs all three — every *passage* does |
| **Losing the entry** | Content no longer has a clear entry door | Preserve the lead. Thread, don't redirect. |

## Scope

Best for:
- Re-working content that's been diagnosed as modal-locked
- Editing existing docs, articles, presentations
- Preparing content after Socratic review
- Making "correct but doesn't land" explanations land

Not for:
- Writing new content from scratch (use feynman, sagan, or tufte)
- Diagnosing what's missing (use socrates)
- Choosing diagram types (use tufte / visual-communication)
