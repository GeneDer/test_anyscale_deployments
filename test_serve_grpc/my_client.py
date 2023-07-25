import grpc
from ray.serve.generated import serve_pb2, serve_pb2_grpc
import asyncio
import struct


async def send_request():
    async with grpc.aio.insecure_channel("localhost:9000") as channel:
        stub = serve_pb2_grpc.PredictAPIsServiceStub(channel)
        response = await stub.Predict(
            serve_pb2.PredictRequest(
                input={"ORANGE": bytes("10", "utf-8"), "APPLE": bytes("3", "utf-8")}
            )
        )
    return response


async def main():
    resp = await send_request()
    print(struct.unpack("f", resp.prediction))


# for python>=3.7, please use asyncio.run(main())
asyncio.get_event_loop().run_until_complete(main())

