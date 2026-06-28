"""
HTTP middleware.

Purpose:
    Cross-cutting concerns that wrap every request/response cycle.

Responsibilities:
    - Attach a unique request-id to each request for tracing
    - CORS policy enforcement
    - Global timing / latency headers
    - Authentication token validation (when introduced)

What belongs here:
    Starlette BaseHTTPMiddleware subclasses or @app.middleware("http") callables.

What does NOT belong here:
    Route-specific logic, business rules, database access.

Future evolution:
    Rate-limiting middleware will be added here when the API is exposed publicly.
    An auth middleware will extract and validate JWT/API-key tokens and attach the
    principal to request.state before the route handler runs.
"""
