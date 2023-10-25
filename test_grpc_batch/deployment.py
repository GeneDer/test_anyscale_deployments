from ray import serve
from typing import Generator, List
from starlette.requests import Request

# Users need to include their custom message type which will be embedded in the request.
from user_defined_protos_pb2 import (
    Request as RequestProto,
    Responses as ResponsesProto,
    UserDefinedMessage,
    UserDefinedResponse,
)


@serve.deployment
class GrpcDeployment:
    async def __call__(self, user_message):
        return await self.handle_batch(user_message)

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=1)
    async def handle_batch(self, user_messages: List[UserDefinedMessage]) -> List[UserDefinedResponse]:
        result = []
        print('batch size: ', len(user_messages))
        for i, user_message in enumerate(user_messages):
            greeting = f"Index {i} Hello {user_message.name} from {user_message.origin}"
            num = user_message.num * 2
            user_response = UserDefinedResponse(
                greeting=greeting,
                num=num,
            )
            result.append(user_response)
        return result


app_grpc = GrpcDeployment.bind()


@serve.deployment
class BatchedDeploymentGrpc:
    @serve.batch(max_batch_size=10, batch_wait_timeout_s=1)
    async def batch_handler(self, requests: List[RequestProto]) -> List[ResponsesProto]:
        response_batch = []
        for r in requests:
            name = r.name
            response_batch.append(
                ResponsesProto(greeting=f"Hello {name}!")
            )

        return ResponsesProto(greeting=response_batch)

    def update_batch_params(self, max_batch_size, batch_wait_timeout_s):
        self.batch_handler.set_max_batch_size(max_batch_size)
        self.batch_handler.set_batch_wait_timeout_s(batch_wait_timeout_s)

    async def __call__2(self, request: RequestProto) -> ResponsesProto:
        return await self.batch_handler(request)


app_grpc2 = BatchedDeploymentGrpc.bind()


@serve.deployment
class BatchedDeploymentHttp:
    @serve.batch(max_batch_size=10, batch_wait_timeout_s=1)
    async def batch_handler(self, requests: List[Request]) -> List[str]:
        response_batch = []
        print('batch size: ', len(requests))
        for r in requests:
            name = (await r.json())["name"]
            response_batch.append(f"Hello {name}!")

        return response_batch

    def update_batch_params(self, max_batch_size, batch_wait_timeout_s):
        self.batch_handler.set_max_batch_size(max_batch_size)
        self.batch_handler.set_batch_wait_timeout_s(batch_wait_timeout_s)

    async def __call__(self, request: Request):
        return await self.batch_handler(request)


app_http = BatchedDeploymentHttp.bind()
