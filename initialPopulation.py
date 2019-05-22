from visibilityPoly import *
import random


def generate_initial_population(poly):
    n = len(poly.vertices)
    population = []

    while len(population) != 6:
        individual = []
        for i in range(0,n):
            r = random.randint(0,1)
            individual.append(r)

        if (valid_coverage(poly, individual)):
            population.append(individual)

    return population
