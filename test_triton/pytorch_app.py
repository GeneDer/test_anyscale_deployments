# serve run pytorch_app:pytorch_Deployment
# curl "http://localhost:8000/generate?prompt=dogs%20in%20new%20york,%20realistic,%204k,%20photograph" > dogs_photo.jpg
# REF: https://huggingface.co/docs/diffusers/en/optimization/torch2.0#stable-diffusion-text-to-image
# serve run pytorch_app:pytorch_deployment
# serve run pytorch_app:pytorch_compiled_deployment

import torch
from diffusers import DiffusionPipeline
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO
from ray import serve

app = FastAPI()


@serve.deployment(
    ray_actor_options={
        "num_gpus": 1,
        "num_cpus": 1,
    },
    num_replicas="auto",
)
@serve.ingress(app)
class PytorchDeployment:
    def __init__(self, run_compile: bool = False):
        self.pipe = DiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            use_safetensors=True,
        ).to("cuda")
        self.pipe = self.pipe.to("cuda")
        self.pipe.unet.to(memory_format=torch.channels_last)

        if run_compile:
            self.pipe.unet = torch.compile(
                self.pipe.unet, mode="reduce-overhead", fullgraph=True,
            )
            # This will compile the model to reduce overhead and improve performance.
            _ = self.pipe("test").images[0]

    @app.get("/generate")
    async def generate(self, prompt: str) -> StreamingResponse:
        print(f"Generating image for prompt: {prompt}")
        image_ = self.pipe(
            prompt,
        ).images[0]

        # Stream back the image to the caller.
        buffer = BytesIO()
        image_.save(buffer, "JPEG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/jpeg")


pytorch_deployment = PytorchDeployment.bind(run_compile=False)
pytorch_compiled_deployment = PytorchDeployment.bind(run_compile=True)
