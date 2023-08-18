import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub, FruitServiceStub
from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedMessage2, FruitAmounts
from ray.serve.generated.serve_pb2_grpc import RayServeAPIServiceStub
from ray.serve.generated.serve_pb2 import HealthzRequest, ListApplicationsRequest


url = "localhost:9000"
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
    ("application", "app3_grpc-deployment"),
)
response, call = stub.__call__.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)


print("\n\n____________test calling Method1 ____________")
response, call = stub.Method1.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)


print("\n\n____________test calling Method2 ____________")
test_in = UserDefinedMessage2()
metadata = (
    ("application", "app3_grpc-deployment"),
)
response, call = stub.Method2.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse2
print("Full output:", response)
print("Output greeting field:", response.greeting)


print("\n\n____________test calling Streaming ____________")
test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app3_grpc-deployment"),
)
responses = stub.Streaming(test_in, metadata=metadata)
for response in responses:
    print("Output type:", type(response))  # Response is a type of UserDefinedResponse
    print("Full output:", response)
    print("Output greeting field:", response.greeting)
    print("Output num_x2 field:", response.num_x2)
print(responses.trailing_metadata())  # Request id is returned in the trailing metadata


print("\n\n____________test calling FruitStand ____________")
stub = FruitServiceStub(channel)
test_in = FruitAmounts(
    orange=4,
    apple=8,
)
metadata = (
    ("application", "app4_grpc-deployment-model-composition"),
)
response, call = stub.FruitStand.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of FruitCosts
print("Full output:", response)
print("Output costs field:", response.costs)
