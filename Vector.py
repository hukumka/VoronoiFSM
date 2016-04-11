import math


class Vect2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vect2(-self.x, -self.y)

    def __abs__(self):
        return (self.x*self.x + self.y*self.y)**0.5

    def __add__(self, other):
        return Vect2(self.x + other.x, self.y + other.y)

    __iadd__ = __add__

    def __sub__(self, other):
        return Vect2(self.x - other.x, self.y - other.y)

    __isub__ = __sub__

    def __mul__(self, mul):
        return Vect2(self.x * mul, self.y * mul)

    __imul__ = __rmul__ = __mul__

    def __truediv__(self, mul):
        return Vect2(self.x / mul, self.y / mul)

    __itruediv__ = __truediv__

    def __repr__(self):
        return "v2({}, {})".format(self.x, self.y)

    def norm(self):
        return Vect2(self.y, -self.x) / abs(self)

    def __hash__(self):
        return hash((self.x, self.y))


    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __eq__(self, other):
        accuracy = 1e-5
        return abs(self - other) <= accuracy

    def __lt__(self, other):
        if self.x == other.x:
            return self.y <= other.y
        else:
            return self.x <= other.x



if __name__ == '__main__':
    v1 = Vect2(1, 2)
    v2 = Vect2(3, 4)
    print(v1 + v2)
    print(v1 * v2)
    print(v1 * 1.5)
    print(-v2 / 2)
    print(-v1 - v2)
    v1 += v2
    print(v1)
    print(Vect2(4, 3).norm())

