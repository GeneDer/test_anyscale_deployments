import time

from fastapi import FastAPI
from ray import serve
from starlette.requests import Request

app = FastAPI()


@serve.deployment(num_replicas=3)
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.post("/hello")
    def root(self, request: Request, user_input: dict):
        return {"app_name": user_input["app_name"]}


serve_app = MyFastAPIDeployment.bind()
