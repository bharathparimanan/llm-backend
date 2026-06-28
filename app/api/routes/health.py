"""
Health-check route.

Provides a lightweight liveness endpoint that load balancers, container
orchestrators (Kubernetes), and uptime monitors can poll to determine
whether the service is running.

Endpoints:
    GET /api/v1/health          — liveness: is the process alive?
    GET /api/v1/health/ready    — readiness: can the service handle requests?
                                  (checks downstream dependencies)

Design:
    - Liveness must always be fast and never depend on external services.
    - Readiness may check database connectivity, provider reachability, etc.
      If any dependency is unhealthy, readiness returns HTTP 503.

FUTURE UPGRADE:
    When external dependencies (database, cache, provider) are introduced,
    the /ready endpoint should probe each one and aggregate their status.
    Return 200 only when all required dependencies report healthy.
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import get_app_settings
from app.core.config import Settings
from app.core.constants import HEALTH_STATUS_DEGRADED, HEALTH_STATUS_OK

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "",
    summary="Liveness check",
    description="Returns 200 when the process is running.  Never depends on external services.",
    response_description="Service status payload.",
)
async def liveness(settings: Settings = Depends(get_app_settings)) -> dict[str, Any]:
    """
    Liveness probe.

    A load balancer that receives a non-200 response will stop routing
    traffic here and trigger a restart.  Keep this endpoint dependency-free
    so that transient downstream failures do not cause unnecessary restarts.
    """
    return {
        "status": HEALTH_STATUS_OK,
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get(
    "/ready",
    summary="Readiness check",
    description="Returns 200 when all required dependencies are reachable.",
    response_description="Readiness status per dependency.",
)
async def readiness(settings: Settings = Depends(get_app_settings)) -> JSONResponse:
    """
    Readiness probe.

    Unlike liveness, readiness verifies that the service can actually handle
    requests end-to-end.  A failing dependency causes a 503 response, which
    signals that traffic should be held back until the dependency recovers.

    FUTURE UPGRADE:
        Add probes for database connectivity and OpenAI API reachability:

        checks = {
            "database": await _check_database(app.state.db_engine),
            "openai":   await _check_openai(app.state.openai_client),
        }
        overall = all(v == HEALTH_STATUS_OK for v in checks.values())
    """
    checks: dict[str, str] = {
        # Placeholder: no external dependencies yet.
        "api": HEALTH_STATUS_OK,
    }

    all_ok = all(status == HEALTH_STATUS_OK for status in checks.values())
    overall_status = HEALTH_STATUS_OK if all_ok else HEALTH_STATUS_DEGRADED
    http_status = 200 if all_ok else 503

    logger.debug("Readiness check: %s", checks)

    return JSONResponse(
        status_code=http_status,
        content={
            "status": overall_status,
            "checks": checks,
        },
    )
