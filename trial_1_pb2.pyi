from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class function_message(_message.Message):
    __slots__ = ["data1", "data2", "function", "ip"]
    DATA1_FIELD_NUMBER: _ClassVar[int]
    DATA2_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    data1: int
    data2: int
    function: int
    ip: str
    def __init__(self, data1: _Optional[int] = ..., data2: _Optional[int] = ..., function: _Optional[int] = ..., ip: _Optional[str] = ...) -> None: ...

class initMessage(_message.Message):
    __slots__ = ["loadType", "autoType", "services"]
    LOADTYPE_FIELD_NUMBER: _ClassVar[int]
    AUTOTYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    loadType: int
    autoType: int
    services: str
    def __init__(self, loadType: _Optional[int] = ..., autoType: _Optional[int] = ..., services: _Optional[str] = ...) -> None: ...

class initReply(_message.Message):
    __slots__ = ["port", "services", "count"]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    port: int
    services: str
    count: int
    def __init__(self, port: _Optional[int] = ..., services: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class returnValue(_message.Message):
    __slots__ = ["val"]
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: float
    def __init__(self, val: _Optional[float] = ...) -> None: ...

class void(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
