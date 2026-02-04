# Source Reference

## Adding Sources

### Git Repository (remote)

```bash
cix source add https://github.com/owner/repo
cix source add https://github.com/owner/repo --name custom-name
cix source add https://github.com/owner/repo --default  # Set as default
```

### Local Repository

```bash
# Directory must be a git repository
cix source add file:///absolute/path/to/repo --name local
```

### Private Repository

```bash
# Uses git credential helper (SSH keys, gh auth)
cix source add git@github.com:org/private-repo.git
```

## Source Operations

```bash
cix source list                  # Show all sources
cix source refresh               # Fetch all sources
cix source refresh my-source     # Fetch specific source
cix source rm my-source          # Remove source
```

## Default Source

The default source is used when no source is specified:

```bash
cix add arch-guild               # Uses default source
cix add other-source/arch-guild  # Uses specified source
```

## Package Discovery

cix looks for packages in:
1. Repository root (each directory with .claude-plugin/)
2. `packages/` subdirectory
3. `extensions/` subdirectory
4. `plugins/` subdirectory

## URL Schemes

| Scheme | Example |
|--------|---------|
| HTTPS | `https://github.com/org/repo` |
| SSH | `git@github.com:org/repo.git` |
| File | `file:///path/to/local/repo` |
