from __future__ import annotations

from typing import TypeVar, TypeAlias, Optional, overload, Any, Protocol, cast, Generic
from collections.abc import Iterable, Callable, Iterator, Sequence
from dataclasses import dataclass
from collections import deque
import builtins

import itertools

from .types import KeyValue
from .typing import SupportsDunderLT, SupportsDunderEQ, SupportsRichComparison, SupportsRichComparisonNeg
from .typing import SupportsRichComparisonT


S = TypeVar("S")
S_contra = TypeVar('S_contra', contravariant=True)
T = TypeVar("T")
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

K = TypeVar("K")
K_contra = TypeVar('K_contra', contravariant=True)

Predicate:TypeAlias = Callable[[T_contra], bool]
Mapper:TypeAlias = Callable[[T],S]
FlatMapper:TypeAlias = Callable[[T],Iterable[S]]
FlatMapperNone:TypeAlias = Callable[[T],Iterable[S|None]]



class Stream(Generic[S]):
    __slots__ = ( '__src', )
    
    def __init__(self, src:Iterable[S]) -> None:
        super().__init__()
        self.__src = src if isinstance(src, Iterator) else iter(src)
        
    def __iter__(self) -> Iterator[S]:
        return iter(self.__src)
    
    def __next__(self) -> S:
        return next(self.__src)
    
    @classmethod
    def from_dict(cls, values:dict[K,S]) -> Stream[KeyValue[K,S]]:
        return Stream((KeyValue(k, v) for k, v in values.items()))
    
    @classmethod
    def generate(cls, init:S, inc:Callable[[S],S]) -> Stream[S]:
        def generate() -> Iterator[S]:
            state = init
            while True:
                yield state
                state = inc(state)
        return Stream(generate())
    
    @classmethod
    def unfold(cls, init:K, unfolder:Callable[[K],tuple[K,S]]) -> Stream[S]:
        def generate() -> Iterator[S]:
            state = init
            while True:
                state, v = unfolder(state)
                yield v
        return Stream(generate())
    
    @classmethod
    def repeat(cls, v:S, times:int) -> Stream[S]:
        import itertools
        return Stream(itertools.repeat(v, times))
    
    @classmethod
    def cycle(cls, itbl:Iterable[S]) -> Stream[S]:
        import itertools
        return Stream(itertools.cycle(itbl))
    
    @classmethod
    def range(cls, start:S, stop:Optional[S]=None, step:Any=1) -> Stream[S]:
        def generate() -> Iterator[S]:
            value = start
            while True:
                if stop is not None and value > stop:   # type: ignore
                    return
                yield value
                value += step
        return Stream(generate())
        
    def where(self, pred:Callable[[S], bool]) -> Stream[S]:
        tar = builtins.filter(pred, self.__src)
        return Stream(tar)
        
    def filter(self, pred:Callable[[S], bool]) -> Stream[S]:
        tar = builtins.filter(pred, self.__src)
        return Stream(tar)
        
    def map(self, mapper:Callable[[S],T]) -> Stream[T]:
        tar = builtins.map(mapper, self.__src)
        return Stream(tar)

    def flatmap(self, mapper:Callable[[S],Optional[Iterable[T]]]) -> Stream[T]:
        mapped_values = (mapper(iv) for iv in self.__src)
        strm_iter = (strm for strm in mapped_values if strm is not None)
        return Stream(itertools.chain.from_iterable(strm_iter))
       
    def take(self, count:int) -> Stream[S]:
        return Stream(itertools.islice(self.__src, 0, count))
       
    def drop(self, count:int) -> Stream[S]:
        return Stream(itertools.islice(self.__src, count, None))
         
    def take_last(self, count:int) -> Stream[S]:
        dequeue = deque([])
        for v in self.__src:
            if len(dequeue) >= count:
                dequeue.popleft()
            dequeue.append(v)
        return Stream(dequeue)
         
    def drop_last(self, count:int) -> Stream[S]:
        def generate() -> Iterator[S]:
            dequeue = deque([])
            for v in self.__src:
                if len(dequeue) >= count:
                    head = dequeue.popleft()
                    yield head
                dequeue.append(v)
        return Stream(generate())

    def take_while(self, pred:Callable[[S], bool]) -> Stream[S]:
        def generate() -> Iterator[S]:
            for v in self.__src:
                if pred(v):
                    yield v
                else:
                    return
        return Stream(generate())
    
    def drop_while(self, pred:Callable[[S], bool]) -> Stream[S]:
        def generate() -> Iterator[S]:
            publishing = False
            for v in self.__src:
                if publishing:
                    yield v
                elif not pred(v):
                    publishing = True
                    yield v
        return Stream(generate())
    
    def islice(self, *args:int) -> Stream[S]:
        from itertools import islice
        return Stream(islice(self.__src, *args))

    def zip_index(self, start:int=0) -> Stream[tuple[int,S]]:
        return Stream(cast(Iterator[tuple[int,S]], enumerate(self.__src)))

    def zip(self, other:Iterable[T],
            *,
            longest:bool=False,
            fill_value:Optional[S|T]=None) -> Stream[tuple[S,T]]:
        if longest:
            from itertools import zip_longest
            return zip_longest(input1, input2, fillvalue=fill_value)    # type: ignore
        else:
            return Stream(builtins.zip(self.__src, other))
        
    def accumulate(self, accum:Callable[[T,S],T], *, initial=None) -> Stream[T]:
        import itertools
        return Stream(itertools.accumulate(self.__src, accum, initial=initial))
    
    def groupby(self, keyer:Callable[[S],K]) -> dict[K,list[S]]:
        groups:dict[K,list[S]] = dict()
        for v in self.__src:
            key = keyer(v)
            if key not in groups:
                groups[key] = []
            groups[key].append(v)
        return groups
        
    def count(self) -> int:
        count = 0
        for _ in self.__src:
            count += 1
        return count
    
    @overload
    def max(self, *, default:Optional[SupportsDunderLT[S]]=None) -> Optional[S]: ...
    @overload
    def max(self, *,
            key:Optional[Callable[[S],SupportsDunderLT[K]]]=None,
            default:Optional[SupportsDunderLT[S]]=None) -> Optional[S]: ...
    def max(self, *, key=None, default=None) -> Optional[S]:
        if key:
            if default is None:
                return builtins.max(self.__src, key=key)
            else:
                return builtins.max(self.__src, key=key, default=default)
        else:
            if default is None:
                return builtins.max(src)
            else:
                return builtins.max(src, default=default)
            
    def min(self, *,
            key:Optional[Callable[[S],K]]=None,
            default:Optional[S]=None) -> Optional[S]:
        if key:
            if default is None:
                return builtins.min(input, key=key)
            else:
                return builtins.min(input, key=key, default=default)
        else:
            if default is None:
                return builtins.min(input)
            else:
                return builtins.min(input, default=default)    

    @overload
    @staticmethod
    def argmax(input:Sequence[SupportsRichComparison]) -> int: ...
    @overload
    @staticmethod
    def argmax(input:Sequence[S], *, key:Callable[[S],SupportsRichComparison]) -> int: ...
    @staticmethod
    def argmax(input, *, key=None) -> int:
        assert len(input) > 0
        key_ext = lambda t: key(t[1]) if key else lambda t: t[1]
        t = max(enumerate(input), key=key_ext)  # type: ignore
        assert t
        return t[0]

    @overload
    @staticmethod
    def argmin(input:Sequence[SupportsRichComparison]) -> int: ...
    @overload
    @staticmethod
    def argmin(input:Sequence[S], *, key:Callable[[S],SupportsRichComparison]) -> int: ...
    @staticmethod
    def argmin(input, *, key=None) -> int:
        assert len(input) > 0
        key_ext = lambda t: key(t[1]) if key else lambda t: t[1]
        t = min(enumerate(input), key=key_ext)    # type: ignore
        assert t
        return t[0]
    
    @overload
    def top_k(self, k:int, *, reversed:bool=False) -> Stream[SupportsRichComparison]: ...
    @overload
    def top_k(self, k:int, *,
            key:Callable[[S],SupportsRichComparisonNeg],
            reversed:bool=False) -> Stream[S]: ...
    def top_k(self, k:int, *, key=None, reversed=False) -> Stream[S]|Stream[SupportsRichComparison]:
        from heapq import nlargest
        if reversed:
            key_ext = lambda v: -key(v)     # type: ignore
            return Stream(nlargest(k, self.__src, key=key_ext))
        else:
            return Stream(nlargest(k, self.__src, key=key))
    
    @overload
    def sorted(self, *, reversed:bool=False) -> Stream[SupportsRichComparison]: ...
    @overload
    def sorted(self, *,
            key:Optional[Callable[[S],SupportsRichComparison]]=None,
            reversed:bool=False) -> Stream[S]: ...
    def sorted(self, *, key=None, reversed:bool=False) -> Stream[S]|Stream[SupportsRichComparison]:
        if key:
            return Stream(builtins.sorted(self.__src, key=key, reverse=reversed))
        else:
            src = cast(Iterable[SupportsRichComparison], self.__src)
            return Stream(builtins.sorted(src, reverse=reversed))
        
    @overload
    def distinct(self:SupportsDunderEQ) -> set[S]: ...
    @overload
    def distinct(self, *, key:Callable[[S],SupportsDunderEQ]) -> set[S]: ...
    def distinct(self, *, key=None) -> set[S]:
        @dataclass(frozen=True, slots=True)
        class Item(Generic[K,S]):
            key: K
            value: S
            
            def __eq__(self, other: Item[K,S]) -> bool:
                if isinstance(other, Item):
                    return self.key == other.key
                else:
                    return False
        
        if key is None:
            return set(self.__src)
        else:
            ditincts = set(map(lambda v: Item(key=key(v), value=v), self.__src))
            return {item.value for item in ditincts}

    def quasi_sort(self, qlen:int, *,
                   key:Optional[Callable[[S],SupportsRichComparisonNeg]]=None,
                   reversed:bool=False) -> Stream[S]:
        def generate() -> Iterator[S]:
            from heapq import heappush, heappop
            heap = []
            if key is None:
                for v in self.__src:
                    if len(heap) >= qlen:
                        yield heappop(heap)
                    heappush(heap, (-v,v) if reversed else v)
                for v in heap:
                    yield v[1] if reversed else v
            else:
                for v in self.__src:
                    if len(heap) >= qlen:
                        yield heappop(heap)[1]
                    heappush(heap, (-key(v), v) if reversed else (key(v), v))
                for k, v in heap:
                    yield v[1]
        return Stream(generate())
    
    def find_first(self, pred:Optional[Callable[[S], bool]]=None,
                   *,
                   default:Optional[S]=None) -> Optional[S]:
        src = builtins.filter(pred, self.__src) if pred else self.__src
        return next(iter(src), default)
    
    def find_last(self, pred:Optional[Callable[[S], bool]]=None,
                  *,
                  default:Optional[S]=None) -> Optional[S]:
        try:
            src = builtins.filter(pred, self.__src) if pred else self.__src
            *_, last = src
            return last
        except ValueError:
            return default
 
    def foreach(self, action:Callable[[S],None]) -> None:
        for v in self.__src:
            action(v)