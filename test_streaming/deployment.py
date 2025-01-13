from ray import serve
from fastapi import APIRouter, FastAPI, Depends
from starlette.responses import StreamingResponse
import logging
from ray._private.pydantic_compat import BaseModel
from typing import Dict
from starlette.requests import Request
import time
import json
from fastapi import Response as FastAPIResponse

ray_serve_logger = logging.getLogger('ray.serve')

server = FastAPI()


class ChatCompletions(BaseModel):
    messages: str
    num_iter: int = 10
    num_delay: float = 0.1


class Payload(BaseModel):
    data: str = ""


@serve.deployment()
@serve.ingress(server)
class ChatServiceRay:
    """
    curl -X POST localhost:8000/test  -H "Content-Type: application/json" -d '{"messages":"Hello2", "num_iter":11, "num_delay": 0.05}'
    """
    # @server.post("/test")
    # async def test(self, payload: ChatCompletions):
    #     print(f"payload!!!: {payload}, {payload.messages}, {payload.num_iter}, {payload.num_delay}")
    #     return "foo"

    @server.post("/completions")
    async def chat_completions(self, request: ChatCompletions):
        print(f"request!!! {request} {request.messages}, {request.num_iter}, {request.num_delay}")
        # ray_serve_logger.error(f"num_iter: {await request.json()}")

        async def _chat_response_generator():
            try:
                for i in range(10):
                    time.sleep(0.1)
                    chunk = {
                        "index": i,
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
            except Exception as e:
                ray_serve_logger.error(f"Error: {e}")
                yield f"data: Error: {str(e)}\n\n"

        return StreamingResponse(_chat_response_generator(), media_type="text/event-stream")


app = ChatServiceRay.bind()
# serve.run(app)

"""
curl -X POST localhost:8000/add_data  -H "Content-Type: application/json" -d '{"messages":"Hello"}'
"""
@serve.deployment()
@serve.ingress(server)
class MyApp:
    @server.post("/add_data")
    def add_data(self, payload: ChatCompletions = None):
        print(f"payload!!!: {payload}")
        return payload


app2 = MyApp.bind()
