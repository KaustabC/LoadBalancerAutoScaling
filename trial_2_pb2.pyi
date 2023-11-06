from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class function_message(_message.Message):
    __slots__ = ["data1", "data2", "function"]
    DATA1_FIELD_NUMBER: _ClassVar[int]
    DATA2_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    data1: int
    data2: int
    function: int
    def __init__(self, data1: _Optional[int] = ..., data2: _Optional[int] = ..., function: _Optional[int] = ...) -> None: ...

class returnValue(_message.Message):
    __slots__ = ["val"]
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: float
    def __init__(self, val: _Optional[float] = ...) -> None: ...

class void(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
