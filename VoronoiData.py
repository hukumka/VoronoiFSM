from VoronoiCWrap import Voronoi


class Cell(Vect2):
    def __init__(self, x, y):
        Vect2.__init__(self, x, y)
        self.neighbors = []
        self.lines = []
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
            self.set_neighbors(point, voronoi)
            self.set_lines(point, voronoi)

    def _set_neighbors(self, point, voronoi):
        neighbors = voronoi._neighbors[point]
        for neighbor_id in neighbors:
            neighbor = self._points[neighbor_id]
            point.neighbors.append(neighbor)

    def _set_lines(self, point, voronoi):
        point.lines = voronoi._lines[point]

    def generate_state(self, state_generator=standart_generator):
        for cell in self._points:
            cell.state = state_generator(cell)

    def update(self, rule):
        for cell in self._points:
            cell._new_state = rule(cell)

        for cell in self._points:
            cell.state = cell._new_state
