# cix - Collaborative Intelligence Extensions

> Package manager for cognitive extensions

cix discovers, installs, and manages Claude Code extensions from marketplace repositories.

## What cix Does

- **Source management**: Register git repos as extension sources (marketplaces)
- **Package discovery**: Scan sources for installable extension packages
- **Installation**: Copy extensions to `~/.claude/plugins/`
- **Lifecycle**: Update, remove, inspect installed extensions

## What cix Does NOT Do

- Create extensions (use plugin-dev for that)
- Validate extension quality (use evaluator agent)
- Run extensions (that's Claude Code's job)

---

## CLI Commands

### Sources (Marketplaces)
```bash
cix source add <url>           # Register a source
cix source list                # Show registered sources
cix source rm <name>           # Remove a source
cix source refresh [name]      # Fetch latest from source(s)
```

### Packages (Extensions)
```bash
cix list                       # Show installed extensions
cix list -a                    # Show available extensions
cix add <package>              # Install an extension
cix rm <package>               # Remove an extension
cix update [package]           # Update extension(s)
cix show <package>             # Show extension details
```

### Info
```bash
cix info                       # Show configuration and status
cix --skill                    # Output skill for Claude
cix --skill --reference sources    # Source management patterns
```

---

## Hexagonal Architecture

```
domain/
├── models.py                  # Source, Package, Extension, Installation
└── ports/_out/                # Interfaces domain requires
    ├── registry.py            # State persistence (sources, installations)
    ├── repository.py          # Package fetching from sources
    └── target.py              # Installation targets (Claude Code, etc.)

application/
└── use_cases.py               # Cix facade - orchestrates operations

adapters/
├── _in/                       # INTO hexagon (user-facing)
│   └── cli.py                 # Rich Click CLI
└── _out/                      # OUT of hexagon (infrastructure)
    ├── filesystem_registry.py # JSON-based state in ~/.cix/
    ├── git_repository.py      # GitPython for source fetching
    └── claude_code_target.py  # ~/.claude/plugins/ installation
```

### Naming Convention
- `_in/` = requests coming INTO the hexagon (CLI, HTTP)
- `_out/` = requests going OUT from hexagon (database, git, targets)

---

## Domain Models

| Model | Purpose |
|-------|---------|
| `Source` | Git repo containing packages (marketplace) |
| `Package` | Installable unit with extensions |
| `Extension` | Single skill/agent/hook/mcp |
| `Extensions` | Collection of extensions in a package |
| `Installation` | Record of installed package |

---

## State Storage

All state lives in `~/.cix/`:
```
~/.cix/
├── sources.json        # Registered sources
├── installations.json  # What's installed where
└── cache/              # Cloned source repos
    └── <source-name>/  # Git clone of source
```

---

## Adding a New Target

1. Create adapter in `adapters/_out/`:
```python
class CursorTargetAdapter:
    @property
    def name(self) -> str:
        return "cursor"

    def is_available(self) -> bool:
        # Check if Cursor is installed
        ...

    def install(self, package: Package, source_path: Path) -> None:
        # Copy to Cursor's extension dir
        ...
```

2. Register in `cli.py` composition root:
```python
target_adapters = {
    "claude-code": ClaudeCodeTargetAdapter(...),
    "cursor": CursorTargetAdapter(...),
}
```

---

## Adding a New Source Type

1. Create adapter in `adapters/_out/`:
```python
class HttpRegistryAdapter:
    def fetch(self, source: Source) -> None:
        # Fetch package index from HTTP API
        ...

    def list_packages(self, source: Source) -> list[Package]:
        # Parse index, return packages
        ...
```

2. Switch based on URL scheme in composition root.

---

## Testing

```bash
uv run pytest tests/
```

Tests use in-memory adapters to avoid filesystem side effects.

---

## Relationship to Other Tools

| Tool | Relationship |
|------|--------------|
| **memex** | Sibling tool - memex excavates artifacts, cix manages extensions |
| **plugin-dev** | Creates extensions that cix installs |
| **evaluator** | Validates extension quality before publishing |
| **Claude Code** | The target that uses installed extensions |

cix and memex are independent - neither imports from the other.
