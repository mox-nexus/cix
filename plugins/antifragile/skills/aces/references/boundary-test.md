# The Boundary Test

Distinguishes a structural boundary from an Inner Platform. Mechanical. Arithmetic.

## The Test

> If the boundary reduces total integration surface, it is a boundary. If it increases total integration surface, it is an Inner Platform.

Integration surface is countable: distinct interfaces crossed per capability-runtime pairing.

Under full coupling, $N$ capabilities across $M$ runtimes cost $NM$. Each capability integrates against each runtime independently. Under protocol mediation, the cost is $N + M + B$, where $B$ is the bounded one-time boundary construction cost. For any $N, M > 2$, the difference grows multiplicatively in $(N, M)$, not linearly. For $N = M = 10$ and $B$ modest, the coupled count is 100; the mediated count is about 21. The ratio widens without bound as $N$ or $M$ grows.

## Why the Inner Platform Fails the Test

The Inner Platform Effect names the failure mode: in trying to abstract over a system, you rebuild the system at a lower fidelity. The abstraction becomes thicker than what it replaced. The total integration surface goes up.

The distinction is Dijkstra's: abstraction toward precision (narrowest correct interface) versus abstraction toward vagueness (lowest-common-denominator wrapper). The Inner Platform abstracts toward vagueness. ACES abstracts toward precision. Opposite directions.

## The Three Mechanisms Pass

- **Wire protocol (Adaptability)**. Thinner than the proprietary surfaces it replaces. It describes the conversation between control plane and data plane. It does not wrap the runtimes. Any runtime speaking the protocol participates. Total integration surface shrinks because $N$ runtimes stop integrating against $N$ proprietary surfaces and start integrating against one protocol.
- **Typed schema (Extensibility)**. Thinner than the mediated-review process it replaces. The schema describes what an extension does at its interface. Validation becomes mechanical. The platform team stops reading extension code. The total integration surface is the schema, not the extension.
- **State contract (Composability)**. Thinner than the emergent-coupling model it replaces. Instead of arbitrary inter-component interaction at runtime, the composition is declared in configuration and validated before execution. What is removed is the ability to do arbitrary things to other components' state. What is gained is the ability to reason about composed behavior from declarations alone.

## Pipeline Envelope

A pattern that frequently arises in migrations away from Coupled Monolith platforms.

**Shape**: Wrap an entire legacy plugin pipeline behind a single protocol adapter, translating at the pipeline boundary rather than per-component. Legacy plugins run unchanged. New capabilities do not have to join the pipeline; they implement the protocol and declare themselves at the boundary.

**Arithmetic**: The envelope is one translation boundary. The plugin pipeline was $n$ plugins sharing a runtime. One boundary is thinner than $n$ couplings. The pattern passes the arithmetic test.

### Transitional, Not Permanent

The envelope is a transitional boundary. It passes the test at the envelope surface for new capabilities arriving at $O(1)$ per unit. The legacy plugins behind it remain in the coupled pipeline; the envelope does not remove their mutual coupling, it only stops new coupling from being added to the same shared runtime.

### Degeneration Condition

The envelope degenerates into an Inner Platform if its protocol accretes semantics specific to the legacy pipeline's internals:
- Timeout profiles tuned to one runtime's garbage collector
- Implicit ordering assumptions leaked from plugin load order
- Tenant-config conventions inherited from the monolith
- Runtime-specific error codes bleeding through the protocol

The test is: **does the protocol surface stay runtime-agnostic?**

- If yes: the envelope is a boundary. Migration can proceed incrementally.
- If no: the envelope is a vendor-specific wrapper wearing a protocol's name. The Inner Platform has already formed.

## Protocol-Level Trust

The Boundary Test is a correctness test, not a trust test. A protocol that passes the arithmetic can still be insecure:

- Authentication and authorization must live at the protocol level.
- Config injection and downgrade attacks expand the attack surface if the protocol carries dynamic configuration.
- Every extension author becomes a trust tier whose code you did not review.

The arithmetic test says the boundary reduces integration surface. It says nothing about adversarial input resistance. Trust boundaries are built on top of correctness boundaries, with different instruments.

## Practical Evaluation

When presented with a proposed boundary, ask in order:

1. **Arithmetic**: does it reduce or increase distinct interfaces crossed per capability-runtime pairing? If increase: Inner Platform. Stop.
2. **Dependency direction**: which way does dependency flow? If the proposed boundary depends on its callers, it is not a boundary.
3. **Protocol purity**: does the protocol surface stay domain-agnostic, or does it accrete runtime-specific semantics? If accreting: degeneration path.
4. **Thinness**: is the boundary narrower than what it replaced? If wider: vagueness-abstraction, not precision-abstraction.
5. **Extensibility envelope**: can new capabilities arrive at $O(1)$ per unit, or is each one a custom integration?

A boundary passes all five. An Inner Platform fails one or more. Transitional boundaries (e.g., Pipeline Envelope) pass at the boundary surface and defer the harder problems behind it.

## Related Patterns

- **Adapter pattern (GoF, 1994)**. Boundary Test applied at the class level. Protocol Envelope and Pipeline Envelope are Adapter scaled to subsystem and to subsystem-collection.
- **Anti-corruption layer (Evans, 2003)**. The pattern for keeping a bounded context from corrupting another. Passes the Boundary Test by construction if it narrows, not expands, the interface between contexts.
- **Strangler fig (Fowler, 2004)**. Progressive replacement. Related but distinct: the Strangler replaces the legacy over time; the Envelope wraps it and lets migration happen incrementally behind the boundary.

## SOLID and Unix Do Not Substitute

SOLID principles operate at the class level, not platform topology. They do not discriminate between a boundary and an Inner Platform at system scale.

The Unix philosophy ("do one thing well") does not substitute either. Shell pipelines are legible, but complex shell scripts decay into the same opacity the cycle describes. The mapping between ACES properties and cycle channels is mechanically specific, not a generic aspiration to "good architecture."

## When the Test Fails in Practice

Integration surface is countable but the count is a vector, not a scalar. Distinct interfaces crossed is one dimension. Other dimensions matter:

- **API breadth**: how many methods on the interface
- **Data coupling**: how tightly the interface's types couple the sides
- **Temporal coupling**: whether the interface forces synchronous interaction
- **Operational coupling**: whether the interface shares failure domains

The arithmetic test is a first-pass filter. A proposed boundary that passes on distinct-interfaces can still fail on temporal coupling (e.g., a synchronous adapter over an asynchronous substrate). Use the test as a necessary-but-not-sufficient check.
