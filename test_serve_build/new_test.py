import logging
from uuid import uuid4
from fastapi import FastAPI, Response
from ray.serve.schema import LoggingConfig
from ray import serve

LOGGER = logging.getLogger("ray.serve")

app = FastAPI()


@serve.deployment(num_replicas=1, logging_config=LoggingConfig(enable_access_log=False, encoding="JSON"))
class TestDeployment:
    def __init__(self) -> None:
        self.logger = logging.getLogger("ray.serve")
        pass

    async def handle_test(self, request_id: str = "no", logger_model_name: str = "no"):
        LOGGER.info("Test 'JSON' logs with extra", extra={"request_id": request_id, "model_name": logger_model_name})
        logging.info("no logger used just logging.info")
        print("just printing stuff")
        self.logger.info("self.logger")
        return Response(status_code=200)


@serve.deployment(num_replicas=1, logging_config=LoggingConfig(enable_access_log=False, encoding="JSON"))
@serve.ingress(app)
class APIIngress:

    def __init__(self, handle) -> None:
        self.handle = handle

    @app.get("/test")
    async def test(self):
        LOGGER.info("here in handler")
        return await self.handle.handle_test.remote(request_id=str(uuid4()), logger_model_name="model-name-in-req")


serve.run(
    APIIngress.bind(TestDeployment.bind()),
    blocking=True,
    logging_config=LoggingConfig(enable_access_log=False, encoding="JSON"),
)
