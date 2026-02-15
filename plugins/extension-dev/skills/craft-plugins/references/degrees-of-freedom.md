# Degrees of Freedom

Match constraint level to the task at hand.

---

## Contents

- [The Spectrum](#the-spectrum)
- [High Freedom](#high-freedom)
- [Medium Freedom](#medium-freedom)
- [Low Freedom](#low-freedom)
- [Choosing the Right Level](#choosing-the-right-level)

---

## The Spectrum

**Analogy:** Narrow bridge (low freedom) vs. open field (high freedom).

| Level | Constraint | Language |
|-------|------------|----------|
| **High** | Guidelines, principles | "Consider...", "Think about..." |
| **Medium** | Defaults with flexibility | "Default to X, adjust for Y" |
| **Low** | Exact requirements | "ALWAYS...", "NEVER...", "MUST..." |

---

## High Freedom

Multiple valid approaches. Context determines best choice.

### When to Use

- Creative tasks
- Exploratory work
- Domain expertise application
- Situations requiring judgment

### Pattern

```markdown
## Code Review

Consider:
- Readability: Is the intent clear?
- Performance: Any obvious bottlenecks?
- Security: Input validation, error handling?
- Maintainability: Would future-you understand this?

Flag concerns. Suggest alternatives. Explain tradeoffs.
```

### Language

| Use | Avoid |
|-----|-------|
| Consider | You must |
| Think about | Always |
| Evaluate | Never |
| May want to | Required |

---

## Medium Freedom

Preferred pattern exists, but variation acceptable for good reasons.

### When to Use

- Standardized processes with edge cases
- Templates that need customization
- Workflows with optional steps
- Situations with sensible defaults

### Pattern

```markdown
## Report Generation

Use this template structure:

1. Executive Summary (required)
2. Findings (required)
3. Methodology (optional, include for technical audience)
4. Appendices (as needed)

Adapt section depth to audience. Technical reports: more detail.
Executive summaries: high-level only.
```

### Language

| Use | Avoid |
|-----|-------|
| Default to | You must always |
| Typically | Never deviate |
| Adjust for | No exceptions |
| Unless [condition] | Under all circumstances |

---

## Low Freedom

Operations fragile. Consistency critical. Deviation causes problems.

### When to Use

- Database migrations
- Security procedures
- Compliance requirements
- Irreversible operations
- Operations with external dependencies

### Pattern

```markdown
## Database Migration

ALWAYS follow this exact sequence:

1. **Backup** - Run `pg_dump` before any changes
2. **Validate** - Check schema compatibility
3. **Migrate** - Apply changes
4. **Verify** - Confirm data integrity

DO NOT skip steps. DO NOT reorder.

If step fails:
- STOP immediately
- Do not proceed to next step
- Restore from backup if needed
```

### Language

| Use | Context |
|-----|---------|
| ALWAYS | Non-negotiable requirement |
| NEVER | Prohibited action |
| MUST | Required step |
| DO NOT | Forbidden variation |
| EXACT | No approximation allowed |

---

## Choosing the Right Level

### Decision Framework

| Question | Yes → | No → |
|----------|-------|------|
| Are there multiple valid approaches? | Higher | Lower |
| Does context significantly change the right answer? | Higher | Lower |
| Is the operation reversible? | Higher | Lower |
| Are mistakes easily corrected? | Higher | Lower |
| Is consistency across executions critical? | Lower | Higher |
| Do external systems depend on exact output? | Lower | Higher |

### Common Mappings

| Task Type | Typical Freedom | Rationale |
|-----------|-----------------|-----------|
| Code review | High | Judgment-dependent |
| Documentation | Medium | Structure + flexibility |
| Report generation | Medium | Template + customization |
| API integration | Low | Exact protocol required |
| Database operations | Low | Data integrity critical |
| Security procedures | Low | No room for interpretation |

### Mixed Freedom

Some capabilities have sections at different levels:

```markdown
## Data Pipeline

### Design Phase (High Freedom)
Consider data volume, latency requirements, cost constraints.
Multiple valid architectures exist.

### Implementation (Medium Freedom)
Use provided templates. Adapt logging and error handling to your needs.

### Deployment (Low Freedom)
ALWAYS follow this exact sequence:
1. Validate config
2. Deploy to staging
3. Run integration tests
4. Deploy to production
```
