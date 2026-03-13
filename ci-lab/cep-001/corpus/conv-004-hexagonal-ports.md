# Hexagonal Architecture: Protocol vs ABC

**Date**: 2025-02-05
**Participants**: user, claude

user: For cix ports — should we use ABC or Protocol? I've seen both in Python hexagonal code.

claude: Strong preference for Protocol. Here's why:

**ABC (Abstract Base Class)**:
- Requires explicit inheritance: `class MyAdapter(Port)`
- Runtime checking via `isinstance`
- Couples the adapter to the port module (import dependency)

**Protocol (typing.Protocol)**:
- Structural typing: if it quacks, it's a duck
- No import needed in the adapter — satisfies the protocol implicitly
- `@runtime_checkable` adds isinstance support if needed
- Aligns with hexagonal's dependency inversion — ports don't leak into adapters

user: The port lives in domain. If adapters import domain ABC, that's an inward dependency — which is fine. But Protocol means they don't even need to import it?

claude: Exactly. With Protocol, an adapter in `adapters/_out/` can satisfy `domain.ports.Storage` without importing it. The type checker verifies structural conformance. This is cleaner dependency inversion.

**Decision**: `typing.Protocol` with `@runtime_checkable` for all hexagonal ports.

**Key fact**: Karman (guild agent) approved this decision — "precision over metaphor."
