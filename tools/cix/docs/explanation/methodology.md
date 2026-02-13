# cix: Methodology

Why a package manager for cognitive extensions exists and how it's designed.

---

## Contents

- [The Problem](#the-problem)
- [Why a Package Manager](#why-a-package-manager)
- [When Manual Management Breaks](#when-manual-management-breaks)
- [The Marketplace Model](#the-marketplace-model)
- [Design Decisions](#design-decisions)
- [Hexagonal Architecture](#hexagonal-architecture)
- [Extension Types](#extension-types)
- [Scope Boundaries](#scope-boundaries)

---

## The Problem

Claude Code extensions (skills, agents, hooks, MCP servers) are files in directories. Installing one means copying the right files to `~/.claude/plugins/`. Discovering what's available means browsing repositories manually. Updating means re-downloading and overwriting.

This is manageable for one or two extensions. At ecosystem scale, it becomes the same problem every language ecosystem solved decades ago:

| Language | Solution | Year |
|----------|----------|------|
| Perl | CPAN | 1995 |
| Python | pip/PyPI | 2008 |
| Node | npm | 2010 |
| Rust | cargo/crates.io | 2014 |

cix is the package manager for Claude Code extensions. It solves discovery, installation, updates, and removal.

---

## Why a Package Manager

Manual extension management has compounding costs:

**Discovery**: How does a user find extensions that match their workflow? Browsing GitHub repos doesn't scale. A curated, searchable catalog does.

**Installation**: Copying files is error-prone. Wrong directory structure, missing dependencies, version mismatches. A `cix add` command handles the mechanics.

**Updates**: Extension authors improve their work. Users who installed v1 need a path to v2. Without a package manager, "update" means "delete and re-install manually."

**Removal**: Clean removal requires knowing every file an extension installed. `cix rm` handles the bookkeeping.

The pattern is well-established. The novel element is **what's being packaged**: cognitive extensions that enhance human-AI collaboration, not libraries or frameworks.

---

## When Manual Management Breaks

You've installed 3 extensions by copying directories into `~/.claude/plugins/`. One gets updated -- which files do you replace? Another has a new dependency on a shared reference file -- do you know? A third changes its directory structure between versions. Manual management works for 1-2 extensions. At 5+, you're maintaining an undocumented dependency graph in your head.

cix makes this a non-problem: `cix update` handles versioning, `cix add` resolves structure, `cix rm` cleans up completely.

---

## The Marketplace Model

cix uses a source-based marketplace model:

```
Source (git repo)
├── marketplace.json        # Registry of available packages
├── plugin-a/               # Package directory
│   ├── .claude-plugin/
│   │   └── plugin.json     # Package manifest
│   ├── skills/
│   ├── agents/
│   └── ...
└── plugin-b/
    └── ...
```

**Sources** are git repositories containing extension packages. Anyone can create a source by structuring a repo with a `marketplace.json` manifest.

**Why git-based?** Git repos are:
- Free to host (GitHub, GitLab, Codeberg)
- Versionable (tags, branches)
- Forkable (users can maintain their own variants)
- Auditable (full history of changes)

This is the same model as Homebrew taps, Arch Linux AUR, and Nix channels.

---

## Design Decisions

### Complementary by Default

Every extension in the cix ecosystem must follow the Collaborative Intelligence thesis: enhance human capability, don't replace it. This is enforced through:

- **Quality evaluation**: The evaluator agent assesses extensions against CI design principles before marketplace inclusion
- **Design documentation**: Extensions include methodology docs explaining *why* they're designed the way they are
- **Transparency**: Extension behavior, sources, and reasoning are inspectable

### Source-Agnostic

cix doesn't run a central registry. It aggregates from user-registered sources. This means:

- No single point of failure
- Users control which sources they trust
- Organizations can run private sources
- The official mox-labs source is just one among potentially many

### CLI-First

```bash
cix add arch-guild           # Install
cix list                     # What's installed
cix update                   # Update all
cix rm arch-guild            # Remove
```

The CLI is the primary interface. It follows the same conventions as `uv`, `cargo`, and `brew` -- subcommand-based, flags for options, human-readable output.

---

## Hexagonal Architecture

cix follows hexagonal architecture (ports and adapters):

**Domain**: Pure models -- Source, Package, Extension, Installation. No infrastructure dependencies.

**Ports**: Protocol-based interfaces:
- `RegistryPort` -- state persistence (sources, installations)
- `RepositoryPort` -- package fetching from sources
- `TargetPort` -- installation targets (Claude Code, potentially others)

**Adapters**:
- `_in/cli.py` -- Rich Click CLI (driving adapter)
- `_out/filesystem_registry.py` -- JSON state in `~/.cix/`
- `_out/git_repository.py` -- GitPython for source fetching
- `_out/claude_code_target.py` -- Installation to `~/.claude/plugins/`

**Why this matters:** The TargetPort abstraction means cix could support installation to Cursor, Windsurf, or any future AI coding tool -- one new adapter, zero domain changes.

In practice: when a new AI coding tool launches (Cursor, Windsurf, etc.), cix can support it with one new target adapter -- no domain changes, no reinstalling your extensions, no breaking existing workflows.

---

## Extension Types

cix manages four types of Claude Code extensions:

| Type | What It Does | Granularity |
|------|-------------|-------------|
| **Skill** | Decision frameworks and methodology for Claude | Loaded into context on activation |
| **Agent** | Specialized subagent with orthogonality lock | Delegated to for specific perspectives |
| **Hook** | Event-triggered behavior (PreToolUse, PostToolUse, etc.) | Runs automatically on events |
| **MCP Server** | External service integration | Bridges systems via protocol |

A **package** bundles one or more extensions into an installable unit. The `arch-guild` package, for example, contains 13 agents and 4 skills.

---

## Scope Boundaries

cix has precise boundaries:

| cix Does | cix Does Not |
|----------|-------------|
| Discover extensions from sources | Create extensions (use plugin-dev) |
| Install to Claude Code plugins dir | Validate extension quality (use evaluator) |
| Track what's installed where | Run extensions (Claude Code does that) |
| Update and remove packages | Host a central registry |

Each "does not" is handled by a different tool or agent in the ecosystem. cix is the package manager, not the IDE, linter, or runtime.
