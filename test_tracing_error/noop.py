from ray import serve

@serve.deployment(
    max_ongoing_requests=100,
    num_replicas=16,
    ray_actor_options={"num_cpus": 1},
)
class A:
    def __call__(self):
        return b"hi"

app = A.bind()
# serve.run(app)
