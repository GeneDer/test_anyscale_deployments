"""
pip uninstall tensorrt

pip install --no-cache-dir --extra-index-url https://pypi.nvidia.com tensorrt==9.2.0.post11.dev5

export S3_MODEL_REPOSITORY=s3://gene-dev2

serve run deployment:triton_deployment

curl --request GET "http://localhost:8000/generate?prompt=dogs%20in%20new%20york,%20realistic,%204k,%20photograph" > dogs_photo.jpg
curl "http://localhost:8000/generate?prompt=dogs%20in%20new%20york,%20realistic,%204k,%20photograph" > dogs_photo.jpg

curl -H "Authorization: Bearer 1mOlytmq5FyMqasp5djCGGYq2UI3zS-EC0yPXr6mjp0" https://gene-test-triton-13-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com/generate?prompt=dogs%20in%20new%20york,%20realistic,%204k,%20photograph
"""

import io
import numpy
import os
import tritonserver
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from ray import serve

# S3_MODEL_REPOSITORY = f'{os.environ["ANYSCALE_ARTIFACT_STORAGE"]}/{os.environ["ANYSCALE_EXPERIMENTAL_USERNAME"]}'
S3_MODEL_REPOSITORY = f'{os.environ["ANYSCALE_ARTIFACT_STORAGE"]}/triton_model_repository'
app = FastAPI()


@serve.deployment(ray_actor_options={"num_gpus": 1})
@serve.ingress(app)
class TritonDeployment:
    def __init__(self):
        self._triton_server = tritonserver

        self._triton_server = tritonserver.Server(
            model_repository=S3_MODEL_REPOSITORY,
            model_control_mode=tritonserver.ModelControlMode.EXPLICIT,
            log_info=False,
        )
        self._triton_server.start(wait_until_ready=True)

        # Load model using Triton.
        self._model = None
        if not self._triton_server.model("stable_diffusion_1_5").ready():  # this can be anything
            self._model = self._triton_server.load(
                "stable_diffusion_1_5"  # this needs to match the prefix in the model repository
            )

            if not self._model.ready():
                raise Exception("Model not ready")

    @app.get("/generate")
    def generate(self, prompt: str) -> StreamingResponse:
        print(f"Generating image for prompt: {prompt}")
        for response in self._model.infer(inputs={"prompt": [[prompt]]}):
            generated_image = (
                numpy.from_dlpack(response.outputs["generated_image"])
                .squeeze()
                .astype(numpy.uint8)
            )

            image_ = Image.fromarray(generated_image)

            # Stream back the image to the caller
            buffer = io.BytesIO()
            image_.save(buffer, 'JPEG')
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="image/jpeg")


triton_deployment = TritonDeployment.bind()
