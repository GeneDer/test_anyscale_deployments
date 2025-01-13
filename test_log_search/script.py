# anyscale job submit -- python script.py

# script.py
import ray

@ray.remote
def hello_world():
    messages = []
    for i in range(10):
        message = f"hello world: {i}"
        print(message)
        messages.append(message)
    return messages

# Automatically connect to the running Ray cluster.
ray.init()
print(ray.get(hello_world.remote()))
