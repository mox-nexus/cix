"""Recon CLI — composition root + commands.

Commands:
  recon survey <name> [-c config]  → run collection mission
  recon init <name> [--template]   → scaffold mission from template
  recon status                     → list missions + archives
  recon query <name> "SQL"         → DuckDB query on JSONL
  recon templates                  → list built-in templates

This is the composition root: it wires adapters to the application layer
via the Collector Protocol registry. Infrastructure transforms ($pdf2text)
are registered here, not in the application layer.

Mission layout:
  .cix/recon/<name>/
    config.yaml
    archive/
      2026-04-01-143022/
        *.jsonl
        meta.yaml
"""

from __future__ import annotations

import importlib.resources
import shutil
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

from recon import __version__
from recon.adapters._out.api_collector import ApiCollector
from recon.adapters._out.cli_collector import CliCollector
from recon.adapters._out.web_collector import WebCollector
from recon.application.recon import run as recon_run
from recon.application.transforms import register_transform
from recon.application.utilization import RateLimiter
from recon.domain.exceptions import ReconError
from recon.domain.models import ReconConfig

# --- Composition: build collector registry ---


def _build_collectors() -> dict:
    """Wire adapter implementations to type names.

    API and Web collectors share a single RateLimiter so hitting the same
    source from both respects a single rate limit.
    """
    rate_limiter = RateLimiter()
    return {
        "cli": CliCollector(),
        "api": ApiCollector(rate_limiter),
        "web": WebCollector(rate_limiter),
    }


# --- Composition: register infrastructure transforms ---


def _pdf2text(path: str) -> str:
    """Extract text from PDF via pymupdf."""
    try:
        import pymupdf

        doc = pymupdf.open(path)
        pages = [page.get_text() for page in doc]
        doc.close()
        return "\n".join(pages)
    except Exception:
        return ""


register_transform("$pdf2text", _pdf2text)


# --- Project root + mission directory ---


console = Console(stderr=True)


def _find_project_root() -> Path:
    """Walk up from cwd looking for .git/."""
    current = Path.cwd()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return Path.cwd()
        current = parent


def _recon_dir() -> Path:
    """Resolve .cix/recon/ directory at project root."""
    return _find_project_root() / ".cix" / "recon"


def _mission_dir(name: str) -> Path:
    """Resolve mission directory at <project>/.cix/recon/<name>/."""
    return _recon_dir() / name


def _list_templates() -> list[str]:
    """List built-in config templates from the package."""
    try:
        configs = importlib.resources.files("recon.configs")
        return sorted(
            p.name.removesuffix(".yaml")
            for p in configs.iterdir()
            if hasattr(p, "name") and p.name.endswith(".yaml")
        )
    except (FileNotFoundError, ModuleNotFoundError):
        return []


def _load_template(name: str) -> str | None:
    """Load a built-in template by name."""
    try:
        ref = importlib.resources.files("recon.configs").joinpath(f"{name}.yaml")
        return ref.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, TypeError):
        return None


# --- Commands ---


@click.group()
@click.version_option(__version__, prog_name="recon")
def main() -> None:
    """Recon — mechanical collection system.

    Config-driven data collection from HTTP APIs, CLI tools, and web pages
    into queryable JSONL. Intelligence lives outside — write the config,
    run the survey, reason over the results.

    \b
    Quick start:
      recon init my-research --template research
      # edit .cix/recon/my-research/config.yaml
      recon survey my-research
      recon query my-research "SELECT title, year FROM s2_search"
    """


@main.command()
@click.argument("name")
@click.option(
    "-t", "--template",
    default="research",
    help="Built-in template to use (default: research). See `recon templates`.",
)
def init(name: str, template: str) -> None:
    """Scaffold a new mission from a built-in template.

    \b
    Examples:
      recon init attention-papers
      recon init my-scan --template research
    """
    mission = _mission_dir(name)
    config_path = mission / "config.yaml"

    if config_path.exists():
        console.print(f"[yellow]Mission '{name}' already exists:[/] {config_path}")
        raise SystemExit(1)

    content = _load_template(template)
    if content is None:
        available = ", ".join(_list_templates()) or "(none)"
        console.print(f"[red]Template not found:[/] {template}")
        console.print(f"[dim]Available: {available}[/]")
        raise SystemExit(1)

    mission.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content)
    console.print(f"[green]Created:[/] {config_path}")
    console.print(f"[dim]Edit the config to set your query, then run: recon survey {name}[/]")


@main.command()
@click.argument("name")
@click.option(
    "-c", "--config",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Config file override (default: .cix/recon/<name>/config.yaml).",
)
def survey(name: str, config: Path | None) -> None:
    """Run a collection mission.

    \b
    Examples:
      recon survey attention-papers
      recon survey my-scan -c custom-config.yaml
    """
    mission = _mission_dir(name)

    if config:
        config_path = config
        # Copy override config into mission dir for reproducibility
        mission.mkdir(parents=True, exist_ok=True)
        dest = mission / "config.yaml"
        if config_path != dest:
            shutil.copy2(config_path, dest)
    else:
        config_path = mission / "config.yaml"

    if not config_path.exists():
        console.print(f"[red]No config found:[/] {config_path}")
        hint = mission / "config.yaml"
        console.print(f"[dim]Run `recon init {name}` or write config to {hint}[/]")
        raise SystemExit(1)

    try:
        raw = yaml.safe_load(config_path.read_text())
        parsed = ReconConfig.model_validate(raw)
    except Exception as exc:
        console.print(f"[red]Config error:[/] {exc}")
        raise SystemExit(1) from exc

    collectors = _build_collectors()

    console.print(
        f"[dim]Mission: {name} — "
        f"{len(parsed.collectors)} collector(s), "
        f"{len(parsed.catalog)} source(s)[/]"
    )

    try:
        archive_dir = recon_run(parsed, collectors, mission)
    except ReconError as exc:
        console.print(f"[red]Error:[/] {exc}")
        raise SystemExit(1) from exc

    # Print archive path to stdout (for piping)
    click.echo(str(archive_dir))


@main.command()
def status() -> None:
    """List missions and their archives.

    \b
    Example:
      recon status
    """
    recon_dir = _recon_dir()

    if not recon_dir.exists():
        console.print("[dim]No missions found. Run `recon init <name>` to get started.[/]")
        return

    missions = sorted(
        d for d in recon_dir.iterdir()
        if d.is_dir() and (d / "config.yaml").exists()
    )

    if not missions:
        console.print("[dim]No missions found. Run `recon init <name>` to get started.[/]")
        return

    table = Table(show_header=True, header_style="dim")
    table.add_column("Mission")
    table.add_column("Archives", justify="right")
    table.add_column("Latest")

    for m in missions:
        archive_dir = m / "archive"
        if archive_dir.exists():
            runs = sorted(d for d in archive_dir.iterdir() if d.is_dir())
            count = str(len(runs))
            latest = runs[-1].name if runs else "—"
        else:
            count = "0"
            latest = "—"
        table.add_row(m.name, count, latest)

    console.print(table)


@main.command()
@click.argument("name")
@click.argument("sql")
@click.option("--run", "run_id", default=None, help="Specific archive timestamp.")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON (for piping).")
def query(name: str, sql: str, run_id: str | None, as_json: bool) -> None:
    """Query mission data with SQL via DuckDB.

    \b
    Examples:
      recon query my-research "SELECT title, year FROM s2_search LIMIT 10"
      recon query my-research "SELECT * FROM arxiv_search" --json
      recon query my-research "SELECT count(*) FROM s2_search" --run 2026-04-01-143022
    """
    import duckdb

    mission = _mission_dir(name)
    archive = mission / "archive"

    if not archive.exists():
        console.print(f"[red]No archives for mission '{name}'[/]")
        raise SystemExit(1)

    if run_id:
        run_dir = archive / run_id
        if not run_dir.exists():
            console.print(f"[red]Archive not found:[/] {run_id}")
            available = sorted(d.name for d in archive.iterdir() if d.is_dir())
            if available:
                console.print(f"[dim]Available: {', '.join(available)}[/]")
            raise SystemExit(1)
    else:
        runs = sorted(d for d in archive.iterdir() if d.is_dir())
        if not runs:
            console.print(f"[red]No archives for mission '{name}'[/]")
            raise SystemExit(1)
        run_dir = runs[-1]

    conn = duckdb.connect()

    jsonl_files = sorted(run_dir.glob("*.jsonl"))
    if not jsonl_files:
        console.print("[yellow]No JSONL files in archive[/]")
        raise SystemExit(1)

    import re as _re

    for jf in jsonl_files:
        table_name = _re.sub(r"[^a-zA-Z0-9_]", "_", jf.stem)
        jf_str = str(jf).replace("'", "''")
        conn.execute(
            f'CREATE VIEW "{table_name}" AS '
            f"SELECT * FROM read_json_auto('{jf_str}')"
        )

    try:
        result = conn.execute(sql)
    except duckdb.Error as exc:
        console.print(f"[red]SQL error:[/] {exc}")
        tables = [jf.stem.replace("-", "_") for jf in jsonl_files]
        console.print(f"[dim]Available tables: {', '.join(tables)}[/]")
        raise SystemExit(1) from exc

    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()

    if as_json:
        import json

        records = [dict(zip(columns, row)) for row in rows]
        click.echo(json.dumps(records, indent=2, default=str))
    else:
        out_table = Table()
        for col in columns:
            out_table.add_column(col)
        for row in rows:
            out_table.add_row(*(str(v) for v in row))
        Console().print(out_table)

    conn.close()


@main.command()
def templates() -> None:
    """List available built-in config templates.

    \b
    Example:
      recon templates
      recon init my-mission --template research
    """
    names = _list_templates()
    if not names:
        console.print("[dim]No built-in templates found[/]")
        return

    for name in names:
        content = _load_template(name)
        # Extract first comment line as description
        desc = ""
        if content:
            for line in content.splitlines():
                if line.startswith("#") and not line.startswith("##"):
                    desc = line.lstrip("# ").strip()
                    break
        console.print(f"  [bold]{name}[/]  {desc}")
