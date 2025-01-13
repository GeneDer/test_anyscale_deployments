# ray job submit --runtime-env-json='{"pip": ["pandas==2.2.2"]}' -- python test_runtime_env.py

import pandas
import ray

@ray.remote
def hello_world():
    version = pandas.__version__
    return f"hello world: version {version}"

# Automatically connect to the running Ray cluster.
ray.init()
print(ray.get(hello_world.remote()))
