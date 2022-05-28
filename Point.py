import math


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point) -> float:
        return math.sqrt(pow(point.x - self.x, 2) + pow(point.y - self.y, 2))
