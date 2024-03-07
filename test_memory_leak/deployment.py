# serve run deployment:app
# while true; do curl localhost:8000; done
from starlette.requests import Request
from ray import serve


@serve.deployment()
class Dep1:
    def get_length(self, params: str):
        return len(params)

    def multiple_by_two(self, length: int):
        return length*2


@serve.deployment()
class Gateway:
    def __init__(self, dep1):
        self.dep1: Dep1 = dep1

    async def __call__(self, http_request: Request) -> str:
        raw_data = await http_request.body()
        length = self.dep1.get_length.remote(raw_data)
        length_ref = await length._to_object_ref(False)
        return await self.dep1.multiple_by_two.remote(length_ref)


app = Gateway.bind(Dep1.bind())
