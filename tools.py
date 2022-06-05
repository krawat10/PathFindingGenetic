import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import json

from Point import Point


def readJson(obj):
    def read(obj, fileName):
        with open(fileName, "r") as read_file:
            data = json.load(read_file)
        for element in data:
            function = list(element.keys())[0]
            if function in ['addCircle', 'setStart', 'setStop', 'addLine']:
                getattr(obj, function)(*element[function])
        return

    obj.readJson = read
    return obj


def convert_to_foruma(p1: Point, p2: Point):
    y1 = p1.y
    y2 = p2.y
    x1 = p1.x
    x2 = p2.x

    A = y1 - y2
    B = x2 - x1
    C = x1 * y2 - y1 * x2

    return A, B, C


def check_collision(p1: Point, p2: Point, circle_point: Point, radius) -> float:
    a, b, c = convert_to_foruma(p1, p2)

    # Finding the distance of line
    # from center.
    try:
        dist = ((abs(a * circle_point.x + b * circle_point.y + c)) / math.sqrt(a * a + b * b))
    except:
        return -sys.maxsize

    # Checking if the distance is less
    # than, greater than or equal to radius.
    if radius >= dist:
        distance_between_points = p1.distance(p2)
        distance_between_p1_circle = p1.distance(circle_point) - radius
        distance_between_p2_circle = p2.distance(circle_point) - radius

        if (distance_between_points > distance_between_p1_circle) and (
                distance_between_points > distance_between_p2_circle):
            return -abs(radius - dist)

    return abs(radius - dist)


@readJson
class Environment(object):
    """klasa przedstawijaca srodowisko
       przyklad uzycia:
       env = Environment()
       env.readJson('scen2.json')
       print(env.staticObstacles)
       env.plot([[0.8, 0.1], [0.8, 0.5]])
    """

    def __init__(self):
        super(Environment, self).__init__()
        self.regionSize = [1, 1]
        self.staticObstacles = set()

    def addCircle(self, x, y, r):
        self.staticObstacles.add((x, y, r))

    def addLine(self, p1, p2, r=0.01, d=0.015):
        nr = np.ceil(np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) / d)
        nr = int(nr)
        x = np.linspace(p1[0], p2[0], num=nr)
        y = np.linspace(p1[1], p2[1], num=nr)
        for px, py in zip(x, y):
            self.addCircle(px, py, r)

    def setStart(self, x, y):
        self.start = (x, y)

    def setStop(self, x, y):
        self.stop = (x, y)

    def plot(self, wayPionts=[]):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'box')
        plt.axis([0, self.regionSize[0], 0, self.regionSize[1]])
        for obj in self.staticObstacles:
            circle = plt.Circle((obj[0], obj[1]), obj[2], color='black')
            ax.add_artist(circle)
        circle = plt.Circle((self.start[0], self.start[1]), 0.01, color='blue')
        ax.add_artist(circle)
        circle = plt.Circle((self.stop[0], self.stop[1]), 0.01, color='green')
        ax.add_artist(circle)
        x = [self.start[0]]
        y = [self.start[1]]
        for point in wayPionts:
            x.append(point[0])
            y.append(point[1])
        x.append(self.stop[0])
        y.append(self.stop[1])
        plt.plot(x, y)
        plt.plot(x[1:-1], y[1:-1], 'rx')
        plt.show()
