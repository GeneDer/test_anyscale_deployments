from typing import Any

from ray import serve
from starlette.requests import Request
from utils.deployment_utils import process_body


@serve.deployment(name="test-deployment")
class TestDeployment:
    async def __call__(self, http_request: Request) -> Any:
        body: bytes = await http_request.body()
        return process_body(body)


test_deployment = TestDeployment.bind()  # type: ignore
