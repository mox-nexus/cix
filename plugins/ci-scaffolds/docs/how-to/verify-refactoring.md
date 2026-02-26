# How to Verify Refactoring is Complete

AI-assisted refactoring is systematically incomplete. Research shows significant declines in refactoring activity since AI adoption — GitClear (2025) found an 8x increase in code duplication and substantial reduction in refactoring work. This guide shows you how to verify your changes are actually done.

## What the Hook Detects

The `incomplete-refactoring-guard.sh` hook runs after git commits that rename files:
- Extracts old basenames from renamed files
- Searches the codebase for remaining references
- Warns when old names still exist

It catches what you forget: renamed files with stale imports, moved modules with old paths in configs, and string references in error messages.

## The Core Problem: Instance vs Category Solving

AI typically solves the specific request without addressing system-wide implications:

**Instance solving (wrong):**
- Rename this function

**Category solving (right):**
- Rename function
- Update all callers
- Grep for string references
- Update tests
- Fix documentation

Always solve the category. If you renamed something, every reference must change.

## The Post-Refactor Checklist

Run these checks after every rename, move, or deletion.

### 1. Zero-Hits Test

For each old name, verify it's gone:

```bash
git grep "old_function_name"
```

Zero hits means you're done. Any hits require action:
- Update to new name
- Delete if it's dead code
- Verify if it's intentional (changelog, migration notes)

### 2. Check Imports

Find stale import paths:

```bash
# Python
rg "import.*old_name|from old_name"
rg "import.*old/path"

# JavaScript/TypeScript
rg "from ['\"].*old_name"
rg "require\(['\"].*old_name"

# Rust
rg "use .*old_name"
```

Update all import statements to new paths. Remove unused imports.

### 3. Find Orphaned Tests

Tests must follow the code they test:

```bash
# Find tests referencing old names
rg "old_function_name" --glob "*test*"
rg "old_function_name" --glob "*spec*"

# Find test files for deleted features
find . -name "*old_feature*test*"
```

Move tests when code moves. Rename tests when code renames. Delete tests when features delete.

Tests that pass but verify wrong behavior are worse than failing tests.

### 4. Scan Configuration Files

Build systems reference paths directly:

```bash
# Check build configs
rg "old_path|old_name" --glob "*.json" --glob "*.toml" --glob "*.yaml"

# Check CI configs
rg "old_path|old_name" .github/ .gitlab-ci.yml

# Check scripts
rg "old_path|old_name" --glob "*.sh" --glob "Makefile"
```

Update:
- Build configs (webpack.config.js, vite.config.ts, Cargo.toml)
- CI pipelines (.github/workflows, .gitlab-ci.yml)
- Shell scripts and Makefiles
- Environment files (.env, .env.example)
- Docker configs (Dockerfile, docker-compose.yml)

### 5. Update Documentation

Documentation must match current reality:

```bash
# Check README files
rg "old_name|old_path" --glob "*README*"

# Check project instructions
rg "old_name|old_path" --glob "*CLAUDE*"

# Check inline comments
rg "old_name" --type rust --type python --type typescript
```

Update:
- README examples and paths
- CLAUDE.md project instructions
- Inline code comments
- API documentation
- Architecture diagrams

### 6. Search for String References

Old names in strings won't break at compile time but will confuse at runtime:

```bash
# Error messages
rg "\".*old_name.*\"" --type rust --type python --type typescript

# Log messages
rg "log.*old_name|print.*old_name"

# User-facing strings
rg "old_name" --glob "*strings*" --glob "*locale*"
```

Update error messages, log output, and user-facing strings to reference current names.

## When the Hook Catches You

If incomplete-refactoring-guard fires after commit:

```
INCOMPLETE REFACTORING DETECTED. Old names still found in codebase:
- `old_module` still referenced in: src/app.ts, tests/integration.test.ts
```

Run the checklist above for each flagged name. Commit the cleanup as a follow-up:

```bash
# Fix remaining references
git add .
git commit -m "fix: complete refactoring cleanup for old_module"
```

## Common Failure Patterns

| Pattern | Symptom | Prevention |
|---------|---------|-----------|
| Rename without grep | Runtime errors from stale references | Always grep after rename |
| Move without import update | Import errors | Run tests before committing |
| Delete without cascade | Orphaned tests, stale config | Grep for deleted name |
| Partial migration | Old way and new way coexist | Complete or revert |
| String references missed | Error messages have old names | Search for strings too |

## Category Thinking: The Boy Scout Rule

Every refactoring should leave the codebase cleaner. If artifacts of old state remain, the work isn't done.

Instead of fixing "this one reference to oldName," search for ALL references and fix them as a batch. Think in categories, not instances:

**Wrong:**
1. Rename file
2. Fix the import error that shows up
3. Commit

**Right:**
1. Rename file
2. Grep for all references
3. Update imports, configs, docs, tests
4. Verify zero hits
5. Commit

The refactoring isn't complete until the old name produces zero grep results.

## Opt-Out

If you need to disable the hook temporarily:

```bash
export SKIP_REFACTOR_HOOKS=1
```

Use sparingly. The hook catches what you miss.
