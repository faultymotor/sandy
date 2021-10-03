import pygame
import numpy as np
from math import sqrt

WIDTH, HEIGHT = 512, 256
FPS = 120

def draw_array_to_screen(array, display):    
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, (0, 0))


def color_monochrome_array(array, colorer):
    width, height = np.shape(array)
    dim = (width, height, 3)
    colored_array = np.zeros(dim)

    for x in range(width):
        for y in range(height):
            colored_array[x][y] = colorer(x, y, array)

    return colored_array.astype('uint8')


clock = pygame.time.Clock()
 
pygame.init()
pygame.display.set_caption('mapped')

display = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
is_mouse_dragging = False

world = np.zeros((WIDTH, HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            is_mouse_dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_dragging = True

    if is_mouse_dragging:
        cur_x, cur_y = pygame.mouse.get_pos()
        del_x, del_y = pygame.mouse.get_rel()
        distance = del_x ** 2 + del_y ** 2
        for i in range(0, 100, 1 if not distance else (100 // distance or 1)):
            x = cur_x - (i / 100) * del_x
            y = cur_y - (i / 100) * del_y
            world[int(x)][int(y)] = 1

    array = color_monochrome_array(world, lambda x, y, array: [array[x][y] * 255] * 3)
    draw_array_to_screen(array, display)

    pygame.display.update()
    clock.tick(FPS)

