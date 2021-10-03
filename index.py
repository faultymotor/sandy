import pygame
import numpy as np

WIDTH, HEIGHT = 512, 256
FPS = 60

clock = pygame.time.Clock()
 
pygame.init()
pygame.display.set_caption('mapped')

display = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

def draw_array_to_screen(array, display):    
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, (0, 0))


def color_monochrome_array(array, colorer):
    width, height = np.shape(array)
    dim = (width, height, 3)
    colored_array = np.zeros(dim)

    for x in range(width):
        for y in range(height):
            colored_array[x][y] = colorer(x, y)

    return colored_array.astype('uint8')


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    array = np.random.rand(WIDTH, HEIGHT)
    array = color_monochrome_array(np.random.rand(WIDTH, HEIGHT), lambda x, y: [array[x][y] * 255] * 3)
    draw_array_to_screen(array, display)

    pygame.display.update()
    clock.tick(FPS)

