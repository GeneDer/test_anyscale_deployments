# anyscale service deploy main:build_app --image-uri geneanyscale/gene-test-anyscale:serve-direct-ingress-v5 --name simple-multi-replica
from typing import Dict

from fastapi import FastAPI
from ray import serve
import os

fastapi_app = FastAPI()


@serve.deployment
@serve.ingress(fastapi_app)
class Test:
    @fastapi_app.get("/")
    def say_hi(self) -> str:
        replica_id = serve.get_replica_context().replica_id.unique_id
        return f"Hello world! {os.getpid()} {replica_id}"


def build_app(args: Dict) -> serve.Application:
    return Test.options(num_replicas=args.get("num_replicas", 8)).bind()
