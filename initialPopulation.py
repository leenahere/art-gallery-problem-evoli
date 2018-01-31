#import generatePolys
import random

#polyPoints = generatePolys.generatePolygon(300, 300, 100, 1, 0.3, 15)

def generateInitialPopulation():
    #n = len(polyPoints)
    n = 15
    population = []

    for p in range(0,3):
        individual = []
        for i in range(0,n-1):
            r = random.randint(0,1)
            individual.append(r)

        population.append(individual)



    print population




if __name__ == "__main__":
    generateInitialPopulation()
