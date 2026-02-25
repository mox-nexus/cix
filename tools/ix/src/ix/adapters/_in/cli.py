"""CLI adapter for ix — Intelligent Experimentation.

Thin driving adapter. Delegates to composition root + service.
Follows cix CLI pattern: Rich Click, helpful errors, color output.
"""

import asyncio
import json
from pathlib import Path

import rich_click as click
from rich.console import Console
from rich.table import Table

from ix import __version__

console = Console()


# --- Output Helpers ---


def _status_style(status: str) -> str:
    return {
        "excellent": "[bold green]EXCELLENT[/bold green]",
        "good": "[green]GOOD[/green]",
        "needs_work": "[yellow]NEEDS WORK[/yellow]",
        "poor": "[bold red]POOR[/bold red]",
    }.get(status, status.upper())


def _print_metrics(results) -> None:
    """Print experiment results — metrics, confusion matrix, interpretation."""
    console.print()
    console.rule("[bold]Results[/bold]")
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("Precision", f"{results.precision:.1%}")
    table.add_row("Recall", f"{results.recall:.1%}")
    table.add_row("F1", f"{results.f1:.1%}")
    console.print(table)

    console.print()
    console.print("[bold]Confusion Matrix:[/bold]")
    console.print(f"  TP={results.tp}  FP={results.fp}")
    console.print(f"  FN={results.fn}  TN={results.tn}")

    console.print()
    console.print(f"Status: {_status_style(results.status)}")

    if results.issues:
        console.print()
        console.print("[bold]Issues:[/bold]")
        for issue in results.issues:
            console.print(f"  [yellow]-[/yellow] {issue}")

    if results.suggestions:
        console.print()
        console.print("[bold]Suggestions:[/bold]")
        for sug in results.suggestions:
            console.print(f"  [cyan]-[/cyan] {sug}")

    console.print()


def _cli_error(message: str, fix: str | None = None) -> None:
    """Print a consistent error message and exit."""
    console.print(f"[red]Error:[/red] {message}")
    if fix:
        console.print(f"  [dim]Fix: {fix}[/dim]")
    raise SystemExit(1)


def _resolve_lab(lab_name: str | None) -> Path:
    """Resolve lab from --lab flag or auto-detect."""
    from ix.config.settings import find_lab

    try:
        return find_lab(lab_name)
    except FileNotFoundError as e:
        _cli_error(str(e))


# --- CLI ---


@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name="ix")
@click.pass_context
def main(ctx: click.Context) -> None:
    """ix — Intelligent Experimentation

    Evals, benchmarks, and QoS experiments for AI agents and skills.
    """
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


# --- Lab Commands ---


@main.group()
def lab() -> None:
    """Manage labs (experiment workspaces)."""


@lab.command("init")
@click.argument("name")
def lab_init(name: str) -> None:
    """Create a new lab.

    A lab is a directory that holds experiments.

    Examples:
        ix lab init ci-lab
        ix lab init perf-lab
    """
    from ix.config.settings import find_project_root

    root = find_project_root()
    lab_path = root / name

    if lab_path.exists():
        console.print(f"[yellow]Lab already exists:[/yellow] {lab_path}")
        return

    lab_path.mkdir(parents=True)
    console.print(f"[green]Created lab:[/green] [cyan]{name}[/cyan] at {lab_path}")
    console.print(f"  [dim]Add experiments: mkdir {name}/<experiment-name>[/dim]")


@lab.command("list")
def lab_list() -> None:
    """List available labs."""
    from ix.config.settings import find_project_root, is_lab

    root = find_project_root()
    labs = [d for d in sorted(root.iterdir()) if d.is_dir() and is_lab(d)]

    if not labs:
        console.print("[dim]No labs found.[/dim]")
        console.print("  [dim]Create one with: ix lab init <name>[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Lab")
    table.add_column("Experiments")
    table.add_column("Path")

    for lab_path in labs:
        exp_count = sum(
            1 for d in lab_path.iterdir() if d.is_dir() and (d / "experiment.yaml").exists()
        )
        table.add_row(
            f"[cyan]{lab_path.name}[/cyan]",
            str(exp_count),
            str(lab_path.relative_to(root)),
        )

    console.print(table)


# --- Run Command ---


@main.command()
@click.argument("name")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
@click.option("--trials", type=int, help="Override trial count")
@click.option("--mock/--live", default=True, help="Mock mode (no API calls) or live mode")
@click.option("--seed", type=int, help="Random seed for deterministic mock runs")
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table")
def run(
    name: str,
    lab_name: str | None,
    trials: int | None,
    mock: bool,
    seed: int | None,
    fmt: str,
) -> None:
    """Run an experiment.

    NAME is the experiment directory name within the lab.

    Examples:
        ix run skill-activation --lab ci-lab --mock
        ix run skill-activation --mock          # auto-detect lab
    """
    from ix.composition import create_service, create_store

    lab_path = _resolve_lab(lab_name)
    store = create_store(lab=lab_path)

    exp_path = lab_path / name
    if not exp_path.exists():
        _cli_error(
            f"Experiment not found: {name}",
            f"ix experiment list --lab {lab_path.name}",
        )

    experiment = store.load_experiment(exp_path)

    if trials:
        experiment = experiment.model_copy(update={"trials": trials})

    skill = experiment.subjects[0].name if experiment.subjects else "build-eval"

    try:
        service = create_service(
            mock=mock,
            skill=skill,
            lab=lab_path,
            seed=seed,
            experiment=experiment,
        )
    except ValueError as e:
        _cli_error(str(e))
    except NotImplementedError as e:
        _cli_error(str(e), "Use --mock until live mode is available (M2)")

    mode_label = "mock" if mock else "live"
    console.print(
        f"Running [bold cyan]{experiment.name}[/bold cyan] "
        f"in lab [cyan]{lab_path.name}[/cyan] "
        f"({len(experiment.probes)} probes, {experiment.trials} trials, {mode_label})"
    )

    def on_probe(probe_result) -> None:
        status = "[green]OK[/green]" if probe_result.correct else "[red]FAIL[/red]"
        console.print(f"  {probe_result.probe_id}: {status} (score={probe_result.score:.0%})")

    exp_results = asyncio.run(service.run(experiment, on_probe_complete=on_probe))

    if fmt == "json":
        console.print(exp_results.model_dump_json(indent=2))
    else:
        _print_metrics(exp_results)


# --- Experiment Commands ---


@main.group()
def experiment() -> None:
    """Manage experiments within a lab."""


@experiment.command("init")
@click.argument("name")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
def experiment_init(name: str, lab_name: str | None) -> None:
    """Scaffold a new experiment.

    Creates the experiment directory with experiment.yaml, tasks/ and subjects/.

    Examples:
        ix experiment init skill-activation --lab ci-lab
        ix experiment init code-gen --lab ci-lab
    """
    lab_path = _resolve_lab(lab_name)
    exp_path = lab_path / name

    if exp_path.exists():
        console.print(f"[yellow]Already exists:[/yellow] {exp_path}")
        return

    exp_path.mkdir(parents=True)
    (exp_path / "tasks").mkdir()
    (exp_path / "subjects").mkdir()
    (exp_path / "experiment.yaml").write_text(
        f'name: {name}\ndescription: ""\nsensor: activation\ntrials: 5\n'
    )
    console.print(f"[green]Created experiment:[/green] [cyan]{name}[/cyan]")
    console.print(f"  [dim]Add tasks: {exp_path}/tasks/must-001.md[/dim]")
    console.print(f"  [dim]Add subjects: {exp_path}/subjects/agent.md[/dim]")


@experiment.command("list")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
def experiment_list(lab_name: str | None) -> None:
    """List experiments in a lab."""
    from ix.composition import create_store

    lab_path = _resolve_lab(lab_name)
    store = create_store(lab=lab_path)
    experiments = store.list_experiments(lab_path)

    if not experiments:
        console.print(f"[dim]No experiments in {lab_path.name}.[/dim]")
        console.print(f"  [dim]Create one: ix experiment init <name> --lab {lab_path.name}[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Cases")
    table.add_column("Trials")
    table.add_column("Subject")

    for exp_path in experiments:
        exp = store.load_experiment(exp_path)
        subject_name = exp.subjects[0].name if exp.subjects else "-"
        table.add_row(
            f"[cyan]{exp.name}[/cyan]",
            str(len(exp.probes)),
            str(exp.trials),
            subject_name,
        )

    console.print(table)


@experiment.command("show")
@click.argument("name")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
def experiment_show(name: str, lab_name: str | None) -> None:
    """Show experiment details."""
    from ix.composition import create_store

    lab_path = _resolve_lab(lab_name)
    exp_path = lab_path / name

    if not exp_path.exists():
        _cli_error(
            f"Experiment not found: {name}",
            f"ix experiment list --lab {lab_path.name}",
        )

    store = create_store(lab=lab_path)
    exp = store.load_experiment(exp_path)

    console.print(f"[bold]{exp.name}[/bold]")
    if exp.description:
        console.print(f"[dim]{exp.description}[/dim]")
    subject_name = exp.subjects[0].name if exp.subjects else "-"
    console.print(f"Subject: [cyan]{subject_name}[/cyan]")
    console.print(f"Sensor: [cyan]{exp.sensor.get('type', 'activation')}[/cyan]")
    console.print(f"Trials: {exp.trials}")
    console.print(f"Probes: {len(exp.probes)}")

    if exp.probes:
        console.print()
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Expectation")
        table.add_column("Prompt", max_width=50)

        for probe in exp.probes:
            expectation = probe.metadata.get("expectation", "-")
            table.add_row(probe.id, expectation, probe.prompt[:50])

        console.print(table)


@experiment.command("validate")
@click.argument("name")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
def experiment_validate(name: str, lab_name: str | None) -> None:
    """Validate experiment structure."""
    from ix.composition import create_store

    lab_path = _resolve_lab(lab_name)
    exp_path = lab_path / name

    issues: list[str] = []

    if not exp_path.exists():
        _cli_error(
            f"Directory not found: {exp_path}",
            f"ix experiment init {name} --lab {lab_path.name}",
        )

    if not (exp_path / "experiment.yaml").exists():
        issues.append("Missing experiment.yaml")

    tasks_dir = exp_path / "tasks"
    cases_dir = exp_path / "cases"
    if not tasks_dir.exists() and not cases_dir.exists():
        issues.append("Missing tasks/ directory (or cases/ for legacy)")
    else:
        probe_dir = tasks_dir if tasks_dir.exists() else cases_dir
        md_files = list(probe_dir.glob("*.md"))
        if not md_files:
            issues.append(f"No .md files in {probe_dir.name}/")

    if issues:
        console.print(f"[red]Validation failed for {name}:[/red]")
        for issue in issues:
            console.print(f"  [red]-[/red] {issue}")
        raise SystemExit(1)

    store = create_store(lab=lab_path)

    try:
        exp = store.load_experiment(exp_path)
        console.print(f"[green]Valid:[/green] {exp.name} ({len(exp.probes)} probes)")
    except Exception as e:
        _cli_error(str(e))


# --- Results Command ---


@main.command()
@click.argument("name")
@click.option("--lab", "lab_name", help="Lab name (auto-detected if omitted)")
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table")
def results(name: str, lab_name: str | None, fmt: str) -> None:
    """Show latest results for an experiment."""
    lab_path = _resolve_lab(lab_name)
    latest = lab_path / name / "results" / "summary-latest.json"

    if not latest.exists():
        _cli_error(
            f"No results for {name}",
            f"ix run {name} --lab {lab_path.name} --mock",
        )

    from ix.eval.models import ExperimentResults

    data = json.loads(latest.read_text())
    exp_results = ExperimentResults.model_validate(data)

    if fmt == "json":
        console.print(latest.read_text())
    else:
        _print_metrics(exp_results)
