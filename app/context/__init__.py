"""
Context construction.

Purpose:
    Assemble the structured context that is passed to the language model.

Responsibilities:
    - Build the list of messages (system, user, assistant) for a given request
    - Apply token budget limits and truncation strategies
    - Inject retrieved documents when RAG is active (future)

What belongs here:
    Context builder classes, message formatters, token counting utilities.

What does NOT belong here:
    Prompt template strings (those live in prompts/), raw provider calls, HTTP code.

Design pattern:
    Builder — context is constructed incrementally (system message → history →
    retrieved chunks → user message) and handed to the service layer as a
    complete, validated object.

Future evolution:
    # FUTURE UPGRADE:
    # Introduce RAG retrieval before context construction.
    # When RAG is active the context builder will receive a list of retrieved
    # document chunks from the retrieval service and embed them between the
    # system message and the user message, respecting the token budget.
"""
