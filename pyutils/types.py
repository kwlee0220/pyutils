from __future__ import annotations

from typing import Generic, TypeVar
from dataclasses import dataclass


class InvalidStateError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


K = TypeVar("K")
T = TypeVar("T")
@dataclass(frozen=True, unsafe_hash=True, slots=True)
class KeyValue(Generic[K,T]):
    key: K
    value: T
    
    def __iter__(self):
        return iter((self.key, self.value))
