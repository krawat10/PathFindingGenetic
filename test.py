import math
import random
import sys
from typing import List
from deap import base
from deap import creator
from deap import tools, algorithms
from Point import Point
from tools import Environment

env = Environment()
env.readJson('scen5.json')

# ------Przykladowe wykorzystanie------ #
print('Od', env.start)
print('Do', env.stop)
print('Przeszkody:', env.staticObstacles)

start_point = Point(env.start[0], env.start[1])
end_point = Point(env.stop[0], env.stop[1])


# ------  Przykładowa struktura  ------ #
class Path(list):
    """klasa stanowiaca przykladowy interfejs
       nie ma obowiazku korzystani z tej struktury
    """
    ABC = 9

    def __init__(self, *args):
        super().__init__(*args)
        self.env = env

    def getPoints(self) -> List[Point]:
        pass

    def plot(self):
        self.env.plot(self.getPoints())

    @staticmethod
    def __distanseBetweenLineAndPoint__(p1, p2, x):
        """obliczenie dystanus miedzy linią dana przez punkty p1 i p2
           a punktem x
        """
        pass

    def convert_to_foruma(self, p1: Point, p2: Point):
        y1 = p1.y
        y2 = p2.y
        x1 = p1.x
        x2 = p2.x

        A = y1 - y2
        B = x2 - x1
        C = x1 * y2 - y1 * x2

        return A, B, C

    def checkCollision(self, p1: Point, p2: Point, circle_point: Point, radius):
        a, b, c = p.convert_to_foruma(p1, p2)

        # Finding the distance of line
        # from center.
        try:
            dist = ((abs(a * circle_point.x + b * circle_point.y + c)) / math.sqrt(a * a + b * b))
        except:
            return sys.maxsize
        check_symbol_x = (p1.x - circle_point.x) * (p2.x - circle_point.x)

        # Checking if the distance is less
        # than, greater than or equal to radius.
        if radius >= dist:
            distance_between_points = p1.distance(p2)
            distance_between_p1_circle = p1.distance(circle_point) - radius
            distance_between_p2_circle = p2.distance(circle_point) - radius

            if (distance_between_points > distance_between_p1_circle) and (
                    distance_between_points > distance_between_p2_circle):
                return True

        return False

    def checkColission(self):
        pass

    def pathLength(self):
        pass


p = Path()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()


def uniform(low, up):
    return random.uniform(low, up)


BOUND_LOW, BOUND_UP = 0.0, 1.0

toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
DEATH_PENALTY = sys.maxsize


def evalOneMax(individual, present=False):
    first_point = Point(individual[0], individual[1])
    second_point = Point(individual[2], individual[3])

    for obstacle in env.staticObstacles:
        obstacle_point = Point(obstacle[0], obstacle[1])
        if p.checkCollision(start_point, first_point, obstacle_point, obstacle[2]):
            return (DEATH_PENALTY),

    for obstacle in env.staticObstacles:
        obstacle_point = Point(obstacle[0], obstacle[1])
        if p.checkCollision(first_point, second_point, obstacle_point, obstacle[2]):
            return (DEATH_PENALTY),

    for obstacle in env.staticObstacles:
        obstacle_point = Point(obstacle[0], obstacle[1])
        if p.checkCollision(second_point, end_point, obstacle_point, obstacle[2]):
            return (DEATH_PENALTY),

    distance = start_point.distance(first_point) + first_point.distance(second_point) + second_point.distance(end_point)

    return (distance),


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxSimulatedBinary, eta=0.3)
toolbox.register("mutate", tools.mutGaussian(), indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)
NGEN = 200

for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.3, mutpb=0.5)
    fits = toolbox.map(toolbox.evaluate, offspring)

    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

top1 = tools.selBest(population, k=1)

env.plot([[top1[0][0], top1[0][1]], [top1[0][2], top1[0][3]]])


# comment
