"""
Test suite for foundation-ai.

Structure mirrors the application package layout:

    tests/
    ├── unit/          — fast, isolated tests with no I/O
    │   ├── core/
    │   ├── services/
    │   ├── providers/
    │   └── ...
    └── integration/   — tests that hit a real or mocked HTTP server
        └── api/

Convention:
    - Unit tests mock all external dependencies.
    - Integration tests use FastAPI's TestClient or AsyncClient.
    - Fixtures shared across the suite live in conftest.py.
"""
