"""Output formatters for CLI commands.

Unified presentation logic - CLI commands delegate here.
"""

import json
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel

if TYPE_CHECKING:
    from memex.domain.models import Fragment


def format_fragments(
    results: list["Fragment"] | list[tuple["Fragment", float]],
    fmt: str,
    console: Console,
) -> None:
    """Format and output search results.

    Args:
        results: Either list of Fragments or list of (Fragment, score) tuples
        fmt: Output format - "panel", "json", or "ids"
        console: Rich console for output
    """
    if fmt == "json":
        _format_json(results, console)
    elif fmt == "ids":
        _format_ids(results, console)
    else:
        _format_panel(results, console)


def _format_json(
    results: list["Fragment"] | list[tuple["Fragment", float]],
    console: Console,
) -> None:
    """JSON output format."""
    output = []
    for item in results:
        if isinstance(item, tuple):
            frag, score = item
            entry = _fragment_to_dict(frag)
            entry["score"] = round(score, 4)
        else:
            entry = _fragment_to_dict(item)
        output.append(entry)
    console.print(json.dumps(output, indent=2))


def _format_ids(
    results: list["Fragment"] | list[tuple["Fragment", float]],
    console: Console,
) -> None:
    """IDs-only output format (for piping)."""
    for item in results:
        if isinstance(item, tuple):
            frag, score = item
            console.print(f"{frag.id}\t{score:.4f}")
        else:
            console.print(item.id)


def _format_panel(
    results: list["Fragment"] | list[tuple["Fragment", float]],
    console: Console,
) -> None:
    """Rich panel output format (default)."""
    console.print()
    for item in results:
        if isinstance(item, tuple):
            frag, score = item
            has_score = True
        else:
            frag = item
            score = 0.0
            has_score = False

        role_color = "cyan" if frag.role == "user" else "green"
        ts = frag.timestamp.strftime("%Y-%m-%d %H:%M") if frag.timestamp else "unknown"
        conv_id = frag.conversation_id[:8] if frag.conversation_id else "?"
        src = frag.provenance.source_kind

        header = f"[{role_color}]{frag.role}[/] • {ts} • {conv_id}... • [dim]{src}[/]"
        if has_score:
            header += f" • [yellow]{score:.2%}[/]"

        content = frag.content
        if len(content) > 500:
            content = content[:500] + "..."

        console.print(Panel(content, title=header, border_style="dim"))


def _fragment_to_dict(frag: "Fragment") -> dict:
    """Convert Fragment to dict for JSON output."""
    return {
        "id": frag.id,
        "conversation_id": frag.conversation_id,
        "role": frag.role,
        "content": frag.content,
        "timestamp": frag.timestamp.isoformat() if frag.timestamp else None,
        "source_kind": frag.provenance.source_kind,
    }
