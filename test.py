import math
import random
import sys
from typing import List
from deap import base
from deap import creator
from deap import tools, algorithms
from Point import Point
from tools import Environment, check_collision

env = Environment()
env.readJson('scen5.json')

# ------Przykladowe wykorzystanie------ #
print('Od', env.start)
print('Do', env.stop)
print('Przeszkody:', env.staticObstacles)
start_point = Point(env.start[0], env.start[1])
end_point = Point(env.stop[0], env.stop[1])

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


def evalOneMin(individual):
    path_points = [start_point]
    distance = 0

    for i in range(int(len(individual) / 2)):
        path_points.append(Point(individual[i * 2], individual[i * 2 + 1]))

    path_points.append(end_point)

    if any([not point.in_range() for point in path_points]):
        return DEATH_PENALTY,

    for i in range(len(path_points) - 1):
        distance += path_points[i].distance(path_points[i + 1])
        for obstacle in env.staticObstacles:
            obstacle_point = Point(obstacle[0], obstacle[1])
            penalty = check_collision(path_points[i], path_points[i + 1], obstacle_point, obstacle[2])
            if penalty != 0:
                distance += (penalty * 500) ** 2

    return distance,


toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxSimulatedBinary, eta=0.3)
toolbox.register("mutate", tools.mutGaussian, indpb=0.05, mu=0, sigma=1)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)
NGEN = 400

for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.3, mutpb=0.5)
    fits = toolbox.map(toolbox.evaluate, offspring)

    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

top1 = tools.selBest(population, k=1)

env.plot([[top1[0][0], top1[0][1]], [top1[0][2], top1[0][3]]])
