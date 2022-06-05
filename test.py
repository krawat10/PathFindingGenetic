import math
import random
import sys
from typing import List

import numpy as np
from deap import base
from deap import creator
from deap import tools, algorithms
from matplotlib import pyplot as plt

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

            if penalty <= 0:
                distance += (penalty * 500) ** 2  # external punishment function
            else:
                distance += 1 / (penalty * 1000) ** 2  # intrinsic punishment function

    return distance,


toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxSimulatedBinary, eta=0.3)
toolbox.register("mutate", tools.mutGaussian, indpb=0.05, mu=0, sigma=1)
toolbox.register("select", tools.selTournament, tournsize=3)

population_size = 300
population = toolbox.population(n=population_size)
NGEN = 500
gen_prices = []
best_diffs = []
avg_pop = []
best_pop = []
worst_diffs = []
best_individuals = []
best_individuals_count = 150

for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.3, mutpb=0.5)

    for best_individual_idx in range(len(best_individuals)):
        offspring[best_individual_idx] = best_individuals[best_individual_idx]


    fits = toolbox.map(toolbox.evaluate, offspring)
    costs = []

    best_price = sys.maxsize
    avg_price = 0
    worst_price = 0
    pop_count = 0
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
        cost = fit[0]
        costs.append(cost)
        if cost < 1000:
            avg_price += cost
            gen_prices.append(cost)
            if cost < best_price:
                best_price = cost
            if cost > worst_price:
                worst_price = cost
            pop_count += 1

    if pop_count > 0:
        avg_price /= pop_count
        avg_pop.append(avg_price)
        best_pop.append(best_price)
        best_diffs.append(abs(best_price - avg_price))
        worst_diffs.append(abs(worst_price - avg_price))

        if len(avg_pop) > 2 and abs(avg_pop[-1] - avg_pop[-2]) < 0.05:
            break

    idx_list = np.argpartition([cost for cost in costs], best_individuals_count)[:best_individuals_count]
    best_individuals = [offspring[idx] for idx in idx_list]

    population = toolbox.select(offspring, k=len(population))

top1 = tools.selBest(population, k=1)
j = evalOneMin(top1[0])
env.plot([[top1[0][0], top1[0][1]], [top1[0][2], top1[0][3]]])

# example data
ay = np.array(avg_pop)

# example error bar values that vary with x-position

fig, ax = plt.subplots()

# error bar values w/ different -/+ errors that
# also vary with the x-position

asymmetric_error = [np.array(best_diffs), np.array(worst_diffs)]

x = np.arange(0, len(avg_pop), 1)
ax.errorbar(x=x, y=ay, yerr=asymmetric_error, fmt='o')
ax.set_title(f'Best-Avg-Worst pop for {len(avg_pop)}, Best cost: {j[0]}')
# ax.set_yscale('log')
plt.show()

fig, ax = plt.subplots()
ax.errorbar(x=x, y=ay, yerr=asymmetric_error, fmt='o')
ax.set_title(f'Best-Avg-Worst pop for {len(avg_pop)}, Best cost: {j[0]}')
ax.set_yscale('log')
plt.show()
