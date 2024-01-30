from __future__ import annotations

from typing import TypeVar, overload, cast
from collections.abc import Sequence, Callable, Iterable
from math import sqrt

import numpy as np

from .size2d import Size2d


class Point(Sequence[float]):
    """A point coordinate in 2d plane.

    Attributes:
        x (float): x-coordinate
        y (float): y-coordinate
    """
    __slots__ = ( '__x', '__y' )
    
    def __init__(self, *xy:float) -> None:
        """(x,y) 좌표를 갖는 Point 객체를 반환한다.

        Args:
            x (float): x 좌표
            y (float): y 좌표
        """
        self.__x = xy[0]
        self.__y = xy[1]

    @property
    def x(self) -> float:
        """Point 객체 좌표의 x축 값.

        Returns:
            float: 좌표의 x축 값.
        """
        return self.__x

    @property
    def y(self) -> float:
        """Point 객체 좌표의 y축 값.

        Returns:
            float: 좌표의 y축 값.
        """
        return self.__y
    
    def norm(self) -> float:
        return sqrt((self.x*self.x) + (self.y*self.y))
        
    def distance_to(self, pt:Point) -> float:
        """Returns an Euclidean distance to the point pt.

        Args:
            pt (Point): target Point object to calculate distance to.

        Returns:
            float: distance.
        """
        return (pt - self).norm()

    def angle_between(self, pt:Point) -> float:
        """본 Point 객체 벡터와 인자 Point 객체 벡터 사이의 각(radian)을 반환한다.

        Args:
            pt (Point): 각을 계산할 대상 Point 객체.

        Returns:
            float: 두 벡터 사이의 각 (단위: radian)
        """
        xy1 = np.array(self, dtype=np.float32)
        xy2 = np.array(pt, dtype=np.float32)
        return cast(float, np.arctan2(np.cross(xy1, xy2), np.dot(xy1, xy2)))

    def line_function_to(self, pt2:Point) -> Callable[[float],float]:
        """본 Point 객체와 인자로 주어진 Point까지를 잇는 1차원 함수를 반환한다.

        Args:
            pt2 (Point): 목표 Point 객체.

        Raises:
            ValueError: 목표 Point 객체의 위치를 잇는 1차원 함수를 구할 수 없는 경우.
                        예를들어 두 Point의 x좌표가 동일한 경우.

        Returns:
            Callable[[float],float]: 1차원 함수.
        """
        delta = self - pt2
        if delta[0] == 0:
            raise ValueError(f"Cannot find a line function: {self} - {pt2}")
        slope = delta.height / delta.width
        y_int = pt2.y - (slope * pt2.x)

        def func(x):
            return (slope * x) + y_int
        return func

    def split_points_to(self, pt2:Point, npoints:int) -> list[Point]:
        func = self.line_function_to(pt2)
        step_x = (pt2.x - self.x) / (npoints+1)
        xs = [self.x + (idx * step_x) for idx in range(1, npoints+1)]
        return [Point(x, func(x)) for x in xs]

    def round(self) -> Point:
        """본 Point 객체의 좌표값을 int형식으로 반올림한 좌표를 갖는 Point 객체를 반환한다.

        Returns:
            Point: int형식으로 반올림한 좌표를 갖는 Point 객체.
        """
        return Point(round(self.__x), round(self.__y))
    
    def __iter__(self) -> Iterable[float]:
        return iter((self.__x, self.__y))
    
    def __len__(self) -> int:
        return 2
    
    @overload
    def __getitem__(self, idx:int) -> float: pass
    @overload
    def __getitem__(self, idx:slice) -> list[float]: pass
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return [self.x, self.y][idx]
        elif isinstance(idx, slice):
            return [self.x, self.y][idx]
        else:
            raise IndexError(f"invalid index: {idx}")

    def __add__(self, rhs:Size2d|Sequence[float]|float|int) -> Point:
        if isinstance(rhs, Size2d):
            return Point(self.x + rhs.width, self.y + rhs.height)
        elif isinstance(rhs, float|int):
            return Point(self.x + rhs, self.y + rhs)
        elif isinstance(rhs, Sequence) and len(rhs) == 2:
            return Point(self.x + rhs[0], self.y + rhs[1])
        else:
            raise ValueError(f"invalid rhs: rhs={rhs}")

    @overload
    def __sub__(self, rhs:Point) -> Size2d: ...
    @overload
    def __sub__(self, rhs:Size2d|Sequence[float]|float|int) -> Point: ...
    def __sub__(self, rhs:Point|Size2d|Sequence|float) -> Point|Size2d:
        if isinstance(rhs, Point):
            return Size2d(self.x - rhs.x, self.y - rhs.y)
        elif isinstance(rhs, Size2d):
            return Point(self.x - rhs.width, self.y - rhs.height)
        elif isinstance(rhs, float|int):
            return Point(self.x - rhs, self.y - rhs)
        elif isinstance(rhs, Sequence) and len(rhs) == 2:
            return Point(self.x - rhs[0], self.y - rhs[1])
        else:
            raise ValueError(f"invalid rhs: rhs={rhs}")

    def __mul__(self, rhs:Size2d|Sequence[float]|float|int) -> Point:
        if isinstance(rhs, Size2d):
            return Point(self.x * rhs.width, self.y * rhs.height)
        elif isinstance(rhs, float|int):
            return Point(self.x * rhs, self.y * rhs)
        elif isinstance(rhs, Sequence) and len(rhs) == 2:
            return Point(self.x * rhs[0], self.y * rhs[1])
        else:
            raise ValueError(f"invalid rhs: rhs={rhs}")

    def __truediv__(self, rhs:Size2d|Sequence[float]|float|int) -> Point:
        if isinstance(rhs, Size2d):
            return Point(self.x / rhs.width, self.y / rhs.height)
        elif isinstance(rhs, float|int):
            return Point(self.x / rhs, self.y / rhs)
        elif isinstance(rhs, Sequence) and len(rhs) == 2:
            return Point(self.x / rhs[0], self.y / rhs[1])
        else:
            raise ValueError('invalid right-hand-side:', rhs)

    def __eq__(self, other:Point):
        import math
        if isinstance(other, Point):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        else:
            raise NotImplemented
        
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"