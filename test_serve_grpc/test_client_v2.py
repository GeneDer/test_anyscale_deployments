import time

import grpc

from ray.serve.generated import serve_pb2, serve_pb2_grpc
from ray.serve.generated.serve_pb2 import TestIn, TestOut


start_time = time.time()
channel = grpc.insecure_channel("localhost:9000")
stub = serve_pb2_grpc.RayServeServiceStub(channel)

test_in = TestIn(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = [
    ("application", "default_grpc-deployment"),
    ("request_id", "123"),
    ("multiplexed_model_id", "456"),
]

response = stub.Predict(request=test_in, metadata=metadata)
print("Time taken:", time.time() - start_time)
print("Output type:", type(response.user_response))
print("Full output:", response.user_response)
print("request_id:", response.request_id)

test_out = serve_pb2.TestOut()
test_out.ParseFromString(response.user_response)
print("Output greeting field:", test_out.greeting)
print("Output num_x2 field:", test_out.num_x2)
