"""
Native OpenTelemetry setup for Keywords AI tracing.

This module configures OpenTelemetry with OTLP export to Keywords AI dashboard.
Provides robust async tracing for LangGraph multi-agent nodes.
"""

import os
import sys
import requests
from typing import List, Dict, Any
from threading import Lock
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import SpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME


class ManualSpanCollector(SpanProcessor):
    """Collects spans in memory for manual ingestion to Keywords AI."""

    def __init__(self):
        self.spans: List[ReadableSpan] = []
        self.lock = Lock()

    def on_start(self, span: ReadableSpan, parent_context=None) -> None:
        """Called when a span starts."""
        pass

    def on_end(self, span: ReadableSpan) -> None:
        """Called when a span ends - collect it."""
        with self.lock:
            self.spans.append(span)

    def get_and_clear_spans(self) -> List[ReadableSpan]:
        """Get all collected spans and clear the buffer."""
        with self.lock:
            spans = self.spans.copy()
            self.spans.clear()
            return spans

    def shutdown(self) -> None:
        """Shutdown the processor."""
        self.spans.clear()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush is a no-op for manual collection."""
        return True


# Global span collector instance
span_collector = ManualSpanCollector()


def ingest_trace_to_keywords(api_key: str, thread_id: str = None) -> bool:
    """
    Manually ingest collected traces to Keywords AI.

    Args:
        api_key: Keywords AI API key
        thread_id: Optional thread/session ID for grouping traces

    Returns:
        bool: True if ingestion succeeded, False otherwise
    """
    try:
        spans = span_collector.get_and_clear_spans()
        if not spans:
            print("[TRACE] No spans to ingest", file=sys.stderr)
            return True

        # Convert spans to Keywords AI format
        # Each span becomes a dict with trace_unique_id, span_unique_id, span_name
        trace_data = []
        for span in spans:
            trace_id = format(span.context.trace_id, "032x")
            span_id = format(span.context.span_id, "016x")

            span_dict = {
                "trace_unique_id": trace_id,
                "span_unique_id": span_id,
                "span_name": span.name,
                "start_time": span.start_time,
                "end_time": span.end_time,
            }

            # Add attributes if present
            if span.attributes:
                span_dict.update({
                    f"attr_{k}": str(v)
                    for k, v in span.attributes.items()
                })

            # Add parent span ID if present
            if span.parent:
                span_dict["parent_span_id"] = format(span.parent.span_id, "016x")

            # Add thread_id if provided (for grouping)
            if thread_id:
                span_dict["thread_id"] = thread_id

            trace_data.append(span_dict)

        # Send to Keywords AI ingestion endpoint
        endpoint = "https://api.keywordsai.co/api/openai/v1/traces/ingest"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        print(f"[TRACE] Sending {len(trace_data)} spans to Keywords AI", file=sys.stderr)

        response = requests.post(
            endpoint,
            json=trace_data,  # Send as list of dicts
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print(f"[TRACE] Successfully ingested {len(trace_data)} spans", file=sys.stderr)
            return True
        else:
            print(f"[TRACE] Ingestion failed: {response.status_code} - {response.text}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"[TRACE] Ingestion error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def setup_otel():
    """
    Initialize OpenTelemetry with Keywords AI OTLP endpoint.

    This setup:
    1. Creates a TracerProvider with service identification
    2. Configures OTLP exporter to send traces to Keywords AI
    3. Uses BatchSpanProcessor for efficient async trace export
    4. Enables force_flush() for immediate export before FastAPI responses
    """

    # Get configuration from environment
    service_name = os.getenv("OTEL_SERVICE_NAME", "canvas-lms-agent")
    api_key = os.getenv("KEYWORDS_AI_API_KEY")

    # Debug: Verify API key is loaded
    if api_key:
        print(f"[DEBUG] API Key found: {api_key[:4]}...", file=sys.stderr, flush=True)
    else:
        print("[ERROR] KEYWORDS_AI_API_KEY not found in environment", file=sys.stderr)
        raise ValueError(
            "KEYWORDS_AI_API_KEY not found in environment. "
            "Please set it in your .env file."
        )

    # Create resource with service identification
    resource = Resource(attributes={
        SERVICE_NAME: service_name,
        "deployment.environment": "production",
        "service.version": "1.0.0"
    })

    # Create TracerProvider
    provider = TracerProvider(resource=resource)

    # Add manual span collector for Keywords AI ingestion
    # We collect spans in memory and send them manually after the request
    provider.add_span_processor(span_collector)

    # Set as global tracer provider
    trace.set_tracer_provider(provider)

    print(f"[OTEL] TracerProvider initialized for service: {service_name}")
    print(f"[OTEL] Exporting traces to: https://api.keywordsai.co")

    return provider


def get_tracer(name: str = "canvas-lms-agent"):
    """
    Get a tracer instance for creating spans.

    Args:
        name: Name of the tracer (typically module or component name)

    Returns:
        Tracer instance for creating spans
    """
    return trace.get_tracer(name)


def get_api_key():
    """Get the Keywords AI API key from environment."""
    return os.getenv("KEYWORDS_AI_API_KEY")
