from ray import serve

from io import BytesIO
from starlette.requests import Request
from typing import Dict
import time
from utils.test import hello

@serve.deployment
class HelloModel:
    def __init__(self):
        
        hello()

    async def __call__(self, starlette_request: Request) -> None:
        hello()
        return 

model = HelloModel.bind()
