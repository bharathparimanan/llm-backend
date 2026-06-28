"""
Observability — metrics, tracing, and structured logging exporters.

Purpose:
    Instrument the application so that its internal behaviour is visible in
    production without changing business code.

Responsibilities:
    - Bootstrap OpenTelemetry SDK (traces + metrics)
    - Provide decorators / context managers for manual span creation
    - Export metrics (token usage, latency, error rate) to the configured backend

What belongs here:
    OTel setup, Prometheus metrics definitions, span helper utilities.
    Logging configuration lives in core/logging.py; only exporters that need
    heavy SDK setup belong here.

What does NOT belong here:
    Business logic, provider calls, route handlers.

Future evolution:
    # FUTURE UPGRADE:
    # Instrument LLM calls with OpenTelemetry semantic conventions for GenAI
    # (OTEL_SEMCONV_STABILITY_OPT_IN=genai) so that token counts, model names,
    # and latencies are exported to Grafana / Datadog / Honeycomb automatically.
"""
