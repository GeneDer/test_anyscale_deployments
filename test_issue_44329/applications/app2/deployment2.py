from typing import Any

from ray import serve
from starlette.requests import Request
from utils.deployment_utils import process_body


@serve.deployment(name="test-deployment-2")
class TestDeploymentV2:
    async def __call__(self, http_request: Request) -> Any:
        body: bytes = await http_request.body()
        return process_body(body) + " v2"


test_deployment_v2 = TestDeploymentV2.bind()  # type: ignore
