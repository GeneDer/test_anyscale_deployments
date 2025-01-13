# pip install locust
# locust --headless --users 10 --spawn-rate 1 -H https://triton-stable-diffusion-a100-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com
# locust --headless --users 1 --run-time 15m --stop-timeout 10s -H http://localhost:8000 -f locustfile.py RayServeUser
# locust --headless --users 1 --run-time 1m --stop-timeout 10s -H http://localhost:8000 -f locustfile.py TritonUser

"""



"""
from locust import HttpUser, task
from PIL import Image
import numpy
import json

PROMPT = "dogs%20in%20new%20york,%20realistic,%204k,%20photograph"


class RayServeUser(HttpUser):
    @task
    def ray_serve_task(self):
        path = f"/generate?prompt={PROMPT}"
        self.client.get(path)


class TritonUser(HttpUser):
    @task
    def triton_task(self):
        path = "/v2/models/stable_diffusion_1_5/generate"
        payload = {"prompt": PROMPT}
        headers = {"content-type": "application/json"}
        response = self.client.post(path, data=json.dumps(payload), headers=headers)
        generated_image = (
            numpy.array(response.json()["generated_image"])
            .squeeze()
            .astype(numpy.uint8)
        )
        _ = Image.fromarray(generated_image)
