from __future__ import annotations

import math
from random import gauss


class Vector:
    def __init__(self, x1: float, y1: float, x2: float = None, y2: float = None):
        if (x2 is not None) and (y2 is not None):
            x = (x1 - x2)
            y = (y1 - y2)
        else:
            x = x1
            y = y1
        self.dir = [x, y]

    def normalize(self) -> Vector:
        length = self.magnitude()
        if length == 0:
            return Vector(0, 0)
        else:
            return Vector(self.dir[0] / length, self.dir[1] / length)

    def magnitude(self) -> float:
        return math.sqrt(self.dir[1] ** 2 + self.dir[0] ** 2)

    def multiply(self, magnitude) -> Vector:
        return Vector(self.dir[0] * magnitude, self.dir[1] * magnitude)

    def get_tuple(self) -> tuple:
        tup: tuple = (self.dir[0], self.dir[1])
        return tup

    def rotate(self, radians, clockwise=False):
        if clockwise:
            radians = - radians
        x = self.dir[0] * math.cos(radians) - self.dir[1] * math.sin(radians)
        y = self.dir[0] * math.sin(radians) + self.dir[1] * math.cos(radians)
        return Vector(x, y)

    def flip(self):
        return self.multiply(-1)

    def add(self, vector2: Vector) -> Vector:
        return Vector(self.dir[0] + vector2.dir[0], self.dir[1] + vector2.dir[1])

    def angle(self):
        origin = Vector(1,0)
        if self.dir[0] == 0:
            return 0
        dot = self.dir[0] * origin.dir[0] + self.dir[1] * origin.dir[1]  # dot product between [x1, y1] and [x2, y2]
        det = self.dir[0] * origin.dir[1] - origin.dir[0] * self.dir[1]  # determinant
        angle = math.atan2(det, dot)
        return angle

    def cross(self, v: Vector):
        cross = self.dir[0] * v.dir[1] - v.dir[0] * self.dir[1]
        return cross

    def clamp(self, magnitude):
        if self.magnitude() > magnitude:
            return self.normalize().multiply(magnitude)
        else:
            return self


def a_is_right_of_b(v1: Vector, v2: Vector) -> int:
    cross = v1.dir[0] * v2.dir[1] - v2.dir[0] * v1.dir[1]
    if cross > 0:
        return -1
    elif cross == 0:
        return 0
    else:
        return 1


def make_rand_unit_vector():
    dims = 2
    vec = [gauss(0, 1) for i in range(dims)]
    mag = sum(x ** 2 for x in vec) ** .5
    return Vector(vec[0] / mag, vec[1] / mag)


def get_distance_from_a_to_b(pos1: tuple, pos2: tuple) -> float:
    return math.sqrt((pos2[1] - pos1[1]) ** 2 + (pos2[0] - pos1[0]) ** 2)


def cap_vector(vector: Vector, magnitude) -> Vector:
    if vector.get_length() > magnitude:
        new_vector = vector.normalize().multiply(magnitude)
        return new_vector
    else:
        return vector
