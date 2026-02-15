"""Observability - Rich console output.

Provides transparent feedback to users about what's happening.
Two consoles: stdout for data, stderr for metadata (hints, progress, errors).
"""

import sys

from rich.console import Console

console = Console()
_stderr = Console(stderr=True)


def is_piped() -> bool:
    """Check if stdout is piped (not a TTY)."""
    return not sys.stdout.isatty()


def status(message: str):
    """Show a status spinner."""
    return console.status(f"[bold green]{message}")


def step(message: str, detail: str | None = None):
    """Log a step in the process."""
    if detail:
        console.print(f"  [dim]→[/] {message}: [cyan]{detail}[/]")
    else:
        console.print(f"  [dim]→[/] {message}")


def success(message: str):
    """Log success."""
    _stderr.print(f"[green]✓[/] {message}")


def warning(message: str):
    """Log warning."""
    _stderr.print(f"[yellow]⚠[/] {message}")


def error(message: str):
    """Log error."""
    _stderr.print(f"[red]✗[/] {message}")


def info(message: str):
    """Log info."""
    _stderr.print(f"[blue]ℹ[/] {message}")


def hint(message: str):
    """Log a next-step hint (always stderr, never pollutes piped output)."""
    _stderr.print(f"[dim]Tip: {message}[/]")


def dim(message: str):
    """Log dim metadata (always stderr — method info, progress notes)."""
    _stderr.print(f"[dim]{message}[/]")
