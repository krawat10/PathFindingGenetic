import math

MAX_X = 1.0
MIN_X = 0.0
MAX_Y = 1.0
MIN_Y = 0.0


class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point) -> float:
        return math.sqrt(pow(point.x - self.x, 2) + pow(point.y - self.y, 2))

    def in_range(self):
        return MIN_X < self.x < MAX_X and MIN_Y < self.y < MAX_Y
