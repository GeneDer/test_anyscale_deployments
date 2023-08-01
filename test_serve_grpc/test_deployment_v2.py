import pickle
import struct
import time
from typing import Dict, Generator

from starlette.requests import Request

import ray
from ray import serve
from ray.serve.generated import serve_pb2
from ray.serve.handle import RayServeDeploymentHandle


@serve.deployment
class GrpcDeployment:
    def __call__(self, my_input: bytes) -> bytes:
        request = serve_pb2.TestIn()
        request.ParseFromString(my_input)
        greeting = f"Hello {request.name} from {request.foo}"
        num_x2 = request.num * 2
        output = serve_pb2.TestOut(
            greeting=greeting,
            num_x2=num_x2,
        )
        return output.SerializeToString()


g = GrpcDeployment.options(name="grpc-deployment").bind()
