from __future__ import annotations

from typing import Union, TypeVar, Optional
from collections.abc import Iterable, Iterator, Callable, Generator, Sequence

T = TypeVar("T")


def find_first(iterable:Iterable[T], cond:Callable[[T], bool]) -> tuple[int,Optional[T]]:
    for idx, elm in enumerate(iterable):
        if cond(elm):
            return idx, elm
    return -1, None



class PeekableIterator(Iterator):
    def __init__(self, iter:Iterator[T]) -> None:
        self.head:T = None
        self.iter = iter
        self.peeked = False
    
    def peek(self) -> T:
        if not self.peeked:
            self.peeked = True
            self.head = next(self.iter)
        return self.head
    
    def __next__(self):
        if self.peeked:
            self.peeked = False
            return self.head
        else:
            return next(self.iter)

def to_peekable(iter:Iterator[T]) -> PeekableIterator[T]:
    if not isinstance(iter, PeekableIterator):
        return PeekableIterator(iter)
    else:
        return iter