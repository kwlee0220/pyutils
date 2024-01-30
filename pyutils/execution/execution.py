from __future__ import annotations

from typing import TypeVar, Generic, Optional, cast, overload
from abc import ABC, abstractmethod
from collections.abc import Sequence, Iterable, Callable
from enum import Enum
from datetime import datetime, timedelta

from ..types import InvalidStateError


T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


class InterruptError(ValueError):
    __slots__ = ()
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class ExecutionError(ValueError):
    __slots__ = ()
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class CancellError(ValueError):
    __slots__ = ()
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AsyncState(Enum):
    NOT_STARTED = 0
    '''Execution is not started.'''
    STARTING = 1
    '''Execution is preparing for start.'''
    RUNNING = 2
    '''Execution is running.'''
    CANCELLING = 3
    '''Execution is stopping.'''
    CANCELLED = 4
    '''Execution has been stopped by something.'''
    FAILED = 5
    '''Execution has been finished because of a failure'''
    COMPLETED = 6
    '''Execution has been done sucessfully.'''
    
    def __init__(self, code:int) -> None:
        self.code = code

class AsyncResult(Generic[T]):
    __slots__ = ('state', 'result', 'failure_cause')
    
    def __init__(self, state:AsyncState, result:Optional[T]=None, failure_cause:Optional[Exception]=None) -> None:
        self.state = state
        self.result = result
        self.failure_cause = failure_cause
    
    def is_running(self) -> bool:
        return self.state.value >= AsyncState.RUNNING.value
    
    def is_completed(self) -> bool:
        return self.state.value >= AsyncState.COMPLETED.value
    
    def is_failed(self) -> bool:
        return self.state.value >= AsyncState.FAILED.value
    
    def is_cancelled(self) -> bool:
        return self.state.value >= AsyncState.CANCELLED.value
    
    def get(self) -> T|None:
        match self.state:
            case AsyncState.COMPLETED:
                return self.result
            case AsyncState.FAILED:
                assert self.failure_cause
                raise self.failure_cause
            case AsyncState.CANCELLED:
                raise CancellError()
            case _:
                raise InvalidStateError(f'not finished')
    
    

class Execution(Generic[T],ABC):
    @property
    @abstractmethod
    def state(self) -> AsyncState: ...
    
    def is_started(self) -> bool:
        return self.state.value >= AsyncState.STARTING.value
    
    def is_running(self) -> bool:
        return self.state.value >= AsyncState.RUNNING.value
    
    def is_completed(self) -> bool:
        return self.state.value >= AsyncState.COMPLETED.value
    
    def is_failed(self) -> bool:
        return self.state.value >= AsyncState.FAILED.value
    
    def is_cancelled(self) -> bool:
        return self.state.value >= AsyncState.CANCELLED.value
    
    def is_stopped(self) -> bool:
        match self.state:
            case AsyncState.COMPLETED | AsyncState.CANCELLED | AsyncState.FAILED:
                return True
            case _:
                return False
            
    def get(self, timeout:Optional[datetime|timedelta]=None) -> T|None:
        return self.wait_for_finished(timeout).get()
    
    @abstractmethod
    def poll(self) -> AsyncResult[T]: ...
    
    @abstractmethod
    def wait_for_finished(self, due:Optional[datetime|timedelta]=None) -> AsyncResult[T]: pass
    
    @abstractmethod
    def cancel(self) -> bool: ...
    
    @abstractmethod
    def when_finished(self, handler:Callable[[Execution[T]],None]) -> None: pass