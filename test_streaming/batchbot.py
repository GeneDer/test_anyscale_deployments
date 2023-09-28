import asyncio
import logging
from queue import Empty, Queue

from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from starlette.responses import StreamingResponse
from typing import List
from ray import serve

logger = logging.getLogger("ray.serve")


class RawStreamer:
    def __init__(self, timeout: float = None):
        self.q = Queue()
        self.stop_signal = None
        self.timeout = timeout

    def put(self, values):
        self.q.put(values)

    def end(self):
        self.q.put(self.stop_signal)

    def __iter__(self):
        return self

    def __next__(self):
        result = self.q.get(timeout=self.timeout)
        if result == self.stop_signal:
            raise StopIteration()
        else:
            return result

fastapi_app = FastAPI()


@serve.deployment
@serve.ingress(fastapi_app)
class Batchbot:
    def __init__(self, model_id: str):
        self.loop = asyncio.get_running_loop()

        self.model_id = model_id
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    @fastapi_app.post("/")
    async def handle_request(self, prompt: str) -> StreamingResponse:
        logger.info(f'Got prompt: "{prompt}"')
        return StreamingResponse(self.run_model(prompt), media_type="text/plain")

    @serve.batch(max_batch_size=2, batch_wait_timeout_s=15)
    async def run_model(self, prompts: List[str]):
        streamer = RawStreamer()
        self.loop.run_in_executor(None, self.generate_text, prompts, streamer)
        on_prompt_tokens = True
        async for decoded_token_batch in self.consume_streamer(streamer):
            # The first batch of tokens contains the prompts, so we skip it.
            if not on_prompt_tokens:
                logger.info(f"Yielding decoded_token_batch: {decoded_token_batch}")
                yield decoded_token_batch
            else:
                logger.info(f"Skipped prompts: {decoded_token_batch}")
                on_prompt_tokens = False

    def generate_text(self, prompts: str, streamer: RawStreamer):
        input_ids = self.tokenizer(prompts, return_tensors="pt", padding=True).input_ids
        self.model.generate(input_ids, streamer=streamer, max_length=10000)

    async def consume_streamer(self, streamer: RawStreamer):
        while True:
            try:
                for token_batch in streamer:
                    decoded_tokens = []
                    for token in token_batch:
                        decoded_tokens.append(
                            self.tokenizer.decode(token, skip_special_tokens=True)
                        )
                    logger.info(f"Yielding decoded tokens: {decoded_tokens}")
                    yield decoded_tokens
                break
            except Empty:
                await asyncio.sleep(0.001)

app = Batchbot.bind("microsoft/DialoGPT-small")
