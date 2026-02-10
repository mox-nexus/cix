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
```

### 2. Assess

Report current state to user:

```
Detected:
- Language: Python (pyproject.toml found, uv)
- Structure: flat (no src/ directory yet)
- Framework: none
- Tests: none
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

```
Proposed structure:
src/{project}/
├── domain/
│   ├── models/          ← Entities, value objects
│   ├── services/        ← Domain logic
│   └── ports/
│       ├── driven/      ← "I need X" (repos, clients)
│       └── driving/     ← "X triggers me" (use cases)
├── adapters/
│   ├── driven/          ← Implements ports/driven/
│   └── driving/         ← Calls ports/driving/
└── config/              ← Wiring (DI, bootstrap)

Create? [y/n]
```

### 5. Execute

Create directories and starter files. Each file gets a brief comment explaining its role, not boilerplate code.

**What to generate:**
- Directory structure
- Port interfaces (empty protocols/interfaces — the contracts)
- Config wiring skeleton
- `__init__.py` / `mod.rs` / `index.ts` as needed

**What NOT to generate:**
- Adapter implementations (those come from actual requirements)
- Test files (those come from actual behavior)
- Domain models (those come from domain discovery)

### 6. Verify

After generation, verify the scaffold:

```
Verify:
- [ ] Domain imports nothing from adapters/ or config/
- [ ] All ports are interfaces/protocols (no implementations in domain/)
- [ ] Config wiring references ports, not concrete adapters
- [ ] Directory names match domain vocabulary
```

## Language-Specific Patterns

### Python

```
Port definition: typing.Protocol (structural subtyping, not abc.ABC)
Wiring: config/container.py with type annotations
Package: pyproject.toml with src layout
```

### TypeScript

```
Port definition: interface (export from domain/ports/)
Wiring: config/container.ts with dependency injection
Package: package.json with src/ paths
```

### Go

```
Port definition: interface in domain/ports/
Wiring: cmd/main.go or internal/config/
Module: go.mod at root
```

### Rust

```
Port definition: trait in domain/ports/
Wiring: src/config/mod.rs
Package: Cargo.toml with workspace if multi-crate
```

## Anti-Patterns to Catch

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| Domain imports ORM | `import sqlalchemy` in domain/ | Pure models, map at adapter boundary |
| God module | Single file > 300 lines | Split by cohesion |
| Premature adapters | Adapter without a port | Port first, adapter second |
| Generic naming | `utils/`, `helpers/`, `common/` | Name by domain concept |
| Circular deps | domain ↔ adapter imports | Invert with port interface |
