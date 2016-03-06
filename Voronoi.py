from Vector import Vect2


class Point(Vect2):
    def __init__(self, x, y, color):
        Vect2.__init__(self, x, y)
        self.color = color


class Voronoi:

    def __init__(self, points):
        self._points = points
        self._lines = {}

        for p1 in points:
            self._lines[p1] = []
            for p2 in filter(lambda x: x is not p1, points):
                line = self.__sep_line(p1, p2)
                for p3 in filter(lambda x: x is not p1 and x is not p2, points):
                    if line is None:
                        break
                    line = self.__reduce_by_halfplane(p1, self.__sep_line(p1, p3), line)

                if line is not None:
                    self._lines[p1].append(line)


    @staticmethod
    def __sep_line(p1, p2):
        LIMIT = 1e8

        center = (p1 + p2) / 2
        norm = (p1 - p2).norm()

        return (center - norm*LIMIT, center + norm*LIMIT)


    @staticmethod
    def __reduce_by_halfplane(point, line, subject):
        p1, p2 = subject
        if Voronoi.__on_one_side(line, point, p1) and Voronoi.__on_one_side(line, point, p2):
            return subject
        elif Voronoi.__on_one_side(line, point, p1) != Voronoi.__on_one_side(line, point, p2):
            if Voronoi.__on_one_side(line, point, p2):
                p1, p2 = p2, p1

            # p1 and point on same halfplane, p2 on other
            return (p1, Voronoi._crossing(line, subject))
        else:
            return None
    
    @staticmethod
    def __on_one_side(line, p1, p2):
        line_begin, line_end = line
        norm = (line_end - line_begin).norm()

        def proj(point):
            return Vect2.dot(line_end - point, norm)

        return proj(p1) * proj(p2) >= 0

    @staticmethod
    def _crossing(line1, line2):
        l1p1, l1p2 = line1
        l2p1, l2p2 = line2
        
        cx = -l1p1.x + l2p1.x
        cy = -l1p1.y + l2p1.y

        x1 = (l1p2 - l1p1).x
        y1 = (l1p2 - l1p1).y

        x2 = (l2p2 - l2p1).x
        y2 = (l2p2 - l2p1).y

        t1 = (y2*cx - x2*cy) / (x1*y2 - x2*y1)

        return l1p1 + t1 * (l1p2 - l1p1)


def random_voronoi(width, height, count):
    from random import randint
    points = [Vect2(randint(0, width), randint(0, height)) for _ in range(count)]
    return Voronoi(points)


if __name__ == '__main__':
    random_voronoi(500, 500, 1000)

