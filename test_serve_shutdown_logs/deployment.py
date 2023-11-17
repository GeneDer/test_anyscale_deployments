import time
from ray import serve
from starlette.requests import Request


@serve.deployment
class HttpDeployment:
    async def __call__(self, request: Request) -> str:
        body = await request.body()
        print("request.body() in HttpDeployment", body)
        return f"Hello {body} {time.time()}"


h = HttpDeployment.options(name="http-deployment").bind()


@serve.deployment
class Lama():
    async def __init__(self):  # <-- this needs to be async def
        handle = serve.get_deployment_handle('DeploymentInfo', 'DeploymentInfoApp')
        grpc_port = await handle.get_port.remote()  # <-- this needs to be await
        print("grpc_port", grpc_port)

lama_app = Lama.bind()


@serve.deployment
class DeploymentInfo():
    def get_port(self):
        # generate port number for the machine
        test_port = 6798
        return test_port


DeploymentInfo_app = DeploymentInfo.bind()
