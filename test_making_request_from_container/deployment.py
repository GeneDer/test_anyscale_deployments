import cv2
import numpy as np
import base64
from fastapi import FastAPI
from pydantic import BaseModel
from ray import serve
import ray

from globals import AppConfig
from Utils.utils import OpenVINOModel, output_dict

ray.init(address="auto", namespace="example")
serve.start(detached=True, http_options={"host": "0.0.0.0"})

app = FastAPI()


class InputImg(BaseModel):
    nid_img: str


@serve.deployment()
@serve.ingress(app)
class OrganicOrienter:
    def __init__(self, config):
        self.vino_client = OpenVINOModel(config)
        self.img_size = config["input_image_size"]
        self.confidence_threshold = config["Confidence_Threshold"]

    def decode_img(self, img):
        img = base64.b64decode(img)
        img = np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    @app.post("/verify")
    async def orient_img(self, data: InputImg):
        img = self.decode_img(data.nid_img)
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = img.transpose(2, 0, 1)
        img = img.reshape(1, 3, self.img_size, self.img_size) / 255.0
        outputs = self.vino_client.run(img)
        scores = next(iter(outputs.values()))[0]

        orientation = np.argmax(scores)

        orientation = {"orientation": float(orientation)}

        return orientation


config = AppConfig("Config/config.json")

orienter_app = OrganicOrienter.bind(config.config["Orienter"])

serve.run(orienter_app)
