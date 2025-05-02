# DD_API_KEY=ecf2dc650787a01636306734e69f7105 DD_SITE="us5.datadoghq.com" bash -c "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"
#
#
#
# pip install opentelemetry-exporter-otlp-proto-http
# pip install opentelemetry-instrumentation
# pip install opentelemetry-instrumentation-fastapi


"""OpenTelemetry trace and span utilities."""

import typing

import fastapi
import opentelemetry.context
import opentelemetry.exporter.otlp.proto.http.trace_exporter
import opentelemetry.instrumentation.fastapi
import opentelemetry.sdk.resources
import opentelemetry.sdk.trace
import opentelemetry.sdk.trace.export
import opentelemetry.semconv._incubating.attributes.peer_attributes
import opentelemetry.semconv.attributes.service_attributes
import opentelemetry.trace


TRACER_NAME = "chaos"


def datadog_span_processor() -> opentelemetry.sdk.trace.SpanProcessor:
    """Return OTEL OTLP SpanExporter for integration with Datadog.

    To enable span export to Datadog over HTTP,
        1. ensure the following deps are installed:

            opentelemetry-exporter-otlp
            opentelemetry-exporter-otlp-proto-http

        2. set the envvar:

            OTEL_EXPORTER_OTLP_ENDPOINT=http://[datadog host]:4318
    """
    return opentelemetry.sdk.trace.export.BatchSpanProcessor(
        opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter()
    )


def debug_span_processor() -> opentelemetry.sdk.trace.SpanProcessor:
    """Return OTEL Console Span export for debugging."""
    return opentelemetry.sdk.trace.export.SimpleSpanProcessor(opentelemetry.sdk.trace.export.ConsoleSpanExporter())


def anyscale_span_processors() -> list[opentelemetry.sdk.trace.SpanProcessor]:
    """Add span processors to instrumentation for use by Anyscale in workspace.

    https://docs.anyscale.com/monitoring/tracing/#developing-on-workspaces

    Automagically, Anyscale adds SpanProcessors to the default TracerProvider during
    tracing initialization. In particular, the value of the envvar

        ANYSCALE_TRACING_EXPORTER_IMPORT_PATH=tl_anyscale_dev.services.utils.tracing:anyscale_span_processors

    should be an importable function which returns a list of SpanProcessors.
    """

    span_processors: list[opentelemetry.sdk.trace.SpanProcessor] = [
        debug_span_processor(),
        datadog_span_processor(),
    ]
    try:
        from ray.anyscale.serve._private.tracing_utils import default_tracing_exporter
        span_processors.extend(default_tracing_exporter("made_up_traces.log"))
    except ImportError:
        pass
    return span_processors


def init_fastapi_instrumentation(app: fastapi.FastAPI) -> None:
    """Initialize FastAPI OTEL third-party tracing for Ray Serve Deployments."""
    # add custom 500 handler
    # NOTE: this must come *before* init-ing the FastAPI instrumentor
    async def _set_otel_status_500_middleware(request: fastapi.Request, call_next: typing.Callable[[fastapi.Request], typing.Awaitable[fastapi.Response]]) -> fastapi.Response:
        """Set span attribute `http.status_code=500` on unhandled exceptions."""
        try:
            return await call_next(request)
        except Exception as exc:
            import opentelemetry
            import opentelemetry.trace.span
            current_span: opentelemetry.trace.span.Span = opentelemetry.trace.get_current_span()
            current_span.set_attribute("http.status_code", 500)
            raise exc from exc
    app.middleware("http")(_set_otel_status_500_middleware)

    fastapi_tracer_provider = get_tracer_provider(service_name="fastapi")
    for span_processor in anyscale_span_processors():
        fastapi_tracer_provider.add_span_processor(span_processor)
    opentelemetry.instrumentation.fastapi.FastAPIInstrumentor().instrument_app(
        app, exclude_spans=["receive", "send"], tracer_provider=fastapi_tracer_provider
    )


def get_tracer(service_name: str) -> opentelemetry.trace.Tracer:
    """Return OTEL application tracer with the given service name."""
    tracer_provider = get_tracer_provider(service_name=service_name)
    for span_processor in anyscale_span_processors():
        tracer_provider.add_span_processor(span_processor)
    return tracer_provider.get_tracer(TRACER_NAME)


def get_tracer_provider(service_name: str) -> opentelemetry.sdk.trace.TracerProvider:
    """Return OTEL application tracer provider with the given service name."""
    return opentelemetry.sdk.trace.TracerProvider(
        resource=opentelemetry.sdk.resources.Resource.create(
            {
                opentelemetry.semconv.attributes.service_attributes.SERVICE_NAME: service_name,
                opentelemetry.semconv._incubating.attributes.peer_attributes.PEER_SERVICE: service_name,
            }
        )
    )
