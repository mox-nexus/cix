# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-02-23

### Added

- **Library**: 9 research synthesis articles grounded in 31 peer-reviewed papers (CHI, PNAS, Nature, NeurIPS, ICLR)
  - The Paradox, The Mechanism, The Generative Step, The Invisibility, The Stakes
  - The Design Lever, Complementary Design, CIX Affordances, Considerations
  - Evidence badge system with four levels (strong, moderate, weak, speculative)
  - Bibliography with 45+ entries, expandable abstracts, and effect sizes
- **Experience site**: SvelteKit documentation with catalog, library, and landing page
  - Two-column article layout with cluster sidebar navigation
  - Reading progress tracking
  - Catalog with plugin detail modals and Mermaid diagrams
- **Plugins**: 8 marketplace extensions
  - `arch-guild` — 13 orthogonal architecture reasoning agents
  - `collab-scaffolds` — Collaboration, problem-solving, and engineering craft scaffolds
  - `craft-rhetoric` — Semantic Stack workflow with 7 agents (feynman, sagan, tufte, socrates, orwell, vyasa, jobs)
  - `craft-extensions` — Plugin creation: skills, agents, hooks, commands, MCPs, tools
  - `craft-evals` — Eval methodology for AI systems
  - `craft-prompts` — Prompt engineering for reasoning models and deep research
  - `data-store` — Database selection, search, hybrid retrieval, RAG
  - `run-openclaw-srt` — OpenClaw with SRT sandbox

### Changed

- Renamed `extensions/cix/` to `tools/cix/`
- Renamed `craft-explanations` to `craft-rhetoric` with Five Canons structure
- Renamed `extension-dev` to `craft-extensions` and `build-evals` to `craft-evals`

### Fixed

- Comprehensive evidence audit across all library citations (Blaurock, Kosmyna, Mozannar, Budzyń, Lee)
- Corrected misattributed studies (Hemmer→Blaurock, Hao→Moon/Kushlev, Anderson→Holzner)
- Fixed Lee et al. β values and Bonferroni threshold disclosure
- Fixed Dohmatob synthetic data threshold (1%, not 1-in-1,000)

## [0.1.0] - 2025-01-30

### Added

- Initial release of cix CLI
- Source management (`cix source add/list/rm/refresh`)
- Extension management (`cix add/rm/update/list/show`)
- System info (`cix info`)
- Git-based source adapter
- Claude Code target adapter
- Filesystem-based registry
- Hexagonal architecture (ports & adapters)

### Technical

- UV workspace structure
- rich-click for styled CLI output
- Pydantic models for domain objects
- Protocol-based port interfaces

[Unreleased]: https://github.com/mox-nexus/cix/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/mox-nexus/cix/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/mox-nexus/cix/releases/tag/v0.1.0
