"""
AI provider adapters.

Purpose:
    Isolate all vendor SDK calls behind a stable internal interface.

Responsibilities:
    - Wrap the OpenAI Python SDK (and future SDKs) in thin adapter classes
    - Translate provider-specific errors into domain exceptions
    - Expose a uniform interface that the service layer calls regardless of
      which underlying model or vendor is active

What belongs here:
    One module per provider (e.g. openai_provider.py, anthropic_provider.py).
    A base interface/protocol that all providers must implement.

What does NOT belong here:
    Business logic, prompt assembly, HTTP route code, database access.

Design pattern:
    Strategy — each provider implements the same interface so the service layer
    can swap them without knowing which vendor is in use.

    # FUTURE UPGRADE:
    # Introduce LiteLLM here when multiple providers must be supported under a
    # single unified API.  LiteLLM acts as an abstraction layer across OpenAI,
    # Anthropic, Cohere, etc., making the strategy swap transparent.

Future evolution:
    A ProviderFactory (Factory pattern) will instantiate the correct provider
    based on runtime configuration when multi-model routing is introduced.
"""
