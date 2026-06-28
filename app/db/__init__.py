"""
Database layer.

Purpose:
    Manage database connections, ORM configuration, and migrations.

Responsibilities:
    - Provide an async SQLAlchemy engine and session factory
    - Define ORM-mapped table classes (SQLAlchemy DeclarativeBase)
    - Expose an AsyncSession dependency consumed by repositories

What belongs here:
    Engine setup, session factory, ORM base class, Alembic migration config.

What does NOT belong here:
    Repository query logic (repositories/), business logic, HTTP code.
    Domain models (models/) are separate from ORM table definitions here.

Future evolution:
    # FUTURE UPGRADE:
    # Add a second engine targeting a vector-capable database (e.g. PostgreSQL
    # with pgvector) when RAG is introduced.  The async session pattern used here
    # makes it straightforward to add a second connection pool alongside the
    # primary relational store.
"""
