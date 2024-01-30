from __future__ import annotations

from collections.abc import Iterable, Sequence
import unittest

from pyutils import Size2d


class Size2dTest(unittest.TestCase):
    def setUp(self) -> None:
        self.size = Size2d(10, 20)
        
    def tearDown(self) -> None:
        del self.size
        
    def test_init(self):
        size = Size2d(10, 20)
        
        self.assertEqual(size.width, 10)
        self.assertEqual(size.height, 20)
        
    def test_from_expr(self):
        size = Size2d.from_expr("10.1x20.4")
        self.assertEqual(size.width, 10.1)
        self.assertEqual(size.height, 20.4)
        
        size = Size2d.from_expr((15, 17))
        self.assertEqual(size.width, 15)
        self.assertEqual(size.height, 17)
        
    def test_iter(self):
        self.assertTrue(isinstance(self.size, Iterable))
        _iter = iter(self.size)
        self.assertEqual(next(_iter), 10)
        self.assertEqual(next(_iter), 20)
        try:
            next(_iter)
            self.fail(f"StopIteration should have raised")
        except StopIteration:
            pass
        
    def test_len(self):
        self.assertTrue(isinstance(self.size, Sequence))
        self.assertEqual(len(self.size), 2)
        
    def test_getitem(self):
        self.assertTrue(isinstance(self.size, Sequence))
        self.assertEqual(10, self.size[0])
        self.assertEqual(20, self.size[1])
        
    def test_area(self):
        self.assertEqual(200, self.size.area())
        
    def test_aspect_ratio(self):
        self.assertEqual(0.5, self.size.aspect_ratio())
        
    def test_eq(self):
        size1 = Size2d.from_expr("3x5")
        size2 = Size2d.from_expr("3x5")
        self.assertEqual(size1, size2)
        
        size1 = Size2d.from_expr("3x5")
        size2 = Size2d.from_expr("3.0x5.0")
        self.assertEqual(size1, size2)
        
    def test_add(self):
        size1 = Size2d.from_expr("3x5")
        size2 = Size2d.from_expr("2x6")
        self.assertEqual(Size2d(5,11), size1+size2)     
        self.assertEqual(Size2d(5, 11), size1+(2,6))      
        self.assertEqual(Size2d(8, 10), size1+5)    
        self.assertEqual(Size2d(5.3, 7.3), size1+2.3)
        
    def test_sub(self):
        size1 = Size2d.from_expr("3x5")
        size2 = Size2d.from_expr("2x1")
        self.assertEqual(Size2d(1,4), size1-size2)     
        self.assertEqual(Size2d(1, -1), size1-(2,6))      
        self.assertEqual(Size2d(-2, 0), size1-5)    
        self.assertEqual(Size2d(0.7, 2.7), size1-2.3)
        
    def test_mul(self):
        size1 = Size2d.from_expr("3x5")
        size2 = Size2d.from_expr("2x1")
        self.assertEqual(Size2d(6,5), size1*size2)     
        self.assertEqual(Size2d(6, 30), size1*(2,6))      
        self.assertEqual(Size2d(15, 25), size1*5)    
        self.assertEqual(Size2d(4.5, 7.5), size1*1.5)
        
    def test_truediv(self):
        size1 = Size2d.from_expr("6x5")
        self.assertEqual(Size2d(2, 2.5), size1/Size2d(3, 2))     
        self.assertEqual(Size2d(2, 2.5), size1/(3,2))   
        self.assertEqual(Size2d(3, 2.5), size1/2)    
        self.assertEqual(Size2d(2, 5/3), size1/3)
        
    def test_to_int_tuple(self):
        size1 = Size2d.from_expr("6.3x5.2")
        self.assertEqual('6x5', str(size1.round()))
        self.assertEqual((6, 5), tuple(size1.round()))
        self.assertEqual([6, 5], list(size1.round()))

        
if __name__ == '__main__':
    unittest.main()
    # size = Size2d(10, 20)
    # print(size)