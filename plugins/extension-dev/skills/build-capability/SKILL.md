---
name: build-capability
description: "Builds software tools - CLI applications, Python packages, APIs, and libraries. Use when: creating a CLI tool, designing an API, packaging for distribution, or building tools like memex, cix, or radix."
---

# Build Capability

Patterns for building actual software tools that users and systems consume.

**Claude Code extensions:** See `build-plugin` skill (skills, hooks, commands, MCP).

---

## Contents

- [Tool Types](#tool-types)
- [CLI Design](#cli-design)
- [API Design](#api-design)
- [Python Packaging](#python-packaging)
- [Rust CLI Patterns](#rust-cli-patterns)
- [Testing Tools](#testing-tools)
- [Distribution](#distribution)

---

## Tool Types

| Building | Approach |
|----------|----------|
| CLI application | argparse/click (Python), clap (Rust), commander (Node) |
| Python library | pyproject.toml + uv/pip |
| REST API | FastAPI/Flask (Python), Axum (Rust) |
| GraphQL API | Strawberry (Python), async-graphql (Rust) |
| System tool | Rust for performance, Python for flexibility |

---

## CLI Design

### Argument Structure

```
tool [global-options] <command> [command-options] [arguments]
```

**Examples:**
```bash
memex --config ~/.memex search "query"
cix build --release ./src
radix convert --format json input.csv
```

### Option Conventions

| Pattern | Use For |
|---------|---------|
| `-v, --verbose` | Increase output detail |
| `-q, --quiet` | Suppress non-error output |
| `--dry-run` | Show what would happen |
| `-o, --output` | Output destination |
| `-f, --force` | Skip confirmations |
| `--config` | Config file path |

### Help Text

```
Usage: tool <command> [options]

Commands:
  init        Initialize a new project
  build       Build the project
  deploy      Deploy to production

Options:
  -v, --verbose    Increase verbosity
  -q, --quiet      Suppress output
  -h, --help       Show this help

Examples:
  tool init my-project
  tool build --release
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse (bad args) |
| 130 | Interrupted (Ctrl+C) |

### Error Messages

```
Error: Could not read config file

  Path: ~/.config/tool/config.toml
  Reason: File not found

  Fix: Run `tool init` to create default config
```

Pattern: What happened + Context + How to fix.

---

## API Design

### REST Conventions

| Method | Action | Idempotent |
|--------|--------|------------|
| GET | Read | Yes |
| POST | Create | No |
| PUT | Replace | Yes |
| PATCH | Update | Yes |
| DELETE | Remove | Yes |

### URL Structure

```
/api/v1/resources
/api/v1/resources/{id}
/api/v1/resources/{id}/subresources
```

### Response Format

```json
{
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid input",
    "details": [
      {"field": "email", "message": "Invalid format"}
    ]
  }
}
```

### Status Codes

| Code | Use |
|------|-----|
| 200 | Success (with body) |
| 201 | Created |
| 204 | Success (no body) |
| 400 | Bad request (client error) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

---

## Python Packaging

### Project Structure

```
my-tool/
├── pyproject.toml
├── src/
│   └── my_tool/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── core.py
├── tests/
│   └── test_core.py
└── README.md
```

### pyproject.toml

```toml
[project]
name = "my-tool"
version = "0.1.0"
description = "What the tool does"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0",
    "rich>=13.0",
]

[project.scripts]
my-tool = "my_tool.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "ruff>=0.4",
]
```

### Entry Points

**CLI via click:**
```python
# src/my_tool/cli.py
import click

@click.group()
@click.option('--verbose', '-v', is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.command()
@click.argument('name')
@click.pass_context
def hello(ctx, name):
    """Say hello."""
    if ctx.obj['verbose']:
        click.echo(f"Verbose: greeting {name}")
    click.echo(f"Hello, {name}!")

def main():
    cli()
```

**__main__.py:**
```python
from my_tool.cli import main

if __name__ == "__main__":
    main()
```

---

## Rust CLI Patterns

### Cargo.toml

```toml
[package]
name = "my-tool"
version = "0.1.0"
edition = "2021"

[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1.0"
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[[bin]]
name = "my-tool"
path = "src/main.rs"
```

### CLI with clap

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "my-tool")]
#[command(about = "What the tool does")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
    
    #[arg(short, long, global = true)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new project
    Init {
        #[arg(value_name = "NAME")]
        name: String,
    },
    /// Build the project
    Build {
        #[arg(short, long)]
        release: bool,
    },
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Init { name } => init(&name),
        Commands::Build { release } => build(release),
    }
}
```

### Error Handling

```rust
use anyhow::{Context, Result};

fn read_config(path: &Path) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read config file")?;
    
    toml::from_str(&content)
        .context("Failed to parse config")
}
```

---

## Testing Tools

### CLI Testing (Python)

```python
from click.testing import CliRunner
from my_tool.cli import cli

def test_hello():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', 'World'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output
```

### CLI Testing (Rust)

```rust
#[cfg(test)]
mod tests {
    use assert_cmd::Command;
    
    #[test]
    fn test_help() {
        let mut cmd = Command::cargo_bin("my-tool").unwrap();
        cmd.arg("--help")
            .assert()
            .success()
            .stdout(predicates::str::contains("Usage"));
    }
}
```

### API Testing

```python
from fastapi.testclient import TestClient
from my_api import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

---

## Distribution

### PyPI (Python)

```bash
# Build
uv build

# Upload to PyPI
uv publish

# Or with twine
twine upload dist/*
```

### crates.io (Rust)

```bash
# Verify
cargo publish --dry-run

# Publish
cargo publish
```

### npm (Node)

```bash
npm publish
```

### Homebrew

Create a formula for macOS distribution. Consider a tap for custom tools.

### GitHub Releases

- Tag releases with semver: `v1.0.0`
- Include pre-built binaries for major platforms
- Generate changelog from commits

---

## Quality Checklist

### Before Release

- [ ] README documents installation and basic usage
- [ ] `--help` works and is helpful
- [ ] Error messages are actionable
- [ ] Exit codes follow conventions
- [ ] Tests cover main functionality
- [ ] Version number updated

### CLI Specific

- [ ] Commands are verbs (build, deploy, init)
- [ ] Options use standard conventions
- [ ] Supports `--dry-run` for destructive operations
- [ ] Respects `--quiet` and `--verbose`

### API Specific

- [ ] Endpoints follow REST conventions
- [ ] Errors include actionable detail
- [ ] Authentication documented
- [ ] Rate limits documented
