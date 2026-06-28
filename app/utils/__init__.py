"""
Shared utilities.

Purpose:
    Collect small, stateless helper functions that are genuinely reused across
    multiple packages and do not belong to any single domain.

Responsibilities:
    - String manipulation helpers
    - Date/time utilities
    - Token counting helpers (wrapping tiktoken)
    - Generic retry logic

What belongs here:
    Pure functions with no side effects and no dependencies on other app layers.
    If a utility grows large or domain-specific, promote it to its own package.

What does NOT belong here:
    Business logic, HTTP code, provider calls, configuration access.
    Utilities that belong to a single domain should live in that domain's package
    rather than here.

Future evolution:
    Keep this package lean.  Each time a helper is added, ask: does this belong
    to a specific domain?  If yes, move it there.
"""
