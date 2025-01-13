from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageClass(_message.Message):
    __slots__ = ["classes", "probabilities"]
    CLASSES_FIELD_NUMBER: _ClassVar[int]
    PROBABILITIES_FIELD_NUMBER: _ClassVar[int]
    classes: _containers.RepeatedScalarFieldContainer[str]
    probabilities: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, classes: _Optional[_Iterable[str]] = ..., probabilities: _Optional[_Iterable[float]] = ...) -> None: ...

class ImageData(_message.Message):
    __slots__ = ["filename", "url"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    filename: str
    url: str
    def __init__(self, url: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class UserDefinedMessage(_message.Message):
    __slots__ = ["name", "num", "origin"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    name: str
    num: int
    origin: str
    def __init__(self, name: _Optional[str] = ..., origin: _Optional[str] = ..., num: _Optional[int] = ...) -> None: ...

class UserDefinedMessage2(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UserDefinedResponse(_message.Message):
    __slots__ = ["greeting", "num"]
    GREETING_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    num: int
    def __init__(self, greeting: _Optional[str] = ..., num: _Optional[int] = ...) -> None: ...

class UserDefinedResponse2(_message.Message):
    __slots__ = ["greeting"]
    GREETING_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    def __init__(self, greeting: _Optional[str] = ...) -> None: ...
