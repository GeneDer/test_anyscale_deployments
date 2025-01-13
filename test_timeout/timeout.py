import time
import logging
from ray import serve

logger = logging.getLogger("ray.serve")


@serve.deployment
def sleep():
    for i in range(20):
        time.sleep(1)
        logger.info(f"{i}")


app = sleep.bind()
