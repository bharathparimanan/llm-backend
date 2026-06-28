"""
HTTP route handlers.

Purpose:
    Define the URL surface area of the application.

Responsibilities:
    - Declare APIRouter instances grouped by domain (health, inference, …)
    - Validate incoming payloads using Pydantic schemas from app/schemas/
    - Delegate work to the service layer; never call providers or DB directly
    - Return typed response models

What belongs here:
    One module per domain (e.g. health.py, completions.py).
    Each module owns one APIRouter that is registered in api/router.py.

What does NOT belong here:
    Business logic, prompt templates, provider SDKs, database sessions.

Future evolution:
    As features expand (RAG, tool calling, agents) add new route modules here.
    Versioning is handled by the parent api/ layer, not inside individual routes.
"""
