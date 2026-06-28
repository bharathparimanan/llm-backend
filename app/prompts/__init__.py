"""
Prompt templates.

Purpose:
    Centralise all prompt strings so they can be versioned, reviewed, and
    tested independently of business logic.

Responsibilities:
    - Store system prompt templates as typed, parameterised objects
    - Provide a registry so services can look up prompts by name/version
    - Enforce prompt structure (system / user / assistant roles)

What belongs here:
    PromptTemplate dataclasses or Pydantic models, a prompt registry,
    template rendering functions.

What does NOT belong here:
    Context assembly (that is context/), provider calls, HTTP code.

Future evolution:
    # FUTURE UPGRADE:
    # Introduce DSPy here when prompts should be optimised automatically.
    # DSPy treats prompts as learnable parameters; the registry abstraction
    # already provides the indirection needed to swap static templates for
    # DSPy-optimised signatures without changing the service layer.
"""
