import aiohttp
import asyncio


async def send_query(num):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/http_entrypoint_service") as response:
            response = await response.text()
            print(f"in fetch_http: \nnum: {num} \n response: {response}")


async def run(num_times):
    tasks = [send_query(num) for num in range(num_times)]
    await asyncio.gather(*tasks)

num_requests = 5
asyncio.run(run(num_requests))
