from typing import Callable

from nnsight.tracing.protocols import Protocol


class LogProtocol(Protocol):

    @classmethod
    def put(cls, fn: Callable):

        pass
