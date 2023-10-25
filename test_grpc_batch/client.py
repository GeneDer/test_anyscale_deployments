# import aiohttp
# import grpc
# import json
# import ray
#
# from user_defined_protos_pb2 import UserDefinedMessage
# from user_defined_protos_pb2_grpc import UserDefinedServiceStub
#
#
# async def fetch_http(session, data):
#     async with session.get("http://localhost:8000/app_http", data=data) as response:
#         response = await response.text()
#         print(f"in fetch_http: data: {data},\n response: {response}")
#
#
# async def fetch_grpc(data):
#     metadata = (("application", "app_grpc"),)
#     async with grpc.aio.insecure_channel("localhost:9000") as channel:
#         stub = UserDefinedServiceStub(channel)
#         response = await stub.__call__(request=data, metadata=metadata)
#         print(f"fetch_grpc: data: {data},\n response: {response}")
#
#
# @ray.remote
# class Client:
#     def __init__(self):
#         self.session = aiohttp.ClientSession()
#
#     def ready(self):
#         return "ok"
#
#     async def do_http_queries(self, num):
#         data = {"name": f"user{num}"}
#         await fetch_http(self.session, json.dumps(data))
#
#     async def do_grpc_queries(self, num):
#         data = UserDefinedMessage(
#             name=f"user{num}",
#             num=num,
#             origin="bar",
#         )
#         await fetch_grpc(data)
#
#
# clients = [Client.remote() for _ in range(10)]
# ray.get([client.ready.remote() for client in clients])
# ray.get([client.do_http_queries.remote(num) for num, client in enumerate(clients)])
# ray.get([client.do_grpc_queries.remote(num) for num, client in enumerate(clients)])

import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage
import asyncio


async def send_query(request):
    metadata = (("application", "app_grpc"),)
    async with grpc.aio.insecure_channel("localhost:9000") as channel:
        stub = UserDefinedServiceStub(channel)
        response = await stub.__call__(request=request, metadata=metadata)
        print(f"greeting: {response.greeting}")  # "Hello foo from bar"
        print(f"num: {response.num}")  # 60


async def run(num_times):
    request = UserDefinedMessage(name="foo", num=30, origin="bar")
    tasks = [send_query(request) for num in range(num_times)]
    await asyncio.gather(*tasks)

num_requests = 100
asyncio.run(run(num_requests))
