import os
from opentelemetry import trace
from opentelemetry.ext.honeycomb import HoneycombSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider

# Replace those with the actual values.
HONEYCOMB_SERVICE_NAME = os.getenv("HONEYCOMB_SERVICE_NAME", "my-service-name")
HONEYCOMB_WRITE_KEY = os.getenv("HONEYCOMB_WRITE_KEY", "ZZzra0vKze3HFSLxzVDJtF")
HONEYCOMB_DATASET_NAME = os.getenv("HONEYCOMB_DATASET_NAME", "my-dataset-name")

trace.set_tracer_provider(TracerProvider())
print(
    f"HONEYCOMB_SERVICE_NAME: {HONEYCOMB_SERVICE_NAME} "
    f"HONEYCOMB_WRITE_KEY: {HONEYCOMB_WRITE_KEY} "
    f"HONEYCOMB_DATASET_NAME: {HONEYCOMB_DATASET_NAME}"
)
exporter = HoneycombSpanExporter(
    service_name=HONEYCOMB_SERVICE_NAME,
    writekey=HONEYCOMB_WRITE_KEY,
    dataset=HONEYCOMB_DATASET_NAME,
)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

tracer = trace.get_tracer(__name__)
for i in range(10):
    with tracer.start_as_current_span('span_one'):
        with tracer.start_as_current_span('span_two'):
            with tracer.start_as_current_span('span_three'):
                print(f"Hello, from a child span: {i}")


# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import (
#     BatchSpanProcessor,
#     ConsoleSpanExporter,
# )
#
# provider = TracerProvider()
# processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor)
#
# # Sets the global default tracer provider
# trace.set_tracer_provider(provider)
#
# # Creates a tracer from the global tracer provider
# tracer = trace.get_tracer("my.tracer.name")
#
#
# def do_work():
#     with tracer.start_as_current_span("parent") as parent:
#         # do some work that 'parent' tracks
#         print("doing some work...")
#         # Create a nested span to track nested work
#         with tracer.start_as_current_span("child") as child:
#             # do some work that 'child' tracks
#             print("doing some nested work...")
#             # the nested span is closed when it's out of scope
#
#         # This span is also closed when it goes out of scope
#
#
# do_work()
