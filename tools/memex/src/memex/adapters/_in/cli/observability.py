"""Observability - Rich console + optional OTEL.

Provides transparent feedback to users about what's happening.
OTEL tracing is opt-in via MEMEX_OTEL_ENABLED=true.
"""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Any

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from memex.config.settings import settings

console = Console()

# OTEL tracer (lazy init)
_tracer = None


def get_tracer():
    """Get OTEL tracer if enabled."""
    global _tracer
    if not settings.otel_enabled:
        return None

    if _tracer is None:
        try:
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            provider = TracerProvider()
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_endpoint))
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            _tracer = trace.get_tracer(settings.otel_service_name)
        except ImportError:
            console.print("[yellow]OTEL enabled but opentelemetry not installed[/]")
            return None

    return _tracer


@contextmanager
def span(name: str, attributes: dict | None = None):
    """Create an OTEL span if tracing is enabled."""
    tracer = get_tracer()
    if tracer:
        with tracer.start_as_current_span(name, attributes=attributes or {}) as s:
            yield s
    else:
        yield None


def traced(name: str | None = None):
    """Decorator to trace a function."""

    def decorator(fn: Callable) -> Callable:
        span_name = name or fn.__name__

        @wraps(fn)
        def wrapper(*args, **kwargs):
            with span(span_name):
                return fn(*args, **kwargs)

        return wrapper

    return decorator


@contextmanager
def progress_context(description: str) -> Iterator[Progress]:
    """Rich progress context for long operations."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        yield progress


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


def verbose(message: str):
    """Log verbose message (only if verbose mode)."""
    if settings.verbose:
        console.print(f"[dim]{message}[/]")


def table(title: str, columns: list[tuple[str, str]], rows: list[list[Any]]) -> None:
    """Display a table."""
    t = Table(title=title)
    for name, style in columns:
        t.add_column(name, style=style)
    for row in rows:
        t.add_row(*[str(c) for c in row])
    console.print(t)
