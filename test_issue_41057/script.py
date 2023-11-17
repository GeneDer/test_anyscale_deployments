# python -m unittest script.py -k test_ray_serve_batch_timeouts_repercussions
# python -m unittest script.py -k test_no_repercussions_with_no_batching

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Tuple
from unittest import TestCase

import ray
import ray.serve as serve
import requests
from starlette.requests import Request


@serve.deployment()
class RayDeploymentWithBatching:
    @serve.batch(max_batch_size=20)
    async def batch(self, batch: List[List[str]]):
        print("in RayDeploymentWithBatching#batch!!!!!!")
        await asyncio.sleep(0.05)
        print(f"Batch size: {len(batch)}, {batch}")
        return [[f"T({text})" for text in request] for request in batch]

    async def __call__(self, request: Request):
        print("in __call__!!!!!!!")
        request_json = await request.json()
        print(f"Request: {request_json}")
        resp = await self.batch(request_json["items"])
        print(f"resp: {resp}")
        return {"response": resp}


@serve.deployment()
class RayDeploymentWithoutBatching:
    @staticmethod
    async def infer_with_no_ray_batching(batch: List[List[str]]):
        await asyncio.sleep(0.05)
        return [[f"T({text})" for text in request] for request in batch]

    async def __call__(self, request):
        request_json = await request.json()
        resp = await self.infer_with_no_ray_batching(request_json["items"])
        return {"response": resp}


class RayClient:
    def __init__(self, url: str, client_timeout: Optional[int] = None):
        self.url = url
        self.client_timeout = client_timeout

    def post_request(self) -> Optional[List[dict]]:
        text_chunk = [str(i) for i in range(5)]
        try:
            resp = requests.post(self.url, json={"items": text_chunk}, timeout=self.client_timeout)
        except Exception as e:
            print(f"Exception: {e}")
            return None
        return resp.json()["response"]


def get_success_rate(results: List[Optional[List[dict]]]) -> float:
    print(results)
    return len([s for s in results if s is not None]) / len(results)


class TestRayServeBatchTimeoutsRepercussions(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ray.init(include_dashboard=False)
        serve.start(detached=True, http_options={"host": "0.0.0.0"})
        serve.run(RayDeploymentWithBatching.bind(), name="batching", route_prefix="/batching")
        serve.run(RayDeploymentWithoutBatching.bind(), name="no-batching", route_prefix="/no-batching")

    @classmethod
    def tearDownClass(cls) -> None:
        ray.shutdown()

    def test_ray_serve_batch_timeouts_repercussions(self):
        ray_client = RayClient(url="http://0.0.0.0:8000/batching")
        s1, s2, s3 = run_queries_experiment_return_success_rate(ray_client)
        self.assertEqual(s1, 1.0)
        self.assertLess(s2, 0.2)
        self.assertLess(s3, 0.2)  # repercussions on success of step 3

    def test_no_repercussions_with_no_batching(self):
        ray_client = RayClient(url="http://0.0.0.0:8000/no-batching")
        s1, s2, s3 = run_queries_experiment_return_success_rate(ray_client)
        self.assertEqual(s1, 1.0)
        self.assertLess(s2, 0.2)
        self.assertEqual(s3, 1.0)  # no repercussions on success of step 3


def run_queries_experiment_return_success_rate(
        ray_client: RayClient, n_requests: int = 60
) -> Tuple[float, float, float]:

    ray_client.client_timeout = 1.0
    s1 = run_queries_return_success_rate(ray_client, n_requests=n_requests)
    print("Done with step 1. Waiting 5 seconds.")
    time.sleep(5)

    print("Starting step 2.")
    ray_client.client_timeout = 0.05
    # ray_client.client_timeout = 1
    s2 = run_queries_return_success_rate(ray_client, n_requests=n_requests)
    print("Done with step 2. Waiting for 5 seconds.")
    time.sleep(5)

    print("Starting step 3.")
    ray_client.client_timeout = 1.0
    s3 = run_queries_return_success_rate(ray_client, n_requests=n_requests)
    print("Done with step 3. Shutting down ray server.")

    print(f"Success rate for 1: {s1}")
    print(f"Success rate for 2: {s2}")
    print(f"Success rate for 3: {s3}")
    return s1, s2, s3


def run_queries_return_success_rate(ray_client: RayClient, n_requests: int) -> float:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(ray_client.post_request) for _ in range(n_requests)]
        results = [future.result() for future in futures]

    return get_success_rate(results)
