from __future__ import annotations

from typing import overload
from collections.abc import Sequence

from .size2di import Size2di


class Size2d(Sequence[float]):
    __slots__ = ( '__width', '__height' )
    
    def __init__(self, *wh:float) -> None:
        self.__width = wh[0]
        self.__height = wh[1]

    @staticmethod
    def from_expr(expr:str|Sequence[float]) -> Size2d:
        """인자 값을 'Size2d' 객체로 형 변화시킨다.
        - 인자가 Size2d인 경우는 별도의 변환없이 인자를 복사하여 반환한다.
        - 인자가 문자열인 경우에는 '<width> x <height>' 형식으로 파싱하여 Size2d를 생성함.
        - 그렇지 않은 경우는 numpy.array() 함수를 통해 numpy array로 변환하고 이를 다시 Size2d로 생성함.

        Args:
            expr (object): 형 변환시킬 대상 객체.

        Returns:
            Size2d: 형 변환된 Size2d 객체.
        """
        if isinstance(expr, str):
            parts: list[float] = [float(p) for p in expr.split("x")]
            if len(parts) == 2:
                return Size2d(*parts[:2])
            raise ValueError(f"invalid Size2d string: {expr}")
        elif isinstance(expr, Sequence):
            return Size2d(*expr[:2])
        else:
            raise ValueError(f"invalid Size2d expression: {expr}")
        
    @property
    def width(self) -> float:
        return self.__width
        
    @property
    def height(self) -> float:
        return self.__height
        
    def __len__(self) -> int:
        return 2
    
    def __iter__(self):
        return iter((self.__width, self.__height))
    
    @overload
    def __getitem__(self, idx:int) -> float: pass
    @overload
    def __getitem__(self, idx:slice) -> list[float]: pass
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return [self.__width, self.__height][idx]
        elif isinstance(idx, slice):
            return [self.__width, self.__height][idx]
        else:
            raise IndexError(f"invalid index: {idx}")
    
    def round(self) -> Size2di:
        return Size2di(round(self.width), round(self.height))

    def area(self) -> float:
        """본 Size2d에 해당하는 영역을 반환한다.

        Returns:
            float: 영역.
        """
        return self.width * self.height
    
    def norm(self) -> float:
        import math
        return math.sqrt((self.width*self.width) + (self.height*self.height))

    def aspect_ratio(self) -> float:
        """본 Size2d의 aspect ratio (=w/h)를 반환한다.

        Returns:
            float: aspect ratio
        """
        return self.width / self.height

    def __add__(self, rhs:Size2d|Sequence[float]|float|int) -> Size2d:
        if isinstance(rhs, Size2d):
            return Size2d(self.width+rhs.width, self.height+rhs.height)
        elif isinstance(rhs, float|int):
            return Size2d(self.width+rhs, self.height+rhs)
        elif isinstance(rhs, Sequence):
            return Size2d(self.width+float(rhs[0]), self.height+float(rhs[1]))
        else:
            raise ValueError(f"incompatible for __add__: {rhs}")

    def __sub__(self, rhs:Size2d|Sequence[float]|float|int) -> Size2d:
        if isinstance(rhs, Size2d):
            return Size2d(self.width-rhs.width, self.height-rhs.height)
        elif isinstance(rhs, float|int):
            return Size2d(self.width-rhs, self.height-rhs)
        elif isinstance(rhs, Sequence):
            return Size2d(self.width-float(rhs[0]), self.height-float(rhs[1]))
        else:
            raise ValueError(f"incompatible for __sub__: {rhs}")

    def __mul__(self, rhs:Size2d|Sequence[float]|float|int) -> Size2d:
        if isinstance(rhs, Size2d):
            return Size2d(self.width*rhs.width, self.height*rhs.height) 
        elif isinstance(rhs, float|int):
            return Size2d(self.width*rhs, self.height*rhs)
        elif isinstance(rhs, Sequence):
            return Size2d(self.width*float(rhs[0]), self.height*float(rhs[1]))
        else:
            raise ValueError(f"incompatible for __mul__: {rhs}")

    def __truediv__(self, rhs:Size2d|Sequence[float]|float|int) -> Size2d:
        if isinstance(rhs, Size2d):
            return Size2d(self.width/rhs.width, self.height/rhs.height)
        elif isinstance(rhs, float|int):
            return Size2d(self.width/rhs, self.height/rhs)
        elif isinstance(rhs, Sequence):
            return Size2d(self.width/rhs[0], self.height/rhs[1])
        else:
            raise ValueError(f"incompatible for __truediv__: {rhs}")

    def __eq__(self, other:Size2d):
        import math
        if isinstance(other, Size2d):
            return math.isclose(self.width, other.width) and math.isclose(self.height, other.height)
        else:
            raise NotImplemented
        
    def __hash__(self):
        return hash((self.__width, self.__height))
    
    def __repr__(self) -> str:
        return f'{self.width}x{self.height}'
    
