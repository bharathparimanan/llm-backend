"""
Domain models.

Purpose:
    Define the core data structures of the application domain — independent of
    any HTTP or persistence framework.

Responsibilities:
    - Represent domain entities (Conversation, Message, Completion, …)
    - Contain domain validation rules that are true regardless of transport
    - Act as the vocabulary shared across services, repositories, and context builders

What belongs here:
    Plain dataclasses, Pydantic BaseModels, or Enum types that represent
    business concepts.  No SQLAlchemy ORM models here — those live in db/.

What does NOT belong here:
    HTTP request/response schemas (schemas/), ORM-mapped tables (db/),
    provider-specific data structures.

Future evolution:
    As the domain grows (tools, agents, memory) new model files are added here.
    Each model file maps to a distinct bounded context within the application.
"""
