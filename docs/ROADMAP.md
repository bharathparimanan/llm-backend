# Roadmap

This repository is an evolving educational reference implementation.
Each module introduces one new architectural concern, building on the
foundation established in the previous module without restructuring it.

---

## Evolution Path

```
Module 1 — Repository Foundation & Architecture  ← YOU ARE HERE
│
│  Establish the layered architecture, package structure, core
│  infrastructure (config, logging, exceptions, lifecycle), and
│  a working FastAPI bootstrap with health-check endpoints.
│
▼

Module 2 — Single-Model Inference
│
│  Implement the OpenAI provider adapter, context builder, prompt
│  registry, and completion service.  Add the /completions route.
│  Introduce the in-memory cache for repeated prompts.
│
▼

Module 3 — Multi-Model Routing
│
│  Introduce LiteLLM as the provider abstraction layer.  Add a
│  ProviderFactory and a model-routing strategy that selects the
│  best provider based on cost, latency, or capability requirements.
│  Add Anthropic and a local model as alternative providers.
│
▼

Module 4 — Conversation Persistence
│
│  Add SQLAlchemy + PostgreSQL.  Implement ConversationRepository
│  and MessageRepository.  Introduce async database sessions.
│  Add conversation management endpoints (create, list, retrieve).
│
▼

Module 5 — Retrieval-Augmented Generation (RAG)
│
│  Add a vector store (pgvector or Pinecone).  Implement a
│  DocumentRepository and an embedding provider.  Extend the
│  context builder to retrieve relevant chunks before assembling
│  the final prompt.  Introduce LlamaIndex for document ingestion.
│  Add RAGAS for RAG evaluation.
│
▼

Module 6 — Tool Calling
│
│  Expose tool definitions to the model.  Implement a tool
│  dispatcher that routes tool calls to registered handlers.
│  Add web search, calculator, and code execution tools.
│
▼

Module 7 — Single Agent
│
│  Introduce an agent loop: plan → act (tool call) → observe →
│  repeat until the goal is achieved.  Introduce LangGraph for
│  graph-based orchestration of multi-step reasoning.
│
▼

Module 8 — Multi-Agent Systems
│
│  Compose multiple specialised agents (researcher, coder, critic)
│  into a supervisor graph.  Agents communicate via a shared message
│  bus.  Introduce agent memory and long-horizon planning.
│
▼

Module 9 — Distributed AI Platform
│
│  Horizontal scaling: stateless API workers, shared Redis cache,
│  distributed tracing with OpenTelemetry, async task queues
│  (Celery or ARQ) for long-running agent runs, and a streaming
│  SSE/WebSocket layer for real-time progress updates.
```

---

## Technology Introduction Map

| Technology | Introduced in | Why at that point |
|---|---|---|
| FastAPI + Pydantic | Module 1 | Core web framework from the start |
| OpenAI SDK | Module 2 | First provider call |
| LiteLLM | Module 3 | Multi-provider abstraction becomes necessary |
| SQLAlchemy + Alembic | Module 4 | Persistence is needed for conversations |
| pgvector / Pinecone | Module 5 | Vector search for RAG retrieval |
| LlamaIndex | Module 5 | Document ingestion pipeline |
| RAGAS | Module 5 | RAG evaluation framework |
| LangChain | Module 6 | Tool-calling chains and agent primitives |
| LangGraph | Module 7 | Graph-based agent orchestration |
| Redis | Module 9 | Distributed cache and task coordination |
| OpenTelemetry | Module 9 | Production observability at scale |
| DSPy | Post-Module 9 | Automatic prompt optimisation |

---

## Stability Guarantee

Each module is backward-compatible with the previous one.
The layered architecture and dependency inversion established in
Module 1 are the reason this guarantee is maintainable: new
capabilities are added by implementing existing interfaces, not by
replacing them.
