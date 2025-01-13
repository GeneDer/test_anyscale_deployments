# serve run deployment:app
#
# while true; do curl localhost:8000; done
from ray import serve
import logging
import json


# logger = logging.getLogger("ray.serve")
logger = logging.getLogger(__name__)


@serve.deployment(name="test-deployment")
class Model:
    def __init__(self):
        self.count = 0

    async def __call__(self) -> int:
        # logger.info(f"Hello world: {self.count}"*int(1e3))
        x = {'foo': 'bar', "hello": "world", "count": self.count, "message": "Hello world"}
        logger.warning(json.dumps(x))
        self.count += 1
        return self.count


app = Model.bind()
