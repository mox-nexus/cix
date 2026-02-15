# Checklists and Feedback Loops

Workflow patterns that ensure completeness and correctness.

---

## Contents

- [Feedback Loops](#feedback-loops)
- [Checklists](#checklists)
- [Combining Patterns](#combining-patterns)
- [When to Use What](#when-to-use-what)

---

## Feedback Loops

For operations with observable success/failure, make the loop explicit.

### Basic Pattern

```markdown
1. Perform action
2. Validate result
3. If issues: fix and return to step 2
4. Only proceed when validation passes
```

### Implementation Examples

**Build validation:**
```markdown
### Build Loop

1. Run: `npm run build`
2. Check output:
   - **Success:** Continue to tests
   - **Error:** Fix issue, return to step 1
3. Do not proceed until build succeeds
```

**Data validation:**
```markdown
### Data Validation Loop

1. Parse input file
2. Run: `python validate.py --input data.json`
3. If errors:
   - Review error messages
   - Fix data issues
   - Return to step 2
4. Only proceed when "Validation passed" appears
```

**Iterative refinement:**
```markdown
### Refinement Loop

1. Generate initial draft
2. Review against criteria:
   - [ ] Clarity
   - [ ] Completeness
   - [ ] Accuracy
3. If any criterion fails:
   - Identify specific issue
   - Revise targeted section
   - Return to step 2
4. Finalize when all criteria pass
```

### Key Principles

- **Explicit exit condition:** State exactly what "pass" looks like
- **Specific actions on failure:** Tell Claude what to do when it fails
- **Bounded iterations:** If needed, add "max 3 attempts, then escalate"

---

## Checklists

For multi-step workflows where steps matter.

### When to Use

- Setup/teardown procedures
- Quality gates
- Compliance requirements
- Handoff procedures

### Basic Pattern

```markdown
## [Phase Name]

- [ ] Step one description
- [ ] Step two description
- [ ] Step three description
```

### Implementation Examples

**Pre-flight checklist:**
```markdown
## Before Deployment

- [ ] All tests pass locally
- [ ] No uncommitted changes
- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] Dependencies up to date
```

**Quality gate:**
```markdown
## Before Merge

- [ ] Code reviewed
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] No TODO comments remaining
- [ ] Changelog entry added
```

**Cleanup checklist:**
```markdown
## After Migration

- [ ] Old tables dropped
- [ ] Unused columns removed
- [ ] Indexes verified
- [ ] Performance tested
- [ ] Rollback script tested
```

### Key Principles

- **Actionable items:** Each item should be verifiable
- **Logical order:** Sequence matters if dependencies exist
- **Complete:** Don't rely on implicit steps

---

## Combining Patterns

Checklists and loops work together.

### Pattern: Loop with Checklist Gate

```markdown
### Development Cycle

1. Make changes
2. Run local tests: `npm test`
3. If tests fail: fix and return to step 2
4. When tests pass, verify checklist:
   - [ ] New tests added
   - [ ] Docs updated
   - [ ] No lint errors
5. If any item unchecked: address and return to step 4
6. Ready for review
```

### Pattern: Checklist-Driven Loop

```markdown
### Release Process

## Pre-Release Checklist
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Dependencies reviewed

## Release Loop
1. Run: `npm publish --dry-run`
2. Review output for issues
3. If issues found: fix and return to step 1
4. When clean: `npm publish`

## Post-Release Checklist
- [ ] Tag created
- [ ] Release notes published
- [ ] Team notified
```

---

## When to Use What

| Situation | Pattern | Rationale |
|-----------|---------|-----------|
| Build/compile/lint | Loop | Observable pass/fail |
| Data transformation | Loop | Validate output |
| Iterative improvement | Loop | Refine until criteria met |
| Setup procedures | Checklist | Many independent steps |
| Quality gates | Checklist | All conditions required |
| Complex workflow | Both | Loop for execution, checklist for verification |

### Not Needed

- Simple single-step operations
- Trivial commands
- Operations without meaningful validation
