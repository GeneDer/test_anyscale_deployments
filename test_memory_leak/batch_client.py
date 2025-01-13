import aiohttp
import grpc
import json
import ray
import asyncio

from user_defined_protos_pb2 import UserDefinedMessage
from user_defined_protos_pb2_grpc import UserDefinedServiceStub



async def fetch_http(session, data):
    async with session.get("http://localhost:8000/app_http", data=data) as response:
        response = await response.text()
        print(f"in fetch_http: data: {data},\n response: {response}")


async def send_query(request):
    metadata = (("application", "app_grpc"),)
    async with grpc.aio.insecure_channel("localhost:9000") as channel:
        stub = UserDefinedServiceStub(channel)
        response = await stub.__call__(request=request, metadata=metadata)
        print(f"greeting: {response.greeting}")  # "Hello foo from bar"
        print(f"num: {response.num}")  # 60


async def run(num_times):
    session = aiohttp.ClientSession()
    prompts = [str(i) for i in range(1000)]
    request = UserDefinedMessage(name="foo", num=30, origin="bar")
    tasks = [send_query(request) for num in range(num_times)]
    await asyncio.gather(*tasks)

num_requests = 1000
asyncio.run(run(num_requests))


import aiohttp


session = aiohttp.ClientSession()
data = {"prompts": [str(i) for i in range(1000)]}
async with session.get("http://localhost:8000", data=data) as response:
    response = await response.text()
    print(f"in fetch_http: data: {data},\n response: {response}")


import requests

data = {"prompts": [str(i) for i in range(1000)]}
resp = requests.post("http://localhost:8000", json=data)
resp.text
