"""
serve run deployment2:app

curl -X POST localhost:8000/completions  -H "Content-Type: application/json" -d '{"messages":"Hello2", "num_iter":11, "num_delay": 0.05}'
"""
import json
import logging
import time
from fastapi import FastAPI
from ray import serve
from ray._private.pydantic_compat import BaseModel
from starlette.responses import StreamingResponse

server = FastAPI()

ray_serve_logger = logging.getLogger('ray.serve')


class ChatCompletions(BaseModel):
    messages: str
    num_iter: int
    num_delay: float


@serve.deployment()
@serve.ingress(server)
class ChatServiceRay:
    def __init__(self):
        # Some model initialization here.
        pass

    @server.post("/completions")
    async def chat_completions(self, request: ChatCompletions):
        ray_serve_logger.error(f"num_iter: {request.num_iter}")

        async def _chat_response_generator():
            try:
                for i in range(request.num_iter):
                    time.sleep(request.num_delay)
                    chunk = {
                        "index": i,
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
            except Exception as e:
                ray_serve_logger.error(f"Error: {e}")
                yield f"data: Error: {str(e)}\n\n"

        return StreamingResponse(_chat_response_generator(), media_type="text/event-stream")


app = ChatServiceRay.bind()
