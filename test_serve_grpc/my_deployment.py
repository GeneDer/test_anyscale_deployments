import ray
from ray import serve
from ray.serve.drivers import DefaultgRPCDriver
from ray.serve.handle import RayServeDeploymentHandle
from ray.serve.deployment_graph import InputNode
from typing import Dict
import struct


@serve.deployment
class FruitMarket:
    def __init__(
        self,
        orange_stand: RayServeDeploymentHandle,
        apple_stand: RayServeDeploymentHandle,
    ):
        self.directory = {
            "ORANGE": orange_stand,
            "APPLE": apple_stand,
        }

    async def check_price(self, inputs: Dict[str, bytes]) -> float:
        costs = 0
        for fruit, amount in inputs.items():
            if fruit not in self.directory:
                return
            fruit_stand = self.directory[fruit]
            ref: ray.ObjectRef = await fruit_stand.remote(int(amount))
            result = await ref
            costs += result
        return bytearray(struct.pack("f", costs))


@serve.deployment
class OrangeStand:
    def __init__(self):
        self.price = 2.0

    def __call__(self, num_oranges: int):
        return num_oranges * self.price


@serve.deployment
class AppleStand:
    def __init__(self):
        self.price = 3.0

    def __call__(self, num_oranges: int):
        return num_oranges * self.price


with InputNode() as input:
    orange_stand = OrangeStand.bind()
    apple_stand = AppleStand.bind()
    fruit_market = FruitMarket.bind(orange_stand, apple_stand)
    my_deployment = DefaultgRPCDriver.bind(fruit_market.check_price.bind(input))

serve.run(my_deployment)
