import time

import ray

ray.init()

database = ["Learning", "Ray", "Flexible", "Distributed", "Python", "for", "Machine", "Learning"]

# Store the database in ray's memory object store
db_object_ref = ray.put(database)


# reserve 2.5GiB of available memory to place this actor
@ray.remote(num_cpus=2, memory=2500 * 1024 * 1024)
class DataTracker:
    def __init__(self):
        self._counts = 0

    def increment(self):
        self._counts += 1

    def counts(self):
        return self._counts


@ray.remote(num_cpus=2)
def retrieve_tracker_task(item, tracker, db):
    time.sleep(item * 10.0)
    tracker.increment.remote()
    return item, db[item]


# Create an Actor task
tracker = DataTracker.remote()

# Retrieve object reference for data stored in object store.
object_references = [retrieve_tracker_task.remote(item, tracker, db_object_ref) for item in range(len(database))]

# Pull data from object store
data = ray.get(object_references)

print(f"Total items in database: {ray.get(tracker.counts.remote())}")
