"""The `list-providers` command — show available providers."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ai_scaffold.providers import AI_PROVIDERS, AUTH_PROVIDERS, DB_PROVIDERS, PAYMENT_PROVIDERS

console = Console()


@click.command("list-providers")
@click.option("--category", "-c", type=click.Choice(["ai", "auth", "db", "payments", "all"]), default="all")
def list_providers(category: str) -> None:
    """List all supported providers by category.

    Examples:

    \b
      ai-scaffold list-providers
      ai-scaffold list-providers --category ai
      ai-scaffold list-providers --category db
    """
    if category in ("ai", "all"):
        _print_table("AI Providers", AI_PROVIDERS)
    if category in ("auth", "all"):
        _print_table("Auth Providers", AUTH_PROVIDERS)
    if category in ("db", "all"):
        _print_table("Database Providers", DB_PROVIDERS)
    if category in ("payments", "all"):
        _print_table("Payment Providers", PAYMENT_PROVIDERS)


def _print_table(title: str, providers: dict) -> None:
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Name", style="cyan", min_width=14)
    table.add_column("Description")
    table.add_column("Env Vars", style="dim")
    for key, info in providers.items():
        table.add_row(key, info["description"], ", ".join(info.get("env_vars", [])))
    console.print(table)
    console.print()
