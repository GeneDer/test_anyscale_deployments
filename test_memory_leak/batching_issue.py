# serve run batching_issue:inference
# curl localhost:8000 --data '{"prompts":["1","2","3"]}'

from ray import serve
import logging
from starlette.requests import Request


@serve.deployment
class Model:
    def __init__(self):
        self.logger = logging.getLogger("ray.serve")

    @serve.batch(max_batch_size=256, batch_wait_timeout_s=5)
    async def batch_predict(self, inputs: list[str]):
        self.logger.info(f"length called: {len(inputs)}")
        return [f"batch_predict({input})" for input in inputs]


@serve.deployment
class Inference:
    def __init__(self, _model):
        self.model = _model

    async def __call__(self, request: Request) -> list[any]:
        request_json = await request.json()
        prompts = request_json.get("prompts")
        responses = [self.model.batch_predict.remote(prompt) for prompt in prompts]
        return await asyncio.gather(*responses)


model = Model.bind()
inference = Inference.bind(model)

# prompts = [str(i) for i in range(1000)]
# handle: DeploymentHandle = serve.run(Model.bind())
# responses = [handle.remote(prompt) for prompt in prompts]
# list(r.result() for r in responses)


import numpy as np
from typing import List
import asyncio


@serve.deployment
class Model1:
    @serve.batch(max_batch_size=256, batch_wait_timeout_s=10)
    async def multiple(self, multiple_samples: List[int]) -> List[int]:
        print(f"length called: {len(multiple_samples)}", multiple_samples)
        # Use numpy's vectorized computation to efficiently process a batch.
        return np.array(multiple_samples) * 2


@serve.deployment
class Model2:
    def __init__(self, _model):
        self.model = _model

    async def __call__(self, request: Request) -> List[int]:
        request_json = await request.json()
        prompts = request_json.get("prompts")
        print("prompts", prompts)
        responses = [self.model.multiple.remote(int(prompt)) for prompt in prompts]
        print("responses", responses)
        return await asyncio.gather(*responses)
        # for prompt in request_json.get("prompts"):
        #     result.append(await self.multiple(int(prompt)))
        # return result


model1 = Model1.bind()
model2 = Model2.bind(model1)
