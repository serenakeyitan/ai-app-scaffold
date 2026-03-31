"""The `add` command — add a provider to an existing project."""

from __future__ import annotations

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

ADDABLE = {
    "monitoring": "Add Sentry error tracking + basic metrics endpoint",
    "docker": "Add Dockerfile + docker-compose.yml",
    "ci": "Add GitHub Actions CI/CD workflow",
    "rate-limiting": "Add Redis-backed rate limiting middleware",
    "feature-flags": "Add feature flag support (LaunchDarkly / Unleash)",
    "analytics": "Add PostHog analytics integration",
}


@click.command()
@click.argument("feature", type=click.Choice(list(ADDABLE.keys())))
@click.option("--project-dir", "-p", default=".", type=click.Path(exists=True), help="Project directory.")
def add(feature: str, project_dir: str) -> None:
    """Add a feature or integration to an existing scaffolded project.

    FEATURE is one of the supported add-ons.

    Examples:

    \b
      ai-scaffold add monitoring
      ai-scaffold add docker
      ai-scaffold add ci
    """
    console.print(
        Panel.fit(
            f"[bold cyan]Adding[/bold cyan] [bold]{feature}[/bold] to project at [dim]{project_dir}[/dim]",
            border_style="cyan",
        )
    )

    # In a real implementation this would render templates into the project dir.
    # For now, we show what would be added.
    console.print(f"\n[green]Would add:[/green] {ADDABLE[feature]}")
    console.print("\n[dim]Full integration coming in v0.2.0 — contributions welcome![/dim]")
    console.print("[dim]https://github.com/serenakeyitan/ai-app-scaffold/issues[/dim]")
