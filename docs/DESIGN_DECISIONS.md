# Design Decisions

Concise rationale for the key architectural choices made in Module 1.

---

## FastAPI

**Choice:** FastAPI as the web framework.

**Rationale:**
- Native async support matches the I/O-bound nature of LLM API calls.
- Pydantic integration provides automatic request validation and OpenAPI
  documentation generation at zero extra cost.
- The dependency injection system (`Depends()`) enables clean separation
  between route handlers and their collaborators.

**Trade-offs:**
- FastAPI is an async-first framework; blocking code in route handlers
  will block the event loop.  All provider calls must be `await`ed.
- Less opinionated than Django; the team must establish conventions
  (this repository) rather than inheriting them from the framework.

---

## Layered Architecture

**Choice:** Strict horizontal layers (API → Service → Domain → Infrastructure).

**Rationale:**
- Each layer can be tested in isolation by mocking the layer below.
- Dependency direction is enforced by convention and code review;
  violations are immediately visible in imports.
- New capabilities (RAG, tool calling) extend existing layers rather
  than cutting across them.

**Trade-offs:**
- Adds indirection for simple CRUD operations.  Acceptable here because
  LLM workflows are never truly simple; they always evolve.
- Requires discipline to maintain; a linter rule (e.g. `import-linter`)
  can enforce layer boundaries automatically.

---

## Dependency Injection

**Choice:** FastAPI `Depends()` for all cross-cutting concerns.

**Rationale:**
- Route handlers declare what they need; they do not construct it.
  This is the classic Dependency Inversion Principle applied at the
  HTTP layer.
- `app.dependency_overrides` makes it trivial to swap any dependency
  in tests without patching or monkeypatching.

**Trade-offs:**
- `Depends()` adds a small amount of boilerplate per route.
- Deeply nested dependencies can be hard to trace; keep the dependency
  graph shallow.

---

## Configuration Isolation (Pydantic Settings)

**Choice:** All runtime settings read from environment variables via
`pydantic-settings.BaseSettings`, accessed through a single `settings` object.

**Rationale:**
- Twelve-Factor App principle: configuration in the environment.
- Type-safe: Pydantic validates and coerces values at startup, so type
  errors surface immediately rather than at the first use of a setting.
- `lru_cache` ensures the `.env` file is parsed once per process.

**Trade-offs:**
- A required field with no default (`openai_api_key`) causes the process
  to exit immediately if not provided.  This is intentional fail-fast
  behaviour.
- Tests must clear the `lru_cache` when overriding settings.

---

## Async Programming

**Choice:** The application is designed to be async-first, even though
Module 1 does not yet make async provider calls.

**Rationale:**
- OpenAI's Python SDK (`openai.AsyncOpenAI`) is async-native.
- Uvicorn runs an asyncio event loop; async route handlers allow many
  concurrent requests to share one event loop thread efficiently.
- Adopting async from the start avoids a painful migration later when
  concurrency becomes a requirement.

**Trade-offs:**
- Blocking code (e.g. CPU-bound tasks, synchronous database drivers)
  must be run in a thread pool (`asyncio.to_thread`) to avoid starving
  the event loop.
- Async code is harder to read and debug than synchronous code for
  engineers unfamiliar with asyncio.

---

## Repository Pattern

**Choice:** Data access hidden behind repository interfaces even though
Module 1 has no database.

**Rationale:**
- Establishing the interface now means services are already written
  against an abstraction.  Adding a real database in Module 2 requires
  only a new concrete implementation, not a refactor of service code.

**Trade-offs:**
- Adds an empty package and some boilerplate in Module 1.  The cost is
  low; the benefit (zero-refactor database introduction) is high.

---

## Separate `models/` and `schemas/`

**Choice:** Domain models (`models/`) are distinct from HTTP schemas (`schemas/`).

**Rationale:**
- HTTP schemas change when the API contract changes.  Domain models
  change when the business rules change.  Mixing them couples two
  independent change axes.
- Domain models can be reused by repository implementations, background
  workers, and CLI scripts without pulling in FastAPI or HTTP concerns.

**Trade-offs:**
- Mapping between schemas and models adds a small amount of code.
  In practice this mapping belongs in the route handler or a dedicated
  mapper function.
