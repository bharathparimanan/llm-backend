"""
FastAPI dependency functions.

Dependencies declared here are injected into route handlers via FastAPI's
Depends() mechanism.  This is the application's primary Dependency Injection
(DI) entry point.

Design:
    - Each function returns a concrete instance (or raises an HTTPException
      if a precondition is not met).
    - Dependencies are composable: a higher-level dependency can call
      lower-level ones via Depends().
    - Keeping all wiring here means route handlers never import concrete
      implementations — they only depend on types/interfaces.

FUTURE UPGRADE:
    When the OpenAI client is stored on app.state (see lifecycle.py), add a
    get_openai_client() dependency that retrieves it from request.app.state
    rather than constructing a new instance per request.

FUTURE UPGRADE:
    When authentication is introduced, add a get_current_user() dependency
    that validates the Bearer token and returns the authenticated principal.
    Route handlers that require auth simply add it to their signature:
        current_user: User = Depends(get_current_user)
"""

import logging

from fastapi import Request

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


def get_app_settings(request: Request) -> Settings:
    """
    Provide the Settings singleton to route handlers.

    Using Depends(get_app_settings) instead of importing `settings` directly
    makes it trivial to override configuration in tests via dependency_overrides.

    Args:
        request: The current HTTP request (injected by FastAPI).

    Returns:
        The application Settings instance.
    """
    return get_settings()
