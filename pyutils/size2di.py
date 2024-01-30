from __future__ import annotations

from typing import overload
from collections.abc import Sequence


class Size2di(Sequence[int]):
    __slots__ = ( '__width', '__height' )
    
    def __init__(self, *wh:int) -> None:
        self.__width = wh[0]
        self.__height = wh[1]

    @staticmethod
    def from_expr(expr:str|Sequence[int]) -> Size2di:
        """인자 값을 'Size2di' 객체로 형 변화시킨다.
        - 인자가 Size2di인 경우는 별도의 변환없이 인자를 복사하여 반환한다.
        - 인자가 문자열인 경우에는 '<width> x <height>' 형식으로 파싱하여 Size2di를 생성함.
        - 그렇지 않은 경우는 numpy.array() 함수를 통해 numpy array로 변환하고 이를 다시 Size2di로 생성함.

        Args:
            expr (object): 형 변환시킬 대상 객체.

        Returns:
            Size2di: 형 변환된 Size2di 객체.
        """
        if isinstance(expr, str):
            parts: list[int] = [int(p) for p in expr.split("x")]
            if len(parts) == 2:
                return Size2di(*parts[:2])
            raise ValueError(f"invalid Size2di string: {expr}")
        elif isinstance(expr, Sequence):
            return Size2di(*expr[:2])
        else:
            raise ValueError(f"invalid Size2di expression: {expr}")
        
    @property
    def width(self) -> int:
        return self.__width
        
    @property
    def height(self) -> int:
        return self.__height
        
    def __len__(self) -> int:
        return 2
    
    def __iter__(self):
        return iter((self.__width, self.__height))
    
    @overload
    def __getitem__(self, idx:int) -> int: pass
    @overload
    def __getitem__(self, idx:slice) -> list[int]: pass
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return [self.__width, self.__height][idx]
        elif isinstance(idx, slice):
            return [self.__width, self.__height][idx]
        else:
            raise IndexError(f"invalid index: {idx}")
    
    def round(self) -> Size2di:
        return Size2di(round(self.width), round(self.height))

    def area(self) -> int:
        """본 Size2di에 해당하는 영역을 반환한다.

        Returns:
            int: 영역.
        """
        return self.width * self.height
    
    def norm(self) -> float:
        import math
        return math.sqrt((self.width*self.width) + (self.height*self.height))

    def aspect_ratio(self) -> float:
        """본 Size2di의 aspect ratio (=w/h)를 반환한다.

        Returns:
            float: aspect ratio
        """
        return self.width / self.height

    def __add__(self, rhs:Size2di|Sequence[int]|int) -> Size2di:
        if isinstance(rhs, Size2di):
            return Size2di(self.width+rhs.width, self.height+rhs.height)
        elif isinstance(rhs, int):
            return Size2di(self.width+rhs, self.height+rhs)
        elif isinstance(rhs, Sequence):
            return Size2di(self.width+int(rhs[0]), self.height+int(rhs[1]))
        else:
            raise ValueError(f"incompatible for __add__: {rhs}")

    def __sub__(self, rhs:Size2di|Sequence[int]|int) -> Size2di:
        if isinstance(rhs, Size2di):
            return Size2di(self.width-rhs.width, self.height-rhs.height)
        elif isinstance(rhs, int):
            return Size2di(self.width-rhs, self.height-rhs)
        elif isinstance(rhs, Sequence):
            return Size2di(self.width-int(rhs[0]), self.height-int(rhs[1]))
        else:
            raise ValueError(f"incompatible for __sub__: {rhs}")

    def __mul__(self, rhs:Size2di|Sequence[int]|int) -> Size2di:
        if isinstance(rhs, Size2di):
            return Size2di(self.width*rhs.width, self.height*rhs.height) 
        elif isinstance(rhs, int):
            return Size2di(self.width*rhs, self.height*rhs)
        elif isinstance(rhs, Sequence):
            return Size2di(self.width*int(rhs[0]), self.height*int(rhs[1]))
        else:
            raise ValueError(f"incompatible for __mul__: {rhs}")

    def __eq__(self, other:Size2di):
        import math
        if isinstance(other, Size2di):
            return math.isclose(self.width, other.width) and math.isclose(self.height, other.height)
        else:
            raise NotImplemented
        
    def __hash__(self):
        return hash((self.__width, self.__height))
    
    def __repr__(self) -> str:
        return f'{self.width}x{self.height}'
    
