from ray import serve


@serve.deployment
class D:
    async def __call__(self) -> str:
        return "ok"

app = D.bind()
