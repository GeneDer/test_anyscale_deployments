import grpc

# Users need to define their custom message and response protobuf
from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedMessage2
from user_defined_protos_pb2_grpc import UserDefinedServiceStub

channel = grpc.insecure_channel("localhost:9002")

stub = UserDefinedServiceStub(channel)

test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app3_grpc-deployment"),
    # ("request_id", "123"),  # Optional, feature parity w/ http proxy
    # ("multiplexed_model_id", "456"),  # Optional, feature parity w/ http proxy
)

# Predict method is defined by Serve's gRPC service use to return unary response
response, call = stub.__call__.with_call(request=test_in, metadata=metadata)

print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)

# Predict method is defined by Serve's gRPC service use to return unary response
response, call = stub.Method1.with_call(request=test_in, metadata=metadata)

print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)

test_in = UserDefinedMessage2()
metadata = (
    ("application", "app3_grpc-deployment"),
    # ("request_id", "123"),  # Optional, feature parity w/ http proxy
    # ("multiplexed_model_id", "456"),  # Optional, feature parity w/ http proxy
)

# Predict method is defined by Serve's gRPC service use to return unary response
response, call = stub.Method2.with_call(request=test_in, metadata=metadata)

print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse2
print("Full output:", response)
print("Output greeting field:", response.greeting)
