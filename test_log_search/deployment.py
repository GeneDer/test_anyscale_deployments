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
from transformers import pipeline
from starlette.requests import Request
from typing import Dict

logger = logging.getLogger("ray.serve")


@serve.deployment()
class Counter:
    def __init__(self):
        print("this\nis\nmutli-line\nlog\nin\n\init\n")
        sys.stdout.write("This is from stdout directly\n")
        sys.stderr.write("This is from stderr directly\n")
        sys.stderr.write("")
        total = 10000
        with tqdm(total=total) as pbar:
            for i in range(total):
                pbar.update(i)

        self.count = 10

    def __call__(self, *args):
        # self.func4()
        self.count += 1
        if self.count % 1000 == 0:
            return f"Hello@{self.count}", time.time()

        logger.warning(f"this is my logging!!! count: {self.count}")
        print("this\nis\nmutli-line\nlog\n")
        return self.count, time.time()

    def func1(self):
        raise RuntimeError("in func1")

    def func2(self):
        return self.func1()

    def func3(self):
        return self.func2()

    def func4(self):
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
        print("print labels", labels)
        for label in labels.split("\n"):
            categories.append(label.strip())
        return categories

    async def __call__(self, *args, **kwargs):
        # Download image
        url="https://github.com/pytorch/hub/raw/master/images/dog.jpg"
        image = await self._image_downloader.remote(url)
        print("print image", image)

        # Preprocess image
        input_batch = await self._data_preprocessor.remote(image)
        print("print input_batch", input_batch)
        # Predict image
        with torch.no_grad():
            output = self.model(input_batch)
        print("print output", output)
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
        return input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model


image_downloader = ImageDownloader.bind()
data_preprocessor = DataPreprocessor.bind()
app2 = ImageClassifier.options(name="image-classifier").bind(
    image_downloader, data_preprocessor
)


@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


app3 = SentimentAnalysisDeployment.bind()
