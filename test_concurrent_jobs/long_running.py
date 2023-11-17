# ray job submit -- python long_running.py --no-wait

import ray
import time

@ray.remote
def hello_world(time_diff):
    return f"hello world: {time_diff}"

ray.init()
start_time = time.time()
diff = time.time() - start_time
while diff < 600:
    print(ray.get(hello_world.remote(diff)))
    time.sleep(1)
    diff = time.time() - start_time
