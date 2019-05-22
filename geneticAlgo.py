from initialPopulation import *
from visibilityPoly import *
from visibilityPoly import Polygon as polygon_vis
from operator import itemgetter
from drawProcess import *


points = [(244, 302), (303, 256), (387, 320), (437, 248), (517, 164), (586, 213), (533, 325), (544, 329), (594, 330), (612, 348), (559, 366), (579, 430), (519, 457), (548, 566), (470, 492), (448, 579), (445, 585), (417, 571), (415, 636), (372, 471), (309, 574), (305, 540), (287, 533), (284, 535), (175, 586), (265, 488), (215, 438), (77, 433), (207, 386), (169, 303)]
#points = [(217, 534), (240, 425), (209, 392), (355, 331), (419, 229), (504, 216), (608, 220), (639, 248), (718, 197), (734, 243), (835, 328), (897, 386), (981, 392), (933, 561), (1046, 700), (984, 746), (944, 824), (895, 880), (813, 943), (700, 999), (558, 1024), (522, 955), (390, 925), (375, 896), (313, 912), (226, 805), (246, 677), (209, 683), (271, 663), (179, 631)]
#points = [(980, 190), (954, 301), (935, 340), (1037, 358), (1003, 460), (841, 561), (1312, 600), (1100, 624), (1063, 667), (1033, 740), (1176, 894), (952, 846), (877, 817), (989, 931), (697, 722), (800, 984), (763, 1013), (705, 1127), (682, 1033), (615, 1116), (603, 946), (600, 865), (541, 988), (436, 1083), (349, 1117), (424, 934), (309, 995), (463, 745), (255, 877), (428, 723), (244, 803), (145, 835), (291, 747), (0, 779), (78, 723), (253, 664), (-41, 639), (380, 591), (160, 495), (308, 467), (253, 440), (229, 337), (327, 400), (80, 100), (306, 316), (340, 274), (472, 419), (293, 73), (432, 214), (454, 162), (504, 17), (590, 530), (581, 276), (602, 314), (602, 327), (632, 303), (766, 77), (862, 39), (824, 161), (791, 356)]


def convert_poly_points(points):
    poly = []
    for point in points:
        formatted_point = Pt(point[0],point[1])
        poly.append(formatted_point)

    return polygon_vis(poly, clockwise=True)


def fitness_func(individual):
    guards_count = 0
    vertice_count = len(individual)

    # Check if individual is a valid guard set
    if not valid_coverage(convert_poly_points(points), individual):
        return 0.1

    # Check how many guards are in guard set
    for vertice in individual:
        if vertice == 1:
            guards_count += 1

    return float(vertice_count) / float(guards_count)


def roulette_wheel_selection(population):
    # Select parents for recombination respective to the fitness value of each individual
    roulette_max = sum(individual['fValue'] for individual in population)
    picker = random.uniform(0, roulette_max)
    current = 0
    for individual in population:
        current += individual['fValue']
        if current > picker:
            return individual


def two_point_crossover(parent_one, parent_two):
    length = len(parent_one)

    # Select two random numbers for the cut positions of the crossover operation
    cross_point_one = random.randint(0, length)
    cross_point_two = random.randint(0, length)

    # Switch cross positions, so that point one has the smaller value
    if cross_point_one >= cross_point_two:
        cross_point_one, cross_point_two = cross_point_two, cross_point_one

    # Cut parts of both parents according to random cross points
    first_part = parent_one[0:cross_point_one]
    second_part = parent_two[cross_point_one:cross_point_two]
    third_part = parent_one[cross_point_two:length]

    individual = first_part + second_part + third_part

    return individual


def mutation(individual):
    # Static mutation rate value
    mutation_rate = 0.2

    # Mutate bits of individual, if random number is smaller than mutation rate
    for i in range(0, len(individual)):
        if (random.random() <= mutation_rate):
            if individual[i] == 1:
                individual[i] = 0
            else:
                individual[i] = 1

    return individual


def genetic_algorithm():
    generation = 0

    # Generate initial population
    poly = convert_poly_points(points)
    print(poly)
    population = generate_initial_population(poly)

    # Count vertice in considered polygon
    vertice_count = len(population[0])

    # Compute termination fitness value for population respective to number of vertices in polygon
    f_pop_termination = vertice_count / 7

    terminate = False

    while not terminate:
        rated_population = []
        print(population)

        for individual in population:
            fitness_value = fitness_func(individual)
            pair = {'individual': individual, 'fValue': fitness_value}
            rated_population.append(pair)

        # Select two parents for recombination
        parent_one = roulette_wheel_selection(rated_population)
        parent_two = roulette_wheel_selection(rated_population)

        # Make sure that there's not one individual reproducing with itself
        while parent_one is parent_two:
            parent_two = roulette_wheel_selection(rated_population)

        # Generate child with 2 point crossover
        child = two_point_crossover(parent_one['individual'], parent_two['individual'])

        # Mutate child with binary mutation
        mutated_child = mutation(child)

        # Sort population by fitness value of each individual in population
        sorted_rated_pop = sorted(rated_population, key=itemgetter('fValue'))
        print(sorted_rated_pop)

        # Select worst indidivudal (worst fitness value) of population
        worst_individual = sorted_rated_pop[0]

        print(worst_individual)

        # Replace worst individual with mutated child
        for i in range(0, len(population)):
            if np.array_equal(population[i], worst_individual['individual']):
                population[i] = mutated_child
                break

        print(population)

        # Select best individual in population (without mutated child)
        best_individual = sorted_rated_pop[len(sorted_rated_pop) - 1]
        print(best_individual)
        best_individual_value = best_individual['fValue']
        best_pop_value = vertice_count / best_individual_value

        # Check if best individual beats termination fitness value
        if best_pop_value < f_pop_termination:
            terminate = True

        # Increase generation count
        generation += 1

        if generation >= 500:
            terminate = True

        # Draw process
        draw_process(points, sorted_rated_pop, vertice_count, generation)

    # Draw final result
    draw_final_result(points, sorted_rated_pop, vertice_count, generation)


if __name__ == '__main__':
    # population = [
    #     [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    #     [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    #     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    # ]

    # population = [
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # ]
    genetic_algorithm()
    # fitVal1 = fitnessFunc(ind1)
    # fitVal2 = fitnessFunc(ind2)
    # print(fitVal1, fitVal2)
    # ind = twoPointCrossover(ind1, ind2)
    # print(ind)
    # mutation(ind1)
