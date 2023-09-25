import argparse
import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub, FruitServiceStub, ImageClassificationServiceStub
from user_defined_protos_pb2 import UserDefinedMessage, UserDefinedMessage2, FruitAmounts, ImageData
from ray.serve.generated.serve_pb2_grpc import RayServeAPIServiceStub
from ray.serve.generated.serve_pb2 import HealthzRequest, ListApplicationsRequest

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str)
parser.add_argument("--token", type=str)
args = parser.parse_args()

credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(args.url, credentials)
auth_token_metadata = ("authorization", f"bearer grpc-{args.token}")

stub = RayServeAPIServiceStub(channel)
metadata = (auth_token_metadata,)

print("\n\n____________test calling ListApplications ____________")
routes_request = ListApplicationsRequest()
response, call = stub.ListApplications.with_call(routes_request, metadata=metadata)
print("response code", call.code())
print("Output type:", type(response))  # Response is a type of ListApplicationsResponse
print("Full output:", response)


print("\n\n____________test calling Healthz ____________")
healthz_request = HealthzRequest()
response, call = stub.Healthz.with_call(healthz_request, metadata=metadata)
print("response code", call.code())
print("Output type:", type(response))  # Response is a type of HealthzResponse
print("Full output:", response)


stub = UserDefinedServiceStub(channel)


print("____________test calling __call__ ____________")
test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app3"),
    auth_token_metadata,
)
response, call = stub.__call__.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)


print("____________test calling Method1 ____________")
response, call = stub.Method1.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
print("Output greeting field:", response.greeting)
print("Output num_x2 field:", response.num_x2)


print("____________test calling Method2 ____________")
test_in = UserDefinedMessage2()
metadata = (
    ("application", "app3"),
    auth_token_metadata,
)
response, call = stub.Method2.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedResponse2
print("Full output:", response)
print("Output greeting field:", response.greeting)


print("____________test calling Streaming ____________")
test_in = UserDefinedMessage(
    name="genesu",
    num=88,
    foo="bar",
)
metadata = (
    ("application", "app3"),
    auth_token_metadata,
)
responses = stub.Streaming(test_in, metadata=metadata)
for response in responses:
    print("Output type:", type(response))  # Response is a type of UserDefinedResponse
    print("Full output:", response)
    print("Output greeting field:", response.greeting)
    print("Output num_x2 field:", response.num_x2)
print(responses.trailing_metadata())  # Request id is returned in the trailing metadata


print("____________test calling FruitStand ____________")
stub = FruitServiceStub(channel)
test_in = FruitAmounts(
    orange=4,
    apple=8,
)
metadata = (
    ("application", "app4"),
    auth_token_metadata,
)
response, call = stub.FruitStand.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of FruitCosts
print("Full output:", response)
print("Output costs field:", response.costs)

print("\n\n____________test calling ImageClassification ____________")
stub = ImageClassificationServiceStub(channel)
test_in = ImageData(
    url="https://github.com/pytorch/hub/raw/master/images/dog.jpg",
)
metadata = (
    ("application", "app6"),
    auth_token_metadata,
)
response, call = stub.Predict.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of ImageClass
print("Full output:", response)
print("Output classes field:", response.classes)
print("Output probabilities field:", response.probabilities)
