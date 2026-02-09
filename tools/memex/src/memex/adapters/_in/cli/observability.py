"""Observability - Rich console output.

Provides transparent feedback to users about what's happening.
"""

from rich.console import Console

console = Console()


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
    console.print(f"[green]✓[/] {message}")


def warning(message: str):
    """Log warning."""
    console.print(f"[yellow]⚠[/] {message}")


def error(message: str):
    """Log error."""
    console.print(f"[red]✗[/] {message}")


def info(message: str):
    """Log info."""
    console.print(f"[blue]ℹ[/] {message}")
