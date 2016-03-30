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
    """Sturucture wich contains data about voronoi diagram as finite state machine"""
    def __init__(self, voronoi):
        """
        Init data

        voronoi - object wich has interface such as Voronoi(from Voronoi.py)
        """
        self._points = [Cell(i.x, i.y) for i in voronoi._points]

        for point in self._points:
            self.__set_neighbors(point, voronoi)
            self.__set_lines(point, voronoi)

        self.__rule = None
        self.__precalculations = None
        self.generate_state()

    def __set_neighbors(self, point, voronoi):
        neighbors = voronoi._neighbors[point]
        for neighbor_id in neighbors:
            neighbor = self._points[neighbor_id]
            point.neighbors.append(neighbor)

    def __set_lines(self, point, voronoi):
        point_set = set()
        for p1, p2 in voronoi._lines[point]:
            point_set.add(p1)
            point_set.add(p2)

        def angle(p):
            return atan2(p.y - point.y, p.x - point.x)
        point.polygone = sorted(list(point_set), key=angle)

    def generate_state(self, state_generator=standart_generator):
        """Initialize state of each cell using generator"""
        for cell in self._points:
            cell.state = state_generator(cell)

    def bind_rule(self, rule):
        """Set default rule"""
        self.__rule = rule

    def bind_precalculations(self, precalculations):
        """Set default list of precalculations"""
        self.__precalculations = precalculations

    def update(self, rule=None, precalculations=None):
        """
        Recalculate state of each cell according to rule
        
        rule - rule to calculate state, default value set by bind_rule
        precalculations - list(iterable) of functions needed by rule to be calculated, default value bind by bind_precalculations
        """
        #  init default args
        if rule is None:
            rule = self.__rule
        if precalculations is None:
            precalculations = self.__precalculations

        #  do stuff
        for precalc in precalculations:
            for cell in self._points:
                precalc(cell)

        # calculate state
        for cell in self._points:
            cell._new_state = rule(cell)

        # update state
        for cell in self._points:
            cell.state = cell._new_state

    def change_closest(self, x, y):
        """Change state of cell containing given point"""
        point = self.find_closest(x, y)
        point.state += 1
        point.state %= 3

    def find_closest(self, x, y):
        """Find cell containing given point"""
        # naive
        vect = Vect2(x, y)
        dppi = ((abs(vect - p), p) for p in self._points)
        return min(dppi, key=lambda x: x[0])[1]
