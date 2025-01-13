# RAY_SERVE_LOG_ENCODING=JSON serve run deployment:app
import logging
from ray import serve

logger = logging.getLogger("ray.serve")


@serve.deployment
class App:
    def __call__(self):
        try:
            raise Exception("fake_exception")
        except Exception as e:
            logger.info("log message", exc_info=e)
        return "foo"


app = App.bind()
