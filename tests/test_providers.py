"""Tests for provider registry."""

from __future__ import annotations

import pytest

from ai_scaffold.providers import (
    AI_PROVIDERS,
    AUTH_PROVIDERS,
    DB_PROVIDERS,
    PAYMENT_PROVIDERS,
)


def test_ai_providers_have_required_keys() -> None:
    required = {"description", "env_vars", "model_default", "sdk", "import", "client_init", "chat_call"}
    for name, info in AI_PROVIDERS.items():
        missing = required - info.keys()
        assert not missing, f"{name} missing keys: {missing}"


def test_auth_providers_have_required_keys() -> None:
    required = {"description", "env_vars"}
    for name, info in AUTH_PROVIDERS.items():
        missing = required - info.keys()
        assert not missing, f"{name} missing keys: {missing}"


def test_all_ai_providers_present() -> None:
    assert "openai" in AI_PROVIDERS
    assert "anthropic" in AI_PROVIDERS
    assert "gemini" in AI_PROVIDERS


def test_all_auth_providers_present() -> None:
    assert "clerk" in AUTH_PROVIDERS
    assert "auth0" in AUTH_PROVIDERS
    assert "supabase-auth" in AUTH_PROVIDERS


def test_all_db_providers_present() -> None:
    assert "supabase" in DB_PROVIDERS
    assert "neon" in DB_PROVIDERS
    assert "sqlite" in DB_PROVIDERS


def test_all_payment_providers_present() -> None:
    assert "stripe" in PAYMENT_PROVIDERS
    assert "lemon-squeezy" in PAYMENT_PROVIDERS
    assert "none" in PAYMENT_PROVIDERS


def test_env_vars_are_lists() -> None:
    for collection in (AI_PROVIDERS, AUTH_PROVIDERS, DB_PROVIDERS, PAYMENT_PROVIDERS):
        for name, info in collection.items():
            assert isinstance(info["env_vars"], list), f"{name}.env_vars should be a list"
