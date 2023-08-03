from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDefinedMessage(_message.Message):
    __slots__ = ["foo", "name", "num"]
    FOO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    foo: str
    name: str
    num: int
    def __init__(self, name: _Optional[str] = ..., foo: _Optional[str] = ..., num: _Optional[int] = ...) -> None: ...

class UserDefinedResponse(_message.Message):
    __slots__ = ["greeting", "num_x2"]
    GREETING_FIELD_NUMBER: _ClassVar[int]
    NUM_X2_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    num_x2: int
    def __init__(self, greeting: _Optional[str] = ..., num_x2: _Optional[int] = ...) -> None: ...
