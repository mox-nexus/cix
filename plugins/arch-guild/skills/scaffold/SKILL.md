---
name: scaffold
description: "Scaffolds project structures following architectural patterns. Use when: user asks to 'scaffold a service', 'set up hexagonal', 'create project structure', 'new service', 'init project', or discusses bootstrapping a new codebase."
---

# Scaffold

Workflow-driven project scaffolding with Guild architectural reasoning.

## What This Adds

Claude already knows hexagonal architecture, directory conventions, and boilerplate. This skill adds the **workflow pattern** (infer → assess → choose → plan → execute → verify) and **Guild review** of the scaffold before generation — catching boundary violations, naming drift, and structural anti-patterns at creation time, not review time.

## Core Rules

- Require explicit approval before creating any files
- Infer language, framework, existing state before asking user
- Show exact directory tree before generating
- Stop on unexpected state and ask for guidance
- Numbered choices so user can reply with a single digit

## Workflow

### 1. Infer

Read-only. Detect what exists before asking anything.

```
Check:
- Language/runtime (pyproject.toml? package.json? go.mod? Cargo.toml?)
- Existing structure (src/? lib/? flat?)
- Framework (if any)
- Test framework (if any)
- Package manager (uv? bun? cargo?)
- Existing hex conventions (port naming, adapter layout)
```

### 2. Assess

Report current state to user:

```
Detected:
- Language: Python (pyproject.toml found, uv)
- Structure: src layout
- Framework: none
- Tests: pytest
- Existing convention: domain/ports/_in/, _out/ (from sibling packages)
```

### 3. Choose

Present architecture pattern options:

```
Architecture:
1. Hexagonal (Ports & Adapters) — recommended for services with external deps
2. Clean Architecture — domain-centric, similar to hex but with use case layer
3. Modular — feature-based modules, good for monoliths
4. Flat — minimal structure, good for libraries/CLIs
```

### 4. Plan

Show exact directory tree before creating anything. Apply Guild lenses:

**Karman check**: Do the directory names match the domain? (not generic `utils/`, `helpers/`)
**Burner check**: Do dependencies point inward? Domain imports nothing external?
**Ace check**: Can a new developer navigate this in 15 minutes?

Present the tree, get explicit approval.

### 5. Execute

Create directories and starter files. Each file gets a brief comment explaining its role, not boilerplate code.

**What to generate:**
- Directory structure
- Port interfaces (empty protocols/interfaces — the contracts)
- Composition root skeleton
- `__init__.py` / `mod.rs` / `index.ts` as needed

**What NOT to generate:**
- Adapter implementations (those come from actual requirements)
- Test files (those come from actual behavior)
- Domain models (those come from domain discovery)

### 6. Verify

After generation, verify the scaffold:

```
Verify:
- [ ] Domain imports nothing from adapters/ or composition/
- [ ] All ports are Protocol definitions (no implementations in domain/)
- [ ] Composition root references port types, wires concrete adapters
- [ ] Directory names match domain vocabulary
- [ ] Port direction naming matches project convention
```

## Hexagonal Template — Python

The reference implementation, based on established project convention (memex, ix, cix).

### Directory Layout

```
src/{package}/
├── domain/                     ← The hexagon. Pure business logic.
│   ├── models.py               ← Entities, value objects (Pydantic frozen models)
│   ├── services/               ← Domain logic, use cases
│   │   └── {service}.py
│   └── ports/
│       ├── _in/                ← Driving ports ("how consumers use me")
│       │   └── {usecase}.py    ← Protocol: what the outside world can ask
│       └── _out/               ← Driven ports ("what I need from the world")
│           └── {dependency}.py ← Protocol: what I depend on
├── adapters/
│   ├── _in/                    ← Driving adapters (implement _in ports)
│   │   └── cli/                ← Example: CLI adapter
│   │       └── main.py
│   └── _out/                   ← Driven adapters (implement _out ports)
│       └── {dependency}/       ← Grouped by port they implement
│           └── {impl}.py       ← Concrete implementation
└── composition/
    └── __init__.py             ← Composition root: wires adapters to ports
```

### Why `_in/` and `_out/` (not `driven/` `driving/`)

- `in` is a Python reserved keyword — `from pkg.ports.in import x` is a syntax error
- `_in/`/`_out/` is the underscore convention used across all project packages
- Maps directly: `_in/` = driving (inbound), `_out/` = driven (outbound)
- Adapters mirror the port direction: `adapters/_out/` implements `domain/ports/_out/`

### Why `composition/` (not `config/`)

- `composition/` is the **composition root** — it wires adapters to ports
- `config/` is for settings, environment variables, YAML loading
- These are different concerns: DI wiring vs configuration parsing
- A package may have both if it needs settings AND dependency injection

### Port Definitions

```python
# domain/ports/_out/runtime.py
from typing import Protocol

class AgentRuntime(Protocol):
    """Invoke an agent. Backend-agnostic."""
    async def invoke(self, system: str, messages: list[dict]) -> str: ...
```

Ports are `typing.Protocol` — structural subtyping. Components implement the protocol without importing it. No `abc.ABC`, no inheritance required.

### Composition Root

```python
# composition/__init__.py
from {package}.adapters._out.{dep}.{impl} import ConcreteAdapter
from {package}.domain.services.{service} import MyService

def create_service(**kwargs) -> MyService:
    adapter = ConcreteAdapter(**kwargs)
    return MyService(dependency=adapter)
```

The composition root is the ONLY place that knows about concrete adapters. Domain code references port protocols. Adapter code implements them. The composition root wires them together.

### Dependency Rule

```
domain/     → imports nothing outside domain/
adapters/   → imports domain/ (ports, models)
composition/→ imports domain/ AND adapters/ (the only place that does both)
```

Verify with: `grep -r "from {pkg}.adapters" src/{pkg}/domain/` → must return nothing.

## Hexagonal Template — TypeScript

```
src/
├── domain/
│   ├── models/
│   ├── services/
│   └── ports/
│       ├── in/                 ← No reserved word issue in TS
│       └── out/
├── adapters/
│   ├── in/
│   └── out/
└── composition/
    └── index.ts
```

Port definition: `interface` exported from `domain/ports/`.

## Hexagonal Template — Go

```
internal/{package}/
├── domain/
│   ├── models.go
│   ├── services/
│   └── ports/
│       ├── in/
│       └── out/
├── adapters/
│   ├── in/
│   └── out/
└── cmd/
    └── main.go                 ← Composition root
```

Port definition: `interface` in `domain/ports/`.

## Hexagonal Template — Rust

```
src/
├── domain/
│   ├── models.rs
│   ├── services/
│   └── ports/
│       ├── inbound/            ← Rust: `in` is reserved keyword
│       └── outbound/
├── adapters/
│   ├── inbound/
│   └── outbound/
└── config/
    └── mod.rs                  ← Composition root
```

Port definition: `trait` in `domain/ports/`.

## Anti-Patterns to Catch

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| Domain imports adapter | `from pkg.adapters` in domain/ | Invert with port protocol |
| God module | Single file > 300 lines | Split by cohesion |
| Premature adapters | Adapter without a port | Port first, adapter second |
| Generic naming | `utils/`, `helpers/`, `common/` | Name by domain concept |
| Circular deps | domain ↔ adapter imports | Invert with port interface |
| Port direction mismatch | adapters/_in/ implementing _out/ port | _in adapters implement _in ports, _out adapters implement _out ports |
| Composition leak | Service imports concrete adapter | Service takes port protocol, composition root wires it |
| `abc.ABC` ports | Abstract base class for ports | `typing.Protocol` — structural subtyping, no import coupling |
