from __future__ import annotations

import unittest

from pyutils import Point, Size2d, Box


class BoxTest(unittest.TestCase):
    def test_init(self):
        box = Box(Point(0,0), Size2d(1,1))
        
        self.assertEqual(box.top_left, Point(0,0))
        self.assertEqual(box.size, Size2d(1,1))
        self.assertEqual(box.bottom_right, Point(1,1))
        self.assertEqual(box.tlbr, (0,0,1,1))
        
    def test_from_tlbr(self):
        box = Box.from_tlbr(0, 0, 1, 1)
        self.assertEqual(box.top_left, Point(0,0))
        self.assertEqual(box.size, Size2d(1,1))
        self.assertEqual(box.bottom_right, Point(1,1))
        self.assertEqual(box.tlbr, (0,0,1,1))
        
    def test_from_tlwh(self):
        box = Box.from_tlwh(0, 0, 1, 1)
        self.assertEqual(box.top_left, Point(0,0))
        self.assertEqual(box.size, Size2d(1,1))
        self.assertEqual(box.bottom_right, Point(1,1))
        self.assertEqual(box.tlbr, (0,0,1,1))
        
    def test_center(self):
        box = Box(Point(0,0), Size2d(2,2))
        self.assertEqual(box.center(), Point(1,1))
        
    def test_seq(self):
        box = Box(Point(0,0), Size2d(2,2))
        self.assertEqual(box.tlwh, tuple(c for c in box))   # type: ignore
        self.assertEqual(len(box), 4)
        self.assertEqual(0, box[0])
        self.assertEqual(0, box[1])
        self.assertEqual(2, box[2])
        self.assertEqual(2, box[3])
        
    def test_intersection(self):
        box1 = Box(Point(0,0), Size2d(1,1))
        box2 = Box(Point(0,0), Size2d(2,2))
        self.assertEqual(box1, box1.intersection(box2))
        
        box1 = Box(Point(0,0), Size2d(2,2))
        box2 = Box(Point(1,0), Size2d(2,2))
        self.assertEqual(Box(Point(1,0), Size2d(1,2)), box1.intersection(box2))
        
        box1 = Box(Point(0,0), Size2d(1,1))
        box2 = Box(Point(1,0), Size2d(2,2))
        self.assertEqual(Box(Point(1,0), Size2d(0,1)), box1.intersection(box2))

        
if __name__ == '__main__':
    unittest.main()