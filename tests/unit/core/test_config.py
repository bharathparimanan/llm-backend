"""
Tests for app.core.config.

These tests verify that Settings correctly reads values and that the
lru_cache can be cleared between tests when environment isolation is needed.
"""

import pytest

from app.core.config import Settings, get_settings


def test_settings_has_defaults() -> None:
    """Settings constructed with only the required field should apply defaults."""
    s = Settings(openai_api_key="sk-test")
    assert s.app_name == "foundation-ai"
    assert s.environment == "development"
    assert s.openai_model == "gpt-4o-mini"
    assert s.default_temperature == 0.7


def test_get_settings_returns_singleton() -> None:
    """get_settings() must return the same object on repeated calls."""
    a = get_settings()
    b = get_settings()
    assert a is b


def test_settings_cache_can_be_cleared(monkeypatch: pytest.MonkeyPatch) -> None:
    """Clearing the lru_cache forces a fresh Settings parse."""
    get_settings.cache_clear()
    monkeypatch.setenv("OPENAI_API_KEY", "sk-cleared-test")
    monkeypatch.setenv("APP_NAME", "test-app")

    fresh = get_settings()
    assert fresh.app_name == "test-app"

    # Restore so other tests are not affected.
    get_settings.cache_clear()
