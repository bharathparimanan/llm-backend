"""
Top-level API router.

Aggregates all domain-specific APIRouters into a single router that is
mounted once in main.py.  This is the only file that needs to change when
a new domain (e.g. completions, conversations, documents) is added to the API.

Pattern:
    Each domain owns its own APIRouter in api/routes/<domain>.py.
    Those routers are imported and included here with an appropriate prefix
    and set of tags for the auto-generated OpenAPI documentation.
"""

from fastapi import APIRouter

from app.api.routes import health

api_router = APIRouter()

# ── Health ─────────────────────────────────────────────────────────────────────
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)

# FUTURE UPGRADE:
# Include the completions router when the inference service is implemented:
#
#   from app.api.routes import completions
#   api_router.include_router(
#       completions.router,
#       prefix="/completions",
#       tags=["completions"],
#   )

# FUTURE UPGRADE:
# Include a conversations router when conversation history is persisted:
#
#   from app.api.routes import conversations
#   api_router.include_router(
#       conversations.router,
#       prefix="/conversations",
#       tags=["conversations"],
#   )
