---
name: cix-architecture
description: "Hexagonal architecture guide for cix. Use when: modifying cix source code, adding features, understanding where code lives, navigating the codebase."
---

# cix Architecture

cix uses **Hexagonal Architecture** (Ports & Adapters) to keep domain logic testable and implementation-swappable.

## Why Hexagonal?

| Problem | Solution |
|---------|----------|
| "Can't test without real git" | Mock the port, test the logic |
| "Locked into filesystem storage" | Swap adapter, keep domain |
| "CLI logic mixed with business logic" | Driving adapter calls application, doesn't contain logic |

## The Hexagon

```
                    ┌─────────────────┐
                    │   CLI (cli.py)  │  ← Driving Adapter (user input)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Application   │  ← Use Cases (orchestration)
                    │   use_cases.py  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    RegistryPort        SourcePort          TargetPort
    (persistence)       (fetching)          (installation)
         │                   │                   │
    Filesystem            Git               Claude Code
    (JSON files)       (GitPython)         (~/.claude/plugins)
```

## Directory Map

```
extensions/cix/src/cix/
├── domain/models.py        # Pure data (Extension, Source, Package)
├── ports/out/              # Interfaces (what we need)
│   ├── registry.py         # State persistence
│   ├── repository.py       # Source fetching
│   └── target.py           # Installation targets
├── adapters/
│   ├── in_/cli.py          # Driving: CLI commands
│   └── out/                # Driven: implementations
│       ├── filesystem_registry.py
│       ├── git_repository.py
│       └── claude_code_target.py
└── application/use_cases.py  # Cix facade
```

## Where to Make Changes

| Want to... | Edit |
|------------|------|
| Add CLI command | `adapters/in_/cli.py` |
| Add domain concept | `domain/models.py` |
| Add source type (HTTP, local) | New adapter implementing `SourcePort` |
| Add install target (VS Code) | New adapter implementing `TargetPort` |
| Change business logic | `application/use_cases.py` |

## Adding a New Adapter

1. Create `adapters/out/new_adapter.py` implementing the port Protocol
2. Wire in `cli.py` composition root (`create_cix` function)

Example for HTTP source:
```python
# adapters/out/http_repository.py
class HttpSourceAdapter:
    def fetch(self, source: Source) -> Path: ...
    def get_ref(self, source: Source) -> str | None: ...
    # ... implement SourcePort protocol
```

## Key Rules

| Rule | Why |
|------|-----|
| Domain imports nothing from adapters | Keeps domain testable |
| Ports are Protocol classes | Structural typing, no inheritance |
| Adapters implement ports | How we actually do I/O |
| CLI creates instances | Composition root wires dependencies |

## Testing Strategy

| Layer | Test Type | Mocking |
|-------|-----------|---------|
| Domain | Unit | None needed (pure) |
| Application | Unit | Mock ports |
| Adapters | Integration | Real systems |
| CLI | E2E | Full stack |

## Collaborative Intelligence Checkpoint

Before adding a feature, ask:

> "Does this make the user more capable, or more dependent?"

cix extensions must be **complementary** — enhance human capability, don't replace it.
