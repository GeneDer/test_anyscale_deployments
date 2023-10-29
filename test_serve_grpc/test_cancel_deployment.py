import time
import asyncio
from ray import serve
from typing import Generator, List
from starlette.requests import Request

# Users need to include their custom message type which will be embedded in the request.
from user_defined_protos_pb2 import (
    UserDefinedResponse,
    UserDefinedMessage,
    UserDefinedResponse2,
    UserDefinedMessage2,
)


WAIT_TIME = 5


@serve.deployment
class GrpcDeployment:
    async def __call__(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        start = time.time()
        while time.time() - start < WAIT_TIME:
            print("sleeping", time.time() - start)
            # time.sleep(1)
            await asyncio.sleep(1)
        greeting = f"Hello {user_message.name} from {user_message.foo}"
        num_x2 = user_message.num * 2
        user_response = UserDefinedResponse(
            greeting=greeting,
            num_x2=num_x2,
        )
        return user_response

    def Method1(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        greeting = f"Hello {user_message.foo} from method1"
        num_x2 = user_message.num * 3
        user_response = UserDefinedResponse(
            greeting=greeting,
            num_x2=num_x2,
        )
        return user_response

    def Method2(self, user_message: UserDefinedMessage2) -> UserDefinedResponse2:
        greeting = "This is from method2"
        user_response = UserDefinedResponse(greeting=greeting)
        return user_response

    def Streaming(
        self, user_message: UserDefinedMessage
    ) -> Generator[UserDefinedResponse, None, None]:
        for i in range(10):
            greeting = f"{i}: Hello {user_message.name} from {user_message.foo}"
            num_x2 = user_message.num * 2 + i
            user_response = UserDefinedResponse(
                greeting=greeting,
                num_x2=num_x2,
            )
            yield user_response

            time.sleep(0.1)

    @serve.multiplexed(max_num_models_per_replica=3)
    async def get_model(self, model_id: str) -> str:
        return f"loading model: {model_id}"

    async def Multiplex(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        model_id = serve.get_multiplexed_model_id()
        model = await self.get_model(model_id)
        user_response = UserDefinedResponse(
            greeting=f"{user_message.name} called model {model}",
        )
        return user_response


g = GrpcDeployment.options(name="grpc-deployment").bind()


@serve.deployment
class HttpDeployment:
    async def __call__(self, request: Request) -> str:
        start = time.time()
        while time.time() - start < WAIT_TIME:
            print("sleeping", time.time() - start)
            # time.sleep(1)
            await asyncio.sleep(1)
        body = await request.body()
        print("request.body() in HttpDeployment", body)
        return f"Hello {body} {time.time()}"


h = HttpDeployment.options(name="http-deployment").bind()
