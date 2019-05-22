import matplotlib.pyplot as plt
from matplotlib import collections
import matplotlib.patches as patches
import numpy as np

background_color = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


def draw_process(poly, population, vertice_count, generation):
    for i in range(0, len(population)):
        ax = plt.subplot(2, 3, i + 1)

        polygon = plt.Polygon(poly, fill=None, edgecolor='black')
        ax.add_patch(polygon)
        for j in range(0, len(population[i]['individual'])):
            if population[i]['individual'][j] == 1:
                if i == len(population) - 1:
                    ax.plot(poly[j][0], poly[j][1], 'yo')
                else:
                    ax.plot(poly[j][0], poly[j][1], 'ro')

        ax.axis('off')
        text_fitness_value = "fitness: {0}".format(population[i]['fValue'])
        text_individual = "individual {0}".format(i)
        ax.set_title(text_individual + "\n" + text_fitness_value, fontsize=10)
        ax.autoscale_view()

    text_vertices = "vertices: {0}".format(vertice_count)
    text_generation = "generation: {0}".format(generation)
    plt.suptitle(text_vertices + '   ' + text_generation, fontsize=12, fontweight='bold')
    plt.show(block=False)
    plt.pause(0.2)
    plt.close()

def draw_final_result(poly, population, vertice_count, generation):
    for i in range(0, len(population)):
        ax = plt.subplot(2, 3, i + 1)

        polygon = plt.Polygon(poly, fill=None, edgecolor='black')
        ax.add_patch(polygon)
        for j in range(0, len(population[i]['individual'])):
            if population[i]['individual'][j] == 1:
                if i == len(population) - 1:
                    ax.plot(poly[j][0], poly[j][1], 'yo')
                else:
                    ax.plot(poly[j][0], poly[j][1], 'ro')

        ax.axis('off')
        text_fitness_value = "fitness: {0}".format(population[i]['fValue'])
        text_individual = "individual {0}".format(i)
        ax.set_title(text_individual + "\n" + text_fitness_value, fontsize=10)
        ax.autoscale_view()

    text_vertices = "vertices: {0}".format(vertice_count)
    text_generation = "generation: {0}".format(generation)
    plt.suptitle(text_vertices + '   ' + text_generation, fontsize=12, fontweight='bold')
    plt.show()


if __name__ == '__main__':
    points2 = [(244, 302), (303, 256), (387, 320), (437, 248), (517, 164), (586, 213),
               (533, 325), (544, 329), (594, 330), (612, 348), (559, 366), (579, 430),
               (519, 457), (548, 566), (470, 492), (448, 579), (445, 585), (417, 571),
               (415, 636), (372, 471), (309, 574), (305, 540), (287, 533), (284, 535),
               (175, 586), (265, 488), (215, 438), (77, 433), (207, 386), (169, 303)]

    points = [[244, 302], [303, 256], [387, 320], [437, 248], [517, 164], [586, 213],
              [533, 325], [544, 329], [594, 330], [612, 348], [559, 366], [579, 430],
              [519, 457], [548, 566], [470, 492], [448, 579], [445, 585], [417, 571],
              [415, 636], [372, 471], [309, 574], [305, 540], [287, 533], [284, 535],
              [175, 586], [265, 488], [215, 438], [77, 433], [207, 386], [169, 303]]
    population = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    draw_process(points, population, 30, 15)
