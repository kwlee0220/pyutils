from __future__ import annotations

from collections.abc import Iterable, Sequence
import unittest
import math

from pyutils import Size2d, Point


class PointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pt = Point(10, 20)
        
    def tearDown(self) -> None:
        del self.pt
        
    def test_init(self):
        pt = Point(10, 20)
        self.assertEqual(pt.x, 10)
        self.assertEqual(pt.y, 20)
        
    def test_iter(self):
        self.assertTrue(isinstance(self.pt, Iterable))
        _iter = iter(self.pt)
        self.assertEqual(next(_iter), 10)
        self.assertEqual(next(_iter), 20)
        try:
            next(_iter)
            self.fail(f"StopIteration should have raised")
        except StopIteration:
            pass
        
    def test_len(self):
        self.assertTrue(isinstance(self.pt, Sequence))
        self.assertEqual(len(self.pt), 2)
        
    def test_getitem(self):
        self.assertTrue(isinstance(self.pt, Sequence))
        self.assertEqual(10, self.pt[0])
        self.assertEqual(20, self.pt[1])
        
    def test_norm(self):
        pt = Point(4, 3)
        self.assertEqual(5, pt.norm())
        
    def test_aspect_ratio(self):
        pt1 = Point(3, 9)
        pt2 = Point(6, 5)
        self.assertEqual(5, pt1.distance_to(pt2))
        
    def test_angle_between(self):
        pt1 = Point(7, 0)
        pt2 = Point(0, 5)
        self.assertAlmostEqual(math.radians(90), pt1.angle_between(pt2), places=7)
        
        pt2 = Point(3, 3)
        self.assertAlmostEqual(math.radians(45), pt1.angle_between(pt2), places=7)
        
    def test_line_function_to(self):
        pt1 = Point(0, 0)
        pt2 = Point(5, 0)
        func = pt1.line_function_to(pt2)
        self.assertEqual(0, func(1))
        self.assertEqual(0, func(2))
        
        pt2 = Point(5, 5)
        func = pt1.line_function_to(pt2)
        self.assertEqual(1, func(1))
        self.assertEqual(2, func(2))
        
    def test_split_points_to(self):
        pt1 = Point(0, 0)
        pt2 = Point(5, 5)
        pts = [tuple(pt.round()) for pt in pt1.split_points_to(pt2, 4)]
        self.assertEqual([(1,1), (2,2), (3,3), (4,4)], pts)
        
        pt2 = Point(-5, -5)
        pts = [tuple(pt.round()) for pt in pt1.split_points_to(pt2, 4)]
        self.assertEqual([(-1,-1), (-2,-2), (-3,-3), (-4,-4)], pts)
        
    def test_eq(self):
        size = Point(3, 5)
        self.assertEqual(size, Point(3, 5))
        self.assertEqual(size, Point(3.0, 5.0))
        
    def test_add(self):
        size1 = Point(3, 5)
        size2 = Point(2, 6)
        self.assertEqual(Point(5, 11), size1+size2)     
        self.assertEqual(Point(5, 11), size1+(2,6))      
        self.assertEqual(Point(8, 10), size1+5)    
        self.assertEqual(Point(5.3, 7.3), size1+2.3)
        
    def test_sub(self):
        pt1 = Point(3, 5)
        pt2 = Point(2, 1)
        self.assertEqual(Size2d(1, 4), pt1-pt2)     
        self.assertEqual(Point(1, -1), pt1-(2,6))      
        self.assertEqual(Point(-2, 0), pt1-5)    
        self.assertEqual(Point(0.7, 2.7), pt1-2.3)
        
    def test_mul(self):
        pt = Point(3, 5)
        size2 = Size2d(2, 1)
        self.assertEqual(Point(6, 5), pt*size2)     
        self.assertEqual(Point(6, 30), pt*(2,6))      
        self.assertEqual(Point(15, 25), pt*5)    
        self.assertEqual(Point(4.5, 7.5), pt*1.5)
        
    def test_truediv(self):
        pt = Point(6, 5)
        self.assertEqual(Point(2, 2.5), pt/Size2d(3, 2))     
        self.assertEqual(Point(2, 2.5), pt/(3,2))   
        self.assertEqual(Point(3, 2.5), pt/2)    
        self.assertEqual(Point(2, 5/3), pt/3)
        
    def test_round(self):
        pt = Point(6.3, 5.2)
        self.assertEqual('(6,5)', str(pt.round()))
        self.assertEqual((6, 5), tuple(pt.round()))
        self.assertEqual([6, 5], list(pt.round()))

        
if __name__ == '__main__':
    unittest.main()