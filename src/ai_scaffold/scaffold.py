"""Core scaffolding logic — renders templates and writes project files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console

from ai_scaffold.providers import AI_PROVIDERS, AUTH_PROVIDERS, DB_PROVIDERS, PAYMENT_PROVIDERS
from ai_scaffold.templates import render_all

console = Console()


@dataclass
class ScaffoldConfig:
    """All options for a scaffold run."""

    project_name: str
    ai_provider: str = "openai"
    auth_provider: str = "clerk"
    db_provider: str = "supabase"
    payment_provider: str = "stripe"
    monitoring: bool = True
    docker: bool = True
    ci: bool = True
    output_dir: Path = field(default_factory=Path)

    @property
    def ai_info(self) -> dict:
        return AI_PROVIDERS[self.ai_provider]

    @property
    def auth_info(self) -> dict:
        return AUTH_PROVIDERS[self.auth_provider]

    @property
    def db_info(self) -> dict:
        return DB_PROVIDERS[self.db_provider]

    @property
    def payment_info(self) -> dict:
        return PAYMENT_PROVIDERS[self.payment_provider]

    @property
    def all_env_vars(self) -> list[str]:
        """Collect every required env var across all chosen providers."""
        env_vars: list[str] = []
        for info in [self.ai_info, self.auth_info, self.db_info, self.payment_info]:
            env_vars.extend(info.get("env_vars", []))
        if self.monitoring:
            env_vars.append("SENTRY_DSN")
        env_vars.extend(["APP_ENV", "SECRET_KEY", "ALLOWED_ORIGINS"])
        return list(dict.fromkeys(env_vars))  # deduplicate, preserve order


@dataclass
class ScaffoldResult:
    project_dir: Path
    files_created: int


class Scaffolder:
    """Renders all template files into the target project directory."""

    def __init__(self, config: ScaffoldConfig) -> None:
        self.config = config

    def scaffold(self) -> ScaffoldResult:
        project_dir = self.config.output_dir / self.config.project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        files = render_all(self.config, project_dir)
        return ScaffoldResult(project_dir=project_dir, files_created=len(files))
