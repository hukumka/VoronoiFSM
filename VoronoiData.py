from Vector import Vect2
from math import atan2
from random import randint


class Cell(Vect2):
    def __init__(self, x, y):
        Vect2.__init__(self, x, y)
        self.neighbors = []
        self.polygone = []
        self.state = None


def standart_generator(cell):
    if randint(1, 4) == 1:
        return 1
    else:
        return 0


class VoronoiData:
    def __init__(self, voronoi):
        self._points = [Cell(i.x, i.y) for i in voronoi._points]

        for point in self._points:
            self._set_neighbors(point, voronoi)
            self._set_lines(point, voronoi)

        self.generate_state()

    def _set_neighbors(self, point, voronoi):
        neighbors = voronoi._neighbors[point]
        for neighbor_id in neighbors:
            neighbor = self._points[neighbor_id]
            point.neighbors.append(neighbor)

    def _set_lines(self, point, voronoi):
        point_set = set()
        for p1, p2 in voronoi._lines[point]:
            point_set.add(p1)
            point_set.add(p2)

        def angle(p):
            return atan2(p.y - point.y, p.x - point.x)
        point.polygone = sorted(list(point_set), key=angle)


    def generate_state(self, state_generator=standart_generator):
        for cell in self._points:
            cell.state = state_generator(cell)

    def update(self, rule):
        for cell in self._points:
            cell._new_state = rule(cell)

        for cell in self._points:
            cell.state = cell._new_state
    
    
    def change_closest(self, x, y):
        point = self.find_closest(x, y)
        point.state += 1
        point.state %= 3

    def find_closest(self, x, y):
        # naive
        vect = Vect2(x, y)
        dppi = ((abs(vect - p), p) for p in self._points)
        return min(dppi, key=lambda x: x[0])[1]


