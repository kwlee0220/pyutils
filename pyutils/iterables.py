from __future__ import annotations

from typing import Union, TypeVar, Optional
from collections.abc import Iterable, Iterator, Callable, Generator, Sequence

T = TypeVar("T")


def find_first(iterable:Iterable[T], cond:Callable[[T], bool]) -> tuple[int,Optional[T]]:
    for idx, elm in enumerate(iterable):
        if cond(elm):
            return idx, elm
    return -1, None