"""
Service layer — business orchestration.

Purpose:
    Coordinate application workflows without owning infrastructure details.

Responsibilities:
    - Implement use-case logic (e.g. "handle a chat completion request")
    - Assemble context, call providers, apply post-processing
    - Own the boundary between the HTTP layer and the provider/repository layers

What belongs here:
    One class or module per use case.  Services accept provider and repository
    interfaces (injected via dependencies.py), not concrete implementations.

What does NOT belong here:
    HTTP request/response code, raw SQL, OpenAI SDK calls, prompt strings.

Design pattern:
    Services act as the Facade / Application Service in DDD terms.  They depend
    on abstractions (interfaces defined in providers/ and repositories/), making
    them easy to unit-test with mocks.

Future evolution:
    When orchestration becomes multi-step and graph-based, services will delegate
    to a LangGraph graph rather than calling providers directly.

    # FUTURE UPGRADE:
    # Introduce LangGraph when orchestration becomes graph-based.
    # Services will become thin entry points that invoke compiled graphs.
"""
