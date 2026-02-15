# Anti-Patterns

What to avoid when authoring capabilities.

---

## Contents

- [Content Anti-Patterns](#content-anti-patterns)
- [Structure Anti-Patterns](#structure-anti-patterns)
- [Description Anti-Patterns](#description-anti-patterns)
- [Operational Anti-Patterns](#operational-anti-patterns)
- [Workflow Anti-Patterns](#workflow-anti-patterns)

---

## Content Anti-Patterns

### Over-Explaining

**Problem:** Explaining things Claude already knows wastes tokens.

```markdown
# Bad
JSON (JavaScript Object Notation) is a lightweight data interchange
format that is easy for humans to read and write...

# Good
Output format: JSON
```

**Rule:** Assume Claude is already very smart. Challenge each explanation: "Does Claude need this?"

### Teaching Basics

**Problem:** Tutorial-style content for concepts Claude has trained on.

```markdown
# Bad
## What is an API?
An API (Application Programming Interface) is a set of protocols...

# Good
## API Integration
Endpoint: `POST /api/v1/analyze`
Auth: Bearer token in header
```

**Rule:** Claude knows what APIs, databases, and frameworks are. Teach your specific usage.

### Excessive Examples

**Problem:** Too many examples when one or two suffice.

```markdown
# Bad
Example 1: [trivial case]
Example 2: [slightly different trivial case]
Example 3: [another trivial case]
Example 4: [yet another case]
...

# Good
Example: [representative case]
Edge case: [the tricky situation]
```

**Rule:** One good example plus edge cases. Not an exhaustive catalog.

---

## Structure Anti-Patterns

### Deep Nesting

**Problem:** References nested in subdirectories don't get read.

```
# Bad
references/
├── category1/
│   └── subcategory/
│       └── file.md
└── category2/
    └── another/
        └── file.md

# Good
references/
├── category1-topic.md
└── category2-topic.md
```

**Rule:** One level deep maximum. Claude reads directories, not trees.

### Missing TOC

**Problem:** Long files without table of contents get partially read or skipped.

```markdown
# Bad (200+ line file with no navigation)
## Section 1
[content]
## Section 2
[content]
...

# Good
## Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
...
```

**Rule:** Add TOC for any file over 100 lines.

### Bloated Main Content

**Problem:** SKILL.md over 500 lines loads too much context.

**Rule:** Move detailed content to references. Main content = decision frameworks + core workflow.

---

## Description Anti-Patterns

### Too Vague

**Problem:** Generic descriptions don't activate when needed.

```yaml
# Bad
description: "Helps with data."

# Good
description: "Analyzes CSV files for statistical patterns. Use when: user asks to 'analyze data', 'find patterns', uploads .csv files."
```

### Missing Triggers

**Problem:** No "Use when:" means poor activation.

```yaml
# Bad
description: "Sophisticated multi-modal analysis system for enterprise data transformation."

# Good
description: "Transforms enterprise data between formats. Use when: user mentions 'ETL', 'data conversion', 'format migration', or asks to 'transform' files."
```

### Wrong Voice

**Problem:** First/second person doesn't match pattern matching.

```yaml
# Bad
description: "I can help you analyze your data and find insights."

# Good
description: "Analyzes data and surfaces insights. Use when: user asks for 'data analysis' or 'insights'."
```

---

## Operational Anti-Patterns

### Recipe When Workflow Needed

**Problem:** Multi-step state-changing operations presented as a static checklist instead of an interactive workflow.

```markdown
# Bad — Recipe: user executes blind steps
## Setup
- [ ] Install dependencies
- [ ] Copy config file
- [ ] Run patch script
- [ ] Verify installation

# Good — Workflow: Claude drives, user approves
## Workflow
1. Infer: Check OS, existing installation, current state
2. Assess: "You have X installed, Y missing"
3. Choose: Present numbered options for config profile
4. Plan: Show exact steps before any changes
5. Execute: Each step with explicit approval
6. Verify: Run checks, diagnose failures, offer fixes
```

**Rule:** If the skill performs state-changing actions (writes files, modifies configs, installs software), use the workflow pattern. Claude can check prerequisites, detect the OS, handle errors, and verify outcomes — a static checklist cannot.

### Permissive Defaults

**Problem:** Config-generating skills default to the most permissive option.

```markdown
# Bad — default allows everything, user must restrict
"allowedDomains": ["*.com", "*.org", "*.io"]

# Good — default allows minimum, user expands
"allowedDomains": ["api.anthropic.com"]
# User adds domains as needed
```

**Rule:** Default to the most restrictive option. Every expansion is a conscious decision. This matters especially for security configs, network allowlists, file permissions, and API scopes.

### Missing Limitations

**Problem:** Skills making security or reliability claims without disclosing what they do NOT protect against.

```markdown
# Bad — claim without bounds
"This skill secures your deployment."

# Good — honest scope
## Limitations
- Does NOT protect against: kernel exploits, physical access
- Mitigated but not eliminated: proxy bypass on apps ignoring HTTP_PROXY
- Out of scope: container-level isolation (see Docker docs)
```

**Rule:** Every security/reliability skill needs a "Limitations" or "What this does NOT protect against" section. Overclaiming erodes trust. Honest bounds build calibrated trust (β = 0.415).

### Untested Descriptions

**Problem:** Descriptions written from the author's perspective, not the user's.

```yaml
# Bad — implementation jargon
description: "Configures SRT sandbox runtime wrapper for process isolation"

# Good — user intent language
description: "Restrict what the AI assistant can access on your machine.
 Use when: protecting credentials, limiting network, preventing unauthorized writes"
```

**Test:** Before shipping, ask "If a user said [common query], would this description match?" Run at least 3 realistic user queries against the description.

---

## Workflow Anti-Patterns

### Implicit Steps

**Problem:** Assuming Claude will infer steps not written.

```markdown
# Bad
Validate the data before proceeding.

# Good
1. Run: `python validate.py --input {file}`
2. Check output:
   - PASS: Continue to step 3
   - FAIL: Review errors, fix data, return to step 1
3. Only proceed when validation passes
```

### No Exit Condition

**Problem:** Loops without clear termination.

```markdown
# Bad
Keep refining until it's good.

# Good
Refine until all criteria pass:
- [ ] Accuracy verified
- [ ] Format correct
- [ ] No errors in output

Max 3 iterations. If still failing, report issues and stop.
```

### Options Without Defaults

**Problem:** Presenting choices without guidance causes paralysis.

```markdown
# Bad
You could use approach A, B, or C.

# Good
Default: Use approach A (fastest, covers 80% of cases).
Use B if: [specific condition]
Use C if: [specific condition]
```

---

## Time-Sensitive Anti-Patterns

### Hardcoded Versions

**Problem:** Version numbers go stale.

```markdown
# Bad
Install Node.js 18.17.0

# Good
Install latest LTS Node.js (check nodejs.org for current version)
```

### Current Best Practices

**Problem:** "Current" and "latest" become wrong.

```markdown
# Bad
The current best practice is to use X.

# Good
Preferred approach: X
(Note: Patterns evolve. Check official docs for updates.)
```

### Deprecated Patterns

**Problem:** No way to signal outdated content.

```markdown
# Good
## Deprecated Patterns
These patterns were previously recommended but are now outdated:
- Pattern X (replaced by Y in v2.0)
- Pattern Z (security concerns discovered)
```
