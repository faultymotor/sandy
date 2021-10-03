import pygame
import numpy as np
from math import sqrt

from sandy import world

WIDTH, HEIGHT = 1024, 512
FPS = 120

world_obj = world.World(WIDTH, HEIGHT)

def draw_array_to_screen(array, display):    
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, (0, 0))

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

    cur_x, cur_y = pygame.mouse.get_pos()
    del_x, del_y = pygame.mouse.get_rel()

    if is_mouse_dragging: world_obj.set_cells(cur_x, cur_y, del_x, del_y, world.SAND)
        
    draw_array_to_screen(world_obj.get_rgbs(), display)

    pygame.display.update()
    world_obj.tick()
    clock.tick(FPS)

    print(int(clock.get_fps()))

