from ray import serve
from starlette.requests import Request


@serve.deployment
async def read_protected(request: Request):
    return {"msg": "pong"}

app = read_protected.bind()
