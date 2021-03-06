from Vector import Vect2

from ctypes import cdll
from ctypes import c_float, POINTER, c_int, byref
from ctypes import Structure

from contextlib import contextmanager

from math import atan2
from random import randint

voronoi_lib = cdll.LoadLibrary("./libvoronoi.so")

c_float_p = POINTER(c_float)
voronoi_lib.createVoronoi.argtypes = [c_float_p, c_float_p, c_int, c_float, c_float, c_float, c_float]


class Edge(Structure):
    _fields_ = [("id1", c_int),
                ("id2", c_int),
                ("x1", c_float),
                ("y1", c_float),
                ("x2", c_float),
                ("y2", c_float)]


class Voronoi:
    """ Class wich generate voronoi diagram from points set
        Adapter to C++ class
    """
    def __init__(self, point_list):
        self._points = point_list
        self._lines = {}
        self._neighbors = {}

        for p in self._points:
            self._lines[p] = []
            self._neighbors[p] = []

        with self.__init_voronoi(point_list) as voronoi_obj: # calculate diagram in c++ (voronoi_obj)
            # iterate all provided edges
            edge = Edge()
            while voronoi_lib.getNextEdge(voronoi_obj, byref(edge)):
                # get points near edge
                p1 = self._points[edge.id1] 
                p2 = self._points[edge.id2]
                # save line, wich represent edge
                line = (Vect2(edge.x1, edge.y1),
                        Vect2(edge.x2, edge.y2))
                self._lines[p1].append(line)
                self._lines[p2].append(line)
                # mark points near edge as neighbors
                self._neighbors[p1].append(edge.id2)
                self._neighbors[p2].append(edge.id1)

        self.__calc_points()

    def __calc_points(self):
        """ create representation of edges as polygone """
        self._line_points = {}
        for point, lines in self._lines.items():
            # find all points (with no repetition)
            point_set = set()
            for p1, p2 in lines:
                point_set.add(p1)
                point_set.add(p2)

            # get ordered list of points
            def angle(p):
                return atan2(p.y - point.y, p.x - point.x)
            self._line_points[point] = sorted(list(point_set), key=angle)

    @contextmanager
    def __init_voronoi(self, pointList):
        """ manage memory of C++ object wich generate voronoi diagram"""
        try:
            # init data and calculate diagram
            xList = [p.x for p in pointList]
            yList = [p.y for p in pointList]

            xList = (c_float * len(xList))(*xList)
            yList = (c_float * len(yList))(*yList)
            end = 1000000
            self.voronoi_obj = voronoi_lib.createVoronoi(xList, yList,
                                                         len(xList),
                                                         -end, end, -end, end)
            yield self.voronoi_obj
        finally:
            voronoi_lib.freeVoronoi(self.voronoi_obj)

    @staticmethod
    def __line_list(point_list):
        """ transform list of vect2 to list of float """
        l = []
        for point in point_list:
            l.append(point.x)
            l.append(point.y)

        return l


def random_voronoi(width, height, count):
    points = [Vect2(randint(0, width), randint(0, height)) for _ in range(count)]
    return Voronoi(points)

if __name__ == '__main__':
    random_voronoi(500, 500, 1000)
