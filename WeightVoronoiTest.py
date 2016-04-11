import unittest

from random import randint
import math

from Vector import Vect2
from WeightVoronoi import *


class WeightVoronoiTest(unittest.TestCase):
    def test_two_equal(self):
        p1 = WeightPoint(0, 0, 1)
        p2 = WeightPoint(0, 2, 1)
        v = Voronoi([p1, p2])
        
        borders_count = len(v.points[0].borders)
        self.assertEqual(borders_count, 1)

        border = v.points[0].borders[0]
        self.assertIsInstance(border, Line)

        self.assertEqual(border.p1, Vect2(10000, 1))
        self.assertEqual(border.p2, Vect2(-10000, 1))


    def test_several_equals(self):
        p1 = WeightPoint(0, 0, 1)
        p2 = WeightPoint(0, 2, 1)
        p3 = WeightPoint(2, 2, 1)
        v = Voronoi([p1, p2, p3])
        for point in v.points:
            self.assertEqual(len(point.borders), 2)

        border1 = v.points[0].borders[0]
        point = border1._point(border1.parts[0][0])
        self.assertEqual(point, Vect2(1, 1))
 

def rand_point():
    return Vect2(randint(-100, 100), randint(-100, 100))

class LineTest(unittest.TestCase):
    def test_intersection(self):
        l1 = Line(None, None, Vect2(0, 1), Vect2(0, 0))
        l2 = Line(None, None, Vect2(1, 0), Vect2(0, 0))

        x = intersection_line_line(l1, l2)
        self.assertEqual(x, [Vect2(0, 0)])

    def test_intersection_second(self):
        l1 = Line(None, None, Vect2(1, -1000), Vect2(1, 1000))
        l2 = Line(None, None, Vect2(-100, 102), Vect2(100, -98))

        x = intersection_line_line(l1, l2)
        self.assertEqual(x, [Vect2(1, 1)])

    def test_symmetry_simple(self):
        l1 = Line(None, None, Vect2(-10, -10), Vect2(50, 0))
        l2 = Line(None, None, Vect2(50, 0), Vect2(-10, -10))
        l3 = Line(None, None, Vect2(100, 0), Vect2(10, 0))

        i1 = intersection_points(l1, l3)
        i2 = intersection_points(l2, l3)
        self.assertEqual(i1, i2)

    def test_intersection_symmetry(self):
        for _ in range(1000):
            p1, p2 = rand_point(), rand_point()
            l1 = Line(None, None, p1, p2)
            l2 = Line(None, None, p2, p1)
            l3 = Line(None, None, rand_point(), rand_point())

            i1 = intersection_points(l1, l3)
            i2 = intersection_points(l2, l3)
            i3 = intersection_points(l3, l1)
            i4 = intersection_points(l3, l2)

            self.assertEqual(i1, i2)
            self.assertEqual(i1, i3)
            self.assertEqual(i1, i4)

    def test_on_one_side(self):
        p1 = Vect2(0, 0)
        p2 = Vect2(2, 0)
        line = Line(p1, p2, Vect2(1, -1), Vect2(1, 1))
        self.assertTrue(line.contain(p1))
        self.assertFalse(line.contain(p2))


class ArcTest(unittest.TestCase):
    def test_intersection(self):
        a1 = Arc(None, None, Vect2(0, 0), 2)
        a2 = Arc(None, None, Vect2(2, 0), 2)
        i1 = intersection_points(a1, a2)

        expect = [Vect2(1, -2*math.sin(math.pi/3)),
                  Vect2(1, 2*math.sin(math.pi/3))]
        self.assertEqual(i1, expect)


    def test_symmetry_simple(self):
        a1 = Arc(None, None, Vect2(0, 0), 2)
        a2 = Arc(None, None, Vect2(2, 0), 3)

        l1 = sorted(intersection_points(a1, a2))
        l2 = sorted(intersection_points(a2, a1))
        self.assertEqual(l1, l2)



    def test_symmetry(self):
        def random_arc():
            center = rand_point()
            radius = randint(1, 50)
            return Arc(None, None, center, radius)

        for _ in range(10000):
            a1 = random_arc()
            a2 = random_arc()

            l1 = sorted(intersection_points(a1, a2))
            l2 = sorted(intersection_points(a2, a1))

            self.assertEqual(l1, l2)


if __name__ == '__main__':
    unittest.main()
