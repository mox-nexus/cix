"""assay CLI — composition root entry point.

Commands:
  assay templates                          list built-in inquiry templates
  assay init <inquiry> --template <name>   scaffold inquiry config
  assay validate <inquiry>                 pre-flight schema check
  assay verify <inquiry> [--claim <id>]    run verification
  assay query <inquiry> "SQL"              DuckDB query on the latest run
  assay show <inquiry> <claim-id>          per-mechanism breakdown for one claim
  assay status                             list inquiries + runs
  assay --skill                            print claude-loadable skill description
  assay --version                          print version

Inquiries live at ./.cix/assay/<inquiry>/.
Each verify run lands at ./.cix/assay/<inquiry>/run-<UTC-timestamp>/.
"""

from __future__ import annotations

import importlib.resources
import json
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from assay import __version__
from assay import skill as skill_module
from assay.composition.root import compose
from assay.config.settings import load_inquiry
from assay.domain.exceptions import AssayError
from assay.domain.services.inquiry_runner import InquiryProgress

CONSOLE = Console()
INQUIRY_ROOT = Path(".cix/assay")
INQUIRY_FILE = "inquiry.yaml"


# --- helpers ---


def _inquiry_dir(name: str) -> Path:
    return INQUIRY_ROOT / name


def _inquiry_yaml(name: str) -> Path:
    return _inquiry_dir(name) / INQUIRY_FILE


def _latest_run(inquiry: str) -> Path | None:
    d = _inquiry_dir(inquiry)
    if not d.exists():
        return None
    runs = sorted(d.glob("run-*"))
    return runs[-1] if runs else None


def _print_progress(p: InquiryProgress) -> None:
    """Per-claim line. Bracketed verdict per mechanism + final adjudication."""
    bits = []
    for r in p.mechanism_results:
        v = r.verdict.value
        bits.append(f"{r.mechanism}={v}")
    final = p.adjudication.final_verdict.value
    state = (
        "DIVERGED"
        if p.adjudication.diverged
        else ("CONVERGED" if p.adjudication.converged else "MIXED")
    )
    CONSOLE.print(f"  {p.claim.id:<40s}  [{state:9s}]  final={final:<9s}  ({', '.join(bits)})")
    if p.adjudication.diverged:
        # Auto-print divergent mechanism reasoning
        for r in p.mechanism_results:
            if r.verdict.value in ("disagree", "uncertain"):
                CONSOLE.print(f"    ↳ {r.mechanism}: {r.summary}")


# --- commands ---


@click.group(invoke_without_command=True)
@click.version_option(__version__, "--version", "-v")
@click.option("--skill", is_flag=True, help="Print the claude-loadable skill description and exit.")
@click.option(
    "-r",
    "--reference",
    default=None,
    help="With --skill: print named reference file from references/.",
)
@click.pass_context
def main(ctx: click.Context, skill: bool, reference: str | None) -> None:
    """assay — cross-family verification harness."""
    if skill or reference:
        click.echo(skill_module.get_skill(reference))
        ctx.exit(0)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
def templates() -> None:
    """List built-in inquiry templates."""
    pkg = importlib.resources.files("assay.configs")
    table = Table(title="Built-in inquiry templates")
    table.add_column("name", style="cyan")
    table.add_column("path", style="dim")
    found = False
    for entry in pkg.iterdir():
        if entry.name.endswith(".yaml"):
            table.add_row(entry.name.removesuffix(".yaml"), str(entry))
            found = True
    if not found:
        CONSOLE.print("[yellow](no templates yet)[/yellow]")
        return
    CONSOLE.print(table)


@main.command()
@click.argument("inquiry")
@click.option("--template", "-t", required=True, help="Template name (see `assay templates`)")
def init(inquiry: str, template: str) -> None:
    """Scaffold a new inquiry from a built-in template.

    Rewrites the template's `name:` field to match the user-supplied <inquiry>
    so that the run output directory matches the inquiry directory.
    """
    pkg = importlib.resources.files("assay.configs")
    src = pkg / f"{template}.yaml"
    if not src.is_file():
        raise click.ClickException(f"unknown template: {template} (see `assay templates`)")
    dst_dir = _inquiry_dir(inquiry)
    if dst_dir.exists():
        raise click.ClickException(f"inquiry already exists: {dst_dir}")
    dst_dir.mkdir(parents=True)
    dst = dst_dir / INQUIRY_FILE
    # Rewrite the name field so inquiry-dir and config.name match.
    import yaml as _yaml

    raw = _yaml.safe_load(src.read_text(encoding="utf-8"))
    raw["name"] = inquiry
    dst.write_text(_yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    CONSOLE.print(f"[green]Scaffolded[/green] {dst}")
    CONSOLE.print(
        f"Edit then run: [cyan]assay validate {inquiry}[/cyan] && "
        f"[cyan]assay verify {inquiry}[/cyan]"
    )


@main.command()
@click.argument("inquiry")
def validate(inquiry: str) -> None:
    """Pre-flight check: load YAML, validate schema, verify claim source exists."""
    yml = _inquiry_yaml(inquiry)
    if not yml.exists():
        raise click.ClickException(f"inquiry not found: {yml}")
    try:
        cfg = load_inquiry(yml)
    except AssayError as e:
        raise click.ClickException(f"validation failed: {e}") from e
    # Try composing without running — surfaces missing env vars, bad backends, etc.
    try:
        runner, run_dir = compose(cfg, run_dir=str(_inquiry_dir(inquiry) / "run-validate-tmp"))
    except AssayError as e:
        raise click.ClickException(f"composition failed: {e}") from e
    finally:
        # Clean the temp validate run dir
        tmp = _inquiry_dir(inquiry) / "run-validate-tmp"
        if tmp.exists():
            shutil.rmtree(tmp)
    _ = runner  # suppress unused
    CONSOLE.print(
        f"[green]OK[/green]  {cfg.name}: {len(cfg.mechanisms)} mechanism(s); "
        f"claims at {cfg.claims_path}"
    )


@main.command()
@click.argument("inquiry")
@click.option("--claim", "claim_id", default=None, help="Run a single claim by id (for debugging)")
def verify(inquiry: str, claim_id: str | None) -> None:
    """Run the verification inquiry. Outputs per-claim line + final summary."""
    yml = _inquiry_yaml(inquiry)
    if not yml.exists():
        raise click.ClickException(f"inquiry not found: {yml}")
    cfg = load_inquiry(yml)
    runner, run_dir = compose(cfg)
    CONSOLE.print(f"Inquiry: [cyan]{cfg.name}[/cyan]  →  {run_dir}")
    CONSOLE.print(f"Mechanisms: {[m.name for m in cfg.mechanisms]}")
    if claim_id:
        CONSOLE.print(f"Single-claim mode: [cyan]{claim_id}[/cyan]")
    CONSOLE.print()
    summary = runner.run(on_progress=_print_progress, only_claim_id=claim_id)
    CONSOLE.print()
    CONSOLE.print(
        f"[bold]Done.[/bold] {summary.claim_count} claim(s) in {summary.elapsed_seconds:.1f}s — "
        f"converged={summary.converged_count}, diverged={summary.diverged_count}, "
        f"error-only={summary.error_only_count}"
    )


@main.command()
@click.argument("inquiry")
@click.argument("sql")
def query(inquiry: str, sql: str) -> None:
    """Run a DuckDB SQL query against the latest run."""
    run = _latest_run(inquiry)
    if run is None:
        raise click.ClickException(f"no runs found for inquiry {inquiry}")
    from assay.adapters._out.verdict_store.duckdb import DuckdbVerdictStore

    store = DuckdbVerdictStore(str(run))
    rows = list(store.query(sql))
    if not rows:
        CONSOLE.print("[yellow](no rows)[/yellow]")
        return
    for row in rows:
        click.echo(json.dumps(row, default=str))


@main.command()
@click.argument("inquiry")
@click.argument("claim_id")
def show(inquiry: str, claim_id: str) -> None:
    """Show per-mechanism breakdown for one claim from the latest run."""
    run = _latest_run(inquiry)
    if run is None:
        raise click.ClickException(f"no runs found for inquiry {inquiry}")
    from assay.adapters._out.verdict_store.duckdb import DuckdbVerdictStore

    store = DuckdbVerdictStore(str(run))
    rows = list(
        store.query(
            f"SELECT * FROM mechanism_results WHERE claim_id = '{claim_id}' ORDER BY mechanism"
        )
    )
    if not rows:
        CONSOLE.print(f"[yellow]no results for claim {claim_id}[/yellow]")
        return
    for r in rows:
        CONSOLE.print(
            f"\n[bold cyan]{r['mechanism']}[/bold cyan]  "
            f"verdict=[bold]{r['verdict']}[/bold]  ({r['elapsed_seconds']:.1f}s)"
        )
        CONSOLE.print(f"  summary: {r['summary']}")
        ev = r.get("evidence")
        if ev:
            CONSOLE.print(f"  evidence: {json.dumps(ev, default=str)[:600]}")


@main.command()
def status() -> None:
    """List inquiries and their runs."""
    if not INQUIRY_ROOT.exists():
        CONSOLE.print(f"[yellow]no inquiries at {INQUIRY_ROOT}[/yellow]")
        return
    table = Table(title=f"Inquiries at {INQUIRY_ROOT}")
    table.add_column("inquiry")
    table.add_column("runs")
    table.add_column("latest")
    for d in sorted(INQUIRY_ROOT.iterdir()):
        if not d.is_dir():
            continue
        runs = sorted(d.glob("run-*"))
        latest = runs[-1].name if runs else "(none)"
        table.add_row(d.name, str(len(runs)), latest)
    CONSOLE.print(table)


if __name__ == "__main__":
    main()
