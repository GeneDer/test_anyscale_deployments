import requests
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import (
    TraceContextTextMapPropagator,
)
from opentelemetry.trace.status import Status, StatusCode
from ray import serve
from ray.anyscale.serve._private.tracing_utils import (
    setup_tracing, get_trace_context
)

# Service specific config
base_url = "https://tracing-service-with-exporter3-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
token = "NelUpLISC7-2qmL6aqtbfuvnUkHif3y-45vLcAk7d2c"
base_url = "https://tracing-service-with-exporter-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
token = "xonUl22Ygnq0UXizVz-X7Ce5gAceK-akeit2W9os2ZU"

# Requests config
path = "/"
full_url = f"{base_url}{path}"

setup_tracing(
    component_name="upstream_app",
    component_id="345",
)
tracer = trace.get_tracer("test_tracing1")

# with tracer.start_as_current_span("upstream_app") as span:
with tracer.start_as_current_span("upstream_app"):
    print(f"tracer.span_processor: {tracer.span_processor}")
    ctx = get_trace_context()
    print(f"in between ctx: {ctx}")

    headers = {"Authorization": f"Bearer {token}"}
    TraceContextTextMapPropagator().inject(headers, ctx)
    print(f"headers: {headers}")
    resp = requests.get(base_url, headers=headers)
    print(resp.text)

    # attributes = {
    #     "deployment": "foo",
    #     "replica_id": "bar"
    # }
    # span.set_attributes(attributes)
    # span.set_status(
    #     Status(status_code=StatusCode.OK)
    # )
