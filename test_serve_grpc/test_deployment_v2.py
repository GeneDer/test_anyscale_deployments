import ray
import requests
import time
import torch
from PIL import Image
from fastapi import FastAPI
from io import BytesIO
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from starlette.requests import Request
from torchvision import transforms
from typing import Dict, Generator, List

# Users need to include their custom message type which will be embedded in the request.
from user_defined_protos_pb2 import (
    FruitAmounts,
    FruitCosts,
    ImageClass,
    ImageData,
    UserDefinedMessage,
    UserDefinedMessage2,
    UserDefinedResponse,
    UserDefinedResponse2,
)


@serve.deployment
class GrpcDeployment:
    def __call__(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        greeting = f"Hello {user_message.name} from {user_message.foo}"
        num_x2 = user_message.num * 2
        user_response = UserDefinedResponse(
            greeting=greeting,
            num_x2=num_x2,
        )
        return user_response

    def Method1(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        greeting = f"Hello {user_message.foo} from method1"
        num_x2 = user_message.num * 3
        user_response = UserDefinedResponse(
            greeting=greeting,
            num_x2=num_x2,
        )
        return user_response

    def Method2(self, user_message: UserDefinedMessage2) -> UserDefinedResponse2:
        greeting = "This is from method2"
        user_response = UserDefinedResponse(greeting=greeting)
        return user_response

    def Streaming(
        self, user_message: UserDefinedMessage
    ) -> Generator[UserDefinedResponse, None, None]:
        for i in range(10):
            greeting = f"{i}: Hello {user_message.name} from {user_message.foo}"
            num_x2 = user_message.num * 2 + i
            user_response = UserDefinedResponse(
                greeting=greeting,
                num_x2=num_x2,
            )
            yield user_response

            time.sleep(0.1)

    @serve.multiplexed(max_num_models_per_replica=3)
    async def get_model(self, model_id: str) -> str:
        return f"loading model: {model_id}"

    async def Multiplex(self, user_message: UserDefinedMessage) -> UserDefinedResponse:
        model_id = serve.get_multiplexed_model_id()
        model = await self.get_model(model_id)
        user_response = UserDefinedResponse(
            greeting=f"{user_message.name} called model {model}",
        )
        return user_response


g = GrpcDeployment.options(name="grpc-deployment").bind()


@serve.deployment
class FruitMarket:
    def __init__(
        self,
        _orange_stand: RayServeDeploymentHandle,
        _apple_stand: RayServeDeploymentHandle,
    ):
        self.directory = {
            "ORANGE": _orange_stand,
            "APPLE": _apple_stand,
        }

    async def FruitStand(self, fruit_amounts_proto: FruitAmounts) -> FruitCosts:
        fruit_amounts = {}
        if fruit_amounts_proto.orange:
            fruit_amounts["ORANGE"] = fruit_amounts_proto.orange
        if fruit_amounts_proto.apple:
            fruit_amounts["APPLE"] = fruit_amounts_proto.apple
        if fruit_amounts_proto.banana:
            fruit_amounts["BANANA"] = fruit_amounts_proto.banana

        costs = await self.check_price(fruit_amounts)
        return FruitCosts(costs=costs)

    async def check_price(self, inputs: Dict[str, int]) -> float:
        costs = 0
        for fruit, amount in inputs.items():
            if fruit not in self.directory:
                return
            fruit_stand = self.directory[fruit]
            ref: ray.ObjectRef = await fruit_stand.remote(int(amount))
            result = await ref
            costs += result
        return costs


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


orange_stand = OrangeStand.bind()
apple_stand = AppleStand.bind()
g2 = FruitMarket.options(name="grpc-deployment-model-composition").bind(
    orange_stand, apple_stand
)


@serve.deployment
class ImageClassifier:
    def __init__(
        self,
        _image_downloader: RayServeDeploymentHandle,
        _data_preprocessor: RayServeDeploymentHandle,
    ):
        self._image_downloader = _image_downloader.options(use_new_handle_api=True)
        self._data_preprocessor = _data_preprocessor.options(use_new_handle_api=True)
        self.model = torch.hub.load(
            "pytorch/vision:v0.10.0", "resnet18", pretrained=True
        )
        self.model.eval()
        self.categories = self._image_labels()

    def _image_labels(self) -> List[str]:
        categories = []
        url = (
            "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        )
        labels = requests.get(url).text
        for label in labels.split("\n"):
            categories.append(label.strip())
        return categories

    async def Predict(self, image_data: ImageData) -> ImageClass:
        # Download image
        image = await self._image_downloader.remote(image_data.url)

        # Preprocess image
        input_batch = await self._data_preprocessor.remote(image)
        # Predict image
        with torch.no_grad():
            output = self.model(input_batch)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        return self.process_model_outputs(probabilities)

    def process_model_outputs(self, probabilities: torch.Tensor) -> ImageClass:
        image_classes = []
        image_probabilities = []
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        for i in range(top5_prob.size(0)):
            image_classes.append(self.categories[top5_catid[i]])
            image_probabilities.append(top5_prob[i].item())

        return ImageClass(
            classes=image_classes,
            probabilities=image_probabilities,
        )


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
g3 = ImageClassifier.options(name="grpc-image-classifier").bind(
    image_downloader, data_preprocessor
)


@serve.deployment
class HttpDeployment:
    async def __call__(self, request: Request) -> str:
        body = await request.body()
        print("request.body() in HttpDeployment", body)
        return f"Hello {body} {time.time()}"


h = HttpDeployment.options(name="http-deployment").bind()


@serve.deployment
class HttpDeployment2:
    async def __call__(self, request: Request) -> str:
        body = await request.body()
        print("request.body() in HttpDeployment2", body)
        return f"World {body} {time.time()}"


h2 = HttpDeployment2.options(name="http-deployment").bind()


app = FastAPI()


@serve.deployment
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.get("/root")
    def root(self):
        return "Hello, world!"

    @app.get("/root2")
    def root2(self):
        return "hello2"


app = MyFastAPIDeployment.bind()
