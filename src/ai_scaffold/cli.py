"""Main CLI entry point for ai-scaffold."""

from __future__ import annotations

import click
from rich.console import Console

from ai_scaffold import __version__
from ai_scaffold.commands.new import new
from ai_scaffold.commands.list_providers import list_providers
from ai_scaffold.commands.add import add
from ai_scaffold.commands.doctor import doctor

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ai-scaffold")
def main() -> None:
    """ai-scaffold — Zero-to-prod AI app in one command.

    Scaffold a production-ready AI application pre-wired with:
    auth, payments, database, monitoring, secrets management, and more.

    Inspired by Karpathy's observation that DevOps assembly is the
    hardest part of shipping an AI app — not the AI code itself.
    """


main.add_command(new)
main.add_command(list_providers)
main.add_command(add)
main.add_command(doctor)
