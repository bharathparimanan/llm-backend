"""
Application lifespan management.

Provides the FastAPI lifespan context manager that runs startup and shutdown
logic exactly once per process.  This is the correct place to:

    - Initialise logging
    - Validate required configuration
    - Create database connection pools
    - Warm up provider clients
    - Register clean-up callbacks

Keeping lifecycle logic here (rather than scattered across main.py or
individual modules) makes the startup sequence easy to read and test.

FUTURE UPGRADE:
    When the application connects to a database, open the async connection
    pool on startup and close it on shutdown here.  Similarly, initialise
    the OpenAI AsyncClient once and store it on app.state so that every
    request reuses the same HTTP connection pool.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan context manager.

    Everything before the ``yield`` runs on startup.
    Everything after the ``yield`` runs on shutdown.

    Args:
        app: The FastAPI application instance.  Use app.state to attach
             shared resources (DB pool, provider client, …).
    """
    # ── Startup ───────────────────────────────────────────────────────────────
    configure_logging(level=settings.log_level, use_json=settings.log_json)

    logger.info(
        "Starting %s v%s in %s environment",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    # FUTURE UPGRADE:
    # Initialise the async database engine here and attach it to app.state:
    #
    #   app.state.db_engine = create_async_engine(settings.database_url)
    #
    # This ensures a single connection pool is shared across all requests
    # rather than opening a new connection per request.

    # FUTURE UPGRADE:
    # Initialise the OpenAI AsyncClient once here:
    #
    #   from openai import AsyncOpenAI
    #   app.state.openai_client = AsyncOpenAI(
    #       api_key=settings.openai_api_key,
    #       timeout=settings.openai_timeout_seconds,
    #       max_retries=settings.openai_max_retries,
    #   )
    #
    # Reusing one client per process is more efficient than constructing
    # a new client for every request.

    logger.info("Startup complete.  Accepting requests.")

    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    logger.info("Shutting down %s — releasing resources.", settings.app_name)

    # FUTURE UPGRADE:
    # Dispose of the async database engine:
    #   await app.state.db_engine.dispose()

    # FUTURE UPGRADE:
    # Close the OpenAI AsyncClient HTTP connection pool:
    #   await app.state.openai_client.close()

    logger.info("Shutdown complete.")
