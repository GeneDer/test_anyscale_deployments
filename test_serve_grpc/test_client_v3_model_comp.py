import grpc

# Users need to define their custom message and response protobuf
from user_defined_protos_pb2 import FruitAmounts
from user_defined_protos_pb2_grpc import FruitServiceStub

channel = grpc.insecure_channel("localhost:9002")

stub = FruitServiceStub(channel)

test_in = FruitAmounts(
    orange=4,
    apple=8,
)
metadata = (
    ("route_path", "/baz"),
    # ("method_name", "method1"),
    # ("application", "default_grpc-deployment"),
    # ("request_id", "123"),  # Optional, feature parity w/ http proxy
    # ("multiplexed_model_id", "456"),  # Optional, feature parity w/ http proxy
)

# Predict method is defined by Serve's gRPC service use to return unary response
response, call = stub.FruitStand.with_call(request=test_in, metadata=metadata)

print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of FruitCosts
print("Full output:", response)
print("Output costs field:", response.costs)
