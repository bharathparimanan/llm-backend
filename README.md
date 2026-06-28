# foundation-ai

A production-grade educational reference implementation of a single-model LLM backend.

Built to demonstrate how modern AI backend systems are designed from first principles —
before introducing frameworks such as LangChain, LangGraph, LiteLLM, DSPy, or LlamaIndex.

---

## Goals

- Teach layered architecture applied to AI backends
- Establish clean architectural contracts that future modules extend without restructuring
- Show how engineering best practices (DI, Repository pattern, Config isolation) apply to LLM systems
- Provide a codebase that reads like production code maintained by an experienced team

---

## Current Scope (Module 1)

- FastAPI application bootstrap
- Layered architecture scaffold
- Core infrastructure: configuration, logging, exceptions, lifespan
- Health-check endpoints (`/api/v1/health`, `/api/v1/health/ready`)
- Request ID middleware
- Test scaffold (unit + integration)

**Not yet implemented:** inference, conversation management, providers, RAG, agents.

---

## Repository Structure

```
foundation-ai/
│
├── app/
│   ├── api/
│   │   ├── routes/          # HTTP route handlers (one module per domain)
│   │   ├── middleware/      # Cross-cutting HTTP middleware
│   │   ├── dependencies.py  # FastAPI Depends() wiring
│   │   └── router.py        # Aggregates all APIRouters
│   │
│   ├── core/
│   │   ├── config.py        # Pydantic Settings — single source of truth
│   │   ├── logging.py       # Structured logging setup
│   │   ├── exceptions.py    # Domain exception hierarchy
│   │   ├── constants.py     # App-wide compile-time constants
│   │   └── lifecycle.py     # FastAPI lifespan (startup / shutdown)
│   │
│   ├── services/            # Use-case orchestration (business layer)
│   ├── providers/           # AI vendor SDK adapters (OpenAI, …)
│   ├── context/             # LLM context assembly
│   ├── prompts/             # Prompt template registry
│   ├── repositories/        # Data access abstractions
│   ├── models/              # Domain entities
│   ├── schemas/             # Pydantic HTTP request/response schemas
│   ├── cache/               # Cache abstraction
│   ├── observability/       # Metrics and tracing
│   ├── db/                  # Database engine and sessions
│   ├── utils/               # Stateless utility functions
│   └── main.py              # Application factory + entry point
│
├── tests/
│   ├── unit/                # Isolated tests, no I/O
│   └── integration/         # Full HTTP pipeline tests
│
├── docs/
│   ├── ARCHITECTURE.md      # Layered architecture, diagrams, patterns
│   ├── DESIGN_DECISIONS.md  # Rationale and trade-offs
│   └── ROADMAP.md           # Evolution from Module 1 → distributed platform
│
├── scripts/
│   └── start.sh             # Development server launcher
│
├── .env.example             # Environment variable reference
├── pyproject.toml           # Tool configuration (pytest, ruff, mypy)
└── requirements.txt         # Python dependencies
```

---

## Development Setup

### Prerequisites

- Python 3.12+
- An OpenAI API key

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd foundation-ai

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set OPENAI_API_KEY

# 5. Start the development server
./scripts/start.sh
# or: uvicorn app.main:app --reload

# 6. Verify the service is running
curl http://localhost:8000/api/v1/health
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=term-missing

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/
```

---

## Request Lifecycle

```
Client
  │
  ▼
Middleware (Request-ID, CORS)
  │
  ▼
Route Handler  ── validates schema ──▶  Pydantic
  │
  ▼
Service  ── assembles context ──▶  Context Builder
  │                                    │
  │                                    ▼
  │                               Prompt Registry
  │
  ├── calls ──▶  Provider (OpenAI)
  │
  ▼
Response  ──▶  Client
```

---

## Documentation

| Document | Description |
|---|---|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Layered architecture, Mermaid diagrams, design patterns |
| [DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md) | Rationale and trade-offs for key choices |
| [ROADMAP.md](docs/ROADMAP.md) | Evolution from single model to distributed AI platform |

---

## Roadmap

```
Module 1  Repository Foundation          ← current
Module 2  Single-Model Inference
Module 3  Multi-Model Routing
Module 4  Conversation Persistence
Module 5  RAG
Module 6  Tool Calling
Module 7  Single Agent
Module 8  Multi-Agent Systems
Module 9  Distributed AI Platform
```

See [ROADMAP.md](docs/ROADMAP.md) for the full technology introduction map.
