"""Memex CLI - Extended memory for you and your agents.

Thin driving adapter. Wiring in composition root. Formatting in formatters.
"""

from pathlib import Path

import rich_click as click
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from memex import skill as skill_module
from memex.adapters._in.cli import observability as obs
from memex.adapters._in.cli.formatters import (
    format_fragments,
    format_thread,
    format_timeline,
    format_trail,
    format_trail_list,
)
from memex.adapters._in.cli.last_results import (
    resolve_conversation_ref,
    resolve_fragment_ref,
    save_results,
)
from memex.composition import (
    EmbeddingDimensionMismatchError,
    create_corpus,
    create_service,
    get_embedder,
    reranker_available,
)


def _default_format() -> str:
    """TTY-aware default output format.

    Panel for humans at a terminal, ids for piped output.
    """
    return "ids" if obs.is_piped() else "panel"


# Configure command groups for better discoverability
click.rich_click.COMMAND_GROUPS = {
    "memex": [
        {
            "name": "Search",
            "commands": ["dig", "keyword", "semantic"],
        },
        {
            "name": "View",
            "commands": ["thread", "timeline", "similar"],
        },
        {
            "name": "Ingest",
            "commands": ["ingest", "backfill", "rebuild", "reset"],
        },
        {
            "name": "Discovery",
            "commands": ["status", "init"],
        },
        {
            "name": "Graph",
            "commands": ["trail"],
        },
        {
            "name": "Power User",
            "commands": ["query", "sql", "corpus", "sources", "schema"],
        },
    ]
}


def _set_global_store(ctx: click.Context, param: click.Parameter, value: bool) -> bool:
    """Eager callback: force global ~/.memex/ store before settings construct."""
    if value:
        import os

        os.environ["MEMEX_CORPUS_PATH"] = str(Path.home() / ".memex" / "corpus.duckdb")
        os.environ["MEMEX_FORCE_GLOBAL"] = "1"
    return value


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option(
    "--global",
    "use_global",
    is_flag=True,
    is_eager=True,
    expose_value=True,
    callback=_set_global_store,
    help="Force global ~/.memex/ store (ignore local .memex/)",
)
@click.option("--skill", is_flag=True, help="Output skill documentation for Claude")
@click.option("--reference", "-r", help="Specific skill reference (use with --skill)")
@click.version_option(prog_name="memex (experimental)")
@click.pass_context
def main(
    ctx: click.Context,
    verbose: bool,
    use_global: bool,
    skill: bool,
    reference: str | None,
):
    """Memex - Extended memory for you and your agents. [experimental]"""
    if verbose:
        import os

        os.environ["MEMEX_VERBOSE"] = "true"

    if skill:
        content = skill_module.get_skill(reference)
        obs.console.print(content)
        ctx.exit(0)


# --- Setup Commands ---


@main.command()
@click.option("--local", is_flag=True, help="Create project-local .memex/ in current directory")
@click.option("--yes", "-y", is_flag=True, help="Skip prompts (scripting)")
@click.option(
    "--import-file",
    "import_path",
    type=click.Path(exists=True, path_type=Path),
    help="Import a file immediately after init",
)
def init(local: bool, yes: bool, import_path: Path | None):
    """Initialize memex for first use.

    Creates config, corpus, and optionally imports conversations.
    Interactive mode (default): Guides you through setup and import.
    Scripting mode (--yes): Creates store silently, no prompts.

    Example:
        memex init                                       # Guided wizard
        memex init --yes                                 # Silent (CI/scripts)
        memex init --import-file ~/Downloads/conv.json   # Init + import
        memex init --local                               # Project-local store
    """
    if local:
        _init_local()
        return

    context = _detect_init_context()
    _init_global_store(quiet=yes)

    # Import: flag takes precedence, then wizard, then hint
    if import_path:
        _ingest_inline(import_path)
    elif not yes and context["is_tty"] and context["first_run"]:
        chosen = _run_import_wizard(context)
        if chosen:
            _ingest_inline(chosen)
        else:
            obs.success("Memex initialized")
            obs.hint("memex ingest <file> when you're ready to import")
    else:
        obs.hint("memex ingest ~/Downloads/conversations.json")


def _init_global_store(*, quiet: bool = False):
    """Initialize global ~/.memex/ store (dirs, config, corpus).

    Pure infrastructure — no wizard prompts. The init() command
    handles UX flow (wizard vs silent) after this returns.
    When quiet=True (--yes mode), suppresses welcome banner.
    """
    from memex.config.settings import (
        config_exists,
        create_default_config,
        get_global_config_path,
        get_global_memex_dir,
    )

    if not quiet:
        obs.console.print("\n[bold]Welcome to Memex[/bold]\n")
        obs.console.print("Extended memory for you and your agents.")
        obs.console.print("Your AI conversations hold decisions, context, and trails of thought.")
        obs.console.print("Memex makes them findable.\n")

    memex_dir = get_global_memex_dir()
    config_path = get_global_config_path()

    if not memex_dir.exists():
        memex_dir.mkdir(parents=True)
        obs.step(f"Created {memex_dir}")

    if config_exists():
        obs.dim(f"Config already exists at {config_path}")
    else:
        config_path.write_text(create_default_config())
        obs.step(f"Created config at {config_path}")

    corpus_path = memex_dir / "corpus.duckdb"
    if not corpus_path.exists():
        from memex.composition import initialize_corpus

        initialize_corpus(corpus_path)
        obs.step(f"Created corpus at {corpus_path}")
    else:
        obs.dim(f"Corpus exists at {corpus_path}")


def _init_local():
    """Initialize project-local .memex/ store in CWD."""
    from memex.config.settings import create_default_config

    local_dir = Path.cwd() / ".memex"

    if local_dir.exists():
        obs.warning(f"Local .memex/ already exists at {local_dir}")
        obs.info("This directory is already a memex workspace.")
        return

    obs.console.print("\n[bold]Initializing local memex store[/bold]\n")

    # Create directory
    local_dir.mkdir(parents=True)
    obs.step(f"Created {local_dir}")

    # Create local config
    corpus_path = local_dir / "corpus.duckdb"
    config_path = local_dir / "config.toml"
    config_path.write_text(create_default_config(corpus_path))
    obs.step(f"Created config at {config_path}")

    # Initialize empty corpus
    from memex.composition import initialize_corpus

    initialize_corpus(corpus_path)
    obs.step(f"Created corpus at {corpus_path}")

    obs.console.print()
    obs.success("Local memex workspace ready")
    obs.info("All memex commands in this directory (and subdirectories) will use this store.")
    obs.info("Tip: Add .memex/ to your .gitignore")
    obs.console.print()


# --- Init Wizard Helpers ---


def _detect_init_context() -> dict:
    """Detect user context for guided init wizard.

    Called BEFORE store creation so first_run reflects true state.
    Export scanning is top-level only (~/Downloads, ~/Desktop) — fast, non-invasive.
    """
    import sys

    from memex.config.settings import config_exists

    context = {
        "first_run": not config_exists(),
        "is_tty": not obs.is_piped() and sys.stdin.isatty(),
    }

    exports: list[Path] = []
    scan_dirs = [Path.home() / "Downloads", Path.home() / "Desktop"]
    patterns = ["conversations.json", "conversations*.json", "chat*.json"]

    for d in scan_dirs:
        if d.is_dir():
            for pattern in patterns:
                for f in d.glob(pattern):
                    if f.is_file() and f.stat().st_size > 100:
                        exports.append(f)
            # Claude exports are often zipped — match export-like names only
            for zip_pattern in ["claude*.zip", "*export*.zip", "*conversations*.zip"]:
                for f in d.glob(zip_pattern):
                    if f.is_file() and f.stat().st_size > 1000:
                        exports.append(f)

    # Newest first, deduplicate, cap at 5
    exports = sorted(set(exports), key=lambda f: f.stat().st_mtime, reverse=True)
    context["exports"] = exports[:5]
    return context


def _run_import_wizard(context: dict) -> Path | None:
    """Interactive import wizard. Returns path to ingest, or None to skip.

    Only called when: first_run + TTY + global init.
    Uses click.prompt for TTY-safe input with defaults and validation.
    """
    obs.console.print()
    obs.console.print("─" * 40)
    obs.console.print()
    obs.console.print("[bold]Ready to import your conversations?[/bold]")
    obs.console.print()

    source = click.prompt(
        "  Where did you export from?\n\n"
        "  [1] Claude  (Settings > Account > Export Data)\n"
        "  [2] ChatGPT (Settings > Data Controls > Export)\n"
        "  [3] I'll do this later\n\n"
        "  Choice",
        type=click.IntRange(1, 3),
        default=1,
    )

    if source == 3:
        obs.console.print()
        obs.info("When you're ready: memex ingest ~/Downloads/conversations.json")
        obs.info("Run memex status anytime to see what's indexed.")
        return None

    # Source-specific export instructions
    if source == 1:
        export_hint = "claude.ai → Settings → Account → Export Data"
    else:
        export_hint = "chatgpt.com → Settings → Data Controls → Export"

    # Check for detected exports
    exports = context.get("exports", [])
    if exports:
        obs.console.print()
        obs.console.print("  [dim]Found likely exports:[/dim]")
        for i, f in enumerate(exports, 1):
            size_mb = f.stat().st_size / (1024 * 1024)
            age = _human_age(f.stat().st_mtime)
            obs.console.print(f"    [{i}] {f.name} ({size_mb:.1f} MB, {age})")

        choice = click.prompt(
            "\n  Which file? (0 to enter path manually)",
            type=click.IntRange(0, len(exports)),
            default=1,
        )
        if choice > 0:
            return exports[choice - 1]

    # Manual entry — no exports found or user chose manual
    obs.console.print()
    if not exports:
        obs.console.print("  [dim]No exports found in ~/Downloads or ~/Desktop.[/dim]")
        obs.console.print(f"  [dim]To export: {export_hint}[/dim]")

    path_str = click.prompt(
        "  File path (Enter to skip)",
        default="",
        show_default=False,
    )

    if path_str.strip():
        p = Path(path_str.strip()).expanduser()
        if p.exists():
            return p
        obs.error(f"File not found: {p}")
        obs.info("When you find the file: memex ingest <path>")

    return None


def _ingest_inline(path: Path):
    """Run ingest as part of init wizard — always embeds, friendly output."""
    _do_ingest(path, embed=True, wizard=True)


def _do_ingest(path: Path, *, embed: bool = True, wizard: bool = False):
    """Shared ingest logic for both init wizard and ingest command.

    Calls through ExcavationService — no direct infrastructure access.
    Args:
        embed: Generate embeddings (True) or keyword-only (False).
        wizard: Use friendly wizard output (True) or standard CLI output (False).
    """
    from memex.config.settings import get_settings

    if embed:
        with obs.status("Loading embedding model..."):
            service = create_service(with_embedder=True)
    else:
        service = create_service()

    try:
        with obs.status("Parsing..."):
            parsed, stored = service.ingest(path)

        obs.dim(f"Parsed {parsed:,} fragments, stored {stored:,} new")

        if embed and stored > 0 and service.embedder:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed:,}/{task.total:,})"),
                TimeElapsedColumn(),
                console=obs.console,
                transient=True,
            ) as progress_bar:
                task = progress_bar.add_task("Embedding", total=stored)

                def embed_progress(processed: int, total: int):
                    progress_bar.update(task, completed=processed, total=total)

                embedded = service.backfill_embeddings(get_settings().batch_size, embed_progress)

            if not wizard and embedded < stored:
                failed = stored - embedded
                obs.warning(f"{failed:,} fragments failed embedding")
                obs.info("Run 'memex backfill' to retry")

        with obs.status("Building search index..."):
            service.rebuild_search_index()

        # Output: wizard gets friendly closing, CLI gets standard hints
        if wizard:
            obs.console.print()
            obs.success(f"Ingested {stored:,} fragments (ready for semantic search)")
            obs.console.print()
            obs.console.print("  You're all set! Try:")
            obs.console.print()
            obs.console.print('    [cyan]memex dig "that auth discussion"[/cyan]')
            obs.console.print("    [cyan]memex status[/cyan]")
            obs.console.print()
        elif embed:
            obs.success(f"Ingested {stored:,} fragments (ready for semantic search)")
            obs.hint('memex dig "your query" to search')
        else:
            obs.success(f"Ingested {stored:,} fragments (keyword search only)")
            obs.info("Run 'memex backfill' for semantic search")
            obs.hint('memex dig "your query" to search')
    except ValueError as e:
        obs.error(str(e))
        obs.info("Supported formats: Claude export (.json, .zip), OpenAI export")
        if not wizard:
            obs.info("Run 'memex sources' for all adapters")
    finally:
        service.close()


def _human_age(mtime: float) -> str:
    """Human-readable file age: 'today', 'yesterday', '3 days ago', or 'Feb 10'."""
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    file_time = datetime.fromtimestamp(mtime, tz=UTC)
    delta = now - file_time

    if delta.days == 0:
        return "today"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days} days ago"
    else:
        return file_time.strftime("%b %d")


# --- Search Commands ---


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--semantic-weight", "-w", default=None, type=float, help="Weight for semantic (0-1)")
@click.option("--no-rerank", is_flag=True, help="Disable reranking (faster, less precise)")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default=None)
def dig(
    query: str,
    limit: int,
    source: str | None,
    semantic_weight: float | None,
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
    from memex.config.settings import get_settings

    # Resolve defaults from settings
    if semantic_weight is None:
        semantic_weight = get_settings().semantic_weight
    use_reranker = reranker_available() and get_settings().rerank_by_default and not no_rerank

    with obs.status("Loading..."):
        service = create_service(with_embedder=True, with_reranker=use_reranker)

    # Show what retrieval methods are active (stderr — metadata, not data)
    methods = ["BM25"]
    if service.has_semantic_search():
        methods.append("semantic")
    else:
        coverage = service.embedding_coverage()
        if coverage[0] == 0:
            obs.info("semantic unavailable: run 'memex backfill' first")
    if service.has_reranker():
        methods.append("reranking")
    obs.dim(f"Using: {' + '.join(methods)}")

    results = service.hybrid_search(
        query, limit, source, semantic_weight, use_reranker=not no_rerank
    )

    if fmt is None:
        fmt = _default_format()

    if not results:
        _handle_no_results(query, service)
        return

    obs.success(f"Found {len(results)} results for '{query}'")
    format_fragments(results, fmt, obs.console)
    if fmt == "panel":
        obs.hint("memex thread @N to view a conversation, memex similar @1 for related")


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default=None)
def keyword(query: str, limit: int, source: str | None, fmt: str):
    """Keyword-only search (all words must match, no embeddings).

    Faster than hybrid but misses conceptual matches.

    Example:
        memex keyword "OAuth" --limit 50
    """
    if fmt is None:
        fmt = _default_format()

    service = create_service()
    results = service.keyword_search(query, limit, source_kind=source)

    if not results:
        _handle_no_results(query, service)
        return

    obs.success(f"Found {len(results)} keyword matches for '{query}'")
    format_fragments(results, fmt, obs.console)
    if fmt == "panel":
        obs.hint("memex thread @N to view a conversation")


@main.command()
@click.argument("query")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--source", "-s", help="Filter by source kind")
@click.option("--min-score", "-m", default=0.3, help="Minimum similarity (0-1)")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default=None)
def semantic(query: str, limit: int, source: str | None, min_score: float, fmt: str):
    """Semantic search using embeddings.

    Example:
        memex semantic "authentication decisions"
        memex semantic "rate limiting" --min-score 0.5
    """
    if fmt is None:
        fmt = _default_format()

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
    if fmt == "panel":
        obs.hint("memex thread @N to view a conversation, memex similar @1 for related")


# --- View Commands ---


@main.command()
@click.argument("conversation_id")
def thread(conversation_id: str):
    """View a full conversation thread.

    Shows all messages in chronological order.
    Accepts full IDs, short prefixes, or @N references from search results.

    Example:
        memex thread 66e1524a                # Short ID prefix
        memex thread @3                      # 3rd result from last search
        memex thread 66e1524a-1234-5678...   # Full UUID
    """
    # Resolve @N references
    resolved_id = resolve_conversation_ref(conversation_id)
    if resolved_id is None:
        obs.error(f"Could not resolve '{conversation_id}'")
        obs.info("Run a search first, then use @N to reference results")
        return

    service = create_service()
    try:
        fragments = service.find_conversation(resolved_id)
        if not fragments:
            obs.warning(f"No conversation found for '{conversation_id}'")
            obs.info("Tip: Use a longer ID prefix for exact matching")
            return
        format_thread(fragments, obs.console)
    finally:
        service.close()


@main.command()
@click.option("--limit", "-n", default=30, help="Max conversations to show")
@click.option("--offset", "-o", default=0, help="Skip first N conversations")
@click.option("--source", "-s", help="Filter by source kind")
def timeline(limit: int, offset: int, source: str | None):
    """Browse recent conversations.

    Shows a table of conversations sorted by most recent activity.
    Use @N with 'memex thread' to view any conversation.

    Example:
        memex timeline
        memex timeline --limit 50
        memex timeline --source openai
    """
    service = create_service()
    try:
        conversations = service.list_conversations(limit, offset, source)
        if not conversations:
            obs.warning("No conversations found")
            if source:
                obs.info(f"No conversations from source '{source}'")
            return

        # Save to register for @N references
        register_entries = [
            {"id": c["conversation_id"], "conversation_id": c["conversation_id"]}
            for c in conversations
        ]
        save_results(register_entries)

        format_timeline(conversations, obs.console, offset)
    finally:
        service.close()


@main.command()
@click.argument("fragment_ref")
@click.option("--limit", "-n", default=10, help="Max similar fragments")
@click.option("--format", "-f", "fmt", type=click.Choice(["panel", "json", "ids"]), default=None)
def similar(fragment_ref: str, limit: int, fmt: str):
    """Find fragments similar to a given one.

    Uses SIMILAR_TO edges from the knowledge graph.
    Accepts fragment IDs or @N references from search results.

    Example:
        memex similar @1                # Similar to result #1
        memex similar abc123            # Similar to fragment abc123
    """
    if fmt is None:
        fmt = _default_format()

    # Resolve @N → fragment ID
    fragment_id = resolve_fragment_ref(fragment_ref)
    if fragment_id is None:
        obs.error(f"Could not resolve '{fragment_ref}'")
        return

    service = create_service()
    try:
        similar_frags = service.find_similar(fragment_id, limit)
        if not similar_frags:
            obs.warning(f"No similar fragments found for '{fragment_ref}'")
            obs.info("Run 'memex backfill' to enable similarity search")
            return
        obs.success(f"Found {len(similar_frags)} similar fragments")
        format_fragments(similar_frags, fmt, obs.console)
        if fmt == "panel":
            obs.hint("memex thread @N to view the full conversation")
    finally:
        service.close()


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
    from memex.config.settings import get_settings

    should_embed = get_settings().embed_by_default and not no_embed
    _do_ingest(path, embed=should_embed)


@main.command()
def rebuild():
    """Rebuild search indexes (FTS and VSS).

    Run this after manual database changes or if search seems broken.

    Example:
        memex rebuild
    """
    service = create_service()
    try:
        with obs.status("Rebuilding FTS (BM25) index..."):
            service.rebuild_search_index()
        obs.success("FTS index rebuilt")
    finally:
        service.close()
    obs.info("VSS (embedding) index is managed automatically")


@main.command()
@click.option("--batch-size", "-b", default=100, help="Fragments per batch")
def backfill(batch_size: int):
    """Generate embeddings for existing fragments.

    Shows progress bar with ETA. Observable by default.

    Example:
        memex backfill
        memex backfill --batch-size 50  # Smaller batches for lower memory
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
        obs.info(f"Batch size: {batch_size}")
        model = getattr(service.embedder, "model_name", "unknown")
        obs.info(f"Model: {model}")

        # Rich progress bar with ETA
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed:,}/{task.total:,})"),
            TimeElapsedColumn(),
            console=obs.console,
            transient=False,
        ) as progress_bar:
            task = progress_bar.add_task("Embedding", total=without)

            def on_progress(processed: int, total: int):
                progress_bar.update(task, completed=processed)

            updated = service.backfill_embeddings(batch_size, on_progress)

        obs.success(f"Generated embeddings for {updated:,} fragments")
        obs.hint('memex dig "your query" for semantic search')
    except MemoryError:
        obs.error("Out of memory. Try: memex backfill --threads 2 --batch-size 50")
        raise SystemExit(137)
    finally:
        service.close()


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
    from memex.config.settings import get_settings

    corpus_path = get_settings().corpus_path

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
    from memex.config.settings import get_settings

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

    from memex import __status__, __version__
    from memex.config.settings import is_local_store

    status_color = {
        "experimental": "yellow",
        "beta": "cyan",
        "stable": "green",
        "deprecated": "red",
    }
    color = status_color.get(__status__, "dim")

    obs.console.print(f"\n[bold]Memex[/bold] v{__version__} [{color}]{__status__}[/{color}]")
    obs.console.print("─" * 40)

    # Store type indicator
    if is_local_store():
        obs.console.print("[cyan]Store:[/cyan]      [green].memex/ (local)[/green]")
    else:
        obs.console.print("[cyan]Store:[/cyan]      ~/.memex/ (global)")

    # Corpus info
    obs.console.print(f"[cyan]Corpus:[/cyan]     {get_settings().corpus_path}")
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
                "  Reranking:       [yellow]Not available[/yellow]"
                " (fastembed cross-encoder missing)"
            )
    elif service and service.has_reranker():
        model_name = service.reranker_model_name() or "cross-encoder"
        obs.console.print(f"  Reranking:       [green]{model_name}[/green]")
    elif reranker_available():
        obs.console.print("  Reranking:       [dim]Available (auto-enabled in dig)[/dim]")
    else:
        obs.console.print(
            "  Reranking:       [yellow]Not available[/yellow] (fastembed cross-encoder missing)"
        )

    # Graph
    if not dimension_mismatch and service:
        edge_data = service.edge_stats()
        trail_data = service.list_trails()
        if edge_data or trail_data:
            obs.console.print("[bold]Knowledge Graph[/bold]")
            for etype, info in edge_data.items():
                obs.console.print(f"  {etype}: [green]{info['count']:,}[/green] edges")
            if trail_data:
                obs.console.print(f"  Trails:  [green]{len(trail_data)}[/green]")
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
    from memex.config.settings import get_settings

    service = create_service()
    stats = service.stats()

    table = Table(title="Corpus Statistics", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold")

    table.add_row("Fragments", f"{stats['total_fragments']:,}")
    table.add_row("Conversations", f"{stats['conversations']:,}")
    table.add_row("Sources", str(stats["sources"]))
    table.add_row("Corpus Path", str(get_settings().corpus_path))
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
    from memex.config.settings import get_settings

    corpus = create_corpus()

    obs.console.print("[bold]Memex SQL Shell[/] (type 'exit' to quit)")
    obs.console.print(f"[dim]Corpus: {get_settings().corpus_path}[/]")

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


# --- Trail Commands ---


@main.group()
def trail():
    """Manage associative trails through your knowledge.

    Trails are named paths through fragments — Vannevar Bush's core vision.
    """
    pass


@trail.command(name="create")
@click.argument("name")
@click.option("--description", "-d", default="", help="Trail description")
def trail_create(name: str, description: str):
    """Create a new trail.

    Example:
        memex trail create "auth decisions"
        memex trail create "onboarding" -d "How I learned this codebase"
    """
    service = create_service()
    try:
        service.create_trail(name, description)
        obs.success(f"Created trail '{name}'")
        obs.hint(f'memex trail add "{name}" @N (search first, then add results)')
    except Exception as e:
        if "UNIQUE" in str(e):
            obs.error(f"Trail '{name}' already exists")
        else:
            raise
    finally:
        service.close()


@trail.command(name="add")
@click.argument("trail_name")
@click.argument("fragment_ref")
@click.option("--note", "-n", default="", help="Annotation for this entry")
def trail_add(trail_name: str, fragment_ref: str, note: str):
    """Add a fragment to a trail.

    Accepts fragment IDs or @N references from search results.

    Example:
        memex trail add "auth decisions" @3
        memex trail add "auth decisions" @1 -n "The key insight"
    """
    # Resolve @N → fragment ID
    fragment_id = resolve_fragment_ref(fragment_ref)
    if fragment_id is None:
        obs.error(f"Could not resolve '{fragment_ref}'")
        obs.info("Run a search first, then use @N to reference results")
        return

    service = create_service()
    try:
        position = service.add_to_trail(trail_name, fragment_id, note)
        obs.success(f"Added to '{trail_name}' at position #{position + 1}")
    except ValueError as e:
        obs.error(str(e))
    finally:
        service.close()


@trail.command(name="follow")
@click.argument("trail_name")
def trail_follow(trail_name: str):
    """Walk a trail — view all entries in order.

    Example:
        memex trail follow "auth decisions"
    """
    service = create_service()
    try:
        entries = service.get_trail(trail_name)
        if not entries:
            obs.warning(f"Trail '{trail_name}' not found or empty")
            return
        format_trail(trail_name, entries, obs.console)
    finally:
        service.close()


@trail.command(name="list")
def trail_list():
    """List all trails.

    Example:
        memex trail list
    """
    service = create_service()
    try:
        trails = service.list_trails()
        format_trail_list(trails, obs.console)
    finally:
        service.close()


@trail.command(name="delete")
@click.argument("trail_name")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def trail_delete(trail_name: str, yes: bool):
    """Delete a trail.

    Example:
        memex trail delete "old trail"
        memex trail delete "old trail" --yes
    """
    if not yes:
        obs.console.print(f"[yellow]Delete trail '{trail_name}'?[/yellow]")
        confirm = obs.console.input("Type 'yes' to confirm: ")
        if confirm.strip().lower() != "yes":
            obs.info("Aborted.")
            return

    service = create_service()
    try:
        if service.delete_trail(trail_name):
            obs.success(f"Deleted trail '{trail_name}'")
        else:
            obs.warning(f"Trail '{trail_name}' not found")
    finally:
        service.close()


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
