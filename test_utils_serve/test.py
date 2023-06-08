from ray import serve
from utils import foo


@serve.deployment() 
class A:
    def __call__(self, *args):
        val = foo()
        return val


def build_app(args):
    return A.bind()

# run serve deploy config.yaml
