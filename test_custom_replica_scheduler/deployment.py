import time
from collections import defaultdict
from ray import serve
from ray.serve.context import _get_global_client, _get_internal_replica_context
from ray.serve.replica_scheduler import ReplicaID, ReplicaSchedulingInfo
from typing import Dict

from test_custom_replica_scheduler.my_custom_schedulers import AllReplicaScheduler


@serve.deployment(
    replica_scheduler=AllReplicaScheduler,
    # replica_scheduler="test_custom_replica_scheduler.my_custom_schedulers:AllReplicaScheduler",
    num_replicas=10,
)
class App1:
    def __init__(self):
        context = _get_internal_replica_context()
        self.replica_id: ReplicaID = context.replica_id

    async def __call__(self):
        return self.replica_id


def _time_ms() -> int:
    return int(time.time() * 1000)


@serve.deployment(
    replica_scheduler="test_custom_replica_scheduler.my_custom_schedulers:ThroughputAwareReplicaScheduler",
    num_replicas=3,
)
class App2:
    def __init__(self):
        self.throughput_buckets: Dict[int, int] = defaultdict(int)
        self.last_throughput_buckets = _time_ms()
        context = _get_internal_replica_context()
        self.replica_id: ReplicaID = context.replica_id

    def __call__(self, reset: bool = False):
        self.publish_throughput()
        return self.replica_id


    def approximate_throughput(self, current_timestamp_ms: int) -> int:
        throughput = 0
        for t in range(current_timestamp_ms - 1000, current_timestamp_ms):
            throughput += self.throughput_buckets[t]
        return throughput

    def publish_throughput(self):
        current_timestamp_ms = _time_ms()

        # Skip if the last throughput bucket is not expired
        if current_timestamp_ms < self.last_throughput_buckets - 1000:
            return

        # Record the request to the bucket
        self.throughput_buckets[current_timestamp_ms] += 1
        self.last_throughput_buckets = current_timestamp_ms

        # Calculate the throughput
        throughput = self.approximate_throughput(current_timestamp_ms)

        # Publish the throughput to the replica scheduler
        _get_global_client().record_replica_scheduling_info(
            ReplicaSchedulingInfo(
                replica_id=self.replica_id,
                scheduling_stats={
                    "throughput": throughput,
                },
            )
        )


app1 = App1.bind()
app2 = App2.bind()
