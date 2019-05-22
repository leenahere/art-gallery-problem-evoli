import pygame

background_color = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)


def screen(vertice_count, generation, population, poly, best_individual):
    pygame.init()
    main_screen = pygame.display.set_mode((1200, 800))
    main_screen.fill(background_color)
    pygame.display.set_caption('Evoli Project - Art Gallery Problem')

    font = pygame.font.SysFont('Helvetica Neue', 20)
    text_vertices = "Vertices: {0}".format(vertice_count)
    vertices_label = font.render(text_vertices, 1, black)
    main_screen.blit(vertices_label, (450, 75))

    text_generation = "Generation: {0}".format(generation)
    generation_label = font.render(text_generation, 1, black)
    main_screen.blit(generation_label, (100, 75))

    draw_poly(main_screen, poly)

    guards = []

    for i in range(0, len(best_individual)):
        if best_individual[i] == 1:
            guards.append(poly[i])

    for guard in guards:
        pygame.draw.circle(main_screen, red, guard, 3)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def draw_poly(main_screen, poly):
    pygame.draw.polygon(main_screen, black, poly, 1)

def draw_initial_individual_one(individual, poly):
    surface = pygame.display.set_mode((800,800))
    draw_poly(surface, poly)


