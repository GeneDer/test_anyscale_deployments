import asyncio
import logging
import time
from fastapi import FastAPI
from ray import serve
from ray.serve import get_app_handle
from ray.serve.handle import DeploymentHandle
from starlette.requests import Request

logger = logging.getLogger("ray.serve")


class Foo:
    def __init__(self, a, i):
        self.a = a
        self.i = i


@serve.deployment()
class SlowThing:

    async def do_it(self, foo: Foo) -> str:
        logger.info(f"{foo.i} Start Request")
        duration = 0
        start = time.time()
        while duration < 10:
            duration = time.time() - start
            print("HI")
            await asyncio.sleep(1)
        logger.info(f"{foo.i} Done Request")

        return foo.a.upper()


app = FastAPI()


@serve.deployment()
@serve.ingress(app)
class HttpEntrypointService:

    def __init__(self):
        self.i = 0

    @app.get("/")
    async def root(self, http_request: Request):
        self.i += 1
        i = self.i
        start = time.time()

        logger.info(f"{i} Got request")
        foo_handle: DeploymentHandle = get_app_handle("slow_thing")
        foo = Foo(a=http_request.url.path, i=i)
        answer = await foo_handle.do_it.remote(foo)

        duration = time.time() - start

        logger.info(f"{i} Sending response {duration}")
        return answer


slow_thing = SlowThing.bind()
http_entrypoint_service = HttpEntrypointService.bind()
