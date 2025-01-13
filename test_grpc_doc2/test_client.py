import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage


# Replace URL and token with your own.
url = "grpc-service-gcp-test-gcp-bxauk.cld-6zjdsbn3kbphvk3l.s.anyscaleuserdata.com"
token = "wbM7cBz2xHg79MjcRWvArsYyTm8EohoPQ_1AU9CKzK0"
url = "grpc-service-gcp-test-aws-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
token = "HcjjdyFMRlKCqHSHcs7pp4J1xb7T9wuRk9Y2FmwWDYk"

credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(url, credentials)
stub = UserDefinedServiceStub(channel)
request = UserDefinedMessage(name="Ray")
auth_token_metadata = ("authorization", f"Bearer {token}")
metadata = (
    ("application", "grpc_app"),
    auth_token_metadata,
)
response, call = stub.__call__.with_call(request=request, metadata=metadata)
print(call.trailing_metadata())  # Request ID is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of UserDefinedMessage
print("Full output:", response)
