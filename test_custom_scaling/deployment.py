import logging
from fastapi import FastAPI
from ray import serve
from starlette.requests import Request
from ray.serve.autoscaling_policy import AutoscalingContext
import requests

logger = logging.getLogger("ray.serve")


def custom_scaling(context: AutoscalingContext):
    # return 4
    # raise Exception("custom_scaling")
    # return requests.get("http://foobar.com").json()
    return requests.get("http://localhost:8000/app_scale/getter").json()["replicas"]


@serve.deployment(
    autoscaling_config={
        # "policy": MyAutoscalingPolicy,
        # "policy": custom_scaling,
        "policy": "deployment:custom_scaling",
        "max_replicas": 10,
        # "policy": "ray.serve._private.autoscaling_policy:BasicAutoscalingPolicy",
    }
)
class Model:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1

        return f"Model count: {self.count}"


app = FastAPI()


@serve.deployment()
@serve.ingress(app)
class Scale:
    def __init__(self):
        self.replicas = 1

    @app.get("/setter")
    async def setter(self, request: Request):
        logger.info("request", request)
        json_input = await request.json()
        logger.info("json_input", json_input)
        self.replicas = json_input["replicas"]
        return f"Scale replicas: {self.replicas}"

    @app.get("/getter")
    async def getter(self):
        return {"replicas": self.replicas}


app_scale = Scale.bind()
app_model = Model.bind()
# serve.run(app_scale, name="app_scale", route_prefix="/app_scale")
# serve.run(app_model, name="app_model", route_prefix="/app_model")
