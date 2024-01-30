from __future__ import annotations

from typing import Protocol, runtime_checkable, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Serializable(Protocol[T_contra]):
    def serialize(self, data:T_contra) -> bytes: ...
    
@runtime_checkable
class Deserializable(Protocol[T_co]):
    def deserialize(self, data:bytes) -> T_co: ...
    
@runtime_checkable
class JsonSerializable(Protocol[T_contra]):
    def to_json(self, data:T_contra) -> str: ...
    
@runtime_checkable
class JsonDeserializable(Protocol[T_co]):
    def from_json(self, data:str) -> T_co: ...