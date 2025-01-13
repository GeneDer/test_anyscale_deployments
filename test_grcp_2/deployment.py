from ray import serve
from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedResponse


@serve.deployment
class GrpcDeployment:
    def __call__(self, user_message) -> UserDefinedResponse:
        greeting = f"From version 2! Hello {user_message.name}!"
        user_response = UserDefinedResponse(greeting=greeting)
        return user_response


grpc_app = GrpcDeployment.options(name="grpc-deployment").bind()
