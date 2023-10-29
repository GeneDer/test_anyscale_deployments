import grpc
import asyncio
import signal
import sys

from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedMessage2
from user_defined_protos_pb2_grpc import UserDefinedServiceStub

# with grpc.insecure_channel("localhost:9000") as channel:
#     stub = UserDefinedServiceStub(channel)
#
#     test_in = UserDefinedMessage(
#         name="genesu",
#         num=88,
#         foo="bar",
#     )
#     metadata = (
#         ("application", "app"),
#     )
#     response, call = stub.__call__.with_call(request=test_in, metadata=metadata)
#     print(call.trailing_metadata())  # Request id is returned in the trailing metadata
#     print("Output type:", type(response))  # Response is a type of UserDefinedResponse
#     print("Full output:", response)
#     print("Output greeting field:", response.greeting)
#     print("Output num_x2 field:", response.num_x2)
#     call.done()


async def send_query(request):
    metadata = (("application", "app"),)
    async with grpc.aio.insecure_channel("localhost:9000") as channel:
        stub = UserDefinedServiceStub(channel)
        response = await stub.__call__(request=request, metadata=metadata)
        print(f"greeting: {response.greeting}")  # "Hello foo from bar"
        print(f"num: {response.num_x2}")  # 60


async def send_query2(request):
    metadata = (("application", "app"),)
    with grpc.insecure_channel("localhost:9000") as channel:
        stub = UserDefinedServiceStub(channel)
        future = stub.__call__.future(
            request=request,
            metadata=metadata,
            wait_for_ready=True,
        )

        def cancel_request(unused_signum, unused_frame):
            print("canceling request", future.cancelled())
            future.cancel()
            print("canceled request", future.cancelled())
            sys.exit(0)

        signal.signal(signal.SIGINT, cancel_request)
        result = future.result()
        print(result)

async def send_query3(request):
    metadata = (("application", "app"),)
    with grpc.insecure_channel("localhost:9000") as channel:
        stub = UserDefinedServiceStub(channel)
        result = stub.__call__(
            request=request,
            metadata=metadata,
        )
        print(result)


async def run(num_times):
    request = UserDefinedMessage(name="foo", num=30, foo="bar")
    tasks = [send_query(request) for num in range(num_times)]
    await asyncio.gather(*tasks)


num_requests = 1
asyncio.run(run(num_requests))
