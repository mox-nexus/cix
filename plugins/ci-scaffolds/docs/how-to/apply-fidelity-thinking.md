# Apply Fidelity Thinking to Development Tasks

Fidelity thinking prevents two wastes: over-building features that don't survive validation, and under-building features that reach production unprepared.

## The Concept

The Iron Triangle says you can control scope, time, and cost. Pick two.

Jeff Patton added a fourth dimension: fidelity. Not everything needs to be finished at the same level of polish. Same feature, different levels of completeness.

This gives you a new way to vary scope without cutting quality.

## Three Fidelity Levels

### Dirt Road

Happy path works. Edge cases might crash it.

Good for:
- Spikes to test if an approach is viable
- Prototypes to prove concepts before investment
- Exploration in unknown territory
- Learning new tools or patterns

Example: CLI that works when called correctly, crashes with stack trace on bad input.

### Cobble Road

Handles edge cases. Has tests. Returns errors instead of crashing. Not hardened for production load.

Good for:
- Internal tools with low blast radius
- Low-stakes features where failures don't cascade
- MVPs to validate with real usage
- First deployment to staging

Example: CLI validates input, shows helpful errors, has test coverage for core paths.

### Tarmac

Production-hardened. Observable. Documented. Load-tested.

Good for:
- User-facing features in critical paths
- High-stakes systems (money, data, reputation)
- Foundation components others build on
- Anything where failures wake people up

Example: CLI with structured logging, metrics, rate limiting, retry logic, operator runbooks.

## How to Apply

### 1. State the Target Before Building

Say it explicitly: "This is a dirt road implementation."

Clarify with stakeholders if not obvious:
- "Is this a spike or will this ship to users?"
- "Internal tool or external API?"
- "MVP or production feature?"

### 2. Build to That Level

Match effort to fidelity target.

Dirt road:
- Write the happy path
- Manual testing is enough
- Skip observability

Cobble road:
- Add error handling
- Write unit tests
- Basic input validation

Tarmac:
- Add logging, metrics, tracing
- Load test
- Write runbooks
- Security review

### 3. Track What's at Which Level

Keep a mental model or explicit list:
- "Auth is tarmac, admin panel is cobble, analytics dashboard is dirt road"

When something at dirt road moves to the critical path, upgrade it.

### 4. Increase Fidelity When Validated

Don't pave the road before you know it goes somewhere useful.

Upgrade triggers:
- Feature proved valuable in practice
- Becoming user-facing
- Causing incidents
- Foundation for other work
- Usage exceeds expectations

## The Traps

Jumping straight to tarmac for everything:
- Slow delivery
- Wasted effort on features that don't survive
- Over-engineering before validation

Stopping at dirt road for everything:
- Accumulated technical debt
- Production incidents from fragile code
- Treating dirt road as if it were tarmac

## Feature Grading

Think of features like school grades:

| Grade | What It Means |
|-------|---------------|
| A | Tarmac where tarmac is needed, dirt where dirt is fine |
| B | Mostly appropriate fidelity, minor mismatches |
| C | Some over-built, some under-built |
| D | Significant fidelity mismatches causing problems |
| F | All tarmac (too slow) or all dirt road (too fragile) |

Grade A isn't "everything is tarmac." It's "fidelity matches stakes."

## The Agile Pattern

Agile combines incremental and iterative:

1. Add features one at a time (incremental)
2. Start each at dirt road (iterative - low fidelity first)
3. Validate with users or reality
4. Selectively pave to cobble or tarmac based on value

This prevents heavy investment before you know if the feature survives contact with users.

Big bang (build everything to full fidelity before integrating) has late integration risk. Incremental alone (one feature at a time to full fidelity) has the "right feature first" problem. Iterative alone (all features at low fidelity) may never reach production quality.

Agile balances both: build the next most important thing at the minimum viable fidelity, then increase fidelity for what proves valuable.

## The Hook Reminder

Every 25 interactions, the fidelity-checkpoint hook reminds you:

"What fidelity level is the current work at?"

This prevents fidelity amnesia - forgetting what's at dirt road and treating it as if it were tarmac.

## Quality at Every Level

Fidelity is not an excuse for sloppiness.

At every level:
- No dead code
- No debug artifacts left in
- Code does what it claims to do

The difference is scope:
- Dirt road: works as intended (narrow scope)
- Cobble road: + handles edge cases, has tests
- Tarmac: + observable, documented, production-hardened

A dirt road has no potholes. It's just narrow and unpaved.
