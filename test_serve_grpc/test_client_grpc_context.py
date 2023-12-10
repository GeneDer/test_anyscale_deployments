import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub, FruitServiceStub, ImageClassificationServiceStub
from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedMessage2, FruitAmounts, ImageData
from ray.serve.generated.serve_pb2_grpc import RayServeAPIServiceStub
from ray.serve.generated.serve_pb2 import HealthzRequest, ListApplicationsRequest


url = "localhost:9002"
channel = grpc.insecure_channel(url)

stub = RayServeAPIServiceStub(channel)


print("\n\n____________test calling ListApplications ____________")
routes_request = ListApplicationsRequest()
response, call = stub.ListApplications.with_call(routes_request)
print("response code", call.code())
print("Output type:", type(response))  # Response is a type of ListApplicationsResponse
print("Full output:", response)


print("\n\n____________test calling Healthz ____________")
healthz_request = HealthzRequest()
response, call = stub.Healthz.with_call(healthz_request)
print("response code", call.code())
print("Output type:", type(response))  # Response is a type of HealthzResponse
print("Full output:", response)


print("\n\n____________test calling __call__ ____________")
stub = UserDefinedServiceStub(channel)
test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app"),
    ("request_id", "123"),
    ("multiplexed_model_id", "456"),
)
try:
    response, call = stub.__call__.with_call(request=test_in, metadata=metadata)
    print(call.trailing_metadata())  # Request id is returned in the trailing metadata
    # print(call.initial_metadata())  # Request id is returned in the trailing metadata
    # print(call.details())
    print("Output type:", type(response))  # Response is a type of UserDefinedResponse
    print("Full output:", response)
    print("Output greeting field:", response.greeting)
    print("Output num_x2 field:", response.num_x2)
except grpc.RpcError as rpc_error:
    print(f"status code: {rpc_error.code()}")  # StatusCode.NOT_FOUND
    print(f"details: {rpc_error.details()}")  # Application metadata not set...
    print(f"trailing_metadata: {rpc_error.trailing_metadata()}")  # Application metadata not set...


print("\n\n____________test calling Streaming ____________")
test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app"),
)
responses = stub.Streaming(test_in, metadata=metadata)
for response in responses:
    print("Output type:", type(response))  # Response is a type of UserDefinedResponse
    print("Full output:", response)
    print("Output greeting field:", response.greeting)
    print("Output num_x2 field:", response.num_x2)
print(responses.trailing_metadata())  # Request id is returned in the trailing metadata
