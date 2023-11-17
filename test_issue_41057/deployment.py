import asyncio
import ray.serve as serve
from starlette.requests import Request
from starlette.responses import StreamingResponse


@serve.deployment()
class RayDeploymentWithBatching:
    @serve.batch(max_batch_size=20)
    async def batch(self, batch: list[list[str]]):
        await asyncio.sleep(0.05)
        return [[f"T({text})" for text in request] for request in batch]

    async def __call__(self, request: Request):
        request_json = await request.json()
        resp = await self.batch(request_json["items"])
        return {"response": resp}


@serve.deployment
class Textgen:
    @serve.batch(max_batch_size=4)
    async def batch_handler(self, prompts: list[str]):
        await asyncio.sleep(0.05)
        for _ in range(10):
            # Check that the batch handler can yield unhashable types
            prompt_responses = [{"value": prompt} for prompt in prompts]
            yield prompt_responses

    async def value_extractor(self, prompt_responses):
        async for prompt_response in prompt_responses:
            yield prompt_response["value"]

    async def __call__(self, request):
        request_json = await request.json()
        print("request_json", request_json)
        prompt = " ".join(request_json["items"])
        response_values = self.value_extractor(self.batch_handler(prompt))
        return StreamingResponse(response_values)


@serve.deployment
class ModelStreaming:
    @serve.batch(max_batch_size=2)
    async def handle_batch(self, requests):
        await asyncio.sleep(0.5)
        for i in range(10):
            yield [str(i + j) for j in range(len(requests))]

    async def __call__(self, request):
        return StreamingResponse(self.handle_batch(request))

# app = RayDeploymentWithBatching.bind()
# app = Textgen.bind()
app = ModelStreaming.bind()
