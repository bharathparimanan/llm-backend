"""
API schemas — Pydantic request and response models.

Purpose:
    Define the public contract of the HTTP API — what the client sends and
    what the server returns.

Responsibilities:
    - Request body validation (Pydantic BaseModel)
    - Response serialisation models
    - API-level field aliasing and example generation for OpenAPI docs

What belongs here:
    Input/output models used directly by route handlers.  Keep these thin —
    they should map cleanly from HTTP payload → domain model.

What does NOT belong here:
    Domain logic, database models, provider-specific structures.
    If a schema is only used internally, it belongs in models/ instead.

Future evolution:
    When the API is versioned (v1 → v2), schemas are namespaced accordingly
    (schemas/v1/, schemas/v2/) so old clients are not broken.
"""
