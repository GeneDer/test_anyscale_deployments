from ray import serve
import os


@serve.deployment()
class Counter:
    def __init__(self):
        self.count = 10

    def __call__(self, *args):
        return self.count, os.getpid()

    def reconfigure(self, config):
        self.count = config["count"]


app = Counter.bind()
