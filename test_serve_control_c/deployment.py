from ray import serve
import logging

logger = logging.getLogger(f"ray.serve.{__name__}")


@serve.deployment
class Deployment:
    def __init__(self):
        pass
        # raise ValueError("123123")

    def __call__(self):
        logger.info("Deployment created!!!!!111", extra={"ray_serve_extra_fields":{"foobar": 111.111222}})
        print(12312)
        # raise ValueError("123123")
        return "hello world11123111"


app = Deployment.bind()
