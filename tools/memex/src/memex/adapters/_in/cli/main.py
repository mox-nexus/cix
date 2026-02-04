"""Memex CLI - Extended memory for you and your agents.

Thin driving adapter. Wiring in composition root. Formatting in formatters.
"""

from pathlib import Path

import rich_click as click
from rich.table import Table

from memex import skill as skill_module
from memex.adapters._in.cli import observability as obs
from memex.adapters._in.cli.formatters import format_fragments
from memex.composition import (
    EmbeddingDimensionMismatchError,
    create_corpus,
    create_service,
    get_embedder,
    reranker_available,
)

# Configure command groups for better discoverability
click.rich_click.COMMAND_GROUPS = {
    "memex": [
        {
            "name": "Search",
            "commands": ["dig", "keyword", "semantic"],
        },
        {
            "name": "Ingest",
            "commands": ["ingest", "backfill", "rebuild", "reset"],
        },
        {
            "name": "Discovery",
            "commands": ["status", "corpus", "sources", "schema", "init"],
        },
        {
            "name": "Power User",
            "commands": ["query", "sql"],
        },
    ]
}


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--skill", is_flag=True, help="Output skill documentation for Claude")
@click.option("--reference", "-r", help="Specific skill reference (use with --skill)")
@click.version_option()
@click.pass_context
def main(ctx: click.Context, verbose: bool, skill: bool, reference: str | None):
    """Memex - Extended memory for you and your agents."""
    from memex.config.settings import settings

    if verbose:
        settings.verbose = True

    if skill:
        content = skill_module.get_skill(reference)
        obs.console.print(content)
        ctx.exit(0)


# --- Setup Commands ---


@main.command()
def init():
    """Initialize memex for first use.

    Creates config file and corpus directory. Run this once to get started.

    Example:
        memex init
    """
    from memex.config.settings import (
        config_exists,
        create_default_config,
        get_config_path,
        get_memex_dir,
    )

    obs.console.print("\n[bold]Welcome to Memex[/bold]\n")
    obs.console.print("Extended memory for you and your agents.\n")
    obs.console.print("Your AI conversations hold decisions, context, and trails of thought.")
    obs.console.print("Memex makes them findable - by you, and by the agents you work with.\n")

    memex_dir = get_memex_dir()
    config_path = get_config_path()

    # Create directory
    if not memex_dir.exists():
        memex_dir.mkdir(parents=True)
        obs.console.print(f"[dim]Created {memex_dir}[/dim]")

    # Create config
    if config_exists():
        obs.console.print(f"[dim]Config already exists at {config_path}[/dim]")
    else:
        config_path.write_text(create_default_config())
        obs.console.print(f"[dim]Created config at {config_path}[/dim]")

    # Initialize corpus (just create empty if not exists)
    from memex.config.settings import settings

    if not settings.corpus_path.exists():
        corpus = create_corpus()
        corpus.close()
        obs.console.print(f"[dim]Created corpus at {settings.corpus_path}[/dim]")
    else:
        obs.console.print(f"[dim]Corpus exists at {settings.corpus_path}[/dim]")

    obs.console.print("\n[bold]Next steps:[/bold]")
    obs.console.print("  1. Export your data:")
    obs.console.print("     - Claude: Settings > Account > Export Data")
    obs.console.print("     - ChatGPT: Settings > Data Controls > Export")
    obs.console.print()
    obs.console.print("  2. Import: [cyan]memex ingest ~/Downloads/conversations.json[/cyan]")
    obs.console.print()
    obs.console.print('  3. Search: [cyan]memex dig "that auth decision"[/cyan]')
    obs.console.print()
    obs.console.print("Run [cyan]memex status[/cyan] anytime to see what's indexed.\n")


# --- Search Commands ---


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--semantic-weight", "-w", default=0.6, help="Weight for semantic (0-1)")
@click.option("--no-rerank", is_flag=True, help="Disable reranking (faster, less precise)")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default="panel")
def dig(
    query: str,
    limit: int,
    source: str | None,
    semantic_weight: float,
    no_rerank: bool,
    fmt: str,
):
    """Search your conversations.

    Finds messages matching your query using keyword + semantic search.
    This is the main search command.

    Example:
        memex dig "auth implementation"
        memex dig "authentication decisions" --semantic-weight 0.8
        memex dig "OAuth" --no-rerank
    """
    # Auto-enable reranker if available and not disabled
    use_reranker = reranker_available() and not no_rerank

    with obs.status("Loading..."):
        service = create_service(with_embedder=True, with_reranker=use_reranker)

    # Show what retrieval methods are active
    methods = ["BM25"]
    if service.has_semantic_search():
        methods.append("semantic")
    else:
        coverage = service.embedding_coverage()
        if coverage[0] == 0:
            obs.console.print("[dim](semantic unavailable: run 'memex backfill' first)[/dim]")
    if service.has_reranker():
        methods.append("reranking")
    obs.console.print(f"[dim]Using: {' + '.join(methods)}[/dim]")

    results = service.hybrid_search(
        query, limit, source, semantic_weight, use_reranker=not no_rerank
    )

    if not results:
        _handle_no_results(query, service)
        return

    obs.success(f"Found {len(results)} results for '{query}'")
    format_fragments(results, fmt, obs.console)


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default="panel")
def keyword(query: str, limit: int, source: str | None, fmt: str):
    """Keyword-only search (all words must match, no embeddings).

    Faster than hybrid but misses conceptual matches.

    Example:
        memex keyword "OAuth" --limit 50
    """
    service = create_service()
    results = service.search(query, limit, source_kind=source)

    if not results:
        _handle_no_results(query, service)
        return

    obs.success(f"Found {len(results)} keyword matches for '{query}'")
    format_fragments(results, fmt, obs.console)


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--min-score", "-m", default=0.3, help="Minimum similarity (0-1)")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default="panel")
def semantic(query: str, limit: int, source: str | None, min_score: float, fmt: str):
    """Semantic search using embeddings.

    Example:
        memex semantic "authentication decisions"
        memex semantic "rate limiting" --min-score 0.5
    """
    with obs.status("Loading embedding model..."):
        service = create_service(with_embedder=True)

    if not service.has_semantic_search():
        obs.error("Semantic search not available")
        obs.info("VSS extension not installed. See: https://duckdb.org/docs/extensions/vss")
        return

    results = service.semantic_search(query, limit, source, min_score)

    if not results:
        coverage = service.embedding_coverage()
        obs.warning(f"No semantic matches for '{query}'")
        obs.info(f"Embeddings: {coverage[0]:,}/{coverage[1]:,} fragments")
        if coverage[0] < coverage[1]:
            obs.info("Tip: Run 'memex backfill' to embed remaining fragments")
        return

    obs.success(f"Found {len(results)} semantic matches")
    format_fragments(results, fmt, obs.console)


# --- Ingestion Commands ---


@main.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--no-embed", is_flag=True, help="Skip embedding (faster, keyword search only)")
def ingest(path: Path, no_embed: bool):
    """Ingest a file into the corpus.

    By default, generates embeddings for semantic search.
    Use --no-embed for faster import (keyword search only).

    Example:
        memex ingest ~/Downloads/conversations.json
        memex ingest export.zip --no-embed
    """
    from memex.config.settings import settings

    # Determine if we should embed (config default, overridden by flag)
    should_embed = settings.embed_by_default and not no_embed

    # Load service with embedder if embedding
    if should_embed:
        with obs.status("Loading embedding model..."):
            service = create_service(with_embedder=True)
    else:
        service = create_service()

    try:
        adapter = None
        for a in service.source_adapters:
            if a.can_handle(path):
                adapter = a
                break

        if adapter is None:
            obs.error(f"No adapter found for {path}")
            obs.info("Supported formats: Claude export (.json, .zip), OpenAI export")
            obs.info("Run 'memex sources' for all adapters")
            return

        obs.step("Adapter", adapter.__class__.__name__)

        # Phase 1: Parse and store (streaming, memory-efficient)
        fragment_count = 0

        def counting_generator():
            nonlocal fragment_count
            for fragment in adapter.ingest(path):
                fragment_count += 1
                yield fragment

        with obs.status("Parsing..."):
            total = service.corpus.store(counting_generator())

        obs.console.print(f"[dim]Parsed {fragment_count:,} fragments, stored {total:,} new[/dim]")

        # Phase 2: Embed if requested (batch, efficient)
        if should_embed and total > 0 and service.embedder:

            def embed_progress(processed: int, batch_total: int):
                pct = processed / batch_total * 100 if batch_total > 0 else 100
                obs.console.print(
                    f"\r[dim]Embedding... {processed:,}/{batch_total:,} ({pct:.0f}%)[/dim]", end=""
                )

            embedded = service.backfill_embeddings(settings.batch_size, embed_progress)
            obs.console.print()  # newline after progress

            if embedded < total:
                failed = total - embedded
                obs.warning(f"{failed:,} fragments failed embedding")
                obs.info("Run 'memex backfill' to retry")

        # Rebuild FTS index (DuckDB FTS doesn't auto-update)
        if hasattr(service.corpus, "rebuild_fts_index"):
            with obs.status("Building search index..."):
                service.corpus.rebuild_fts_index()

        # Final status
        if should_embed:
            obs.success(f"Ingested {total:,} fragments (ready for semantic search)")
        else:
            obs.success(f"Ingested {total:,} fragments (keyword search only)")
            obs.info("Run 'memex backfill' for semantic search")
    finally:
        service.corpus.close()


@main.command()
def rebuild():
    """Rebuild search indexes (FTS and VSS).

    Run this after manual database changes or if search seems broken.

    Example:
        memex rebuild
    """
    corpus = create_corpus()

    # Rebuild FTS index
    if hasattr(corpus, "rebuild_fts_index") and corpus.has_fts():
        with obs.status("Rebuilding FTS (BM25) index..."):
            corpus.rebuild_fts_index()
        obs.success("FTS index rebuilt")
    else:
        obs.warning("FTS not available")

    corpus.close()
    obs.info("VSS (embedding) index is managed automatically")


@main.command()
@click.option("--batch-size", "-b", default=100, help="Fragments per batch")
def backfill(batch_size: int):
    """Generate embeddings for existing fragments.

    Example:
        memex backfill
    """
    with obs.status("Loading embedding model..."):
        service = create_service(with_embedder=True)

    try:
        coverage = service.embedding_coverage()
        without = coverage[1] - coverage[0]

        if without == 0:
            obs.success("All fragments have embeddings")
            return

        obs.info(f"Fragments without embeddings: {without:,}")

        def progress(processed: int, total: int):
            pct = processed / total * 100 if total > 0 else 100
            obs.console.print(f"\r[dim]Progress: {processed:,}/{total:,} ({pct:.1f}%)[/]", end="")

        updated = service.backfill_embeddings(batch_size, progress)

        obs.console.print()
        obs.success(f"Generated embeddings for {updated:,} fragments")
    finally:
        service.corpus.close()


@main.command()
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.option("--backup", "-b", is_flag=True, help="Backup before deleting")
def reset(yes: bool, backup: bool):
    """Delete the corpus and start fresh.

    Use this before re-ingesting with a different embedding model,
    or to clear all data and start over.

    Example:
        memex reset              # Interactive confirmation
        memex reset --yes        # Skip confirmation
        memex reset --backup     # Backup to corpus.duckdb.bak first
    """
    from memex.config.settings import settings

    corpus_path = settings.corpus_path

    if not corpus_path.exists():
        obs.warning("No corpus found. Nothing to reset.")
        return

    # Show what will be deleted
    try:
        corpus = create_corpus()
        stats = corpus.stats()
        corpus.close()
        obs.console.print(f"\n[bold]Corpus:[/bold] {corpus_path}")
        obs.console.print(f"[bold]Fragments:[/bold] {stats['total_fragments']:,}")
        obs.console.print()
    except Exception:
        obs.console.print(f"\n[bold]Corpus:[/bold] {corpus_path}")
        obs.console.print()

    if not yes:
        obs.console.print("[yellow]This will permanently delete all data.[/yellow]")
        confirm = obs.console.input("Type 'reset' to confirm: ")
        if confirm.strip().lower() != "reset":
            obs.info("Aborted.")
            return

    # Backup if requested
    if backup:
        backup_path = corpus_path.with_suffix(".duckdb.bak")
        import shutil

        shutil.copy2(corpus_path, backup_path)
        obs.success(f"Backed up to {backup_path}")

    # Delete corpus
    corpus_path.unlink()
    obs.success("Corpus deleted. Run 'memex ingest' to start fresh.")


# --- Discovery Commands ---


@main.command()
def status():
    """Show memex configuration and capabilities.

    Displays corpus stats, embedding coverage, and which features
    are active (reranking, semantic search, etc.).
    """
    from memex.config.settings import settings

    # Get embedder info (doesn't require corpus)
    embedder = get_embedder()

    # Try to create service - may fail if corpus dimensions mismatch
    service = None
    corpus_dims = None
    try:
        service = create_service(with_embedder=True, with_reranker=reranker_available())
        stats = service.stats()
        coverage = service.embedding_coverage()
        dimension_mismatch = False
    except EmbeddingDimensionMismatchError:
        # Show status even with mismatch, but flag the issue
        dimension_mismatch = True
        corpus = create_corpus()  # FTS-only mode
        stats = corpus.stats()
        corpus_dims = corpus.embedding_dimensions()
        coverage = (0, stats["total_fragments"])  # All need re-embedding
        corpus.close()

    obs.console.print("\n[bold]Memex Configuration[/bold]")
    obs.console.print("─" * 40)

    # Corpus info
    obs.console.print(f"[cyan]Corpus:[/cyan]     {settings.corpus_path}")
    obs.console.print(f"[cyan]Fragments:[/cyan]  {stats['total_fragments']:,}")
    if coverage[1] > 0:
        pct = coverage[0] / coverage[1] * 100
        obs.console.print(f"[cyan]Embeddings:[/cyan] {coverage[0]:,}/{coverage[1]:,} ({pct:.0f}%)")
    obs.console.print()

    # Capabilities
    obs.console.print("[bold]Active Capabilities[/bold]")

    # Embedding model
    model_info = f"[green]{embedder.model_name}[/green] ({embedder.dimensions}-dim)"
    obs.console.print(f"  Embedding Model: {model_info}")

    # Keyword search
    obs.console.print("  Keyword Search:  [green]BM25 via DuckDB FTS[/green]")

    # Semantic search
    if dimension_mismatch:
        obs.console.print("  Semantic Search: [red]Dimension mismatch[/red] (requires reset)")
    elif service and service.has_semantic_search():
        obs.console.print("  Semantic Search: [green]HNSW via DuckDB VSS[/green]")
    else:
        obs.console.print("  Semantic Search: [yellow]Not available[/yellow] (VSS not loaded)")

    # Reranking
    if dimension_mismatch:
        if reranker_available():
            obs.console.print("  Reranking:       [dim]Available (after reset)[/dim]")
        else:
            obs.console.print(
                "  Reranking:       [yellow]Not installed[/yellow] (uv add sentence-transformers)"
            )
    elif service and service.has_reranker():
        model_name = service.reranker_model_name() or "cross-encoder"
        obs.console.print(f"  Reranking:       [green]{model_name}[/green]")
    elif reranker_available():
        obs.console.print("  Reranking:       [dim]Available (auto-enabled in dig)[/dim]")
    else:
        obs.console.print(
            "  Reranking:       [yellow]Not installed[/yellow] (uv add sentence-transformers)"
        )

    obs.console.print()

    # Pending actions / issues
    pending = []

    if dimension_mismatch:
        msg = (
            f"[red]Corpus has {corpus_dims}-dim embeddings "
            f"but embedder is {embedder.dimensions}-dim.[/red]\n"
            f"    Run: [bold]memex reset[/bold] then re-ingest"
        )
        pending.append(msg)
    elif coverage[0] < coverage[1]:
        missing = coverage[1] - coverage[0]
        pending.append(f"{missing:,} fragments need embeddings. Run: [bold]memex backfill[/bold]")

    if pending:
        obs.console.print("[bold]Pending[/bold]")
        for item in pending:
            obs.console.print(f"  • {item}")
        obs.console.print()


@main.command()
def corpus():
    """Show corpus statistics."""
    from memex.config.settings import settings

    service = create_service()
    stats = service.stats()

    table = Table(title="Corpus Statistics", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold")

    table.add_row("Fragments", f"{stats['total_fragments']:,}")
    table.add_row("Conversations", f"{stats['conversations']:,}")
    table.add_row("Sources", str(stats["sources"]))
    table.add_row("Corpus Path", str(settings.corpus_path))
    if stats["earliest"]:
        table.add_row("Earliest", stats["earliest"].strftime("%Y-%m-%d"))
    if stats["latest"]:
        table.add_row("Latest", stats["latest"].strftime("%Y-%m-%d"))

    obs.console.print(table)


@main.command(name="schema")
def schema_cmd():
    """Show corpus schema."""
    service = create_service()
    schema = service.schema()

    for table_name, columns in schema.items():
        table = Table(title=f"[bold]{table_name}[/]", show_header=True)
        table.add_column("Column", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Nullable")

        for col in columns:
            table.add_row(col["name"], col["type"], "✓" if col["nullable"] else "✗")
        obs.console.print(table)


@main.command()
def sources():
    """Show available source adapters."""
    service = create_service()

    table = Table(title="Available Sources", show_header=True)
    table.add_column("Source Kind", style="cyan")
    table.add_column("Adapter", style="green")
    table.add_column("Formats")

    for adapter in service.source_adapters:
        table.add_row(adapter.source_kind(), adapter.__class__.__name__, ".json, .zip")

    obs.console.print(table)
    obs.console.print()
    obs.info("To add more sources, export from:")
    obs.console.print("  • Claude.ai: Settings → Account → Export Data")
    obs.console.print("  • ChatGPT: Settings → Data Controls → Export")


# --- SQL Escape Hatch ---


@main.command()
@click.argument("sql_query")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "json", "csv"]), default="table")
def query(sql_query: str, fmt: str):
    """Execute raw SQL (DuckDB-specific escape hatch).

    Example:
        memex query "SELECT COUNT(*) FROM fragments"
    """
    import json

    corpus = create_corpus()
    try:
        rows = corpus.query_sql(sql_query)

        if not rows:
            obs.warning("No results")
            return

        obs.success(f"{len(rows)} rows")

        if fmt == "json":
            obs.console.print(json.dumps(rows, indent=2, default=str))
        elif fmt == "csv":
            for row in rows:
                obs.console.print(",".join(str(v) for v in row))
        else:
            for row in rows:
                obs.console.print(str(row))
    finally:
        corpus.close()


@main.command()
def sql():
    """Interactive SQL shell (DuckDB-specific)."""
    from memex.config.settings import settings

    corpus = create_corpus()

    obs.console.print("[bold]Memex SQL Shell[/] (type 'exit' to quit)")
    obs.console.print(f"[dim]Corpus: {settings.corpus_path}[/]")

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


# --- Helpers ---


def _handle_no_results(query: str, service):
    """Helpful guidance on no results."""
    try:
        stats = service.stats()
        if stats["total_fragments"] == 0:
            obs.warning(f"No results for '{query}'")
            obs.info("Corpus is empty. Run 'memex ingest <file>' first.")
        else:
            obs.warning(f"No results for '{query}'")
            obs.info(f"Corpus has {stats['total_fragments']:,} fragments.")
            obs.info("Tip: Try different terms or adjust --semantic-weight")
            coverage = service.embedding_coverage()
            if coverage[0] < coverage[1]:
                missing = coverage[1] - coverage[0]
                obs.info(f"Tip: Run 'memex backfill' ({missing:,} need embeddings)")
    except Exception:
        obs.warning(f"No results for '{query}'")


if __name__ == "__main__":
    main()
