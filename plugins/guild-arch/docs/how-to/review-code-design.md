# How to Review Code and API Design

This guide covers using the Guild's design skill for code-level and API-level review. Where the architecture skill evaluates system structure, the design skill evaluates the code within that structure -- naming, abstractions, boundaries, developer experience.

## Invoking a Design Review

The design skill activates on phrases like:

- "Review this code design"
- "Check this API design"
- "Evaluate these abstractions"
- "Review the naming in this module"
- "Is this interface right?"

Point at specific code:

```
"Review the design of src/domain/models.py"
"Check the API surface of our SDK"
"Evaluate the abstractions in the billing module"
```

## The Three Design Lenses

Design reviews use three primary agents, applied in order:

### 1. Karman -- Does the model match reality?

Karman checks whether code models the actual domain, not just the database or the framework.

What Karman catches:
- **Anemic domain models** -- data bags without behavior, where all logic lives in services operating on inert objects
- **Abstraction drift** -- code says "Order" but actually means "ShoppingCartSnapshot"
- **Naming that satisfies developers but confuses domain experts** -- the business calls it a "claim," the code calls it a "request"
- **God classes** -- a 2000-line `UserService` that merges distinct bounded contexts

Karman's test: "Can you explain each entity without referencing implementation? Would a domain expert recognize these names?"

### 2. Burner -- Are boundaries clean?

Burner checks dependency direction, layer violations, and coupling.

What Burner catches:
- **Domain importing infrastructure** -- `from app.adapters.postgres import engine` inside domain logic
- **Circular dependencies** -- A imports B imports A
- **Logic bleeding across layers** -- a controller doing domain calculations
- **Coupling disguised as convenience** -- two services sharing a database

Burner's test: "If I swap the database, does business logic change? If I delete this module, what breaks outside it?"

### 3. Ace -- Can the next developer understand this?

Ace checks cognitive load, error clarity, and discoverability.

What Ace catches:
- **Cryptic errors** -- `Error: 500` with no details
- **Invisible affordances** -- the right way to use the API exists but nothing signals it
- **Tribal knowledge** -- "everyone knows you have to call init() first"
- **Surprise behavior** -- `delete()` that doesn't delete but marks as deleted

Ace's ACES check:
- **Adaptable** -- Can behavior change without code changes?
- **Composable** -- Can pieces combine in new ways?
- **Extensible** -- Can new cases be added without modifying existing code?
- **Separable** -- Can components be understood independently?

## Specialist Triggers

Beyond the three primary lenses, specialists activate when context demands:

| Trigger | Specialist | What They Add |
|---------|-----------|---------------|
| Auth flow, payments, state machines | **Dijkstra** | Formal correctness -- preconditions, invariants, postconditions |
| Loops, aggregations, high-cardinality data | **Knuth** | Complexity analysis -- O(n) vs O(n^2), scaling projections |
| API authentication, input handling | **Vector** | Attack surface -- injection, trust boundaries, STRIDE |

## What to Say

Be specific about what you want reviewed. Compare:

| Vague | Specific |
|-------|----------|
| "Review this code" | "Review the domain model in src/billing/models.py" |
| "Is this API good?" | "Check if the SDK's public interface guides correct usage" |
| "Look at this" | "Evaluate the abstraction boundaries between orders and shipping" |

The more context you provide, the sharper the review. Mention:
- What the code does in business terms
- Who will use this API (internal team, external developers, CLI users)
- What concerns prompted the review

## Reading the Output

Design reviews follow this structure:

```
## Design Review: {Component}

### Karman (Domain Alignment)
- Model matches business terminology
- OrderItem conflates line items and adjustments -- split needed

### Burner (Boundaries)
- Domain is clean -- no infrastructure imports
- PaymentService imports Stripe types directly -- needs a port

### Ace (Developer Experience)
- Error messages include context and suggested fixes
- SDK requires reading 4 files to understand one operation -- too many

### Specialists Invoked
- Dijkstra: Payment flow -- verified state transitions are complete

### Conflicts
Karman wants a richer domain model (split OrderItem into LineItem + Adjustment).
Ace says more types increase cognitive load for new developers.

### Recommendations
1. Split OrderItem (Karman) but add a factory that handles the common case (Ace)
2. Create a PaymentGateway port to decouple from Stripe (Burner)
```

The "Conflicts" section is where the real value lives. When Karman and Ace disagree, that's a genuine tension between domain truth and cognitive simplicity. The review surfaces it -- you resolve it.

## Design Review vs Architecture Review

| Question | Skill |
|----------|-------|
| "Is the service boundary right?" | Architecture |
| "Is the API surface right?" | Design |
| "Should billing be its own service?" | Architecture |
| "Should Order contain shipping info?" | Design |
| "How should these services communicate?" | Architecture |
| "What should we name this entity?" | Design |

When in doubt, start with design. If the review surfaces structural concerns that cross service boundaries, escalate to architecture.
