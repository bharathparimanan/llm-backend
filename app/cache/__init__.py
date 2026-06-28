"""
Caching layer.

Purpose:
    Provide a simple, swappable cache abstraction to reduce redundant provider
    calls and improve response latency.

Responsibilities:
    - Define a CacheBackend interface (get / set / delete / clear)
    - Supply an in-process in-memory implementation for development
    - Provide a key-construction strategy (hash of model + messages)

What belongs here:
    Cache interface, in-memory backend, cache key helpers.

What does NOT belong here:
    Business logic, provider calls, HTTP code.

Future evolution:
    # FUTURE UPGRADE:
    # Replace the in-memory cache with Redis for distributed deployments.
    # When the application runs across multiple workers or pods, the in-process
    # cache is no longer shared.  Redis (via redis-py or aioredis) provides a
    # network-accessible store with TTL support and eviction policies.
    # The CacheBackend interface means this swap requires zero changes to the
    # service layer.
"""
