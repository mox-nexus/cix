"""Memex CLI - Excavating Collaborative Intelligence Artifacts.

Driving adapter for the CLI interface.
"""

from pathlib import Path

import rich_click as click
from rich.panel import Panel
from rich.table import Table

from memex.adapters._out.corpus import DuckDBCorpus
from memex.adapters._out.sources import ClaudeConversationsAdapter, OpenAIConversationsAdapter
from memex.domain.services import ExcavationService
from memex.config.settings import settings
from memex.adapters._in.cli import observability as obs
from memex import skill as skill_module


def get_service() -> ExcavationService:
    """Wire up the service with adapters."""
    corpus = DuckDBCorpus(settings.corpus_path)
    adapters = [
        ClaudeConversationsAdapter(),
        OpenAIConversationsAdapter(),
    ]
    return ExcavationService(corpus, adapters)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.version_option()
def main(verbose: bool):
    """Memex - Excavating Collaborative Intelligence Artifacts."""
    if verbose:
        settings.verbose = True


@main.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def ingest(path: Path):
    """Ingest a file into the corpus.

    Example:
        memex ingest ~/Downloads/conversations.json
    """
    with obs.span("ingest", {"path": str(path)}):
        service = get_service()

        obs.step("Source", path.name)
        obs.step("Corpus", str(settings.corpus_path))
        obs.verbose(f"Full path: {path.absolute()}")

        # Find the right adapter
        adapter = None
        for a in service.source_adapters:
            if a.can_handle(path):
                adapter = a
                break

        if adapter is None:
            obs.error(f"No adapter found for {path}")
            return

        obs.step("Adapter", adapter.__class__.__name__)

        # Count fragments while ingesting
        fragment_count = 0

        def counting_generator():
            nonlocal fragment_count
            with obs.status(f"Parsing {path.name}..."):
                with obs.span("parse"):
                    for fragment in adapter.ingest(path):
                        fragment_count += 1
                        yield fragment

        with obs.span("store"):
            total = service.corpus.store(counting_generator())

        obs.success(f"Ingested {total:,} new fragments from {path.name}")
        obs.step("Parsed", f"{fragment_count:,} fragments")

        stats = service.stats()
        obs.info(
            f"Corpus: {stats['total_fragments']:,} fragments, "
            f"{stats['conversations']:,} conversations"
        )


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
def dig(query: str, limit: int, source: str | None):
    """Search the corpus.

    Example:
        memex dig "auth implementation"
        memex dig "rate limiting" --limit 50
        memex dig "hexagonal" --source claude_conversations
    """
    with obs.span("dig", {"query": query, "limit": limit}):
        service = get_service()

        obs.verbose(f"Query: {query}")
        obs.verbose(f"Limit: {limit}")

        with obs.status("Searching..."):
            results = service.search(query, limit)

        if not results:
            obs.warning(f"No results for '{query}'")
            return

        obs.success(f"Found {len(results)} results for '{query}'")
        obs.console.print()

        for frag in results:
            # source_kind is now a string, not enum
            if source and frag.provenance.source_kind != source:
                continue

            role_color = "cyan" if frag.role == "user" else "green"
            ts = frag.timestamp.strftime("%Y-%m-%d %H:%M") if frag.timestamp else "unknown"
            conv_id = frag.conversation_id[:8] if frag.conversation_id else "?"
            src = frag.provenance.source_kind

            header = f"[{role_color}]{frag.role}[/] • {ts} • {conv_id}... • [dim]{src}[/]"

            content = frag.content
            if len(content) > 500:
                content = content[:500] + "..."

            obs.console.print(Panel(content, title=header, border_style="dim"))


@main.command()
@click.argument("sql")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "json", "csv"]), default="table")
def query(sql: str, fmt: str):
    """Execute raw SQL (power-user escape hatch).

    NOTE: This is a DuckDB-specific feature, not part of the portable CorpusPort.

    Example:
        memex query "SELECT COUNT(*) FROM fragments"
        memex query "SELECT * FROM fragments LIMIT 5" --format json
    """
    with obs.span("query", {"sql": sql}):
        # Direct access to DuckDB adapter for SQL escape hatch
        corpus = DuckDBCorpus(settings.corpus_path)
        obs.verbose(f"SQL: {sql}")

        try:
            with obs.status("Executing query..."):
                rows = corpus.query_sql(sql)

            if not rows:
                obs.warning("No results")
                return

            obs.success(f"{len(rows)} rows")
            obs.console.print()

            if fmt == "json":
                import json
                obs.console.print(json.dumps(rows, indent=2, default=str))
            elif fmt == "csv":
                if rows:
                    # Simple CSV output
                    obs.console.print(",".join(str(v) for v in rows[0]))
                    for row in rows[1:]:
                        obs.console.print(",".join(str(v) for v in row))
            else:
                for row in rows:
                    obs.console.print(str(row))
        except Exception as e:
            obs.error(str(e))
        finally:
            corpus.close()


@main.command()
def corpus():
    """Show corpus statistics."""
    with obs.span("corpus"):
        service = get_service()

        try:
            with obs.status("Loading corpus stats..."):
                stats = service.stats()
        except Exception:
            obs.warning("Corpus is empty. Run 'memex ingest <file>' first.")
            return

        table = Table(title="Corpus Statistics", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold")

        table.add_row("Fragments", f"{stats['total_fragments']:,}")
        table.add_row("Conversations", f"{stats['conversations']:,}")
        table.add_row("Sources", str(stats['sources']))
        table.add_row("Corpus Path", str(settings.corpus_path))
        if stats['earliest']:
            table.add_row("Earliest", stats['earliest'].strftime("%Y-%m-%d"))
        if stats['latest']:
            table.add_row("Latest", stats['latest'].strftime("%Y-%m-%d"))

        obs.console.print(table)


@main.command(name="schema")
def schema_cmd():
    """Show corpus schema."""
    with obs.span("schema"):
        service = get_service()
        schema = service.schema()

        for table_name, columns in schema.items():
            table = Table(title=f"[bold]{table_name}[/]", show_header=True)
            table.add_column("Column", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Nullable")

            for col in columns:
                table.add_row(
                    col["name"],
                    col["type"],
                    "✓" if col["nullable"] else "✗"
                )
            obs.console.print(table)
            obs.console.print()


@main.command()
def sql():
    """Interactive SQL shell (DuckDB-specific)."""
    with obs.span("sql_shell"):
        # Direct DuckDB access for interactive SQL
        corpus = DuckDBCorpus(settings.corpus_path)

        obs.console.print("[bold]Memex SQL Shell[/] (type 'exit' to quit)")
        obs.console.print(f"[dim]Corpus: {settings.corpus_path}[/]")
        obs.console.print("[dim]Table: fragments[/]\n")

        try:
            while True:
                try:
                    sql_input = obs.console.input("[cyan]memex>[/] ").strip()
                    if sql_input.lower() in ("exit", "quit", "q"):
                        break
                    if not sql_input:
                        continue

                    rows = corpus.query_sql(sql_input)
                    if rows:
                        for row in rows[:100]:
                            obs.console.print(str(row))
                        if len(rows) > 100:
                            obs.console.print(f"[dim]({len(rows)} rows, showing first 100)[/]")
                    else:
                        obs.console.print("[dim]OK[/]")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    obs.error(str(e))
        finally:
            corpus.close()

        obs.console.print("\n[dim]Goodbye.[/]")


@main.command()
def sources():
    """Show available source adapters."""
    service = get_service()

    table = Table(title="Available Sources", show_header=True)
    table.add_column("Source Kind", style="cyan")
    table.add_column("Adapter", style="green")
    table.add_column("Formats")

    for adapter in service.source_adapters:
        # source_kind is now a string, not enum
        table.add_row(
            adapter.source_kind(),
            adapter.__class__.__name__,
            ".json, .zip"
        )

    obs.console.print(table)
    obs.console.print()
    obs.info("To add more sources, export from:")
    obs.console.print("  • Claude.ai: Settings → Account → Export Data")
    obs.console.print("  • ChatGPT: Settings → Data Controls → Export")


@main.command()
@click.option("--reference", "-r", help="Specific reference to load")
@click.option("--list", "-l", "list_refs", is_flag=True, help="List available references")
@click.option("--source", "-s", help="Get skill for a specific source adapter")
@click.option("--corpus", "-c", "show_corpus", is_flag=True, help="Get skill for corpus backend")
def skill(reference: str | None, list_refs: bool, source: str | None, show_corpus: bool):
    """Output skill documentation for Claude.

    Example:
        memex skill                          # Main skill
        memex skill --reference query        # Query patterns
        memex skill -l                       # List references
        memex skill --source claude_conversations  # Source adapter skill
        memex skill --corpus                 # Corpus backend skill
    """
    service = get_service()

    if source:
        content = service.get_source_skill(source)
        if content:
            obs.console.print(content)
        else:
            obs.error(f"Unknown source: {source}")
            obs.info(f"Available: {', '.join(service.available_sources())}")
        return

    if show_corpus:
        obs.console.print(service.get_corpus_skill())
        return

    if list_refs:
        refs = skill_module.list_references()
        obs.console.print("[bold]Available references:[/]")
        for ref in refs:
            obs.console.print(f"  • {ref}")
        return

    content = skill_module.get_skill(reference)
    obs.console.print(content)


if __name__ == "__main__":
    main()
