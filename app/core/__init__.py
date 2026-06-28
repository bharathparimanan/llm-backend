"""
Core infrastructure.

Purpose:
    Provide foundational primitives that the entire application depends on.

Responsibilities:
    - Application configuration (config.py)
    - Logging setup (logging.py)
    - Custom exception hierarchy (exceptions.py)
    - Application-wide constants (constants.py)
    - Application lifespan management (lifecycle.py)

What belongs here:
    Pure infrastructure — things that are true regardless of which feature or
    domain is being served.

What does NOT belong here:
    Business logic, route handlers, AI provider code, database models.

Future evolution:
    As the system grows, core may gain a security.py (JWT helpers) and a
    telemetry.py (OpenTelemetry instrumentation bootstrap).
"""
