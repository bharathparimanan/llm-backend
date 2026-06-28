"""
Custom exception hierarchy.

Defines domain exceptions that carry semantic meaning independent of the
HTTP transport layer.  Route handlers translate these into appropriate
HTTPException responses; the service layer raises them without knowing
anything about HTTP status codes.

Hierarchy:
    AppError (base)
    ├── ConfigurationError     — misconfigured settings at startup
    ├── ProviderError          — upstream AI provider failure
    │   ├── ProviderTimeoutError
    │   └── ProviderRateLimitError
    ├── ContextError           — context construction failure
    └── NotFoundError          — requested resource does not exist
"""

from typing import Any


class AppError(Exception):
    """
    Base class for all application-defined exceptions.

    Carries an optional detail payload so callers can attach structured
    context without subclassing further.
    """

    def __init__(self, message: str, detail: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, detail={self.detail!r})"


class ConfigurationError(AppError):
    """
    Raised when required configuration is missing or invalid at startup.

    This is a programmer / ops error, not a user error.  The application
    should fail fast and loudly rather than silently using a bad default.
    """


class ProviderError(AppError):
    """
    Raised when an AI provider call fails for any reason.

    Subclasses narrow the cause so the service layer can apply different
    retry or fallback strategies.
    """


class ProviderTimeoutError(ProviderError):
    """
    Raised when the provider does not respond within the configured timeout.

    # FUTURE UPGRADE:
    # When multiple providers are available, a timeout here can trigger
    # automatic failover to a secondary provider via the ProviderFactory.
    """


class ProviderRateLimitError(ProviderError):
    """
    Raised when the provider returns a 429 / rate-limit response.

    The service layer should apply exponential back-off before retrying.
    """


class ContextError(AppError):
    """
    Raised when context construction fails (e.g. token budget exceeded).
    """


class NotFoundError(AppError):
    """
    Raised when a requested entity (conversation, document, …) does not exist.
    """
