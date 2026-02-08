# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/mox-nexus/cix/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mox-nexus/cix/releases/tag/v0.1.0
