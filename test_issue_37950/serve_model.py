import ray
import torch
import logging

from starlette.requests import Request
from transformers import BartTokenizer, BartForConditionalGeneration

LOGGER = logging.getLogger(__name__)

def get_torch_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


@ray.serve.deployment
class ModelServer:
    def __init__(self, model_id: str = "facebook/bart-large"):
        # Load model
        device = get_torch_device()
        self.model_id = model_id
        self.model = BartForConditionalGeneration.from_pretrained(model_id).to(device)
        self.tokenizer = BartTokenizer.from_pretrained(model_id)


    def generate_text(self, input_text):
        # Tokenize the input text
        input_tokens = self.tokenizer(input_text, return_tensors='pt')

        # Move the input tokens to the same device as the model
        input_tokens = input_tokens.to(self.model.device)

        # Generate text using the fine-tuned model
        output_tokens = self.model.generate(**input_tokens, max_new_tokens=200)

        # Decode the generated tokens to text
        output_text = self.tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        return output_text

    async def __call__(self, http_request: Request) -> str:
        data = await http_request.json()
        output = self.generate_text(data["inputs"])
        LOGGER.warning(f"Output: {output}")
        return output


serve_model_app = ModelServer.bind()
