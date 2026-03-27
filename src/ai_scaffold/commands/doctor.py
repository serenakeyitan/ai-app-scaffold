"""The `doctor` command — verify environment and installed tools."""

from __future__ import annotations

import shutil
import subprocess
import sys

import click
from rich.console import Console
from rich.table import Table

console = Console()

REQUIRED_TOOLS = [
    ("python", "Python 3.10+", "python --version"),
    ("node", "Node.js (for frontend)", "node --version"),
    ("npm", "npm package manager", "npm --version"),
    ("docker", "Docker (for local services)", "docker --version"),
    ("git", "Git version control", "git --version"),
]

OPTIONAL_TOOLS = [
    ("stripe", "Stripe CLI (for payments webhooks)", "stripe --version"),
    ("supabase", "Supabase CLI (for local DB)", "supabase --version"),
    ("vercel", "Vercel CLI (for deployment)", "vercel --version"),
    ("flyctl", "Fly.io CLI (for deployment)", "flyctl version"),
]


@click.command()
def doctor() -> None:
    """Check your environment for required and optional dependencies.

    Verifies that all tools needed by ai-scaffold are installed and
    reports their versions.

    Examples:

    \b
      ai-scaffold doctor
    """
    console.print("\n[bold cyan]ai-scaffold doctor[/bold cyan]\n")

    _check_tools("Required tools", REQUIRED_TOOLS, required=True)
    _check_tools("Optional tools", OPTIONAL_TOOLS, required=False)

    console.print(
        "[dim]Tip: Install missing tools and re-run `ai-scaffold doctor` to verify.[/dim]\n"
    )


def _check_tools(section: str, tools: list, required: bool) -> None:
    table = Table(
        title=section,
        show_header=True,
        header_style="bold",
    )
    table.add_column("Tool", style="cyan", min_width=12)
    table.add_column("Purpose")
    table.add_column("Status", min_width=12)
    table.add_column("Version", style="dim")

    for cmd, purpose, version_cmd in tools:
        found = shutil.which(cmd) is not None
        if found:
            try:
                out = subprocess.check_output(
                    version_cmd.split(), stderr=subprocess.STDOUT, text=True
                ).strip().splitlines()[0]
            except Exception:
                out = "installed"
            status = "[green]found[/green]"
        else:
            out = "—"
            status = "[red]missing[/red]" if required else "[yellow]optional[/yellow]"

        table.add_row(cmd, purpose, status, out)

    console.print(table)
    console.print()
