# ray job submit -- python long_running.py --no-wait

import ray
import time

@ray.remote(num_cpus=1, scheduling_strategy="SPREAD")
def hello_world(time_diff):
    time.sleep(500)
    return f"hello world: {time_diff}"

ray.init()
start_time = time.time()
diff = time.time() - start_time
while diff < 50:
    print(ray.get(hello_world.remote(diff)))
    time.sleep(1)
    diff = time.time() - start_time
