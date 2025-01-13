from fastapi import FastAPI
from fp import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from ray import serve
from ray.anyscale.serve._private.tracing_utils import (
    get_trace_context
)
from ray.serve.handle import DeploymentHandle
import random

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)


@serve.deployment
@serve.ingress(app)
class MyIngress:
    def __init__(self, model: DeploymentHandle):
        self.model = model

    @app.get("/")
    def hello(self):
        # Create a new span that is associated with the current trace
        tracer = trace.get_tracer("test_tracing")
        with tracer.start_as_current_span(
                "ingress_span", context=get_trace_context()
        ) as span:
            prediction = self.model.predict.remote().result()

            replica_context = serve.get_replica_context()
            attributes = {
                "deployment": replica_context.deployment,
                "replica_id": replica_context.replica_id.unique_id
            }
            span.set_attributes(attributes)
            span.set_status(
                Status(status_code=StatusCode.OK)
            )

            # Return message
            return f"Hello world! {prediction}"


@serve.deployment
class MyModel:
    def predict(self):
        tracer = trace.get_tracer("test_tracing")
        with tracer.start_as_current_span(
                "predict_span", context=get_trace_context()
        ) as span:
            return random.randint(1,10)


app = MyIngress.bind(MyModel.bind())
