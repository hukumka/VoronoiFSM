from Vector import Vect2

from ctypes import cdll
from ctypes import c_double

voronoi_lib = cdll.LoadLibrary("./libvoronoi.so")


voronoi_lib.getLineP1X.restype = c_double
voronoi_lib.getLineP1Y.restype = c_double
voronoi_lib.getLineP2X.restype = c_double
voronoi_lib.getLineP2Y.restype = c_double


from contextlib import contextmanager

from math import atan2
from random import randint

from Rule import rule


class Voronoi:
    def __init__(self, point_list):
        self._points = point_list
        self._lines = {}
        self._neighbors = {}

        with self.__init_voronoi(point_list) as voronoi_obj:
            for i, point in enumerate(point_list):
                self._lines[point] = []
                # load lines
                line_count = voronoi_lib.getLinesCount(voronoi_obj, i)
                for j in range(line_count):
                    p1x = voronoi_lib.getLineP1X(voronoi_obj, i, j);
                    p1y = voronoi_lib.getLineP1Y(voronoi_obj, i, j);
                    p2x = voronoi_lib.getLineP2X(voronoi_obj, i, j);
                    p2y = voronoi_lib.getLineP2Y(voronoi_obj, i, j);
                
                    p1 = Vect2(p1x, p1y)
                    p2 = Vect2(p2x, p2y)

                    self._lines[point].append((p1, p2))
                # load neighbors
                self._neighbors[point] = []
                neighbors_count = voronoi_lib.getNeighborsCount(voronoi_obj, i)
                for j in range(neighbors_count):
                    neighbor_point = point_list[voronoi_lib.getNeighbor(voronoi_obj, i, j)]
                    self._neighbors[point].append(neighbor_point)

        self.__calc_points();
        self._state = {}
        self._swap_state = {}
        for p, _ in self._neighbors.items():
            self._state[p] = randint(0, 1)*randint(0, 1)

    def __calc_points(self):
        self._line_points = {}
        for point, lines in self._lines.items():
            point_set = set()
            for p1, p2 in lines:
                point_set.add(p1)
                point_set.add(p2)

            def angle(p):
                return atan2(p.y - point.y, p.x - point.x)
            self._line_points[point] = sorted(list(point_set), key=angle)

    def update(self):
        for point, n in self._neighbors.items():
            neighbors = [self._state[p] for p in n]
            state = self._state[point]
            self._swap_state[point] = rule(state, neighbors)

        self._swap_state, self._state = self._state, self._swap_state


    def get_color(self, point):
        colors = [[0, 0, 0],
                  [1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 0],
                  [0, 1, 1],
                  [1, 0, 1]]
        return colors[self._state[point]]


    @contextmanager
    def __init_voronoi(self, point_list):
        try:
            arr = self.__line_list(point_list)
            carr = (c_double * len(arr))(*arr)
            self.voronoi_obj = voronoi_lib.generateVoronoi(carr, len(point_list))
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

    def change_closest(self, x, y):
        point = self.find_closest(x, y)
        self._state[point] += 1
        self._state[point] %= 3

    def find_closest(self, x, y):
        # naive
        vect = Vect2(x, y)
        dppi = ((abs(vect - p), p) for p in self._points)
        return min(dppi, key=lambda x: x[0])[1]



def random_voronoi(width, height, count):
    points = [Vect2(randint(0, width), randint(0, height)) for _ in range(count)]
    return Voronoi(points)

if __name__ == '__main__':
    random_voronoi(500, 500, 1000)
