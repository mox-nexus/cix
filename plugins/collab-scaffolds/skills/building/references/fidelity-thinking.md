# Fidelity Thinking

Build at the right level of completeness. Based on Jeff Patton's fidelity dimension and the Iron Triangle.

## The Iron Triangle + Fidelity

Traditional Iron Triangle: Scope, Time, Cost (with Quality in the center as non-negotiable).

**Fidelity is the 4th dimension:** the finesse/completeness of each feature.

- Low-fidelity solution solves the problem with less precision, granularity, usability
- Fidelity lets you vary scope without cutting quality — the key insight
- Same feature can be delivered at different fidelity levels

## Three Levels

### Dirt Road

**Characteristics:**
- Happy path works
- Minimal error handling (crashes loudly on bad input)
- No tests beyond manual verification
- No edge case handling
- No documentation beyond comments
- "Does the idea even work?"

**When Enough:**
- Spikes — exploring if an approach is viable
- Prototypes — proving concepts before investment
- Exploration — learning unknown terrain
- Internal-only experimentation

**Example:** CLI that works when called correctly, crashes with stack trace if not.

### Cobble Road

**Characteristics:**
- Handles edge cases explicitly
- Has tests (unit tests at minimum)
- Error handling present (returns errors, doesn't crash)
- Basic input validation
- No observability (no logging, metrics, tracing)
- No load testing
- Minimal documentation (README, basic usage)
- "Does this work reliably?"

**When Enough:**
- Internal tools (low blast radius)
- Low-stakes features (failures don't cascade)
- First deployment to staging
- MVP where "good enough" actually is

**Example:** CLI that validates input, shows helpful errors, has test coverage for core paths.

### Tarmac

**Characteristics:**
- Production-hardened (handles load, graceful degradation)
- Observable (logging, metrics, tracing)
- Documented (usage, architecture, runbooks)
- Load-tested and performance-tuned
- Security reviewed
- Error recovery strategies
- Monitoring/alerting configured
- "Can this run in production without waking anyone up?"

**When Enough:**
- User-facing features
- High-stakes systems (money, data, reputation)
- Foundation components others build on
- Anything in the critical path

**Example:** CLI with structured logging, metrics, rate limiting, retry logic, runbooks for operators.

## Feature Grading (Jeff Patton)

Like school grades — each feature can be graded A through F:

| Grade | Quality | Description |
|-------|---------|-------------|
| **A** | Excellent | Best solution, tarmac quality |
| **B** | Good | Solid solution, cobble quality |
| **C** | Acceptable | Works, dirt road that doesn't embarrass |
| **D** | Barely functional | Needs improvement before shipping |
| **F** | Unacceptable | Not fit for purpose |

**Minimum acceptable grade depends on stakes and audience:**
- Internal spike: C is fine
- Internal tool: B is sufficient
- User-facing feature: A is required

## Four Approaches (From Patton Article)

| Approach | Description | Risk | When |
|----------|-------------|------|------|
| **Big Bang** | Build everything to full fidelity before integrating | Late integration, high risk of wrong solution | Never (unless unchangeable requirements) |
| **Incremental** | One feature at a time, each to full fidelity | "Right feature first" problem — invest heavily before validation | Known domain, clear priorities |
| **Iterative** | All features at low fidelity, then increase together | May never reach tarmac, accumulates debt | Prototypes, MVPs |
| **Agile** | Features one by one at low fidelity, then increase both | Balances risk and discovery | Default choice for most work |

**Agile approach combines incremental and iterative:**
1. Add features one at a time (incremental)
2. Start each at dirt road (low fidelity)
3. Validate with users/reality
4. Selectively pave to cobble or tarmac based on feedback and value

This prevents over-investment in features that won't survive contact with users.

## Practical Application

### Before Starting

Ask or infer: "What fidelity level does this need?"

**Signals for dirt road:**
- "Spike this approach"
- "See if X is feasible"
- "Quick prototype"
- "Proof of concept"

**Signals for cobble road:**
- "Internal tool"
- "First version"
- "MVP"
- "Get it working"

**Signals for tarmac:**
- "Production-ready"
- "User-facing"
- "Replace existing system"
- "Foundational component"

### During Implementation

**State the target:** "This is a dirt road implementation."

**Build to that level:**
- Don't over-build (wasted effort on features that might not survive)
- Don't under-build (if tarmac is needed, dirt road is insufficient)

**Track what's at which level:**
- Mental model: "Auth is tarmac, admin panel is cobble, analytics is dirt road"
- Explicit tracking: README with feature fidelity table

### Common Traps

| Trap | Symptom | Cost |
|------|---------|------|
| **All-tarmac** | Building everything to production quality | Slow, wasted effort on features that don't survive validation |
| **All-dirt-road** | Never increasing fidelity | Accumulating debt, fragile system, incidents |
| **Fidelity amnesia** | Forgetting what's at dirt road | Treating dirt road as tarmac → production incidents |
| **Premature optimization** | Adding observability before validating the feature exists | Effort on wrong things |
| **Debt denial** | "It's fine for now" becomes permanent | Dirt road in critical path causes outages |

### When to Increase Fidelity

Upgrade from dirt → cobble or cobble → tarmac when:

| Trigger | From → To | Reasoning |
|---------|-----------|-----------|
| Feature proved valuable | Dirt → Cobble | Worth investing in reliability |
| Becoming user-facing | Cobble → Tarmac | Blast radius increased |
| Causing incidents | Any → Tarmac | Current fidelity insufficient |
| Foundation for other features | Any → Tarmac | Instability cascades |
| Usage exceeds expectations | Cobble → Tarmac | Load demands observability |

## Decision Framework

| Question | Answer Guides Fidelity |
|----------|------------------------|
| Who uses this? | Internal → lower, External → higher |
| What if it fails? | Low impact → lower, High impact → higher |
| How often used? | Rarely → lower, Constantly → higher |
| Is it foundational? | No → lower, Yes → higher |
| Do we know it's valuable? | No → lower, Yes → higher |

## Integration with Quality

**Quality is non-negotiable at every fidelity level.**

| Level | What Quality Means |
|-------|-------------------|
| Dirt road | No dead code, no debug artifacts, works as intended |
| Cobble road | + Tests pass, errors handled, edge cases covered |
| Tarmac | + Observable, documented, production-hardened |

Fidelity is not an excuse for sloppiness. A dirt road still has no potholes — it's just narrow and unpaved.

## References

- Jeff Patton's article on the fidelity dimension
- Iron Triangle (Scope/Time/Cost trade-off)
- Agile development patterns
