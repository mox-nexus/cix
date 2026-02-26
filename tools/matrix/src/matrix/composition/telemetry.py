"""Telemetry — optional SDK configuration for Matrix tracing.

Requires: uv add matrix[otel]

Matrix instruments with opentelemetry-api (always available, no-op by default).
This module configures the SDK so spans actually get exported. For custom
setups, configure the OpenTelemetry SDK directly — Matrix doesn't care how.
"""

from __future__ import annotations

import os


def configure_telemetry(
    *,
    service_name: str = "matrix",
    endpoint: str | None = None,
    console: bool = False,
) -> None:
    """Configure OpenTelemetry SDK for Matrix tracing.

    Args:
        service_name: Service name in traces.
        endpoint: OTLP gRPC endpoint (e.g. "http://localhost:4317").
            Falls back to OTEL_EXPORTER_OTLP_ENDPOINT env var.
        console: Print spans to stdout (useful for debugging).

    Raises:
        ImportError: If opentelemetry-sdk is not installed.

    Example::

        # Phoenix (local UI at localhost:6006)
        configure_telemetry(endpoint="http://localhost:4317")

        # Debug to console
        configure_telemetry(console=True)

        # Production (reads OTEL_EXPORTER_OTLP_ENDPOINT from env)
        configure_telemetry(service_name="ix-experiments")
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            BatchSpanProcessor,
            ConsoleSpanExporter,
            SimpleSpanProcessor,
        )
    except ImportError as e:
        raise ImportError(
            "Telemetry requires opentelemetry-sdk. Install with: uv add matrix[otel]"
        ) from e

    resolved_endpoint = endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    if not resolved_endpoint and not console:
        return  # Nothing to export — API stays no-op

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    if resolved_endpoint:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )

        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=resolved_endpoint))
        )

    if console:
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
