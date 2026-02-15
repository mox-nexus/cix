# Refactoring Completeness

A checklist for Claude when refactoring. Load this when doing renames, moves, deletions, or structural changes.

## Contents

- [The Research](#the-research)
- [Category Solving vs Instance Solving](#category-solving-vs-instance-solving)
- [The Post-Refactor Checklist](#the-post-refactor-checklist)
- [Common Failure Patterns](#common-failure-patterns)
- [Hook Enforcement](#hook-enforcement)

---

## The Research

AI-assisted refactoring is systematically incomplete:

| Finding | Source | What It Means |
|---------|--------|---------------|
| Refactoring dropped from 24.1% to 9.5% | GitClear 2025 (211M lines) | AI writes new code, doesn't restructure |
| Moved code decreased 17.3% | GitClear 2025 | AI leaves files where they are |
| Copy-paste increased 4x | GitClear 2025 | AI duplicates instead of extracting |
| 63% of AI refactorings break code | CodeScene 2025 | Regressions, dead references, incomplete renames |
| 2x redundancy score | MSR 2026 | AI creates duplication humans would eliminate |
| 37% more unused constructs | Cotroneo ISSRE 2025 | Dead code, unreachable branches accumulate |

**The pattern:** AI solves the immediate instance without solving the category.

---

## Category Solving vs Instance Solving

The core failure: AI addresses the specific request without addressing the system-wide implications.

| Instance Solving (Wrong) | Category Solving (Right) |
|--------------------------|--------------------------|
| Rename this function | Rename + update all callers + grep for string references |
| Move this file | Move + update imports + fix relative paths + update configs |
| Delete this feature | Delete code + tests + config + docs + CI references |
| Fix this bug | Fix + fix the pattern that enabled it |
| Extract this logic | Extract + remove duplication + update call sites |

**Always solve the category.** If you renamed something, grep for the old name. If you deleted something, grep for references to it.

---

## The Post-Refactor Checklist

Run this after every refactoring operation. Each item is a grep or verification command.

### 1. Dead Code Sweep

Search for functions/classes/variables no longer called:

```bash
# Find function definitions that may be orphaned
rg "def function_name|function function_name|fn function_name"

# Check if anything imports or calls it
rg "function_name" --type-not test

# For classes
rg "class ClassName"
rg "ClassName\(" --type-not test
```

What to look for:
- Functions defined but never called
- Classes defined but never instantiated
- Utility functions used by deleted code
- Imports of deleted modules
- Code commented out "just in case"

**Action:** Delete dead code. Don't leave it "in case we need it later."

### 2. Import/Dependency Cleanup

Update import paths and remove stale dependencies:

```bash
# Find imports of the old module name
rg "import.*old_name|from old_name"

# Find imports of moved files
rg "import.*old/path"

# Check for unused imports (language-specific tools)
# Python: pylint --disable=all --enable=unused-import
# Rust: cargo clippy
# TypeScript: eslint no-unused-vars
```

What to check:
- Import paths for moved files
- Imports of deleted modules
- Circular dependencies from restructuring
- package.json / Cargo.toml / requirements.txt if modules were deleted

**Action:** Update all import paths. Remove unused imports.

### 3. Test Alignment

Tests must follow the code they test:

```bash
# Find tests referencing old names
rg "old_function_name" --glob "*test*"
rg "old_function_name" --glob "*spec*"

# Find test files for deleted features
find . -name "*old_feature*test*"
```

What to verify:
- Tests still test the right behavior (not just pass)
- Moved tests follow moved code
- Deleted feature tests are deleted
- Test helpers/fixtures reference current structure
- Mock data reflects new structure
- Test imports use new paths

**Action:** Move/rename/delete tests to match code changes.

### 4. Configuration & CI

Build systems and scripts reference paths:

```bash
# Check build configs
rg "old_path|old_name" --glob "*.json" --glob "*.toml" --glob "*.yaml"

# Check CI configs
rg "old_path|old_name" .github/ .gitlab-ci.yml

# Check scripts
rg "old_path|old_name" --glob "*.sh" --glob "Makefile" --glob "justfile"
```

What to update:
- Build configs (webpack, vite, tsconfig, Cargo.toml)
- CI pipelines (.github/workflows, .gitlab-ci.yml)
- Scripts (.sh, Makefile, justfile)
- Environment variable references (.env files)
- Docker configs referencing paths

**Action:** Update all config references to new structure.

### 5. Documentation

Documentation must match current reality:

```bash
# Check README files
rg "old_name|old_path" --glob "*README*"

# Check Claude instructions
rg "old_name|old_path" --glob "*CLAUDE*"

# Check inline comments
rg "old_name" --type rust --type python --type typescript
```

What to update:
- README files with old examples
- CLAUDE.md with old paths/names
- Inline code comments referencing old behavior
- API documentation
- Architecture diagrams
- Migration guides

**Action:** Update all documentation to current state.

---

## The Zero-Hits Test

For each renamed/moved/deleted item, run:

```bash
git grep "old_name"
```

**Zero hits** = refactoring complete
**Any hits** = more work required

Go through each hit and either:
- Update it to the new name/path
- Delete it if it's dead code
- Verify it's intentional (historical references, changelogs)

---

## Common Failure Patterns

| Pattern | Symptom | Prevention |
|---------|---------|-----------|
| **Rename without grep** | Runtime errors from old references | Always grep after rename |
| **Move without import update** | Import errors | Run tests before committing |
| **Delete without cascade** | Orphaned tests, stale config | Grep for the deleted name |
| **Partial migration** | Old way and new way coexist | Complete the migration or revert |
| **Copy-paste refactoring** | Two copies that diverge | Extract shared abstraction instead |
| **String references missed** | Error messages, logs have old names | Grep for strings too |
| **Test "fixes" instead of updates** | Tests pass but verify wrong behavior | Tests should fail when behavior changes |

---

## Hook Enforcement

Two hooks enforce refactoring completeness:

### incomplete-refactoring-guard

**Triggers:** PostToolUse:Bash after git commits with file renames

**What it does:**
- Detects file renames in the commit
- Greps for old filenames in the codebase
- Warns if references remain

**What it catches:**
- Renamed file, old imports exist
- Moved file, old paths in configs
- File renamed but string references remain

**What it doesn't catch:**
- Semantic renames (function/variable names)
- Dead code that was never referenced
- Config values using strings rather than imports

### scaffolding-cleanup-gate

**Triggers:** PreToolUse:Bash before git commits

**What it does:**
- Checks for debug artifacts (console.log, TODO, debugger, breakpoint)
- Blocks commit if found

**What it catches:**
- Debug print statements
- Temporary breakpoints
- TODO comments from refactoring
- Commented-out code "for reference"

**What it doesn't catch:**
- Dead code (definitions not called)
- Stale imports
- Outdated documentation

**Manual verification covers what hooks miss.**

---

## Refactoring Decision Flow

```
┌─────────────────────────┐
│ Plan the refactoring    │
│ - What changes?         │
│ - What stays?           │
│ - What's the scope?     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Make the change         │
│ - Rename / Move / Delete│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Run the checklist       │
│ 1. Dead code            │
│ 2. Imports              │
│ 3. Tests                │
│ 4. Config               │
│ 5. Docs                 │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Zero-hits test          │
│ git grep "old_name"     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Zero hits? ────Yes────► Done
│      │                  │
│      No                 │
│      │                  │
│      ▼                  │
│ Fix remaining hits      │
│ Loop back to test       │
└─────────────────────────┘
```

---

## When Refactoring is Done

Refactoring is complete when:

1. **Zero-hits test passes** — old name produces zero grep results
2. **Tests pass** — and test the right behavior
3. **No dead code** — every definition is used
4. **No stale imports** — every import resolves
5. **Config updated** — build/CI/scripts use new structure
6. **Docs current** — README/comments reflect reality

If any item is incomplete, the refactoring isn't done.
