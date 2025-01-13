import os

from opentelemetry.ext.honeycomb import HoneycombSpanExporter
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from typing import List

# Replace those with the actual values.
HONEYCOMB_SERVICE_NAME = os.getenv("HONEYCOMB_SERVICE_NAME", "my-service-name")
HONEYCOMB_WRITE_KEY = os.getenv("HONEYCOMB_WRITE_KEY", "ZZzra0vKze3HFSLxzVDJtF")
HONEYCOMB_DATASET_NAME = os.getenv("HONEYCOMB_DATASET_NAME", "my-dataset-name2")


def default_tracing_exporter() -> List[SpanProcessor]:
    print(f"default_tracing_exporter() is called, {HONEYCOMB_WRITE_KEY}")
    exporter = HoneycombSpanExporter(
        service_name=HONEYCOMB_SERVICE_NAME,
        writekey=HONEYCOMB_WRITE_KEY,
        dataset=HONEYCOMB_DATASET_NAME,
    )
    return [SimpleSpanProcessor(exporter)]
