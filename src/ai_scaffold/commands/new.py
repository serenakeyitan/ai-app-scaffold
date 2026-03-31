"""The `new` command — scaffold a new AI app project."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ai_scaffold.scaffold import ScaffoldConfig, Scaffolder
from ai_scaffold.providers import AI_PROVIDERS, AUTH_PROVIDERS, DB_PROVIDERS, PAYMENT_PROVIDERS

console = Console()

AI_PROVIDER_CHOICES = list(AI_PROVIDERS.keys())
AUTH_CHOICES = list(AUTH_PROVIDERS.keys())
DB_CHOICES = list(DB_PROVIDERS.keys())
PAYMENT_CHOICES = list(PAYMENT_PROVIDERS.keys())


@click.command()
@click.argument("project_name")
@click.option(
    "--ai",
    type=click.Choice(AI_PROVIDER_CHOICES, case_sensitive=False),
    default=None,
    help="AI provider to use.",
)
@click.option(
    "--auth",
    type=click.Choice(AUTH_CHOICES, case_sensitive=False),
    default=None,
    help="Auth provider to use.",
)
@click.option(
    "--db",
    type=click.Choice(DB_CHOICES, case_sensitive=False),
    default=None,
    help="Database provider to use.",
)
@click.option(
    "--payments",
    type=click.Choice(PAYMENT_CHOICES, case_sensitive=False),
    default=None,
    help="Payments provider to use.",
)
@click.option(
    "--monitoring/--no-monitoring",
    default=True,
    help="Include monitoring setup (Sentry + basic metrics).",
)
@click.option(
    "--docker/--no-docker",
    default=True,
    help="Include Dockerfile and docker-compose.yml.",
)
@click.option(
    "--ci/--no-ci",
    default=True,
    help="Include GitHub Actions CI/CD workflow.",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    type=click.Path(),
    help="Directory to create the project in.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip interactive prompts and use defaults.",
)
def new(
    project_name: str,
    ai: str | None,
    auth: str | None,
    db: str | None,
    payments: str | None,
    monitoring: bool,
    docker: bool,
    ci: bool,
    output_dir: str,
    yes: bool,
) -> None:
    """Scaffold a new production-ready AI application.

    PROJECT_NAME is the name of your new project (also used as the directory name).

    Examples:

    \b
      # Interactive mode — guided prompts for all choices
      ai-scaffold new my-ai-app

    \b
      # Fully specified — no prompts
      ai-scaffold new my-ai-app --ai openai --auth clerk --db supabase --payments stripe

    \b
      # Minimal — AI only, skip auth/payments
      ai-scaffold new my-ai-app --ai anthropic --no-monitoring
    """
    console.print(
        Panel.fit(
            f"[bold cyan]ai-scaffold[/bold cyan] — creating [bold]{project_name}[/bold]",
            border_style="cyan",
        )
    )

    # Resolve choices interactively if not provided via flags
    if not yes:
        ai = ai or _prompt_choice("AI provider", AI_PROVIDERS, default="openai")
        auth = auth or _prompt_choice("Auth provider", AUTH_PROVIDERS, default="clerk")
        db = db or _prompt_choice("Database", DB_PROVIDERS, default="supabase")
        payments = payments or _prompt_choice("Payments", PAYMENT_PROVIDERS, default="stripe")
    else:
        ai = ai or "openai"
        auth = auth or "clerk"
        db = db or "supabase"
        payments = payments or "stripe"

    config = ScaffoldConfig(
        project_name=project_name,
        ai_provider=ai,
        auth_provider=auth,
        db_provider=db,
        payment_provider=payments,
        monitoring=monitoring,
        docker=docker,
        ci=ci,
        output_dir=Path(output_dir),
    )

    scaffolder = Scaffolder(config)

    console.print()
    console.print("[bold]Project configuration:[/bold]")
    _print_config_table(config)
    console.print()

    with console.status("[bold green]Scaffolding project...[/bold green]"):
        result = scaffolder.scaffold()

    console.print(f"[bold green]Created {result.files_created} files in {result.project_dir}[/bold green]")
    console.print()
    _print_next_steps(config, result)


def _prompt_choice(label: str, options: dict, default: str) -> str:
    """Prompt user to pick from a set of options."""
    console.print(f"\n[bold]{label}:[/bold]")
    items = list(options.items())
    for i, (key, info) in enumerate(items, 1):
        marker = " [cyan](default)[/cyan]" if key == default else ""
        console.print(f"  {i}. [cyan]{key}[/cyan] — {info['description']}{marker}")

    default_idx = list(options.keys()).index(default) + 1
    raw = click.prompt(
        f"Choose {label} [1-{len(items)}]",
        default=str(default_idx),
    )
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(items):
            return items[idx][0]
    except (ValueError, IndexError):
        pass
    return default


def _print_config_table(config: ScaffoldConfig) -> None:
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold")
    table.add_column("Value", style="cyan")
    rows = [
        ("AI Provider", config.ai_provider),
        ("Auth", config.auth_provider),
        ("Database", config.db_provider),
        ("Payments", config.payment_provider),
        ("Monitoring", "Sentry + metrics" if config.monitoring else "disabled"),
        ("Docker", "included" if config.docker else "disabled"),
        ("CI/CD", "GitHub Actions" if config.ci else "disabled"),
    ]
    for k, v in rows:
        table.add_row(k, v)
    console.print(table)


def _print_next_steps(config: ScaffoldConfig, result) -> None:  # type: ignore[no-untyped-def]
    steps = [
        f"[bold cyan]cd {result.project_dir}[/bold cyan]",
        "[bold cyan]cp .env.example .env[/bold cyan]  # fill in your API keys",
        "[bold cyan]pip install -e .[/bold cyan]       # install Python deps",
    ]
    if config.docker:
        steps.append("[bold cyan]docker compose up[/bold cyan]        # start all services")
    else:
        steps.append("[bold cyan]python -m uvicorn app.main:app --reload[/bold cyan]")

    console.print("[bold]Next steps:[/bold]")
    for i, step in enumerate(steps, 1):
        console.print(f"  {i}. {step}")
    console.print()
    console.print("[dim]Full docs: https://github.com/serenakeyitan/ai-app-scaffold[/dim]")
