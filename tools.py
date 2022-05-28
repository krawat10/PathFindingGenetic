import matplotlib.pyplot as plt
import numpy as np
import json


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
