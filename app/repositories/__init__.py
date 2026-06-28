"""
Data access layer (Repository pattern).

Purpose:
    Abstract all persistence operations behind a stable interface so the
    service layer never depends on a specific database technology.

Responsibilities:
    - Define repository interfaces (protocols) for each domain entity
    - Provide concrete implementations backed by the chosen database
    - Translate ORM/query results into domain models

What belongs here:
    Abstract base repositories (interfaces), concrete implementations per
    storage technology (SQL, vector store, Redis, …).

What does NOT belong here:
    Business logic, HTTP code, provider SDK calls.

Design pattern:
    Repository — services call repository.save() / repository.find_by_id()
    without knowing whether the backend is PostgreSQL, SQLite, or a vector DB.

Future evolution:
    # FUTURE UPGRADE:
    # Introduce a VectorRepository when RAG is active.
    # It will expose find_similar(query_embedding, k) backed by pgvector,
    # Pinecone, or Weaviate — the service layer calls the same interface
    # regardless of which vector store is configured.
"""
