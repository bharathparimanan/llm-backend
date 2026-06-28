"""
Request ID middleware.

Attaches a unique identifier to every incoming request and propagates it
through the response headers.  This enables end-to-end tracing across logs,
metrics, and external systems without requiring a full tracing SDK.

Behaviour:
    1. If the incoming request contains an X-Request-ID header, use it.
    2. Otherwise, generate a new UUID4.
    3. Store the ID on request.state.request_id.
    4. Echo the ID back in the response via X-Request-ID.

FUTURE UPGRADE:
    When OpenTelemetry is introduced (observability/), replace this with
    proper W3C Trace Context propagation (traceparent / tracestate headers).
    The request_id stored on request.state will then map directly to the
    OTel trace-id, making log→trace correlation automatic.
"""

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.core.constants import REQUEST_ID_HEADER

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that ensures every request has a unique ID.

    Inherits BaseHTTPMiddleware for simplicity at this scale.

    FUTURE UPGRADE:
        For high-throughput scenarios, replace BaseHTTPMiddleware with a raw
        ASGI middleware class to avoid the overhead of the extra asyncio.Task
        that BaseHTTPMiddleware introduces.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response:  # type: ignore[override]
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id

        logger.debug(
            "Request received",
            extra={"request_id": request_id, "method": request.method, "path": request.url.path},
        )

        response: Response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response


# Typing import needed at module scope to satisfy the Any annotation above.
from typing import Any  # noqa: E402
