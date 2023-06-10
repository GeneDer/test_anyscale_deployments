from ray import serve


@serve.deployment()
class A:
    def __call__(self, *args):
        return "hello_world"


def build_app(args):
    my_app = A.bind()
    return my_app
