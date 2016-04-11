import math
from Vector import Vect2


class WeightPoint(Vect2):
    def __init__(self, x, y, weight):
        Vect2.__init__(self, x, y)
        self.weight = weight


class Domain:
    def __init__(self, inner_point, other_point):
        self.inner_point = inner_point
        self.other_point = other_point
        self.parts = []

    def intersect(self, other):
        intersections = intersection_points(self, other)
        intersections_values = list(sorted((self._value(p) for p in intersections)))
        self._split_parts(intersections_values)
        self._choose_parts(other)

    def _split_parts(self, value_list):
        for value in value_list:
            self._split_with_value(value)

    def _split_with_value(self, value):
        def find_range():
            for i, (begin, end) in enumerate(self.parts):
                if begin < value < end:
                    return i
            return None

        range_id = find_range()
        if range_id is not None:
            begin, end = self.parts[range_id]
            self.parts[range_id] = (begin, value)
            self.parts.insert(range_id + 1, (value, end))

    def _choose_parts(self, other):
        def is_inside(part):
            b, e = part
            center = self._point((b + e)/2)
            return other.contain(center)
        
        self.parts = [part for part in self.parts if is_inside(part)]


class Arc(Domain):
    SEGMENTS_ON_ARC = 200
    def __init__(self, inner_point, other_point, center, radius):
        Domain.__init__(self, inner_point, other_point)
        self.center = center
        self.radius = radius
        self.parts = [(0, 2*math.pi)]

    def _value(self, point):
        """ returns angle, with determines ray from center, containing provided point """
        direction = point - self.center
        angle = math.atan2(direction.y, direction.x)
        if angle < 0:
            angle += math.pi * 2
        return angle

    def _point(self, angle):
        """ returns point on arc on selected angle """
        return Vect2(math.cos(angle), math.sin(angle)) * self.radius + self.center

    def contain(self, point):
        return self.__circle_contain(point) == self.__circle_contain(self.inner_point)

    def __circle_contain(self, point):
        return abs(self.center - point) <= self.radius

    def lines(self):
        for part in self.parts:
            for line in self.__part_lines(part):
                yield line

    def __part_lines(self, part):
        start, end = part
        for i in range(self.SEGMENTS_ON_ARC):
            l1 = start + (end - start) * i / self.SEGMENTS_ON_ARC
            l2 = start + (end - start) * (i + 1) / self.SEGMENTS_ON_ARC
            yield self._point(l1), self._point(l2)


class Line(Domain):
    def __init__(self, inner_point, other_point, p1, p2):
        Domain.__init__(self, inner_point, other_point)
        self.p1 = p1
        self.p2 = p2
        self.parts = [(0, 1)]

    def contain(self, point):
        return self.__positive_halfplane(point) == self.__positive_halfplane(self.inner_point)

    def __positive_halfplane(self, point):
        return Vect2.dot(self.norm(), point - self.p1) >= 0

    def _value(self, point):  # return position on cut [p1, p2] there p1 on 0 and p2 on 1
        direction = self.p2 - self.p1
        return Vect2.dot(direction, point - self.p1) / abs(direction)**2

    def _point(self, value):
        return self.p1 + (self.p2 - self.p1) * value

    def norm(self):
        return (self.p1 - self.p2).norm()

    def shortest_vect_from(self, point):
        return Vect2.dot(self.p1 - point, self.norm()) * self.norm()
    
    def lines(self):
        for start, end in self.parts:
            print(self._point(start), self._point(end))
            yield self._point(start), self._point(end)

def intersection_points(d1, d2):
    if isinstance(d1, Arc) and isinstance(d2, Arc):
        return intersection_arc_arc(d1, d2)
    elif isinstance(d1, Arc) and isinstance(d2, Line):
        return intersection_arc_line(d1, d2)
    elif isinstance(d1, Line) and isinstance(d2, Arc):
        return intersection_arc_line(d2, d1)
    else:
        return intersection_line_line(d1, d2)


def intersection_arc_arc(arc1, arc2):
    distance = abs(arc1.center - arc2.center)
    if distance < arc1.radius + arc2.radius and distance > abs(arc1.radius - arc2.radius):  # i do not care about signle common point
        a = (arc1.radius**2 - arc2.radius**2 + distance**2) / (2*distance)
        p0 = arc1.center + a/distance * (arc2.center - arc1.center)

        h = math.sqrt(arc1.radius**2 - a**2)

        norm = (arc2.center - arc1.center).norm()

        p1 = p0 + norm*h
        p2 = p0 - norm*h
        return [p1, p2]
    else:
        return []


def intersection_arc_line(arc, line):
    vect = line.shortest_vect_from(arc.center)
    h = abs(vect)
    if h < arc.radius:
        a = math.sqrt(arc.radius**2 - h**2)
        p1 = arc.center + vect + a * vect.norm()
        p2 = arc.center + vect - a * vect.norm()
        return [p1, p2]
    else:
        return []


def intersection_line_line(line1, line2):
    det = (line1.p1.x - line1.p2.x)*(line2.p1.y - line2.p2.y) \
            - (line1.p1.y - line1.p2.y)*(line2.p1.x - line2.p2.x)

    if det == 0:
        return []
    else:
        d1 = line1.p1.x*line1.p2.y - line1.p1.y*line1.p2.x
        d2 = line2.p1.x*line2.p2.y - line2.p1.y*line2.p2.x
        
        x = (d1 * (line2.p1.x - line2.p2.x) - d2 * (line1.p1.x - line1.p2.x)) / det
        y = (d1 * (line2.p1.y - line2.p2.y) - d2 * (line1.p1.y - line1.p2.y)) / det
        return [Vect2(x, y)]


def build_domain(p1, p2):
    if p1.weight == p2.weight:
        return line_beetwen_point(p1, p2)
    else:
        return circle_beetween(p1, p2)


def line_beetwen_point(p1, p2):
    norm = (p2 - p1).norm()
    
    center = (p1 + p2) * 0.5
    start = center + 10000 * norm
    end = center - 10000 * norm
    return Line(p1, p2, start, end)


def circle_beetween(p1, p2):
    k = p2.weight/p1.weight
    i1 = p1 + (p2 - p1) / (1 + k)
    i2 = p1 + (p2 - p1) / (1 - k)
    center = (i1 + i2) / 2
    radius = abs(i1 - i2) / 2
    return Arc(p1, p2, center, radius)


class Voronoi:
    def __init__(self, points):
        self.points = points[:]
        for p1 in self.points:
            p1.borders = []
            p1.neighbors = []
            for p2 in self.__points_except(p1):
                border = self.__find_actual_border(p1, p2)
                if border is not None:
                    p1.borders.append(border)
                    p1.neighbors.append(p2)

    def __points_except(self, *points):
            return (p for p in self.points if p not in points)
    
    def __find_actual_border(self, point, other_point):
        border = build_domain(point, other_point)
        for p3 in self.__points_except(point, other_point):
            border.intersect(build_domain(point, p3))
            if not border.parts:
                return None
        
        return border
