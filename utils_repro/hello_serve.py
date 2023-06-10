import time
from ray import serve
from starlette.requests import Request

from utils.test import hello


@serve.deployment
class HelloModel:
    def __init__(self):
        hello()

    async def __call__(self, starlette_request: Request) -> None:
        hello()
        return f"{hello()}, {time.time()}"


model = HelloModel.bind()
