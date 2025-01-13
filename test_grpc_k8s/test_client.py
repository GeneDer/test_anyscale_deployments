import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage


# Replace URL and token with your own.
# gke
url = "grpc-service2-fntsn.cld-7evuj33xt338jd5d.s.anyscale-test.com"
token = "vXbKMlOKbO3nCzxRGQHxre0F5xj4Oi3PJva_ywOAPh0"

# eks
url = "grpc-service-eks-8f6fb.cld-qleup8acrih5jfh1.s.anyscale-test.com"
token = "ZljfOQf-FYVpaphFOAGyh3MCqwL9P5RLswUjaoaD_BI"

credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(url, credentials)
stub = UserDefinedServiceStub(channel)
request = UserDefinedMessage(name="Ray")
auth_token_metadata = ("authorization", f"Bearer {token}")
metadata = (
    ("application", "grpc_app"),
    auth_token_metadata,
    # ("x-anyscale-version", "canary"),
    ("x-anyscale-version", "primary"),
)
response, call = stub.__call__.with_call(request=request, metadata=metadata)
print(call.trailing_metadata())  # Request ID is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedMessage
print("Full output:", response)




from ray.serve.generated.serve_pb2_grpc import RayServeAPIServiceStub
from ray.serve.generated.serve_pb2 import HealthzRequest, ListApplicationsRequest


stub = RayServeAPIServiceStub(channel)
auth_token_metadata = ("authorization", f"Bearer {token}")
metadata = (
    auth_token_metadata,
)
request = ListApplicationsRequest()
response, _ = stub.ListApplications.with_call(request=request, metadata=metadata)
print(f"Applications: {response.application_names}")  # ["app1"]

request = HealthzRequest()
response, _ = stub.Healthz.with_call(request=request, metadata=metadata)
print(f"Health: {response.message}")  # "success"
