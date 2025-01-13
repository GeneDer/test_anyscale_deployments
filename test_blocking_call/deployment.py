from ray import serve
import time
import asyncio

@serve.deployment
class MyApp:
    async def __call__(self):
        time.sleep(5)
        # await asyncio.sleep(5)
        return "Hello World!"


app = MyApp.bind()
