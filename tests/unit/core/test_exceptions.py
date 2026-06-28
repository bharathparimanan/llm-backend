"""
Tests for app.core.exceptions.

Verifies that the exception hierarchy is structured correctly and that
each exception carries the expected attributes.
"""

from app.core.exceptions import (
    AppError,
    ConfigurationError,
    ContextError,
    NotFoundError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
)


def test_app_error_is_exception() -> None:
    exc = AppError("something went wrong", detail={"code": 42})
    assert isinstance(exc, Exception)
    assert exc.message == "something went wrong"
    assert exc.detail == {"code": 42}


def test_configuration_error_is_app_error() -> None:
    exc = ConfigurationError("missing key")
    assert isinstance(exc, AppError)


def test_provider_timeout_is_provider_error() -> None:
    exc = ProviderTimeoutError("timed out")
    assert isinstance(exc, ProviderError)
    assert isinstance(exc, AppError)


def test_provider_rate_limit_is_provider_error() -> None:
    exc = ProviderRateLimitError("rate limited")
    assert isinstance(exc, ProviderError)


def test_context_error_is_app_error() -> None:
    assert isinstance(ContextError("ctx"), AppError)


def test_not_found_error_is_app_error() -> None:
    assert isinstance(NotFoundError("missing"), AppError)
