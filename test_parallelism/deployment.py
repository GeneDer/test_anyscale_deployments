import asyncio
from ray import serve


@serve.deployment(num_replicas=2)
class Preprocessor:
    def __init__(self):
        pass

    async def __call__(self, audio):
        await asyncio.sleep(1)
        return f"from preprocessor: {audio}"


@serve.deployment(
    autoscaling_config={"min_replicas": 2, "max_replicas": 3},
)
class Translator:
    def __init__(self, process):
        self.process = process.options(use_new_handle_api=True)

    async def translate(self, request) -> str:
        samples = await self.process.remote(request["audio"])
        return [{"text": samples}]

    async def __call__(self, request):
        request = await request.json()
        return await self.translate(request)


app = Translator.options(route_prefix="/translate").bind(Preprocessor.bind())
