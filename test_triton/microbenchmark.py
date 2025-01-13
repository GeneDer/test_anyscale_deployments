# Runs several scenarios with varying max batch size, max concurrent queries,
# number of replicas, and with intermediate serve handles (to simulate ensemble
# models) either on or off.

# pip install -U ipywidgets
# mkdir images
"""
{'num_client:1:average_tps': 1.19,
 'num_client:1:latencies_df_avg': 835.9882778700194,
 'num_client:1:latencies_df_p50': 835.6177715013473,
 'num_client:1:latencies_df_p90': 841.4031098996929,
 'num_client:1:latencies_df_p99': 846.0978874203647,
 'num_client:2:average_tps': 1.22,
 'num_client:2:latencies_df_avg': 1636.7600462902556,
 'num_client:2:latencies_df_p50': 1636.0014559995761,
 'num_client:2:latencies_df_p90': 1641.775923601017,
 'num_client:2:latencies_df_p99': 1646.7504066884794,
 'num_client:3:average_tps': 1.23,
 'num_client:3:latencies_df_avg': 2222.741298680048,
 'num_client:3:latencies_df_p50': 2440.652664001391,
 'num_client:3:latencies_df_p90': 2493.7225220000983,
 'num_client:3:latencies_df_p99': 2510.68231457266,
 'num_client:4:average_tps': 1.54,
 'num_client:4:latencies_df_avg': 2828.163798889655,
 'num_client:4:latencies_df_p50': 3236.595654001576,
 'num_client:4:latencies_df_p90': 3283.062529700692,
 'num_client:4:latencies_df_p99': 3303.194299107199,
 'num_client:5:average_tps': 1.22,
 'num_client:5:latencies_df_avg': 4099.61410294989,
 'num_client:5:latencies_df_p50': 4098.838455502118,
 'num_client:5:latencies_df_p90': 4133.036406398969,
 'num_client:5:latencies_df_p99': 4151.088387300698,
 'num_client:6:average_tps': 1.6,
 'num_client:6:latencies_df_avg': 4067.804265129998,
 'num_client:6:latencies_df_p50': 4081.8604594987846,
 'num_client:6:latencies_df_p90': 4117.418732200531,
 'num_client:6:latencies_df_p99': 4130.44314632014,
 'num_client:7:average_tps': 1.72,
 'num_client:7:latencies_df_avg': 4043.654275360168,
 'num_client:7:latencies_df_p50': 4077.1006899994973,
 'num_client:7:latencies_df_p90': 4093.969417299013,
 'num_client:7:latencies_df_p99': 4099.8640448820515,
 'num_client:8:average_tps': 2.03,
 'num_client:8:latencies_df_avg': 3935.0797017700456,
 'num_client:8:latencies_df_p50': 4080.3068565001013,
 'num_client:8:latencies_df_p90': 4146.7350331997295,
 'num_client:8:latencies_df_p99': 4168.758071991033}
"""


import aiohttp
import asyncio
import nest_asyncio
import ray
# from PIL import Image
# from io import BytesIO
from pprint import pprint
from ray.serve._private.benchmarks.common import run_throughput_benchmark, run_latency_benchmark
from typing import Dict

NUM_CLIENTS = [1, 8, 16]
CALLS_PER_BATCH = 1
NUM_REQUESTS = 100
URL = "http://localhost:8000/generate?prompt=dogs%20in%20new%20york,%20realistic,%204k,%20photograph"


async def fetch(session):
    async with session.get(URL) as response:
        status = response.status
        request_id = response.headers.get("x-request-id")
        assert status == 200, f"status: {status}, request_id: {request_id}"
        # print("raw response", response)
        # print("response.status", status)
        # print("response.headers['x-request-id']", request_id)
        # await response.read()
        img_raw = await response.read()
        # im = Image.open(BytesIO(img_raw))
        # im.save(f"images/{request_id}.jpg", "JPEG")


@ray.remote
class Client:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def do_queries(self, num):
        for _ in range(num):
            await fetch(self.session)


async def trial(num_client: int) -> Dict[str, float]:
    results = {}

    clients = [Client.remote() for _ in range(num_client)]

    async def multi_client_queries():
        ray.get([a.do_queries.remote(CALLS_PER_BATCH) for a in clients])

    multi_client_avg_tps, _ = await run_throughput_benchmark(
        multi_client_queries,
        multiplier=CALLS_PER_BATCH * num_client,
    )

    results[f"num_client:{num_client}:average_tps"] = multi_client_avg_tps

    latencies_df = await run_latency_benchmark(multi_client_queries, NUM_REQUESTS)
    results[f"num_client:{num_client}:latencies_df_avg"] = latencies_df.mean()
    results[f"num_client:{num_client}:latencies_df_p50"] = latencies_df.quantile(0.5)
    results[f"num_client:{num_client}:latencies_df_p90"] = latencies_df.quantile(0.9)
    results[f"num_client:{num_client}:latencies_df_p99"] = latencies_df.quantile(0.99)
    return results


async def main():
    results = {}
    for num_client in NUM_CLIENTS:
        results.update(await trial(num_client=num_client))

    print("Results from all conditions:")
    pprint(results)
    return results


# ray.init()
nest_asyncio.apply()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
