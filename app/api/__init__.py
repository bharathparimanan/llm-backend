"""
API layer — HTTP boundary of the application.

Purpose:
    Translate HTTP requests into service calls and service results back into
    HTTP responses.

Responsibilities:
    - Route registration and versioning
    - Request/response serialisation via Pydantic schemas
    - Middleware (auth, CORS, request-id, rate limiting)
    - FastAPI dependency wiring

What belongs here:
    Routes, middleware, request/response schemas used only at the HTTP boundary,
    FastAPI dependency functions.

What does NOT belong here:
    Business logic, database queries, AI provider calls, prompt construction.
    All of that lives in services/, providers/, and repositories/.

Future evolution:
    When the API grows across versions (v1 → v2), each version gets its own
    sub-package under api/v1/, api/v2/.  The router.py aggregator remains the
    single mount point in main.py.
"""
