"""
CLI adapter for cix - Collaborative Intelligence Extensions.

Command structure follows noun-verb pattern:
- cix source add/list/rm/refresh
- cix list/add/rm/update/show
- cix info

Design principles:
- Helpful error messages with guidance
- Color-coded output (green success, red error, cyan names)
- Progress feedback with Rich tables
"""

from pathlib import Path

import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cix import __version__
from cix.application.use_cases import (
    Cix,
    CixError,
    PackageNotFoundError,
    SourceNotFoundError,
)
from cix.adapters.out.filesystem_registry import FilesystemRegistryAdapter
from cix.adapters.out.git_repository import GitSourceAdapter
from cix.adapters.out.claude_code_target import ClaudeCodeTargetAdapter

console = Console()


# =============================================================================
# Composition Root
# =============================================================================


def create_cix(
    config_dir: Path | None = None,
    cache_dir: Path | None = None,
) -> Cix:
    """
    Create a Cix instance with default adapters.

    This is the composition root - where dependencies are wired together.
    """
    config_dir = config_dir or Path.home() / ".cix"
    cache_dir = cache_dir or config_dir / "cache"

    source_adapter = GitSourceAdapter(cache_dir)
    registry_adapter = FilesystemRegistryAdapter(config_dir)
    target_adapters = {
        "claude-code": ClaudeCodeTargetAdapter(global_config=True),
    }

    return Cix(
        source_port=source_adapter,
        registry_port=registry_adapter,
        targets=target_adapters,
    )


def get_cix() -> Cix:
    """Get a Cix instance. Convenience for CLI commands."""
    return create_cix()


# =============================================================================
# Output Helpers
# =============================================================================


def success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]✓[/green] {message}")


def error(message: str, guidance: str | None = None) -> None:
    """Print an error message with optional guidance."""
    console.print(f"[red]✗[/red] {message}")
    if guidance:
        console.print(f"  [dim]{guidance}[/dim]")


def info(message: str) -> None:
    """Print an info message."""
    console.print(f"[cyan]ℹ[/cyan] {message}")


# =============================================================================
# Main CLI Group
# =============================================================================


@click.group()
@click.version_option(__version__, prog_name="cix")
def main() -> None:
    """
    cix - Collaborative Intelligence Extensions

    Discover, install, and manage cognitive extensions that enhance
    rather than replace human capability.
    """
    pass


# =============================================================================
# Source Commands
# =============================================================================


@main.group()
def source() -> None:
    """Manage extension sources (marketplaces)."""
    pass


@source.command("add")
@click.argument("url")
@click.option("-n", "--name", help="Source name (derived from URL if not provided)")
@click.option("-d", "--default", is_flag=True, help="Set as default source")
def source_add(url: str, name: str | None, default: bool) -> None:
    """Register a new extension source."""
    try:
        cix = get_cix()
        src = cix.add_source(url, name=name, set_default=default)
        success(f"Added source [cyan]{src.name}[/cyan]")

        if default:
            info("Set as default source")

        # Show available packages
        packages = cix.list_packages(src.name)
        if packages:
            info(f"Found {len(packages)} package(s)")

    except CixError as e:
        error(str(e), guidance="Check URL and try again")
        raise SystemExit(1)


@source.command("list")
def source_list() -> None:
    """List registered sources."""
    cix = get_cix()
    sources = cix.list_sources()

    if not sources:
        info("No sources registered")
        console.print("  [dim]Add one with: cix source add <url>[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("URL")
    table.add_column("Default")
    table.add_column("Pinned")

    for src in sources:
        table.add_row(
            f"[cyan]{src.name}[/cyan]",
            src.url,
            "✓" if src.default else "",
            src.ref or "",
        )

    console.print(table)


@source.command("rm")
@click.argument("name")
def source_rm(name: str) -> None:
    """Remove a registered source."""
    try:
        cix = get_cix()
        cix.remove_source(name)
        success(f"Removed source [cyan]{name}[/cyan]")

    except SourceNotFoundError as e:
        error(str(e), guidance="Run 'cix source list' to see available sources")
        raise SystemExit(1)


@source.command("refresh")
@click.argument("name", required=False)
def source_refresh(name: str | None) -> None:
    """Fetch latest from source(s)."""
    try:
        cix = get_cix()
        sources = cix.refresh_source(name)

        for src in sources:
            success(f"Refreshed [cyan]{src.name}[/cyan]")

    except SourceNotFoundError as e:
        error(str(e), guidance="Run 'cix source list' to see available sources")
        raise SystemExit(1)


# =============================================================================
# Package Commands
# =============================================================================


@main.command("list")
@click.option("-a", "--available", is_flag=True, help="Show available (not just installed)")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed information")
def list_packages(available: bool, verbose: bool) -> None:
    """List installed or available extensions."""
    cix = get_cix()

    if available:
        # Show available packages
        try:
            packages = cix.list_packages()
        except SourceNotFoundError as e:
            error(str(e))
            return

        if not packages:
            info("No packages available")
            return

        table = Table(show_header=True, header_style="bold")
        table.add_column("Package")
        table.add_column("Version")
        table.add_column("Extensions")
        if verbose:
            table.add_column("Description")

        for pkg in packages:
            row = [
                f"[cyan]{pkg.name}[/cyan]",
                pkg.version,
                pkg.extensions.summary,
            ]
            if verbose:
                row.append(pkg.description[:60] + "..." if len(pkg.description) > 60 else pkg.description)
            table.add_row(*row)

        console.print(table)
        console.print(f"\n[dim]{len(packages)} package(s) available[/dim]")

    else:
        # Show installed packages
        installations = cix.list_installed()

        if not installations:
            info("No extensions installed")
            console.print("  [dim]Install with: cix add <package>[/dim]")
            return

        table = Table(show_header=True, header_style="bold")
        table.add_column("Package")
        table.add_column("Source")
        table.add_column("Extensions")
        table.add_column("Target")
        if verbose:
            table.add_column("Commit")

        for inst in installations:
            row = [
                f"[cyan]{inst.package.name}[/cyan]",
                inst.source.name,
                inst.package.extensions.summary,
                inst.target,
            ]
            if verbose:
                row.append(inst.commit[:8] if inst.commit else "")
            table.add_row(*row)

        console.print(table)
        console.print(f"\n[dim]{len(installations)} extension(s) installed[/dim]")


@main.command("add")
@click.argument("package")
@click.option("-t", "--target", default="claude-code", help="Installation target")
def add_package(package: str, target: str) -> None:
    """Install an extension."""
    try:
        cix = get_cix()
        installation = cix.install(package, target=target)

        success(f"Installed [cyan]{installation.package.name}[/cyan]")
        info(f"Extensions: {installation.package.extensions.summary}")
        info(f"Target: {installation.target}")

    except (SourceNotFoundError, PackageNotFoundError) as e:
        error(str(e), guidance="Run 'cix list -a' to see available packages")
        raise SystemExit(1)
    except CixError as e:
        error(str(e))
        raise SystemExit(1)


@main.command("rm")
@click.argument("package")
def rm_package(package: str) -> None:
    """Remove an installed extension."""
    try:
        cix = get_cix()
        cix.uninstall(package)
        success(f"Removed [cyan]{package}[/cyan]")

    except PackageNotFoundError as e:
        error(str(e), guidance="Run 'cix list' to see installed packages")
        raise SystemExit(1)


@main.command("update")
@click.argument("package", required=False)
def update_package(package: str | None) -> None:
    """Update installed extension(s)."""
    try:
        cix = get_cix()
        updated = cix.update(package)

        if not updated:
            info("Nothing to update")
            return

        for inst in updated:
            success(f"Updated [cyan]{inst.package.name}[/cyan]")

    except PackageNotFoundError as e:
        error(str(e), guidance="Run 'cix list' to see installed packages")
        raise SystemExit(1)


@main.command("show")
@click.argument("package")
def show_package(package: str) -> None:
    """Show extension details."""
    try:
        cix = get_cix()
        pkg, src = cix.get_package(package)

        panel_content = f"""[bold]{pkg.name}[/bold] v{pkg.version}
[dim]from {src.name}[/dim]

{pkg.description}

[bold]Extensions:[/bold]
"""
        if pkg.extensions.skills:
            panel_content += f"  Skills: {', '.join(pkg.extensions.skills)}\n"
        if pkg.extensions.agents:
            panel_content += f"  Agents: {', '.join(pkg.extensions.agents)}\n"
        if pkg.extensions.hooks:
            panel_content += f"  Hooks: {', '.join(pkg.extensions.hooks)}\n"
        if pkg.extensions.mcps:
            panel_content += f"  MCPs: {', '.join(pkg.extensions.mcps)}\n"

        if pkg.author:
            panel_content += f"\n[dim]Author: {pkg.author}[/dim]"
        if pkg.license:
            panel_content += f"\n[dim]License: {pkg.license}[/dim]"

        console.print(Panel(panel_content.strip(), title="Extension Details", border_style="cyan"))

    except (SourceNotFoundError, PackageNotFoundError) as e:
        error(str(e), guidance="Run 'cix list -a' to see available packages")
        raise SystemExit(1)


# =============================================================================
# Info Command
# =============================================================================


@main.command("info")
def show_info() -> None:
    """Show cix configuration and status."""
    cix = get_cix()

    sources = cix.list_sources()
    installations = cix.list_installed()
    targets = cix.get_targets()

    panel_content = f"""[bold]cix[/bold] v{__version__}
Collaborative Intelligence Extensions

[bold]Sources:[/bold] {len(sources)} registered
[bold]Installed:[/bold] {len(installations)} extension(s)

[bold]Targets:[/bold]
"""
    for name, available in targets.items():
        status = "[green]✓ available[/green]" if available else "[red]✗ not found[/red]"
        panel_content += f"  {name}: {status}\n"

    panel_content += f"""
[bold]Paths:[/bold]
  Config: ~/.cix/
  Cache: ~/.cix/cache/
"""

    console.print(Panel(panel_content.strip(), title="cix Info", border_style="cyan"))


# =============================================================================
# Entry Point
# =============================================================================


if __name__ == "__main__":
    main()
