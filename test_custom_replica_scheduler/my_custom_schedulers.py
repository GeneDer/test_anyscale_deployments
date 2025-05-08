from typing import (
    AsyncGenerator,
    List,
    Optional,
)
from ray.serve.replica_scheduler import (
    LocalityScheduleMixin,
    MultiplexScheduleMixin,
    ReplicaScheduler,
    RunningReplica,
    PendingRequest,
)


class AllReplicaScheduler(ReplicaScheduler):
    async def choose_replicas(
        self,
        pending_request: Optional[PendingRequest] = None,
    ) -> AsyncGenerator[List[RunningReplica], None]:
        print(f"AllReplicaScheduler: choose_replicas called {pending_request=}")
        yield self._replicas.values()


class ThroughputAwareReplicaScheduler(
    MultiplexScheduleMixin, LocalityScheduleMixin, ReplicaScheduler
):
    async def choose_replicas(
        self,
        pending_request: Optional[PendingRequest] = None,
    ) -> AsyncGenerator[List[RunningReplica], None]:

        if (
            pending_request is not None
            and pending_request.metadata.multiplexed_model_id
        ):
            candidate_replica_ids = self.apply_multiplex_scheduling(
                pending_request=pending_request,
            )
        else:
            candidate_replica_ids = self.apply_locality_scheduling(
                pending_request=pending_request,
            )

        print(f"in ThroughputAwareReplicaScheduler {[(r_id.unique_id, r.scheduling_stats.get('throughput')) for r_id, r in self._replicas.items()]}")
        yield sorted(
            [self._replicas[chosen_id] for chosen_id in candidate_replica_ids],
            key=lambda r: r.scheduling_stats.get("throughput", 0),
        )
