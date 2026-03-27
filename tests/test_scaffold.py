"""Tests for the core scaffolding logic."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_scaffold.scaffold import ScaffoldConfig, Scaffolder


def test_scaffold_config_defaults() -> None:
    config = ScaffoldConfig(project_name="my-app")
    assert config.ai_provider == "openai"
    assert config.auth_provider == "clerk"
    assert config.db_provider == "supabase"
    assert config.payment_provider == "stripe"
    assert config.monitoring is True
    assert config.docker is True
    assert config.ci is True


def test_scaffold_config_all_env_vars_deduped() -> None:
    config = ScaffoldConfig(project_name="test", db_provider="supabase", auth_provider="supabase-auth")
    env_vars = config.all_env_vars
    # Deduplication — no duplicates
    assert len(env_vars) == len(set(env_vars))


def test_scaffold_config_ai_info() -> None:
    config = ScaffoldConfig(project_name="test", ai_provider="anthropic")
    assert config.ai_info["sdk"] == "anthropic"
    assert "ANTHROPIC_API_KEY" in config.ai_info["env_vars"]


def test_scaffolder_creates_files(tmp_path: Path) -> None:
    config = ScaffoldConfig(
        project_name="demo",
        ai_provider="openai",
        auth_provider="clerk",
        db_provider="sqlite",
        payment_provider="stripe",
        monitoring=True,
        docker=True,
        ci=True,
        output_dir=tmp_path,
    )
    scaffolder = Scaffolder(config)
    result = scaffolder.scaffold()

    project_dir = tmp_path / "demo"
    assert project_dir.exists()
    assert result.files_created > 0
    assert (project_dir / ".env.example").exists()
    assert (project_dir / ".gitignore").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "Dockerfile").exists()
    assert (project_dir / "docker-compose.yml").exists()
    assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
    assert (project_dir / "app" / "main.py").exists()
    assert (project_dir / "app" / "settings.py").exists()
    assert (project_dir / "app" / "routes" / "chat.py").exists()
    assert (project_dir / "app" / "db" / "models.py").exists()


def test_scaffolder_no_docker(tmp_path: Path) -> None:
    config = ScaffoldConfig(
        project_name="nodock",
        ai_provider="gemini",
        docker=False,
        ci=False,
        monitoring=False,
        output_dir=tmp_path,
    )
    result = Scaffolder(config).scaffold()
    project_dir = tmp_path / "nodock"
    assert not (project_dir / "Dockerfile").exists()
    assert not (project_dir / "docker-compose.yml").exists()


def test_scaffold_env_example_contains_ai_key(tmp_path: Path) -> None:
    config = ScaffoldConfig(
        project_name="envtest",
        ai_provider="anthropic",
        payment_provider="none",
        output_dir=tmp_path,
    )
    Scaffolder(config).scaffold()
    env_text = (tmp_path / "envtest" / ".env.example").read_text()
    assert "ANTHROPIC_API_KEY" in env_text


def test_scaffold_readme_contains_stack(tmp_path: Path) -> None:
    config = ScaffoldConfig(
        project_name="readmetest",
        ai_provider="openai",
        auth_provider="auth0",
        db_provider="neon",
        payment_provider="stripe",
        output_dir=tmp_path,
    )
    Scaffolder(config).scaffold()
    readme = (tmp_path / "readmetest" / "README.md").read_text()
    assert "openai" in readme
    assert "auth0" in readme
    assert "neon" in readme
    assert "stripe" in readme
