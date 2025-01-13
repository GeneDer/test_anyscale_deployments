import asyncio
import string
import uuid
import random
from typing import Any, Dict, List, Tuple, Optional
import aiohttp
from aiohttp import ClientSession, TCPConnector

url = "http://localhost:8000/hello"

RANDOM_STRING_ALPHABET = string.ascii_lowercase + string.digits


def get_random_string(length=8):
    return "".join(random.choices(RANDOM_STRING_ALPHABET, k=length))


async def generate_data() -> List[Dict[str, Any]]:
    bodies=[]
    for x in range(20):
        bodies.append({"app_name":get_random_string()})
    return bodies


def create_request_id() -> str:
    return "jugal-" + str(uuid.uuid4())


async def send_request(session: ClientSession, body: Dict[str, Any], request_id: Optional[str]) -> Tuple[str, str]:
    # Uncomment the below to create a new request id for each request
    #request_id = create_request_id()

    headers = {
        "x-request-id": request_id,
    }

    async with session.post(url=url, headers=headers, json=body) as response:
        status = response.status
        result = await response.json()
        print(f"status = {status}")
        assert result['app_name'] == body["app_name"], f"expected {body['app_name']} got {result['app_name']}"
        return body["app_name"], result['app_name']


async def main():
    bodies = await generate_data()
    connector = TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        request_id = create_request_id()
        tasks = [send_request(session, body, request_id=request_id) for body in bodies]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)


asyncio.run(main())
