from ray import serve
import ray

@serve.deployment
class Upstream:
    def __call__(self):
        request_id = ray.serve.context._get_serve_request_context().request_id
        return request_id


@serve.deployment
class Downstream:
    def __init__(self, upstream_handle):
        self.upstream_handle = upstream_handle
    async def __call__(self):
        request_id = ray.serve.context._get_serve_request_context().request_id
        upstream_request_id = await self.upstream_handle.remote()
        return request_id + " " + upstream_request_id

app1 = Upstream.bind()
app2 = Downstream.bind(app1)

handle1 = serve.run(app1, route_prefix="/upstream")
handle2 = serve.run(app2, route_prefix="/downstream")
