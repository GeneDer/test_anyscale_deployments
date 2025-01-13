import asyncio
import logging
from fastapi import FastAPI
from ray import serve
from ray.serve.handle import DeploymentHandle


webapp = FastAPI()
logger = logging.getLogger(__name__)


@serve.deployment(
    autoscaling_config={
        # "max_ongoing_requests": 5,
        "min_replicas": 3,
        "max_replicas": 3,
    },
)
@serve.ingress(webapp)
class Ingress:
    def __init__(self, pipeline: DeploymentHandle):
        self.pipeline = pipeline

    @webapp.get("/")
    async def health_check(self) -> str:
        logger.info("Ray health check initiated.")
        return "Healthy!"

    @webapp.post("/conversations")
    async def start_conversation(self):
        logger.info("in start_conversation before sleep")
        await asyncio.gather(
            self.pipeline.start.remote(),
        )
        logger.info("in start_conversation after sleep")


@serve.deployment
class Pipeline:
    async def start(self):
        await asyncio.sleep(310)


app = Ingress.bind(Pipeline.bind())
