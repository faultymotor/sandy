import pygame
import numpy as np
from math import sqrt

from pygame import color

WIDTH, HEIGHT = 1024, 512
FPS = 120

world = np.zeros((WIDTH, HEIGHT))
colored_array = np.zeros((WIDTH, HEIGHT, 3))
changes = []

def draw_array_to_screen(array, display):    
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, (0, 0))


def color_monochrome_array(array, colorer, changes):
    for change in changes:
        x, y = change
        colored_array[x][y] = colorer(x, y, array)


clock = pygame.time.Clock()
 
pygame.init()
pygame.display.set_caption('mapped')

display = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
is_mouse_dragging = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            is_mouse_dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_dragging = True

    changes = []

    cur_x, cur_y = pygame.mouse.get_pos()
    del_x, del_y = pygame.mouse.get_rel()

    if is_mouse_dragging:
        distance = del_x ** 2 + del_y ** 2
        for i in range(0, 100, 1 if not distance else (100 // distance or 1)):
            x = cur_x - (i / 100) * del_x
            y = cur_y - (i / 100) * del_y
            x, y = int(x), int(y)
            world[x][y] = 1
            changes += [[x, y]]

    color_monochrome_array(world, lambda x, y, array: [array[x][y] * 255] * 3, changes)
    draw_array_to_screen(colored_array, display)

    pygame.display.update()
    clock.tick(FPS)
    print(int(clock.get_fps()))

