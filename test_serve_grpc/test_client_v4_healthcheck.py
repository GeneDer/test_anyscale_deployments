import grpc
from user_defined_protos_pb2_grpc import ServeAPIServiceStub
from google.protobuf.any_pb2 import Any as AnyProto


channel = grpc.insecure_channel("localhost:9000")

stub = ServeAPIServiceStub(channel)

routes_request = AnyProto()
response, call = stub.ServeRoutes.with_call(routes_request)

print("response code", call.code())
print("Output type:", type(response))  # Response is a type of RoutesResponse
print("Full output:", response)


# Predict method is defined by Serve's gRPC service use to return unary response
healthz_request = AnyProto()
response, call = stub.ServeHealthz.with_call(healthz_request)

print("response code", call.code())
print("Output type:", type(response))  # Response is a type of UserDefinedResponse
print("Full output:", response)
