"""Output formatters for CLI commands.

Unified presentation logic - CLI commands delegate here.
"""

import json
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if TYPE_CHECKING:
    from memex.domain.models import Fragment


def format_fragments(
    results: list["Fragment"] | list[tuple["Fragment", float]],
    fmt: str,
    console: Console,
    save_register: bool = True,
) -> None:
    """Format and output search results.

    Args:
        results: Either list of Fragments or list of (Fragment, score) tuples
        fmt: Output format - "panel", "json", or "ids"
        console: Rich console for output
        save_register: Whether to save results to last-results register
    """
    if save_register and results:
        _save_to_register(results)

    if fmt == "json":
        _format_json(results, console)
    elif fmt == "ids":
        _format_ids(results, console)
    else:
        _format_panel(results, console)


def format_thread(
    fragments: list["Fragment"],
    console: Console,
) -> None:
    """Format a conversation thread — all messages in order."""
    if not fragments:
        console.print("[dim]Empty conversation[/dim]")
        return

    conv_id = fragments[0].conversation_id or "?"
    src = fragments[0].provenance.source_kind
    first_ts = fragments[0].timestamp
    last_ts = fragments[-1].timestamp

    # Thread header
    console.print()
    header = f"[bold]Thread[/bold] {conv_id[:12]}... • [dim]{src}[/dim]"
    if first_ts:
        header += f" • {first_ts.strftime('%Y-%m-%d')}"
        if last_ts and last_ts.date() != first_ts.date():
            header += f" → {last_ts.strftime('%Y-%m-%d')}"
    console.print(header)
    console.print(f"[dim]{len(fragments)} messages[/dim]")
    console.print()

    for frag in fragments:
        role_color = "cyan" if frag.role == "user" else "green"
        ts = frag.timestamp.strftime("%H:%M") if frag.timestamp else ""

        content = frag.content
        if len(content) > 2000:
            content = content[:2000] + "\n[dim]... (truncated)[/dim]"

        title = f"[{role_color}]{frag.role}[/]"
        if ts:
            title += f" • {ts}"

        console.print(Panel(content, title=title, border_style="dim", expand=True))


def format_timeline(
    conversations: list[dict],
    console: Console,
    offset: int = 0,
) -> None:
    """Format conversation list as a timeline table."""
    if not conversations:
        console.print("[dim]No conversations found[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="yellow", width=4)
    table.add_column("Date", style="dim", width=12)
    table.add_column("Messages", justify="right", width=5)
    table.add_column("Source", style="dim", width=10)
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Preview", ratio=1)

    for i, conv in enumerate(conversations, start=offset + 1):
        ts = conv["last_timestamp"]
        date_str = ts.strftime("%Y-%m-%d") if ts else "?"
        preview = conv.get("preview") or "[dim]no user message[/dim]"
        conv_id = conv["conversation_id"][:8] + "..." if conv["conversation_id"] else "?"

        table.add_row(
            str(i),
            date_str,
            str(conv["message_count"]),
            conv["source_kind"] or "?",
            conv_id,
            preview,
        )

    console.print(table)
    console.print("\n[dim]Use [cyan]memex thread @N[/cyan] to view a conversation[/dim]")


def _save_to_register(results: list) -> None:
    """Save result metadata to last-results register."""
    from memex.adapters._in.cli.last_results import save_results

    entries = []
    for item in results:
        frag = item[0] if isinstance(item, tuple) else item
        entries.append(
            {
                "id": frag.id,
                "conversation_id": frag.conversation_id,
            }
        )
    save_results(entries)


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
    """Rich panel output format (default), with display indices.

    Rank order (@N) is the score — raw logits are meaningless to humans.
    Scores are preserved in json/ids formats for programmatic consumption.
    """
    console.print()
    for i, item in enumerate(results, start=1):
        frag = item[0] if isinstance(item, tuple) else item

        role_color = "cyan" if frag.role == "user" else "green"
        ts = frag.timestamp.strftime("%Y-%m-%d %H:%M") if frag.timestamp else "unknown"
        conv_id = frag.conversation_id[:8] if frag.conversation_id else "?"
        src = frag.provenance.source_kind

        header = (
            f"[yellow]@{i}[/] [{role_color}]{frag.role}[/] • {ts} • {conv_id}... • [dim]{src}[/]"
        )

        content = frag.content
        if len(content) > 500:
            content = content[:500] + "..."

        console.print(Panel(content, title=header, border_style="dim"))


def format_trail(
    trail_name: str,
    entries: list[tuple["Fragment", str]],
    console: Console,
) -> None:
    """Format a trail — named sequence of fragments with optional notes."""
    if not entries:
        console.print(f"[dim]Trail '{trail_name}' is empty[/dim]")
        return

    console.print()
    console.print(f"[bold]Trail:[/bold] {trail_name} ({len(entries)} entries)")
    console.print()

    for i, (frag, note) in enumerate(entries, start=1):
        role_color = "cyan" if frag.role == "user" else "green"
        ts = frag.timestamp.strftime("%Y-%m-%d %H:%M") if frag.timestamp else "?"
        conv_id = frag.conversation_id[:8] if frag.conversation_id else "?"
        src = frag.provenance.source_kind

        title = (
            f"[yellow]#{i}[/] [{role_color}]{frag.role}[/] • {ts} • {conv_id}... • [dim]{src}[/]"
        )
        if note:
            title += f" • [italic]{note}[/]"

        content = frag.content
        if len(content) > 1000:
            content = content[:1000] + "\n[dim]... (truncated)[/dim]"

        console.print(Panel(content, title=title, border_style="dim", expand=True))

        # Trail connector between entries
        if i < len(entries):
            console.print("[dim]  │[/dim]")


def format_trail_list(
    trails: list[dict],
    console: Console,
) -> None:
    """Format list of trails as a table."""
    if not trails:
        console.print('[dim]No trails yet. Create one with: memex trail create "name"[/dim]')
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name", style="cyan")
    table.add_column("Entries", justify="right")
    table.add_column("Created", style="dim")
    table.add_column("Description", ratio=1)

    for t in trails:
        created = t["created_at"].strftime("%Y-%m-%d") if t["created_at"] else "?"
        table.add_row(
            t["name"],
            str(t["entry_count"]),
            created,
            t.get("description") or "",
        )

    console.print(table)


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
