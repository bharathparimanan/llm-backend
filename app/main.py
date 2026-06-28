"""
Application entry point.

Constructs and configures the FastAPI application instance.  This module is
intentionally thin — it is responsible only for assembling components that
are defined elsewhere.

Responsibilities:
    - Instantiate FastAPI with the lifespan context manager
    - Register middleware in the correct order
    - Mount the top-level API router
    - Register global exception handlers

What does NOT belong here:
    Business logic, route handler implementations, database setup, provider
    calls.  Each of those concerns lives in its own package.

Running locally:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.middleware.request_id import RequestIDMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.constants import API_V1_PREFIX
from app.core.exceptions import AppError, NotFoundError, ProviderError
from app.core.lifecycle import lifespan

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Application factory.

    Using a factory function (rather than a module-level ``app = FastAPI()``)
    makes it easy to create isolated app instances in tests without sharing
    global state.
    """
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "foundation-ai — a production-grade educational reference implementation "
            "of a single-model LLM backend built with FastAPI."
        ),
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    _register_middleware(application)
    _register_routers(application)
    _register_exception_handlers(application)

    return application


def _register_middleware(app: FastAPI) -> None:
    """
    Register middleware in outermost-first order.

    Starlette processes middleware in LIFO order relative to registration,
    so the first middleware added here wraps the outermost layer of the
    request pipeline.
    """
    # CORS — must be the outermost middleware so pre-flight OPTIONS requests
    # are handled before any auth or business logic runs.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Tighten this per environment via settings.
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request ID — attach early so all subsequent middleware and handlers
    # have access to request.state.request_id for structured logging.
    app.add_middleware(RequestIDMiddleware)

    # FUTURE UPGRADE:
    # Add rate-limiting middleware here when the API is exposed publicly.
    # A token-bucket or sliding-window limiter keyed on the authenticated
    # user or IP address prevents abuse without changing route handlers.


def _register_routers(app: FastAPI) -> None:
    """Mount the versioned API router."""
    app.include_router(api_router, prefix=API_V1_PREFIX)


def _register_exception_handlers(app: FastAPI) -> None:
    """
    Map domain exceptions to HTTP responses.

    Centralising error translation here means the service layer can raise
    typed exceptions (ProviderError, NotFoundError, …) without knowing
    anything about HTTP status codes.
    """

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": "not_found", "message": exc.message})

    @app.exception_handler(ProviderError)
    async def provider_error_handler(request: Request, exc: ProviderError) -> JSONResponse:
        logger.error("Provider error: %s", exc.message, extra={"detail": exc.detail})
        return JSONResponse(
            status_code=502,
            content={"error": "provider_error", "message": "Upstream AI provider request failed."},
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.error("Application error: %s", exc.message, extra={"detail": exc.detail})
        return JSONResponse(
            status_code=500,
            content={"error": "internal_error", "message": "An unexpected error occurred."},
        )


# ── Module-level app instance used by uvicorn ──────────────────────────────────
app: FastAPI = create_app()
