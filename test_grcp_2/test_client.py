import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage


# Replace URL and token with your own.
# url = "grpc-service-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
# token = "ABNM_uL1LdlNhqB-jy_h0Jmb5JmocVHPwfZOL7iyTe4"
# url = "grpc-service-test-10-8-2024-cfyuy.cld-kvedzwag2qa8i5bj.b3fs3s.s.anyscale-test.com"
# token = "e6UcRSBcG4pcjURy8tP9GJQaDQQ1Spk4wl68UX3uUlk"

# url = "grpc-service5-yxtjv.cld-6zjdsbn3kbphvk3l.b32gkq.s.anyscale-test.com"
# token = "6vz7RBqEhNt5fDHB3nFRl11cSbveBpL7ucQJ7jW1XrY"

# url = "grpc-service-yxtjv.cld-6zjdsbn3kbphvk3l.b32gkq.s.anyscale-test.com"
# token = "Pt_EiNVuWtdiQAhZ_vn4LKK-xCfR4B01aTsxV4ZpUTc"

# url = "grpc-service-gcp-bxauk.cld-6zjdsbn3kbphvk3l.s.anyscaleuserdata.com"
# token = "oRx1oyYaIsBfaWy-pO3fwuRh4z8UIJ9IIwTfcj_prOE"

url = "localhost:9000"

# credentials = grpc.ssl_channel_credentials()
#
# channel = grpc.secure_channel(url, credentials)
channel = grpc.insecure_channel("localhost:9000")

stub = UserDefinedServiceStub(channel)
request = UserDefinedMessage(name="Ray")
# auth_token_metadata = ("authorization", f"Bearer {token}")
metadata = (
    ("application", "grpc_app"),
    # auth_token_metadata,
    # ("x-anyscale-version", "canary"),
)
response, call = stub.__call__.with_call(request=request, metadata=metadata)
print(call.trailing_metadata())  # Request ID is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedMessage
print("Full output:", response)

from ray.serve.generated.serve_pb2_grpc import RayServeAPIServiceStub
from ray.serve.generated.serve_pb2 import HealthzRequest, ListApplicationsRequest


stub = RayServeAPIServiceStub(channel)
# auth_token_metadata = ("authorization", f"Bearer {token}")
metadata = (
    # auth_token_metadata,
)
request = ListApplicationsRequest()
response, _ = stub.ListApplications.with_call(request=request, metadata=metadata)
print(f"Applications: {response.application_names}")  # ["app1"]

request = HealthzRequest()
response, _ = stub.Healthz.with_call(request=request, metadata=metadata)
print(f"Health: {response.message}")  # "success"
