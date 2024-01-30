from __future__ import annotations

from typing import cast, overload
from collections.abc import Sequence, Iterable

from .size2d import Size2d
from .point import Point


class Box(Sequence[float]):
    __slots__ = ('__top_left', '__size')
    
    def __init__(self, top_left:Point, size:Size2d) -> None:
        super().__init__()
        
        self.__top_left = top_left
        self.__size = size

    @classmethod
    def from_tlbr(cls, *tlbr:float) -> Box:
        tl = Point(*tlbr[:2])
        br = Point(*tlbr[2:])
        return Box(tl, br - tl)
    
    @classmethod
    def from_tlwh(cls, *tlwh:float) -> Box:
        return Box(Point(*tlwh[:2]), Size2d(*tlwh[2:]))
    
    @property
    def top_left(self) -> Point:
        return self.__top_left
    
    @property
    def bottom_right(self) -> Point:
        return self.__top_left + self.__size
    
    @property
    def tlbr(self) -> tuple[float,float,float,float]:
        return cast(tuple[float,float,float,float], tuple(self.top_left) + tuple(self.bottom_right))
    @property
    def tlwh(self) -> tuple[float,float,float,float]:
        return cast(tuple[float,float,float,float], tuple(self.top_left) + tuple(self.size))

    @property
    def size(self) -> Size2d:
        '''Returns width of this box object.'''
        return self.__size
    
    def center(self) -> Point:
        '''Returns the ``Point`` object of the center of this box object.'''
        return self.top_left + (self.size / 2)

    def area(self) -> float:
        """Returns the area of this box.
        If the box is invalid, zero will be returned.

        Returns:
            float: area
        """
        return self.size.area()
    
    def __iter__(self) -> Iterable[float]:
        return iter(self.tlwh)
    
    def __len__(self) -> int:
        return 4
    
    @overload
    def __getitem__(self, idx:int) -> float: pass
    @overload
    def __getitem__(self, idx:slice) -> list[float]: pass
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self.tlwh[idx]
        elif isinstance(idx, slice):
            return (list(self.top_left) + list(self.size))[idx]
        else:
            raise IndexError(f"invalid index: {idx}")

    def intersection(self, bbox:Box) -> Box:
        """Returns the intersection box of this box and the box given by the argument.

        Args:
            bbox (Box): a box object to take intersection with.

        Returns:
            Box: intersection box
        """
        self_br = self.bottom_right
        other_br = bbox.bottom_right
        x1 = max(self.top_left.x, bbox.top_left.x)
        y1 = max(self.top_left.y, bbox.top_left.y)
        x2 = min(self_br.x, other_br.x)
        y2 = min(self_br.y, other_br.y)
        return Box.from_tlbr(x1, y1, x2, y2)

    def iou(self, box:Box) -> float:
        inter_area = self.intersection(box).area()
        area1, area2 = self.area(), box.area()
        return inter_area / (area1 + area2 - inter_area)

    def __eq__(self, other:Box):
        if isinstance(other, Box):
            return self.top_left == other.top_left and self.size == other.size
        else:
            raise NotImplemented

    def is_valid(self) -> bool:
        """본 Box의 유효성 여부를 반환한다.

        Returns:
            bool: 유효성 여부.  l <= r and t <= b
        """
        x1, y1, x2, y2 = self.tlbr
        return x1 <= x2 and y1 <= y2

    def contains_point(self, pt:Point) -> bool:
        """Returns whether this box contains the given point or not.

        Args:
            pt (Point): a Point object for containment test.

        Returns:
            bool: True if this box contains the point object, otherwise False.
        """
        x, y = tuple(pt)
        br = self.bottom_right
        return x >= self.top_left.x and y >= self.top_left.y and x < br.x and y < br.y
    
    def __repr__(self):
        return f"{self.top_left}:{self.size}"
