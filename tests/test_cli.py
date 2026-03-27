"""Integration tests for CLI commands."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from ai_scaffold.cli import main


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ai-scaffold" in result.output.lower() or "scaffold" in result.output.lower()


def test_cli_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_new_command_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["new", "--help"])
    assert result.exit_code == 0
    assert "project_name" in result.output.lower() or "PROJECT_NAME" in result.output


def test_new_command_creates_project(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "new", "my-test-app",
            "--ai", "openai",
            "--auth", "clerk",
            "--db", "sqlite",
            "--payments", "stripe",
            "--yes",
            "--output-dir", str(tmp_path),
        ],
    )
    assert result.exit_code == 0
    assert (tmp_path / "my-test-app").exists()


def test_list_providers_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["list-providers"])
    assert result.exit_code == 0
    assert "openai" in result.output.lower()
    assert "anthropic" in result.output.lower()
    assert "stripe" in result.output.lower()


def test_list_providers_ai_only() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["list-providers", "--category", "ai"])
    assert result.exit_code == 0
    assert "openai" in result.output.lower()


def test_doctor_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 0
    assert "python" in result.output.lower()
