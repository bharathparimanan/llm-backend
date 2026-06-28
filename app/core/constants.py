"""
Application-wide constants.

These values are fixed at compile time and do NOT vary by environment.
If a value can change between environments, it belongs in config.py instead.

Grouping constants here prevents magic strings and numbers from scattering
across the codebase, making refactors and audits straightforward.
"""

# ─── API ──────────────────────────────────────────────────────────────────────

API_V1_PREFIX: str = "/api/v1"

# ─── HTTP headers ─────────────────────────────────────────────────────────────

REQUEST_ID_HEADER: str = "X-Request-ID"
CORRELATION_ID_HEADER: str = "X-Correlation-ID"

# ─── OpenAI roles ─────────────────────────────────────────────────────────────

ROLE_SYSTEM: str = "system"
ROLE_USER: str = "user"
ROLE_ASSISTANT: str = "assistant"

# ─── Token limits ─────────────────────────────────────────────────────────────

# Conservative upper bound used when a per-request max_tokens is not specified.
# Adjust in config.py (default_max_tokens) for environment-specific overrides.
ABSOLUTE_MAX_TOKENS: int = 4096

# ─── Health check ─────────────────────────────────────────────────────────────

HEALTH_STATUS_OK: str = "ok"
HEALTH_STATUS_DEGRADED: str = "degraded"

# ─── Cache ────────────────────────────────────────────────────────────────────

# Default TTL for cached completions (seconds).  In-memory only for now.
# FUTURE UPGRADE:
# When Redis is introduced, this TTL will be passed to the SET command.
CACHE_DEFAULT_TTL_SECONDS: int = 300
