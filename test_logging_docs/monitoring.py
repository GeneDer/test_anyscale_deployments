from ray import serve
import logging
from starlette.requests import Request

logger = logging.getLogger("ray.serve")
logger2 = logging.getLogger("ray2")


@serve.deployment
class SayHello:
    async def __call__(self, request: Request) -> str:
        logger.info("this is from serve logger")
        logger2.info("this is from logger2")
        print("this is from print")
        raise RuntimeError("this is error")
        return "hi"


@serve.deployment
class Silenced:
    def __init__(self):
        logger.setLevel(logging.ERROR)


say_hello = SayHello.bind()
