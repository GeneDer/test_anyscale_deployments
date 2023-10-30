import grpc
from user_defined_protos_pb2_grpc import ImageClassificationServiceStub
from user_defined_protos_pb2 import ImageData


url = "grpc-service-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
token = "ABNM_uL1LdlNhqB-jy_h0Jmb5JmocVHPwfZOL7iyTe4"

credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(url, credentials)
stub = ImageClassificationServiceStub(channel)
test_in = ImageData(
    url="https://github.com/pytorch/hub/raw/master/images/dog.jpg",
)
auth_token_metadata = ("authorization", f"bearer {token}")
metadata = (
    ("application", "grpc_image_classifier"),
    auth_token_metadata,
)
response, call = stub.Predict.with_call(request=test_in, metadata=metadata)
print(call.trailing_metadata())  # Request id is returned in the trailing metadata
print("Output type:", type(response))  # Response is a type of ImageClass
print("Full output:", response)
print("Output classes field:", response.classes)
print("Output probabilities field:", response.probabilities)
