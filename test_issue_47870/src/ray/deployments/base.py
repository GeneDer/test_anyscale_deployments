import gc
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
from functools import partial, wraps
from typing import Any, Dict

import ray
import torch
from minio import Minio
from pydantic import BaseModel, ConfigDict
from torch.amp import autocast
from torch.cuda import (max_memory_allocated, memory_allocated,
                        reset_peak_memory_stats)
from transformers import PreTrainedModel

from nnsight.contexts.backends.RemoteBackend import RemoteMixin
from nnsight.models.mixins import RemoteableMixin

from src.telemetry.logging import load_logger
from src.telemetry import NDIFGauge
from src.schema import (BackendRequestModel, BackendResponseModel,
                       BackendResultModel)
from . import protocols


class BaseDeployment:

    def __init__(
        self,
        api_url: str,
        object_store_url: str,
        object_store_access_key: str,
        object_store_secret_key: str,
    ) -> None:
        super().__init__()

        self.api_url = api_url
        self.object_store_url = object_store_url
        self.object_store_access_key = object_store_access_key
        self.object_store_secret_key = object_store_secret_key

        self.object_store = Minio(
            self.object_store_url,
            access_key=self.object_store_access_key,
            secret_key=self.object_store_secret_key,
            secure=False,
        )

        self.logger = load_logger(
            service_name=str(self.__class__), logger_name="ray.serve"
        )
        self.gauge = NDIFGauge(service="ray")


class BaseDeploymentArgs(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    api_url: str
    object_store_url: str
    object_store_access_key: str
    object_store_secret_key: str


def threaded(method, size: int = 1):

    group = ThreadPoolExecutor(size)

    @wraps(method)
    def inner(*args, **kwargs):

        return group.submit(method, *args, **kwargs)

    return inner


class BaseModelDeployment(BaseDeployment):

    def __init__(
        self,
        model_key: str,
        execution_timeout: float | None,
        device_map: str | None,
        dispatch: bool,
        dtype: str | torch.dtype,
        *args,
        extra_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.model_key = model_key
        self.execution_timeout = execution_timeout

        if isinstance(dtype, str):

            dtype = getattr(torch, dtype)

        torch.set_default_dtype(torch.bfloat16)

        self.model = RemoteableMixin.from_model_key(
            self.model_key,
            device_map=device_map,
            dispatch=dispatch,
            torch_dtype=dtype,
            **extra_kwargs
        )

        if dispatch:
            self.model._model.requires_grad_(False)

        torch.cuda.empty_cache()

    async def __call__(self, request: BackendRequestModel) -> Any:

        try:

            result = None

            protocols.LogProtocol.put(partial(self.log, request=request))

            self.pre(request)

            with autocast(device_type="cuda", dtype=torch.get_default_dtype()):

                result = self.execute(request)

                if isinstance(result, Future):
                    result = result.result(timeout=self.execution_timeout)

            self.post(request, result)

        except TimeoutError as e:

            exception = Exception(f"Job took longer than timeout: {self.execution_timeout} seconds")

            self.exception(request, exception)

        except Exception as e:

            self.exception(request, e)

        finally:

            del request
            del result

            self.cleanup()

    def status(self):

        model: PreTrainedModel = self.model._model

        return {
            "config_json_string": model.config.to_json_string(),
            "repo_id": model.config._name_or_path,
        }

    # Ray checks this method and restarts replica if it raises an exception
    def check_health(self):
        pass

    ### ABSTRACT METHODS #################################

    def pre(self, request: BackendRequestModel):

        request.create_response(
            status=BackendResponseModel.JobStatus.RUNNING,
            description="Your job has started running.",
            logger=self.logger,
            gauge=self.gauge,
        ).respond(self.api_url, self.object_store)

        request.object = ray.get(request.object)

    def execute(self, request: BackendRequestModel):

        # For tracking peak GPU usage
        if torch.cuda.is_available():
            reset_peak_memory_stats()
            model_memory = memory_allocated()

        # Deserialize request
        obj = request.deserialize(self.model)

        # Execute object.
        result = obj.local_backend_execute()

        # Compute GPU memory usage
        if torch.cuda.is_available():
            gpu_mem = max_memory_allocated() - model_memory
        else:
            gpu_mem = 0

        return result, obj, gpu_mem

    def post(self, request: BackendRequestModel, result: Any):

        obj: RemoteMixin = result[1]
        gpu_mem: int = result[2]
        result: Any = result[0]

        BackendResultModel(
            id=request.id,
            value=obj.remote_backend_postprocess_result(result),
        ).save(self.object_store)

        # Send COMPLETED response.
        request.create_response(
            status=BackendResponseModel.JobStatus.COMPLETED,
            description="Your job has been completed.",
            logger=self.logger,
            gauge=self.gauge,
            gpu_mem=gpu_mem,
        ).respond(self.api_url, self.object_store)

    def exception(self, request: BackendRequestModel, exception: Exception):

        request.create_response(
            status=BackendResponseModel.JobStatus.ERROR,
            description=str(exception),
            logger=self.logger,
            gauge=self.gauge,
        ).respond(self.api_url, self.object_store)

    def cleanup(self):

        self.model._model.zero_grad()

        gc.collect()

        torch.cuda.empty_cache()

    def log(self, data: Any, request: BackendRequestModel):

        request.create_response(
            status=BackendResponseModel.JobStatus.LOG,
            description=str(data),
            logger=self.logger,
            gauge=self.gauge,
        ).respond(self.api_url, self.object_store)


class BaseModelDeploymentArgs(BaseDeploymentArgs):

    model_key: str
    execution_timeout: float | None = None
    device_map: str | None = "auto"
    dispatch: bool = True
    dtype: str | torch.dtype = torch.bfloat16
