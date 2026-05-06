# Tutorial: Build a Code Review Skill from Scratch

Build a working Claude Code skill in under 20 minutes. By the end, you'll have a `code-review` skill installed in a plugin that activates when users ask for code reviews and teaches Claude your team's review patterns.

---

## Contents

- [Prerequisites](#prerequisites)
- [Step 1: Create the Plugin Structure](#step-1-create-the-plugin-structure)
- [Step 2: Write the Description](#step-2-write-the-description)
- [Step 3: Write the SKILL.md Body](#step-3-write-the-skillmd-body)
- [Step 4: Add a Reference File](#step-4-add-a-reference-file)
- [Step 5: Add Human Documentation](#step-5-add-human-documentation)
- [Step 6: Test Activation](#step-6-test-activation)
- [Step 7: Run the Evaluator](#step-7-run-the-evaluator)
- [What You Built](#what-you-built)

---

## Prerequisites

- Claude Code installed and working
- A project with a `.claude/` directory
- ~20 minutes

---

## Step 1: Create the Plugin Structure

Create the directory structure for your plugin:

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills/code-review/references
mkdir -p my-plugin/docs/explanation
```

Create `my-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Team conventions and workflows. Use when: user asks about code review, team patterns, or project conventions.",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT"
}
```

Your directory now looks like:

```
my-plugin/
  .claude-plugin/
    plugin.json
  skills/
    code-review/
      references/
  docs/
    explanation/
```

---

## Step 2: Write the Description

Create `my-plugin/skills/code-review/SKILL.md` and start with the frontmatter. This is the part that controls when your skill activates.

```yaml
---
name: code-review
description: "Code review patterns for pull requests. Use when: user asks to 'review this code', 'check this PR', 'look at my changes', 'review before merge', or mentions 'code quality'."
---
```

Two things to get right here:

1. **Plain language** -- describe what the skill does in words a user would understand, not implementation jargon.
2. **"Use when:" triggers** -- list actual phrases users type. Think about how YOU ask for code reviews. "Review this PR" is realistic. "Execute static analysis pipeline" is not.

---

## Step 3: Write the SKILL.md Body

Add the body below the frontmatter. This is what Claude reads when the skill activates.

```markdown
---
name: code-review
description: "Code review patterns for pull requests. Use when: user asks to 'review this code', 'check this PR', 'look at my changes', 'review before merge', or mentions 'code quality'."
---

# Code Review

Review code for problems that tests and linters miss: design issues, 
maintainability traps, and assumptions that will break later.

## Review Priorities

Not all issues are equal. Prioritize by impact:

| Priority | Category | Examples |
|----------|----------|---------|
| **Blocking** | Correctness, security | Race conditions, SQL injection, data loss |
| **Important** | Design, maintainability | God functions, leaky abstractions, missing error handling |
| **Minor** | Style, naming | Inconsistent naming, unclear variable names |

Review blocking issues first. Don't bury a security problem under 15 naming suggestions.

## What to Look For

### The questions that catch real bugs

- **Does the change do what the commit message says?** Mismatches between intent and implementation are the most common bug source.
- **What happens at the boundaries?** Empty inputs, nil values, max-size payloads, concurrent access. Most code works for the happy path. Boundaries are where bugs live.
- **Would you understand this in 6 months?** If a function needs a comment to explain what it does, it probably needs a better name or a simpler design instead.
- **What's not tested?** The untested code path is the one that will break in production.

### What NOT to spend time on

- Formatting (that's what formatters are for)
- Style preferences with no functional impact
- Bikeshedding on naming when the current name is clear enough
- Suggestions that would require a major refactor unrelated to the PR's purpose

## Review Format

Present findings in a structured table:

| # | Severity | File:Line | Issue | Suggestion |
|---|----------|-----------|-------|------------|

End with a one-paragraph summary: what the PR does well, what needs attention, and whether it's ready to merge.

## Gotchas

- **Review the PR, not the codebase.** Stay scoped to the diff. "While you're here, you should also fix..." is a different task.
- **Name the risk, not just the pattern.** "This could cause a race condition" is better than "This isn't thread-safe" -- it tells the author what might actually go wrong.
- **One approval with findings > zero response.** If the PR is good with minor issues, approve with comments. Don't block on style.

## Limitations

- This skill teaches review patterns. It does not run static analysis, linters, or tests.
- Automated tools catch syntax and formatting. This skill focuses on what automation misses.

## References

| Need | Load |
|------|------|
| Security-specific review patterns | [security-review.md](references/security-review.md) |
```

Notice what's NOT in this skill:

- No explanation of what a code review is (Claude knows)
- No tutorial on how to read a diff (Claude knows)
- No list of every possible code smell (that's a textbook, not a skill)

The skill adds value through the prioritization framework, the specific questions, and the gotchas -- things that reflect real-world judgment.

---

## Step 4: Add a Reference File

Create `my-plugin/skills/code-review/references/security-review.md`:

```markdown
# Security Review Patterns

Patterns for reviewing security-sensitive code. Load this reference 
when a PR touches authentication, authorization, input handling, 
or data storage.

---

## Contents

- [Input Handling](#input-handling)
- [Authentication Changes](#authentication-changes)
- [Data Storage](#data-storage)

---

## Input Handling

Every input is hostile until validated.

| Check | Why |
|-------|-----|
| Is user input used in SQL queries? | SQL injection |
| Is user input rendered in HTML? | XSS |
| Is user input used in file paths? | Path traversal |
| Is user input used in shell commands? | Command injection |
| Are file uploads validated (type, size)? | Resource exhaustion, malware |

If input validation happens at the handler level only, flag it. 
Validation should happen at the boundary where data enters the system, 
not scattered across business logic.

## Authentication Changes

| Check | Why |
|-------|-----|
| Are passwords hashed with bcrypt/argon2? | Weak hashing = breach |
| Are tokens time-limited? | Stolen tokens = permanent access |
| Is the session invalidated on password change? | Old sessions persist |
| Are auth errors generic? | "Invalid email" leaks user existence |

## Data Storage

| Check | Why |
|-------|-----|
| Are secrets in environment variables, not code? | Committed secrets = breach |
| Is PII encrypted at rest? | Compliance, breach mitigation |
| Are database credentials scoped to minimum privilege? | Blast radius reduction |
| Are backups encrypted? | Backups are a common breach vector |
```

This reference loads only when Claude needs it -- during security-focused reviews. It stays out of the token budget for regular code reviews.

---

## Step 5: Add Human Documentation

Create `my-plugin/docs/explanation/code-review.md`:

```markdown
# Why This Code Review Skill Exists

## The Problem

Claude already knows how to review code. But without guidance, it 
tends toward two failure modes:

1. **Exhaustive but unhelpful** -- flags every style issue, buries 
   the real problems in noise.
2. **Polite but toothless** -- "This looks good! One minor suggestion..." 
   when there's a race condition on line 42.

## Design Decisions

### Priority ordering over completeness

The skill prioritizes by severity (blocking > important > minor) 
because a review that finds 3 real issues is worth more than one that 
finds 30 style nits.

### Questions over rules

"Does the change do what the commit message says?" works across every 
language and framework. "Check for null pointer dereference" is 
language-specific and Claude handles it anyway.

### Scoped to the diff

"Review the PR, not the codebase" prevents scope creep. It's tempting 
to fix everything you see, but a review that suggests a major refactor 
unrelated to the PR is a review that gets ignored.
```

This file is for human maintainers. It explains the thinking behind the skill's design. If someone asks "why does this skill ignore formatting issues?" the answer is here, not buried in the SKILL.md.

---

## Step 6: Test Activation

Install your plugin by adding it to your project's `.claude/settings.json` or use `claude plugin add`. Then test with real prompts:

**Should activate:**
- "Review this PR for me"
- "Can you check my changes before I push?"
- "Look at this code and tell me if anything is wrong"

**Should NOT activate:**
- "Write a function that sorts a list"
- "Help me set up my database"
- "What does this error mean?"

If the skill activates on the wrong prompts, tighten the description triggers. If it misses prompts it should handle, add more trigger phrases.

---

## Step 7: Run the Evaluator

If you have the `craft-extensions` plugin installed, run the evaluator:

```
"Evaluate my-plugin"
```

The evaluator checks 9 quality gates. For a first skill, pay attention to these:

| Gate | What it checks | Your skill should... |
|------|---------------|---------------------|
| Content Quality | Does this add value beyond what Claude knows? | Teach prioritization and judgment, not syntax |
| Activation | Does the description trigger correctly? | Have specific "Use when:" phrases |
| Expert Value | Would an experienced reviewer learn something? | Focus on non-obvious patterns |
| Content Efficiency | Is every line earning its token cost? | Skip basics, focus on gotchas |

If you get **NEEDS WORK**, run the optimizer:

```
"Optimize my-plugin based on the evaluation"
```

If you get **PASS** (>= 24/27), ship it.

---

## What You Built

```
my-plugin/
  .claude-plugin/
    plugin.json
  skills/
    code-review/
      SKILL.md                  # Core skill (< 500 lines)
      references/
        security-review.md      # Loaded on demand
  docs/
    explanation/
      code-review.md            # Human docs (why, not what)
```

Your skill has:

- **Progressive disclosure**: metadata (always loaded) -> SKILL.md (when activated) -> references (on demand). Token-efficient.
- **Motivation over mandate**: teaches Claude the reasoning behind review patterns, not just rules to follow.
- **Appropriate degrees of freedom**: high freedom for review judgment ("consider", "look for"), structured format for output.
- **Two-audience docs**: SKILL.md is optimized for Claude. `docs/explanation/` is optimized for humans.

### Adapt it

This tutorial used code review as the example, but the structure works for any domain:

- Replace the review priorities with your domain's decision framework
- Replace the questions with your domain's non-obvious patterns
- Replace the gotchas with your domain's hard-won lessons
- Add references for specialized sub-topics

The value is always in the same place: judgment that Claude doesn't have by default, structured so it loads efficiently.
