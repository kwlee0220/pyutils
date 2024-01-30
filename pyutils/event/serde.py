from __future__ import annotations

from typing import TypeAlias, TypeVar, Generic
from collections.abc import Callable
from abc import ABC, abstractmethod


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)

Serializer:TypeAlias = Callable[[T], bytes]
Deserializer:TypeAlias = Callable[[bytes], T]


class Serde(ABC, Generic[T]):
    @abstractmethod
    def serializer(self) -> Serializer[T_contra]: pass
    
    @abstractmethod
    def deserializer(self) -> Deserializer[T_co]: pass