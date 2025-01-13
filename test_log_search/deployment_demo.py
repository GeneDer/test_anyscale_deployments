"""
RAY_SETUP_DEFAULT_LOGGER=1 RAY_SERVE_LOG_ENCODING=JSON serve run config.yaml

serve run config.yaml
curl localhost:8000
curl localhost:8000
curl localhost:8000
curl localhost:8000?err=1

serve deploy -f config.yaml --name obs-logs-$RANDOM
curl -H 'Authorization: Bearer UEhQbJPL7346ycAx-EBpedErPYc2k67aou5SojZL8dA' https://obs-logs-15184-jey3f.cld-e41shsjiiyhyuvcw.s.anyscaleuserdata-staging.com/

"""
from ray import serve
import time
import logging
import requests
import torch
from typing import List
from PIL import Image
from io import BytesIO
from torchvision import transforms
from ray.serve.handle import DeploymentHandle
from tqdm import tqdm
import sys
import ray

logger = logging.getLogger(__file__)

@ray.remote
def foo():
    logger.info('this is from the logger in a ray task!!!')
    request_context = ray.serve.context._serve_request_context.get()
    logger.info(request_context)


@serve.deployment()
class Counter:
    def __init__(self):
        with tqdm(total=100) as pbar:
            for _ in range(10):
                time.sleep(0.1)
                pbar.update(10)

        self.count = 12344

    def __call__(self, request):
        if request.query_params.get("err"):
            self.func4()

        self.count += 1

        logger.warning(f"This is from my logger!!! count: {self.count}")
        print(f"This is from print!!! count: {self.count}")
        sys.stdout.write(f"This is from stdout directly!!! count: {self.count}\n")
        sys.stderr.write(f"This is from stderr directly!!! count: {self.count}\n")
        print(f"This\nis\nmulti-line\nlog\n!!! count: {self.count}")

        obj_ref = foo.remote()
        ray.get(obj_ref)

        return self.count, time.time()

    def func1(self):
        print("in func1")
        raise RuntimeError("fail in in func1")

    def func2(self):
        print("in func2")
        return self.func1()

    def func3(self):
        print("in func3")
        return self.func2()

    def func4(self):
        print("in func4")
        return self.func3()

    def reconfigure(self, config):
        self.count = config["count"]


app = Counter.bind()


@serve.deployment
class ImageClassifier:
    def __init__(
            self,
            _image_downloader: DeploymentHandle,
            _data_preprocessor: DeploymentHandle,
    ):
        self._image_downloader = _image_downloader
        self._data_preprocessor = _data_preprocessor
        self.model = torch.hub.load(
            "pytorch/vision:v0.10.0", "resnet101", pretrained=True
        )
        self.model.eval()
        self.categories = self._image_labels()

    def _image_labels(self) -> List[str]:
        categories = []
        url = (
            "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        )
        labels = requests.get(url).text
        print("From ImageClassifier, labels:", labels)
        for label in labels.split("\n"):
            categories.append(label.strip())
        return categories

    async def __call__(self, *args, **kwargs):
        # Download image
        url = "https://github.com/pytorch/hub/raw/master/images/dog.jpg"
        image = await self._image_downloader.remote(url)
        print("From ImageClassifier, image:", image)

        # Preprocess image
        input_batch = await self._data_preprocessor.remote(image)
        print("From ImageClassifier, input_batch:", input_batch)
        # Predict image
        with torch.no_grad():
            output = self.model(input_batch)
        print("From ImageClassifier, output:", output)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        return self.process_model_outputs(probabilities)

    def process_model_outputs(self, probabilities: torch.Tensor):
        image_classes = []
        image_probabilities = []
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        for i in range(top5_prob.size(0)):
            image_classes.append(self.categories[top5_catid[i]])
            image_probabilities.append(top5_prob[i].item())

        return {
            "classes": image_classes,
            "probabilities": image_probabilities,
        }


@serve.deployment
class ImageDownloader:
    def __call__(self, image_url: str):
        image_bytes = requests.get(image_url).content
        print(f"From ImageDownloader, image_bytes: {image_bytes}")
        return Image.open(BytesIO(image_bytes)).convert("RGB")


@serve.deployment
class DataPreprocessor:
    def __init__(self):
        self.preprocess = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def __call__(self, image: Image):
        input_tensor = self.preprocess(image)
        print(f"From DataPreprocessor, input_tensor: {input_tensor}")
        return input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model


image_downloader = ImageDownloader.bind()
data_preprocessor = DataPreprocessor.bind()
app2 = ImageClassifier.options(name="image-classifier").bind(
    image_downloader, data_preprocessor
)
